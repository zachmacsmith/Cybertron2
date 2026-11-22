# Design wave part 3a, keeping: processing containers, the smokehouse as a store, conditional rules, worked through a winter

22 Nov 2026, 37.2 (design subagent, thread W-80, under W-73). A design note for Zach's morning. Nothing here is decided, nothing
built, no code or record changed. No live model runs.

**Read with:** `wave1_physical_basis.md` (part 1, final: the prices below come from it); `wave4_people.md` (part 4, final: how rules
and crafts are shown); `docs/cybertron2/proposals/hunt_fish_materials.md` §7.3 to §7.6 and open question 10 (the smokehouse as a
store); `proposals/store_rules.md` (D2-274); `proposals/standing_rules.md` (37.4's; read, not edited); `proposals/building_clock.md`
(D2-276); `spec/core/clocks.md` (D2-273); the notes `smokehouse_capacity.md`, `storage.md`, `store_management.md` in this folder and
`docs/review/37_growth/02zzx_salting_rates.md`; the code in `cybertron2/engine/keeping.py`, `night.py`, `verbs.py`, `data.py`,
`run.py`, `clocks.py`. Making chains (how racks, tubs, pits and ponds are made, and from what) are part 2's (`wave2_making.md`, in
progress); this note uses part 1's prices for them and leaves the chains alone.

**Fixed inputs** (decided, treated as given): D2-271 (three smoke depths by smokehouse kind; racks of withies), D2-272 (a store never
slows a food below its base), D2-273 (three clocks), D2-274 (one book of standing rules), D2-276 (making durable things on the year
clock), D2-279 (stores as space and containers), D2-281 (tanning in this build, bark a new good; pollution from retting and tanning),
D2-282 (rules may fire on state changes), and from tonight **D2-283** (salting about 20 kg an hour with gutting, 1 kg of salt to 4 kg
of fish, meat 1 to 8) and **D2-284** (a smokehouse's capacity comes from racks fitted, about 250 kg of fish a set; the building caps
the sets; material sets the depths, life and fire risk; a keeping smoke holds its racks 1 night, a hard cure 2 to 3 after salting).

**How the numbers are marked.** **[p1 §n]**: from part 1, `wave1_physical_basis.md`, at its section (part 1 marks its own sources).
**[m]**: read from the engine's data or code on main. **(prov.)**: my own number, not in part 1, to be checked. **(est.)**: a real
figure from general knowledge I could not check against a source tonight (no web fetches were made for this note). Decisions are
cited by number.

---

## 0. In brief

- **One engine unit for every processing container.** Smoke racks, a salting tub or barrel, a drying rack (at the hearth or in the
  wind), a tanning pit and a retting pond are one shape: a container holding **lots**; each lot is a good on its way from one state
  to another, counting **nights** while its **conditions** hold (a tended fire, dry weather, still water, a fed pit) and suffering
  its **failure** when they do not (the fire dies, rain, a spate, weak liquor, a hut fire). Each process is a data row: in and out
  goods, nights by depth, ratio, inputs, capacity, labour to load, unload and tend, failures, over-processing, fouling, and what the
  container protects once the lot is done. Today's smokehouse and hearth-rack code (`keeping.py`, `night.py:286-309`,
  `verbs.py:790-831`) is already most of this engine and becomes its first rows. Five bespoke mechanisms would each need their own
  capacity code, night step, failure, signs and rule triggers (§2).
- **It sits with D2-272 by changing what the good is, never by slowing it.** A lot in process is an in-process good ("smoking fish")
  whose base is its rate in the container's conditions (0.03 a night in the smoke [p1 §2.2]); a failure puts the outside rate back
  (the fire out: the fresh rate, 0.37); at the end the lot is a different good with its own base. Once done, the container is a
  store: it removes its own risks for the done good, never below that good's base (§2.4).
- **A clock rule falls out of it, and I recommend writing it down:** work that scales with **quantity** (hanging, salting, scraping)
  is at real hours; work that scales with **duration** (tending a smoulder, feeding a tan pit) compresses with the duration, about
  1/11.4. That is what 1 tending unit a smoke night already is (11 to 33 real hours over 11 real days, /11.4), so the "named
  departure" of smokehouse_capacity.md and part 1 §3.1 becomes a rule (§2.5).
- **The smokehouse as a store (D2-284; part 1 §3.6):** a set of racks holds 250 fish on 1 space; a wattle hut takes 1 set; a small
  timber or stone room 3 to 4 tiered sets (750 to 1,000 fish) with 2 spaces to work in; a loft or the roof's hooks a store for cured
  goods. A set passes 250 kg a night on a keeping smoke and 85 to 125 kg on a hard cure. With nothing hanging there is no fire and
  the house is a dry, fly-free store at base. A finished keeping smoke under a continued fire gains nothing; a salted lot deepens to
  a hard cure only in timber or stone (§3).
- **Conditional rules (D2-282):** a `when` clause on any rule, and `if` beside `unless`. Triggers are **states that persist** ("a lot
  on the racks is cured", "the racks have room", "the bins are under 20"), latched when they come true and held until the chore is
  done, so a missed chore is not lost; **events that leave no state** (the fire died, the run was seen) latch for the day. A trigger
  reads **only what the household knows** (its own containers and stores, its acts' results, the calendar, signs its members
  noticed), never hidden state such as the run's pulses. Chores run in a **chore phase** after the day's plans and **before the
  fallback** (`run.py:1036`), from spare units, in the order tend, load the most perishable, take down, move (§4).
- **The winter, worked night by night, on part 1's prices (§5).** A household of four with six wicker traps and one turn at the
  village weir lands about **243 kg of eel** in an autumn run (about 112 food) and eats about 60 food of it by spring. The wattle hut
  **never binds** (at most about 150 kg hangs against 250) and the hands barely do (about 6 units on the biggest day against 7
  spare). What binds is **how fast the keeping smoke goes off** (half in 9.7 nights [p1 §2.2]) and **the fuel**: about 220 to 310 kg
  of wood for the run's smoking [p1 §3.1], 7 to 10 units of gathering, as much work as the hanging. At spring:
  - the hut with 15 kg of salt, salting 60 kg on purpose, has **17 food** left; hanging first and salting only "what does not fit",
    the salt is never used and it has **10.5**, the same as a household with no salt;
  - a timber smokehouse with a hard cure has **18.5**, 16 kg of it hard cure that keeps to the next run and travels; its 750 kg of
    racks are never a quarter full;
  - with **no rules**, three ordinary misses (the fire untended on the big night, a catch not hung, a cured lot left up) leave it
    with **nothing**: the untended night alone loses 26 food, because a lot whose fire dies spoils at the fresh rate.
- **What the result turns on is how "keeps d days" becomes a nightly loss.** Part 1 reads it as half lost by then (§2.1 there). On
  that reading a careful household keeps 10 to 20 food of 112; read as a quarter lost, 28 to 34; as a tenth, 40 to 43. With
  smoked fish at today's rate, salting makes a household worse off (§5.6). The convention is the largest lever in keeping, larger
  than the racks or the rules.
- **Five questions matter most** (§9): what "keeps for d days" means as a loss, against part 1's half (W80-Q1); one engine unit for
  processing containers (W80-Q2); how conditional rules fire (W80-Q3); duration work compressing with the duration (W80-Q4); a brine
  container before the cooper, since salt reaches its year only in brine (W80-Q9).

---

## 1. What the engine does now (read 22 Nov) [m]

| What | Now | Where |
|---|---|---|
| Smoke racks | a fitting, 2 timber, 2 units, 3 spaces, `apart` (a building of its own), `racks: 1` | `data.py:275-277` |
| Room on the racks | fittings x `racks` x the technique's batch (40), less what is still curing; done lots do not count | `keeping.py:39-47`, `:28-31` |
| Smoke fish, smoke meat | up to 40 a batch, **1 unit whatever the batch**, 3 nights of tended fire, to half the weight | `data.py:623-635` |
| Tend the smoke | 1 unit a day, or the fire dies that night: the lot pauses and spoils at the open rate | `data.py:636-638`, `keeping.py:106-136`, `:169-193` |
| Fuel | 0.5 heat a night burning (1 firewood), flat, whatever hangs | `data.py:835`, `keeping.py:186` |
| Fire | a keyed chance a night burning by structure (wattle 0.02, timber 0.008, stone 0.0003); it spreads to buildings on the parcel | `data.py:835-836`, `keeping.py:192-208` |
| A done lot | into the building's store if the hanger is of its household and there is room, else it waits on the rack | `night.py:286-309`, `keeping.py:239-245` |
| Hearth rack (dry fish, dry meat) | 8 a batch, 3 nights, in the hearth's smoke inside or by a fire ring outside | `data.py:643-650`, `verbs.py:809-831` |
| Salting | an act at once: 4 fish and 1 salt to 4 salt fish, 1 unit; meat the same | `data.py:639-642` |
| In-process spoil | `drying meat` decay: open_dry 1.0, open_wet 3.0, smoke 0.25 (`smoking fish` spoil 0.15) | `data.py:54`, `:122`, `night.py:331-334` |
| Shelf lives | smoked fish 0.005, salt fish 0.01, dried fish 0.02, salt meat 0.003, fresh fish 0.30; in a store x `house_spoil` 0.3 x the best fitting's `spoil`; fresh fish x2 in a store | `data.py:49-58`, `:93`, `:776`, `night.py:339-352` |
| Retting, tanning, bark | none | (no code) |
| Standing rules | none; the fallback (D4-76) runs on units left after the plan | `run.py:1036-1057` |
| A day's acts | interleaved: each person's first act, then each person's second, in `order` | `run.py:995-1035` |
| Verb costs | whole units, charged before the act; under 1 is free | `verbs.py:116-150`, `run.py:1014` |

Today a smokehouse is a pile on a rack per act, inside a building with smoke racks, counted by nights of fire. That is already a
processing container in all but name.

---

## 2. Processing containers as one engine unit

### 2.1 The shape

Three things, each of which the engine has in some form:

- **A process** (a data row, `PROCESSES`): what goes in (a good, or a good in a state), what comes out, nights at each depth, the
  ratio of weight out to in, inputs used at loading (salt, bark, ash) and as a total over the nights (fuel), the conditions a night
  must meet to count, the failure when it does not, what happens to a lot left past its nights, its fouling, and its labour (to load
  a kg, to unload, to tend a night).
- **A container** (a fitting in a building, a work on a parcel, or ground of a cover): which processes it runs, its capacity in kg
  (`holds`, its own number, not the technique's batch; smokehouse_capacity §8, part 1 §7's hand-on to 37.4), and what it protects
  once a lot is done.
- **A lot** (today's rack pile, `kind: "pile"` with a `rack` record, `verbs.py:812-816`): who loaded it, the process and depth, the day
  loaded, nights counted and needed, `done` once finished. Each loading is its own lot with its own nights, as now.

**The night step** (one function for every process, replacing `keeping.night` and the rack part of `night.py:204-207`):

1. For each container with lots not done, read tonight's conditions: the fire tended and fuelled; the weather at the parcel; the
   river in spate or not; the pit fed this stage.
2. Conditions met: the lot counts a night; the fire's chance to catch is rolled once a container (as now, `keeping.py:192`).
3. Not met: the lot does not count; its in-process good spoils at the outside rate (the failure's penalty); a destroying failure (a
   spate, a fire) takes its share.
4. Spoilage runs as now (`night.py:176-203`), each in-process good at its own base in its container.
5. A lot whose nights are counted becomes the output good at the ratio, **stays in the container**, and raises the state "done" for
   its household (the trigger for §4). Today it goes into the building's store at once if there is room (`night.py:300-307`); I
   propose it stays, so that taking it down is a visible choice and full racks cost the next catch (W80-Q11).

**Loading** is the act it is now (`make` with the technique's `rack` record), charged by quantity (§2.5); **unloading** is a `move`
out of the container (free within the building, D2-274); **tending** is today's act, generalised to any container whose process
needs it.

### 2.2 The five containers, row by row

Hold times are real durations at 1/11.4, at least a night, in whole nights [p1 §2.4]. Labour and inputs are part 1's [p1 §3.1] where
it gives them.

| | **Smoke racks** (keeping smoke; hard cure) | **Salting tub or barrel** | **Drying rack** (at the hearth; in the wind) | **Tanning pit** | **Retting pond** |
|---|---|---|---|---|---|
| Container | a set of racks in a smokehouse: 2 withies, 2 timber, 1 unit, 250 fish on 1 space; a tiered set 3 withies, 3 timber [p1 §3.6] | a tub or trough (W80-Q9) now; a cooper's barrel later: 7 timber, 0.3 withies, 1 unit, 120 kg, 4 a space [p1 §3.3] | hearth: a rack in the hearth's smoke (`hearth`, `fire ring`, as now); wind: a pole rack outdoors (later) | a work by water: a lime pit and tan pits (making: part 2) | a work beside water (the retting pit), or the river, or a meadow for dew retting (making: part 2) |
| In -> out | fish or meat -> smoking -> smoked (keeping, to 0.5 the weight); salt fish -> hard-cured fish (0.4 of the fresh weight, 1.15 food a kg) [p1 §1.1] | fish or meat + salt -> salt fish or meat (the weight kept) | fish or meat -> drying -> dried (0.5) | hide + ash -> limed hide; scraped hide + bark liquor -> leather (3 from a 6 kg hide) [p1 §3.1] | flax -> retting flax -> retted flax |
| Inputs | fuel as a total: 0.1 to 0.2 firewood (10 kg) a fish for a keeping smoke; 0.25 for a hard cure [p1 §3.1] | salt 1 to 4 (fish), 1 to 8 (meat) (D2-283) | hearth: the house fire; wind: none | wood ash; 2 bark (20 kg) a hide [p1 §3.1] | water; stones to weight it |
| Hold, real | keeping smoke 4 to 14 days; hard cure 3 weeks to a month and more after salting [p1 §2.4] | fish settle in the barrel about 10 days [p1 §2.4]; bacon dry-cures about a month (02zzx) | thin fish or strips over a hearth days to about 2 weeks [p1 §2.4]; Fraser wind-dried salmon 3 to 4 days (smokehouse_capacity §3); stockfish 2 to 3 months (est.) | liming 2 to 6 weeks; bark pits 6 to 18 months [p1 §2.4] | in water 1 to 2 weeks; on grass 3 to 6 weeks [p1 §2.4] |
| Hold, engine | **keeping 1 night, hard cure 2 to 3 (D2-284)** | fish: at once (W80-Q8; part 1 lists 1 night of settling); meat: 3 nights (prov.) | hearth **1 night** [p1 §2.4]; wind 1 night (strips) to 6 to 8 (stockfish, later) | liming 2 to 4 nights; tanning **16 to 48** [p1 §2.4], so a hide laid down in spring comes out the next year (W80-Q12) | water 1 night; dew 3 to 4 [p1 §2.4] |
| Capacity | **250 kg a set (D2-284)**; sets per building §3 | 120 kg a barrel [p1 §3.3]; a trough the same (prov.) | hearth rack 8 a batch (kept [p1 §3.1]); wind rack about 25 kg a m² of rack (est.) | about 20 hides a pit (est.) | a household's flax from a close; a pond by its size |
| Load | **30 kg a unit**, splitting included [p1 §3.1] | **40 kg a unit with gutting (D2-283)** | 8 a unit [p1 §3.1] | **1.5 units a hide over the pit's nights** [p1 §3.1] (liming, scraping, moving between pits) | **1 unit to lay, 1 to lift** [p1 §3.1] |
| Unload | free within the building (D2-274) | none: the barrel is the store | free | in the 1.5 a hide | in the lift |
| Tending | **1 unit a night while anything hangs** [p1 §3.1] (§2.5) | none (meat: topping up the brine once, est.) | none; someone takes a wind rack in before rain or loses it | in the 1.5 a hide (feeding the pits at each stage) | none |
| Failure | fire not tended: the lot pauses and spoils at the fresh rate (0.37 [p1 §2.2]); the hut catches (by structure, as now) and burns with its lot | meat above the brine goes bad ("will become wormy", storage §3.6); a barrel leaks at the end of its life | rain on a wind rack: `open_wet` (x3 on the hazard); flies in the warm season x1.5 [p1 §2.3] | pits not fed: the hides rot slowly (a share a night, prov.); a flood into the pits | a spate washes a river lot away (a share, as a spate wrecks traps, 02zzy: `wreck` 0.5); left in, the fibre weakens |
| Left past its nights | keeping: kept, no deeper, fuel wasted; salted: deepens to a hard cure in timber or stone | kept: it is the store | kept (dry) | longer is stronger leather (est.) | about a third of the fibre lost a night left in (prov.) |
| Fouling (hunt_fish_materials §7.5) | smoke in the air only (a sign) | brine and offal: none to water now (offal later, L-145) | offal and flies about a wind rack | lime, flesh, hair, bark liquor: all year, lingering (D2-281) | oxygen used up: a pulse while a lot is in (D2-281) |
| Once done, protects | the smoke loft and racks: flies; dried goods from floor damp [p1 §2.3] | in brine: air, flies, vermin; salt goods at base; out of brine x2, on a dry floor packed in salt x1.5 [p1 §2.3] | hearth: flies (the smoke) | nothing (leather is kept in the house) | nothing |

**Two keeping paths are not containers.** A **hot smoke** (D2-271: hours, at a hearth or an open fire) is an act on the day clock:
1 unit for 10 fish, the same day, 1 to 2 firewood, giving 6.5 **hot-smoked fish** (0.69 food a kg, half-life 2.4 nights) [p1 §1.1,
§2.2, §3.1]. **Eating fresh** is no process.

### 2.3 How the five read against each other

- **Smoke racks** are the one that binds a run's glut: big, a night, worked by hand, fuel-hungry, a fire risk.
- **The salting tub** is quicker per kilogram (40 kg a unit against hanging's 30) and needs no fuel, but costs salt at a quarter of
  the fish's weight: 60 kg of eel takes 15 kg of salt, which an inland household buys. A household short of hands or wood and long on
  salt salts; short of salt, it hangs.
- **The drying rack** is the cheap one, and the weather's: the eels run on rain after dry days (`wild/kinds.py:873`, cue
  `rain_after_dry`), so a wind rack meets the eel run in the wet and fails it. It suits lean fish and meat in dry or cold weather,
  which is real: eels are fat and were smoked or salted, not air-dried (est.). The engine's fish is one good, so this cannot be said
  today (W80-Q10).
- **The tanning pit** holds a lot for half a year or more: capital tied up, needing a steady flow of hides and bark.
- **The retting pond** is the short one whose harm is to others (the fishers below), which is why it is in (D2-264, D2-281).

### 2.4 How it sits with D2-272

D2-272: a food's base rate is its rate well kept, the rate its preserving gives it; stores remove outside penalties and never slow a
food below its base.

- **A process changes the good, so it changes the base.** Fresh fish (0.37 a night) becomes smoked fish (0.069) [p1 §2.2]. Nothing
  in a store slows the fresh fish; the process replaces it with another good.
- **A lot in process is its own good, with its base taken in the container's conditions.** Today `smoking fish` spoils 0.15 and the
  smoke multiplies it by 0.25 (`data.py:54`, `:122`; `night.py:331-334`): a factor below the good's own rate, which read literally is
  what D2-272 forbids. Part 1 already sets the in-process base at **0.03 a night in the smoke**, with the fire out at the fresh rate
  [p1 §2.2]: the base is the rate in the smoke, and the fire dying is the outside penalty. Rain on a wind rack reads the same way.
- **Once done, the container is a store.** The smoke loft removes flies and, for dried goods, floor damp; brine removes air for salt
  goods [p1 §2.3]. A smokehouse with no fire and cured fish in it is a dry, fly-free store at base, which answers Zach's "should
  storing it in there mean its lifetime doesn't decay": it decays at its base, the slowest it can, and no slower.
- **Over-processing is not slowing either.** A keeping smoke left under fire stays smoked fish at the same base; the fire buys
  nothing. Only a salted lot in timber or stone becomes something else (a hard cure), because D2-271 says that path exists.

### 2.5 Labour and fuel on the clocks: quantity work and duration work

D2-273: work rates per hour are never compressed; durations are. D2-276: what is used up is priced at real hours. Processing has
both kinds of work:

| Kind | Scales with | Clock | Examples | Engine cost |
|---|---|---|---|---|
| **Quantity work** | kg handled | day (real hours) | hanging (30 a unit), salting (40, D2-283), scraping a hide, laying flax | real hours, in batches |
| **Duration work** | nights of process | year (compressed with the duration) | tending a smoulder, feeding a pit, watching a pond | its real hours over the real days x 1/11.4 |
| **Materials** | kg | real totals (D2-276) | fuel for the whole smoke, salt, bark, ash | real quantity |

Tending a keeping smoke: about 1 to 3 hours a real day (est., smokehouse_capacity §5) for about 11 real days is 11 to 33 hours; at
1/11.4, 1 to 3 hours: **0.5 to 1.5 units a night**. The engine's 1 unit a night is that, not a departure. Part 1 §3.1 keeps it and
calls it "a named departure"; under this rule it is not one (W80-Q4). It settles any later chore that runs through a compressed wait
(a cheese turned, a rick watched) without a departure each time.

**Fuel** is a total by the fish hung, 0.1 to 0.2 firewood (1 to 2 kg of wood) a kg [p1 §3.1], not today's flat firewood a night
(`data.py:835`), which charges an almost empty set as much as a full one. At part 1's bundle of 10 kg a full set is 25 to 50
bundles: **the wood is now a real bind**, a run's smoking costing about as many units of gathering (3 bundles a unit [p1 §3.1]) as
of hanging (§5).

Costs are whole units charged before the act (`verbs.py:116-150`); a batch technique already takes "whatever one has, up to the
batch" (`verbs.py:790-792`), so hanging at 30 a unit is the batch set to 30 and a `qty` of units; a chore's fractions carry over as
`labour.step` does (store_rules.md).

### 2.6 What people sense of it (per `guides/senses.md`)

The household knows its own containers without a roll (`keeping.house_lines`, `keeping.py:139-166`): what is in each, nights left,
the fire tended or not, the fuel. That stays, generalised to every container, and carries the chore lines of §4.6. For others, a
small bundle a container, each a change worth acting on (own and reach (prov.), to be checked through `perceive.chance_of` as the
guide's checklist says; not done tonight):

| Sign | Sense, kind | Own, reach | Why it earns its place |
|---|---|---|---|
| smoke rising from the smoke hut in the morning | sight, nearby and far | about 1.5, around | a lit hut is a change: someone is keeping a catch; a buyer or a thief reads it |
| the smell of smoke and fish about the hut | smell, nearby | about 1.2, around | the same in the dark or fog |
| "the smoke hut at Reed House is a heap of black wattle and ash" | sight, lingering (days) | as the fire bundle (D4-74) | the fire is already a bundle; the lots lost go with it |
| "the fish on the rack by Holt House are wet through" | sight, conditional (rain on a wind rack) | 1.0, near | the owner should take them in; others see the loss |
| the stink of the retting pond; below, dead fish turning in the shallows | smell around; sight at the water below | as hunt_fish_materials §9 | already in the design |
| the tan pits emptied and refilled: the stink sharp, the water below stained | smell carries; sight below | about 2, around, while a stage turns | a standing stink is ambience, never acted on (guide §2); the change is the stage turning |

Nothing about a lot "being cured" goes to others: it is not visible, and the household already knows.

### 2.7 One unit against five bespoke mechanisms

| | One unit (recommended) | Five bespoke mechanisms |
|---|---|---|
| Code | one lot record, one night step, one load, one tend, one unload; the processes as data rows | five capacity checks, night steps and failures; salting an instant act, retting and tanning written fresh |
| Rules (§4) | one trigger vocabulary ("done", "has room", "fire out") for all | a trigger per mechanism, or rules that reach only the smokehouse |
| Signs | one house-line generator; one bundle shape per container | five sets of lines |
| D2-244 seams | a core unit (data, verbs, process, signs listed together); each process row belongs to its feature package (smoking to the water pack, retting to materials, tanning to its own) and moves with it | each its own package, much duplicated |
| Fit to the real thing | strained where a process is not a wait (salting fish is a step): a row may have no nights | each can be exact |
| Risk | a general shape that tempts adding processes nobody needs | drift: today's hearth rack and smokehouse already count nights differently (`keeping.py:65-75`) |

The hearth rack and the smokehouse already share the rack pile and `_dried`. The unit costs a refactor of `keeping.py` and the rack
branch of `verbs._make`, plus a `PROCESSES` table; five mechanisms cost writing retting and tanning from nothing and special-casing
rules and signs for each. I recommend the unit (W80-Q2), with the rule that a process enters only if its wait, its capacity or its
failure binds something (§2.3's test).

---

## 3. The smokehouse as a store (D2-284 as fixed)

### 3.1 Capacity: racks, and the building capping them

D2-284 fixes about 250 kg a set, one set in a wattle hut, and timber or stone by room size, tiers and a loft. Part 1 §3.6 sets the
rest, following the brief: **a set is 250 fish on 1 space** (50 kg a m², the middle of smokehouse_capacity's 30 to 70); a small timber
or stone room takes **3 to 4 tiered sets** (750 to 1,000 fish) with 2 spaces left to work, hang and keep the fire. That replaces
smokehouse_capacity §8's and storage §11's 500 on 2 spaces (part 1 §5.4 item 15). Extending it by the same rule (prov.):

| Smokehouse | Floor (spaces) | Sets | Holds on racks | Loft | Depths | Fire a night burning [m] | Cost at 1/7 [p1 §3.6] |
|---|---|---|---|---|---|---|---|
| wattle smoke hut (a 2-space hut room) | 2 | 1 (no tiers: wattle is too low and hot) | 250 kg | none | hot, keeping | 0.02 | 7 to 14 units, with its racks |
| timber, small room | 6 | 3 to 4 tiered | 750 to 1,000 kg | hooks in the roof, a store for cured goods: 1 unit, 0.2 timber [p1 §3.4] | all three | 0.008 | 35 to 55 units, a carpenter |
| stone, small room | 6 | 3 to 4 tiered | 750 to 1,000 kg | as timber | all three | 0.0003 | 48 to 94 units, a mason |
| timber or stone, medium room | 12 | 8 to 10 tiered (prov.) | 2,000 to 2,500 kg | as above | all three | as above | part 1 §3.5's room plus the sets |
| a hall | 30 | a herring works (later) | | | | | |

**Tiers** are a taller frame with three tiers of rails [p1 §3.6], in timber or stone only; the upper tiers sit in cooler smoke, where
a hard cure hangs (est., from the cold-smoke practice in smokehouse_capacity §3). **The loft** is not a set but a store (D2-279),
counted as storage.

**Material sets the rest** (D2-284): wattle burns with its lot (0.02 a burning night, spreading to the parcel's buildings) and wears
as wattle; timber seldom burns (0.008); stone almost never (0.0003) [m]. Over §5's three burning nights a wattle hut has about a 6%
chance of burning; over a season of 8, about 15% (timber 6%). Those are the engine's numbers, not checked against a real record of
smokehouse fires (frequent in the herring towns by the accounts in smokehouse_capacity §6; no rate found).

### 3.2 Hold time per depth, and throughput

| Depth | Where | Nights on the racks (D2-284) | Throughput a set a night | A 750 kg house | Fuel a set (250 kg) [p1 §3.1] |
|---|---|---|---|---|---|
| hot smoke | hearth, open fire | an act, no lot | (hands: 10 fish a unit) | | 1 to 2 firewood a 10 fish |
| keeping smoke | hut, timber, stone | 1 | 250 kg | 750 kg | 25 to 50 firewood |
| hard cure (salted first) | timber, stone | 2 to 3 | about 85 to 125 kg | about 250 to 375 kg | about 60 firewood |

A timber house on a hard cure passes what a hut passes on a keeping smoke (hunt_fish_materials Q10(b)). The hands bind first: a full
set is 8.5 units of hanging [p1 §3.6] and a tend, more than one person's day. A set binds only on a day when more than 250 kg lands:
a peak night's whole offer at Lowstrand (333 kg, 02zzu_lookup), or a weir section's 100 kg on top of a household's traps. At 1 night a
lot yesterday's set is free by morning.

### 3.3 Fire kept or not

- **Nothing hanging: no fire.** The house is a store at base, its loft and racks keeping flies off. No tending, no fuel.
- **A lot curing: fire,** tended each day and fuelled; the lot counts its nights.
- **A lot done, the fire still kept:** a keeping smoke gains nothing (§2.4), and the house line says so as a fact: "the eels on the
  racks have had their smoke; more fire does them no good". The fuel is spent and the fire chance rolled.
- **A salted lot, timber or stone:** counts toward a hard cure; at 2 to 3 nights it is hard-cured fish.
- **A salted lot in a wattle hut:** refused at loading with the reason ("a hard cure needs the long cool smoke of a timber or stone
  smokehouse; the hut's fire is too close and hot"). It stays salt fish.

### 3.4 Racks as containers under the book

Racks are containers in D2-279's sense: each set has a tag, its fill and its lots, and is shown in one line of the store ("the Smoke
Hut: 122 kg of eel on the racks, cured tomorrow; the fire tended; firewood for the night"). Unlike a sack or a chest, **putting goods
into a set is work** (hanging), so D2-274's free arrival into a household store does not apply to racks: a `go` to racks is a chore
(§4.4).

---

## 4. Conditional standing rules on state changes (D2-282)

### 4.1 The grammar addition

store_management.md §2's rule record gains two fields and three verbs:

```
{"rule": "go" | "keep" | "hold back" | "first" | "eat" | "move" | "drop"
         | "load" (hang, salt, sink, lay in, spread: a container's own verb) | "tend" | "take down" (a move out of a container),
 "goods": ..., "to" | "in" | "from": ..., "qty"?, "before"?, "who"?, "by"?,
 "when"?: a state, below (fires when it comes true; stays pending until done, or until it is no longer true),
 "if"?: a state (applies only while it is true; beside the existing "unless"),
 "unless"?: as now ("someone is starving", "winter", "it is full"),
 "words": "their sentence"}
```

**The states a rule may name** (each read only from what the household knows, §4.2):

| State | Of | Persists? | Example words |
|---|---|---|---|
| done (cured, retted, tanned, dried) | a lot in one of its containers | yes, until unloaded | "when the eels are smoked" |
| has room / is full | a container or store | yes | "when the racks have room"; "if the racks are full" |
| under n / over n | a store's good | yes | "when the bins are under 20 grain" |
| arrives | goods coming home (store_rules' first moment) | the day | "whatever eels come home" |
| the fire is out / was not tended | a container's fire | the day | "if the hut's fire died" |
| seen | a sign a member noticed and holds (the run begun, frost, the river rising) | the day it is noticed | "when we see the eels running" |
| a season or a day | the calendar | yes | "in winter"; "from autumn's first day" |
| someone is back, or away | a member at the place | yes | "when Wat is home" |

Part 4's rules block (`wave4_people.md` §2.4) gives the grammar in one sentence ("... with 'unless' (someone is starving, it is winter,
it is full)"). With this, it would add: "and 'when' or 'if' (a cure is done, a store is full or has room, a store is under so much,
something is seen)", about 20 words.

### 4.2 States, not events, and only what the household knows

- **Triggers are persisting states with a latch, not raw events.** "When the eels are cured, take them down" reads "a cured lot is on
  the racks". If nobody has spare units today, the lot is still cured tomorrow and the rule fires then; the miss is shown, not lost. A
  trigger on an event that leaves no state (the fire died; a sign seen) latches for that day only. D2-282's words ("a rule may fire
  when a good, container or place changes state") are met: the rule fires on the change, and keeps firing while the changed state
  waits for its chore.
- **A trigger reads only what the household could know**: its own containers and stores (known without a roll today,
  `keeping.py:139`), the results of its members' acts (a lift's take), the calendar, and the beliefs its members hold from signs they
  noticed (D4-35, the senses guide). "When the eels run" fires on a member's noticed sign of the run (river_signs.md, W-72) or a lift
  that brought a run's catch, never on the engine's pulse record (`wild/runs.py`). Otherwise a rule would be an oracle and the river's
  signs would stop mattering.

### 4.3 How it reads at the five moments of store_rules.md

| Moment (store_rules.md) | What `when` and `if` add |
|---|---|
| 1. goods arrive | `when arrives` and `if` on go rules ("eels go to the racks; if the racks are full, to the salting tub"); a go into a processing container becomes a pending load chore (§4.4), not a free move |
| 2. a store's goods change | states recomputed (full, has room, under n, done); latches set |
| 3. drawing | `if` on first and hold back ("eat the smoked eel before the salt, unless the smoked runs short") |
| 4. the night's meal | `if` on eat ("half rations if the store is under 10 nights") |
| 5. spare units | **the chore phase**: every pending `when` chore and every `load`, `tend`, `take down`, `move` whose `if` holds is done here, in order (§4.4) |
| (the night) | lots finish, fires die, goods spoil: states change, latches set for tomorrow's chore phase |
| (the morning) | the house lines show what latched overnight and what will fire (§4.6) |

### 4.4 The chore phase, precedence and labour

- **Where:** after the plan loop and before the fallback (`run.py:1036`). The fallback takes every unit left over, and agents fill it
  with firewood (144 to 432 firewood fallbacks a run while the stores held 60 to 135, 02zzy §2; L-142). If it ran first no chore
  would ever have units. A rule is an instruction for a known need; a fallback is a filler. **Chores first** (W80-Q13).
- **Why after the plans:** the plan loop interleaves people's acts (`run.py:995-1000`), so by hand Agnes's "hang the eels" can run
  before Wat's lift brings them home and be refused, and a refused act is not tried again that day (`run.py:1007-1009`). A chore phase
  after every plan sees what the day brought. That is the plainest value of rules over hand acts: **they adapt to quantities nobody
  knew at dawn.**
- **Who:** the rule's `by` (a person, or "whoever has time": the members at the container's place with units left, the most spare
  first). A member away does nothing. A chore never takes units from a plan (D2-274).
- **Order when chores compete for the same units** (prov.): (1) **tend** (a fire dying ruins a lot already worked: on part 1's rates a
  night with the fire out loses about a third of what hangs, one unit saves many); (2) **load the most perishable first** (fresh fish
  and meat before hides and flax), into the containers the book names, in its order; (3) **take down** done lots that block a load
  waiting today; (4) **moves** between stores; then the book's own order within each. A household may reorder with `first` ("Hob
  tends before anything").
- **Precedence between rules** is store_rules.md's (an act in a turn, the person's rule, the household's, the default; the most
  specific wins; then the newer), with one addition: **a rule whose `when` or `if` holds counts as more specific than the same rule
  without.** So "eels go to the house" and "if the racks have room, eels go to the racks" agree: the second applies while it holds.
- **Partial chores:** a load done in part splits the goods; what was hung is hung, the rest falls through to the next rule that takes
  it, then the default store (home), and the line says so.
- **Cascades:** a chore can change a state (taking down frees a rack, firing "when the racks have room, hang the salted fish"). Each
  rule fires at most once a day; cascades go at most three deep, in the order above; deterministic and replay-safe.
- **Refusals:** a rule naming an act outside keeping (lift the traps, fish, hunt, trade, travel) is refused when set, with the reason
  ("rules keep and move goods and tend what is in hand; work and trips are yours to choose each day"), as standing_rules.md item 7
  says for trade and trips (W80-Q6). The children's standing work (D2-148, `bots_livelihood.py:192`) is the head's order, a separate
  thing.

### 4.5 Worked examples, in the agents' own sentences

What the agent writes, then the engine's reading shown back.

1. *"When the eels are smoked, take them down and put them in the house loft."*
   -> Take down: smoked fish, from the Smoke Hut's racks, to Reed House's loft, when a lot is cured; by whoever has time. (Free within a
   building; across the yard about 0.04 units for 120 kg at store_rules' rate.)
2. *"Whatever eels come home, keep enough for tonight's supper and hang the rest in the smoke hut. If the racks are full or nobody has
   time, salt them. Salt the first 60 kg for the end of winter."*
   -> Hold back: fish, one night's meal, at home, when fish arrives. Load (salt): fish, up to 60 kg in all, into the salting tub, while
   salt lasts, when fish arrives. Load (hang): fish, into the Smoke Hut's racks, when fish arrives, if the racks have room. Load (salt):
   fish, into the salting tub, if the racks are full or the hanging was not done, while salt lasts. (Four rules, read in that order.)
3. *"Keep the hut's fire going while anything hangs. Hob first."*
   -> Tend: the Smoke Hut, if a lot is curing; by Hob, then whoever has time.
4. *"Eat the smoked eel before the salt."*
   -> First: smoked fish before salt fish, at the meal. (The default already eats the most perishable first; shown as agreeing.)
5. *"When the bins get under 20, fill them from the granary."*
   -> Move: grain, from the Granary to Holt House's bins, up to full, when the bins hold under 20; by whoever has time.
6. *"Once the flax is retted, lift it out and spread it on the bleaching green."*
   -> Take down: retted flax, from the retting pit to the Green, when the lot is done; by Agnes (1 unit to lift [p1 §3.1]). Without it
   the flax lies in the pit and weakens, which the morning line says.
7. *"When the racks free up, hang the salted fish for a hard cure."* (a timber smokehouse)
   -> Load (hang for a hard cure): salt fish, into the Fish House's racks, when the racks have room. In a wattle hut: refused when set,
   with D2-271's reason.
8. *"When the eels start running, everyone stays at the river."*
   -> Refused: a rule cannot plan the day's work or keep people from going; "when we see the eels running" can be a trigger for keeping
   chores only.

### 4.6 Visibility (D2-274): what fired, what was missed

The morning's house lines (prompt.py `_house_lines`; store_management §5) gain the chore record, one line a chore, facts only:

> By your rules yesterday: Agnes hung 126 kg of eel in the Smoke Hut (4 units); Hob tended its fire (1 unit); Joan salted 24 kg into
> the tub (0.6 units; 6 kg of salt; the salt is used up). The eels on the racks cure tonight.
> Not done: 30 kg of eel waited unhung (nobody with time was at Reed House); it lies in the house.
> Pending today: take down the cured eels when they are done (rule 1).

And a lapse plainly: "Rule 2's salting stopped: there is no salt in the house." The evening shows the book with what each rule did;
attending to the store shows each container's lots, nights left and the rule that put them there.

### 4.7 What the rules do not do

No production, trade, travel or taking from another household's container (Q-80: another household's lot in a shared smokehouse is
theirs; `keeping.done_into_store`, `keeping.py:239-245`, already holds it on the racks for its owner). A village smokehouse shared by
rota is a rule book across households (L-151), later. No default keeping rule: as with putting carried goods away (D2-274), nothing is
loaded, tended or taken down unless the book or an act says so; the house lines say what waits.

---

## 5. One household, an autumn eel run to spring, night by night

### 5.1 The household and the basis

- **Reed House**, four people: Wat (head, fisher, adult: 6 units in autumn, 5 in winter, D2-275), Agnes (adult), Hob (youth, 4 units,
  as the runs' youths), Old Joan (elder, 3). They eat about **4 food a night** (1 food = 2,500 kcal, D2-258).
- Six wicker traps at the Isel (up to about 6 a set, D2-264), each holding 10 kg a night (`trap in water`, 02zzy); one turn at the
  village weir's gap (100 kg a night, the first section).
- **The run** (silver eels, down-run, autumn, cued by rain after dry days, 0.6 of those left each cue night, `wild/kinds.py:873`): cue
  nights 17, 19 and 21. Lifted next morning: **45 kg** (day 18), **58 kg from the traps and 100 kg from the weir, 158 kg** (day 20),
  **30 kg** (day 22); about 2 kg off the run on autumn mornings, about 1 kg every other winter morning (ice, little fish). **243 kg in
  all, about 112 food fresh** (fish 0.46 a kg) (prov.: the catch is mine, read against the trap's hold and the weir's 100 kg).
- **Spare units for keeping chores**, after their own plans (the lifts, the weir crew, firewood, withies, mending, fowling in winter):
  about 8 a day in autumn, 7 on the weir day, 6 in winter (prov.).
- **Rates [p1]:** hanging 30 kg a unit; salting 40 kg a unit with 1 salt to 4 fish (D2-283); keeping smoke 1 night, hard cure 3
  (D2-284); tending 1 unit a night; fuel 0.15 firewood (10 kg) a kg hung for a keeping smoke, 0.25 for a hard cure; smoked fish half
  the weight at 0.92 food a kg; hard-cured fish 0.4 of the fresh weight at 1.15; taking down free within the building (D2-274).
- **Shelf lives [p1 §2.2]:** fresh fish 0.37 a night; smoking fish in the smoke 0.03, with the fire out 0.37; keeping smoke 0.069
  (half-life 9.7 nights); hard cure 0.027 (25.5); salt fish 0.020 in brine (33.8), x1.5 on the hazard on a dry floor packed in salt
  (0.030), which is how it lies here: no barrel and no tub.
- Eating: the most perishable first (store_rules' default).

The walk is arithmetic (a small script, not the engine), night by night: the morning's landing, the chores, the meal, the night's
spoiling, the lots' nights. "Lost" is food spoilt that night; smoked fish's loss of weight in the smoke is not a loss (the food a kg
doubles).

### 5.2 A. Wattle hut, 15 kg of salt, with the book

The book (the household's, set by Wat):
1. "Keep enough fresh eel for tonight's supper." 2. "Salt the first 60 kg after that, for the end of winter." 3. "Hang the rest in the
smoke hut." 4. "If the racks are full or nobody has time, salt what's left while the salt lasts." 5. "Keep the hut's fire going while
anything hangs: Hob first." 6. "When the eels are smoked, take them down into the house loft." 7. "Eat the smoked eel before the salt."

| night | landed (kg) | hands (units) | hung (kg) | salted (kg) | eaten (kg) | lost (food) | on racks (kg) | smoked / salt / hard (kg) | food kept |
|---|---|---|---|---|---|---|---|---|---|
| 18 (autumn 3) | 45 | 0.9 | 0 | 36 | 8.7 fresh | 0.5 | 0 | 0 / 35 / 0 | 16.2 |
| 19 (autumn 4) | 2 | 0 | 0 | 0 | 2 fresh, 6.7 salt | 0.4 | 0 | 0 / 28 / 0 | 12.7 |
| 20 (autumn 5) | 158 | 5.8 | 126 | 24 | 8.7 fresh | 2.4 | 122 | 0 / 50 / 0 | 78.9 |
| 21 (autumn 6) | 2 | 0 | 0 | 0 | 2 fresh, 3.3 smoked | 4.3 | 0 | 54 / 48 / 0 | 71.5 |
| 22 (autumn 7) | 30 | 1.7 | 21 | 0 | 8.7 fresh | 4.4 | 21 | 50 / 47 / 0 | 77 |
| 23 (autumn 8) | 2 | 0 | 0 | 0 | 2 fresh, 3.3 smoked | 4.3 | 0 | 53 / 45 / 0 | 69.6 |
| 24 (winter 1) | 1 | 0 | 0 | 0 | 1 fresh, 3.8 smoked | 3.7 | 0 | 46 / 44 / 0 | 62.3 |
| 25 (winter 2) | 0 | 0 | 0 | 0 | 4.3 smoked | 3.2 | 0 | 39 / 43 / 0 | 55.1 |
| 26 (winter 3) | 1 | 0 | 0 | 0 | 1 fresh, 3.8 smoked | 2.8 | 0 | 32 / 41 / 0 | 48.7 |
| 27 (winter 4) | 0 | 0 | 0 | 0 | 4.3 smoked | 2.3 | 0 | 26 / 40 / 0 | 42.4 |
| 28 (winter 5) | 1 | 0 | 0 | 0 | 1 fresh, 3.8 smoked | 2 | 0 | 21 / 39 / 0 | 36.9 |
| 29 (winter 6) | 0 | 0 | 0 | 0 | 4.3 smoked | 1.6 | 0 | 15 / 38 / 0 | 31.3 |
| 30 (winter 7) | 1 | 0 | 0 | 0 | 1 fresh, 3.8 smoked | 1.2 | 0 | 11 / 37 / 0 | 26.5 |
| 31 (winter 8) | 0 | 0 | 0 | 0 | 4.3 smoked | 0.9 | 0 | 6 / 35 / 0 | 21.6 |
| 32 (spring 1) | 0 | 0 | 0 | 0 | 4.3 smoked | 0.6 | 0 | 1 / 34 / 0 | 17 |

Totals: eaten 59.5 food; lost 34.7; keeping work 8.4 units (about 3% of the household's 267 units over these 15 days); fuel 22
firewood (220 kg, about 7 units of gathering); the fire burned 2 nights, about a 4% chance the hut burned; **17 food kept at spring**,
nearly all of it 34 kg of salt fish.

**The nights in words.**
- *Day 18.* Wat lifts 45 kg. Rule 1 keeps 8.7 kg back for supper; rule 2 salts the other 36 (Joan and Agnes, 0.9 units, 9 kg of
  salt). Nothing to hang; no fire.
- *Day 19.* A thin morning (2 kg). They eat it and some salt fish. Night 19 is the second cue: the eels run.
- *Day 20, the big day.* Wat and Hob work the weir's gap and lift the traps: 158 kg home by midday. Rule 1 keeps supper back; rule 2
  salts its last 24 kg (the salt runs out); rule 3 hangs 126 kg (Agnes and Joan, about 4 units, Wat when back); rule 5 has Hob tend.
  5.8 units of the 7 spare. Next morning: "Rule 2's salting stopped: no salt left". About 19 firewood go on the fire.
- *Night 20.* 122 kg in the smoke. A 2% chance the hut goes up that night.
- *Day 21.* Rule 6 at dawn: the cured eel (about 60 kg smoked) comes down into the house. Night 21, the third cue.
- *Day 22.* 30 kg: supper back, 21 kg hung, tended; down on day 23.
- *Winter.* The house eats smoked eel first (rule 7, the default), losing about 3 to 4 food a night to its going off at first, about 1
  by spring. The salt fish is hardly touched: it is what reaches the spring's lean days. Part 1's own check says the same: of fish
  kept from night 18, 37% of a keeping smoke is left at the end of winter against 75% of salt in brine [p1 §2.2].

**What binds.** Not the hut: the most on its racks at once is 122 kg of 250. Not the hands: 5.8 units on the biggest day against 7
spare. **The keeping smoke's shelf life** (about 7% a night) and **the wood**: 220 kg of it, about as many units to gather as to hang.

**A1, the same book without rule 2** (hang first, salt only what does not fit): rule 4 never fires, because the hut always has room
and the hands are enough. **The salt sits unused** and the household reaches spring with 10.5 food, the same as a household with no
salt (B below) and 6.5 less than A. A rule that salts "if the hut is full" is for a village smokehouse, not a household's: a household
that wants salt's long keeping must salt on purpose. That is a lesson for the fisher's lore (L-141) and the head's management lines
(part 4 HH3: "what is dried, smoked, salted ... keeps" could add "smoke is for the winter, salt for the spring and the long gap").

### 5.3 B. Wattle hut, no salt

The same book; rules 2 and 4 lapse ("there is no salt in the house").

| night | landed (kg) | hands (units) | hung (kg) | salted (kg) | eaten (kg) | lost (food) | on racks (kg) | smoked / salt / hard (kg) | food kept |
|---|---|---|---|---|---|---|---|---|---|
| 18 (autumn 3) | 45 | 2.2 | 36 | 0 | 8.7 fresh | 0.5 | 35 | 0 / 0 / 0 | 16.2 |
| 19 (autumn 4) | 2 | 0 | 0 | 0 | 2 fresh, 3.3 smoked | 0.9 | 0 | 13 / 0 / 0 | 12.2 |
| 20 (autumn 5) | 158 | 6 | 149 | 0 | 8.7 fresh | 2.9 | 145 | 12 / 0 / 0 | 78 |
| 21 (autumn 6) | 2 | 0 | 0 | 0 | 2 fresh, 3.3 smoked | 5.2 | 0 | 76 / 0 / 0 | 69.7 |
| 22 (autumn 7) | 30 | 1.7 | 21 | 0 | 8.7 fresh | 5.1 | 21 | 71 / 0 / 0 | 74.4 |
| 23 (autumn 8) | 2 | 0 | 0 | 0 | 2 fresh, 3.3 smoked | 4.9 | 0 | 72 / 0 / 0 | 66.4 |
| 24 (winter 1) | 1 | 0 | 0 | 0 | 1 fresh, 3.8 smoked | 4.3 | 0 | 64 / 0 / 0 | 58.6 |
| 25 (winter 2) | 0 | 0 | 0 | 0 | 4.3 smoked | 3.8 | 0 | 55 / 0 / 0 | 50.8 |
| 26 (winter 3) | 1 | 0 | 0 | 0 | 1 fresh, 3.8 smoked | 3.3 | 0 | 48 / 0 / 0 | 44 |
| 27 (winter 4) | 0 | 0 | 0 | 0 | 4.3 smoked | 2.8 | 0 | 40 / 0 / 0 | 37.2 |
| 28 (winter 5) | 1 | 0 | 0 | 0 | 1 fresh, 3.8 smoked | 2.3 | 0 | 34 / 0 / 0 | 31.4 |
| 29 (winter 6) | 0 | 0 | 0 | 0 | 4.3 smoked | 1.9 | 0 | 28 / 0 / 0 | 25.5 |
| 30 (winter 7) | 1 | 0 | 0 | 0 | 1 fresh, 3.8 smoked | 1.5 | 0 | 22 / 0 / 0 | 20.4 |
| 31 (winter 8) | 0 | 0 | 0 | 0 | 4.3 smoked | 1.1 | 0 | 17 / 0 / 0 | 15.3 |
| 32 (spring 1) | 0 | 0 | 0 | 0 | 4.3 smoked | 0.8 | 0 | 11 / 0 / 0 | 10.5 |

Totals: eaten 59.5; lost 41.3; keeping work 9.9 units; fuel 31 firewood (310 kg, about 10 units of gathering); 3 burning nights, about
a 6% chance of fire; **10.5 food at spring**, all of it smoked eel going off at 7% a night: two and a half nights of eating, gone in a
week. Salt's worth shows over the spring and the long gap, not the winter: of 100 kg kept from one autumn to the next (32 nights),
about 10 kg of keeping smoke is left, 42 of a hard cure, 52 of salt fish in brine [rates p1 §2.2].

### 5.4 C. Timber smokehouse (3 sets), 15 kg of salt, two parts in five salted for a hard cure

The book as A with rule 2 replaced by *"Salt two parts in five of what comes in and hang it for a hard cure, while the salt lasts"*
(a load into the tub and a hang for a hard cure, §4.5 example 7).

| night | landed (kg) | hands (units) | hung (kg) | salted (kg) | eaten (kg) | lost (food) | on racks (kg) | smoked / salt / hard (kg) | food kept |
|---|---|---|---|---|---|---|---|---|---|
| 18 (autumn 3) | 45 | 2.6 | 36 | 15 | 8.7 fresh | 0.5 | 35 | 0 / 0 / 0 | 16.2 |
| 19 (autumn 4) | 2 | 1 | 0 | 0 | 2 fresh, 3.3 smoked | 0.7 | 14 | 7 / 0 / 0 | 12.5 |
| 20 (autumn 5) | 158 | 7.1 | 149 | 45 | 8.7 fresh | 2.7 | 158 | 6 / 0 / 0 | 78.5 |
| 21 (autumn 6) | 2 | 1 | 0 | 0 | 2 fresh, 3.3 smoked | 4.2 | 43 | 50 / 0 / 5 | 71.2 |
| 22 (autumn 7) | 30 | 1.7 | 21 | 0 | 8.7 fresh | 4.2 | 62 | 46 / 0 / 5 | 76.8 |
| 23 (autumn 8) | 2 | 0 | 0 | 0 | 2 fresh, 3.3 smoked | 4 | 0 | 49 / 0 / 21 | 69.7 |
| 24 (winter 1) | 1 | 0 | 0 | 0 | 1 fresh, 3.8 smoked | 3.5 | 0 | 42 / 0 / 20 | 62.6 |
| 25 (winter 2) | 0 | 0 | 0 | 0 | 4.3 smoked | 3.1 | 0 | 36 / 0 / 20 | 55.6 |
| 26 (winter 3) | 1 | 0 | 0 | 0 | 1 fresh, 3.8 smoked | 2.6 | 0 | 29 / 0 / 19 | 49.4 |
| 27 (winter 4) | 0 | 0 | 0 | 0 | 4.3 smoked | 2.2 | 0 | 23 / 0 / 19 | 43.2 |
| 28 (winter 5) | 1 | 0 | 0 | 0 | 1 fresh, 3.8 smoked | 1.8 | 0 | 18 / 0 / 18 | 37.9 |
| 29 (winter 6) | 0 | 0 | 0 | 0 | 4.3 smoked | 1.4 | 0 | 13 / 0 / 18 | 32.4 |
| 30 (winter 7) | 1 | 0 | 0 | 0 | 1 fresh, 3.8 smoked | 1.1 | 0 | 8 / 0 / 17 | 27.8 |
| 31 (winter 8) | 0 | 0 | 0 | 0 | 4.3 smoked | 0.8 | 0 | 4 / 0 / 17 | 23 |
| 32 (spring 1) | 0 | 0 | 0 | 0 | 3.8 smoked, 0.4 hard | 0.5 | 0 | 0 / 0 / 16 | 18.5 |

Totals: eaten 59.5; lost 33.3; keeping work 13.4 units (the hard cure's fish salted and hung, and tended three nights); fuel about 39
firewood (390 kg: the hard cure at 0.25 a kg, about 13 units of gathering); 5 burning nights, about a 4% chance of fire (the hut's 3
nights: 6%); **18.5 food at spring**, 16 kg of it hard-cured eel that will see the next run and can travel.

**Reading.**
- **At spring the timber house is no better fed than the hut with salt** (18.5 against 17). Its gains are elsewhere: the hard cure is
  light (1.15 food a kg against salt fish's 0.46), dry, needs no barrel, and keeps to the next autumn (42% after a year), so it is the
  trade good and the long gap's food; and the house seldom burns.
- **Its 750 kg of racks are never a quarter full** (158 kg at most). For one household a timber smokehouse is not more room: it is
  the building of a village's fish trade, of a weir-holding household, or of a buyer. Since only it makes the good that travels
  (D2-271), it is a chokepoint (scenario_design §1).
- **It costs more for the same food**: 13.4 units against 8.4, and nearly twice the wood. The work buys keeping into next year and
  trade, not food this winter. The building itself is 35 to 55 units at 1/7 against the hut's 7 to 14 [p1 §3.6].

### 5.5 D. Wattle hut, 15 kg of salt, no rules: everything by hand

The same household and catch, every keeping step an act in someone's plan, made at dawn without knowing the catch. The agents drop
routine things (standing_rules.md, "Alternatives"; 02zzy §3: Haiku youths tended when told to and "trapped only when told to"). Three
ordinary misses, each of a kind the runs showed:

- **Day 20, the fire not tended.** Agnes hangs 149 kg (her plan says "smoke fish" five times); Hob's plan, made at dawn, has him at
  the weir; nobody plans "tend the smoke". The fire dies, the lot does not count the night and spoils at the fresh rate: **26 food lost
  that night**. It cures a night late.
- **Day 21, the cured lot left up.** Nobody plans "take down"; the lot is still curing from the missed night in any case.
- **Day 22, the catch not hung.** Wat lifts 30 kg; Agnes's plan had "smoke fish", but in the interleaved order (`run.py:995-1000`) her
  first act ran before his lift and was refused ("you have no fish to hand"), and a refused act is not tried again that day
  (`run.py:1007-1009`). The fish waits a night in the house; 7 kg is hung on day 23. The salt is never used: nobody's plan thought of
  it.

| night | landed (kg) | hands (units) | hung (kg) | salted (kg) | eaten (kg) | lost (food) | on racks (kg) | smoked / salt / hard (kg) | food kept |
|---|---|---|---|---|---|---|---|---|---|
| 18 (autumn 3) | 45 | 2.2 | 36 | 0 | 8.7 fresh | 0.5 | 35 | 0 / 0 / 0 | 16.2 |
| 19 (autumn 4) | 2 | 0 | 0 | 0 | 2 fresh, 3.3 smoked | 0.9 | 0 | 13 / 0 / 0 | 12.2 |
| 20 (autumn 5) | 158 | 5 | 149 | 0 | 8.7 fresh | 26.3 | 94 | 12 / 0 / 0 | 54.6 |
| 21 (autumn 6) | 2 | 1 | 0 | 0 | 2 fresh, 3.3 smoked | 1.9 | 91 | 8 / 0 / 0 | 49.7 |
| 22 (autumn 7) | 30 | 0 | 0 | 0 | 8.7 fresh | 7.1 | 0 | 50 / 0 / 0 | 52.4 |
| 23 (autumn 8) | 2 | 1.2 | 7 | 0 | 8.7 fresh | 3.3 | 7 | 47 / 0 / 0 | 46.1 |
| 24 (winter 1) | 1 | 0 | 0 | 0 | 1 fresh, 3.8 smoked | 2.9 | 0 | 43 / 0 / 0 | 39.6 |
| 25 (winter 2) | 0 | 0 | 0 | 0 | 4.3 smoked | 2.5 | 0 | 36 / 0 / 0 | 33.1 |
| 26 (winter 3) | 1 | 0 | 0 | 0 | 1 fresh, 3.8 smoked | 2 | 0 | 30 / 0 / 0 | 27.6 |
| 27 (winter 4) | 0 | 0 | 0 | 0 | 4.3 smoked | 1.6 | 0 | 24 / 0 / 0 | 21.9 |
| 28 (winter 5) | 1 | 0 | 0 | 0 | 1 fresh, 3.8 smoked | 1.3 | 0 | 19 / 0 / 0 | 17.1 |
| 29 (winter 6) | 0 | 0 | 0 | 0 | 4.3 smoked | 0.9 | 0 | 13 / 0 / 0 | 12.2 |
| 30 (winter 7) | 1 | 0 | 0 | 0 | 1 fresh, 3.8 smoked | 0.6 | 0 | 9 / 0 / 0 | 8.1 |
| 31 (winter 8) | 0 | 0 | 0 | 0 | 4.3 smoked | 0.3 | 0 | 4 / 0 / 0 | 3.8 |
| 32 (spring 1) | 0 | 0 | 0 | 0 | 4.1 smoked | 0 | 0 | 0 / 0 / 0 | 0 |

Totals: eaten 59.3 (a fifth of a meal short on the first night of spring); lost 52; keeping work 9.4 units; fuel 29 firewood; **nothing
left at spring** against A's 17. One untended night on the big lot costs more than the whole winter's other losses together. The
misses are real behaviour, not an engine fault; rules are the household's way to stop making them, which is what D4-16 and
standing_rules.md "Why" (Ashford's seed) wanted rules for. A careful Opus head writing a full plan each day would miss less; the gap
between rules and hand acts is largest for routine steps and for steps that hang on what the day brought.

**A design note from D.** Part 1's "fire out: the fresh rate" makes a single missed tend lose about a third of a hanging lot, and the
lot then cures a night later in any case. That is harsher than a real smoulder going out for a night (the fish half-dry by then,
est.). A middle rate (the fresh rate under a roof for the first night out, the in-smoke rate's x3 say) is worth a look in part 1 (§7
item 3).

### 5.6 What the result turns on: how a shelf life becomes a nightly loss

The same households under part 1's reading ("keeps d days" = half lost by then, on its curve's nights) and two others, with the same
nights; and with smoked fish at today's rate (food kept at spring, and food lost over the run and winter):

| | half lost (part 1 §2.1) | a quarter lost | a tenth lost | smoked fish at today's rate (0.0015 a night in a house) |
|---|---|---|---|---|
| A (hut, 60 kg salted first) | 17 kept, 35 lost | 32.7 kept, 19 lost | 42.8 kept, 9 lost | 40.3, 12 |
| A1 / B (hut, salt unused / no salt) | 10.5 kept, 41 lost | 28.4 kept, 23 lost | 40.4 kept, 11 lost | 47.7, 4 |
| C (timber, hard cure) | 18.5 kept, 33 lost | 32.3 kept, 20 lost | 41.2 kept, 11 lost | 40.3, 11 |
| D (no rules) | 0 kept, 52 lost | 9.5 kept, 42 lost | 16.1 kept, 36 lost | 20.2, 32 |
| A with brine (a tub or barrel) | 19.5 kept, 32 lost | 34 kept, 18 lost | 43.3 kept, 8 lost | 42.8, 9 |

(The last column changes only smoked fish; salt fish stays on part 1's rate there, which is why salting loses food there: it turns a
good that never spoils into one that does.)

- **Under today's smoked-fish rate, salting and the hard cure make a household worse off** (47.7 against 40.3): hunt_fish_materials
  §7.3's "smoking would make salt pointless". Part 1's curve is what gives salt, brine, the hard cure and the timber smokehouse their
  reasons.
- **Under part 1's half-lost reading, a careful household ends the winter with 10 to 20 food of 112 caught, and the run's catch mostly
  rots or is eaten in the first fortnight.** That is harsher than the real record: salmon kept "over winter in a cool, dry place"
  (smokehouse_capacity §3) did not lose a third by midwinter (est.). Under a quarter lost, the households keep 28 to 34, salt still adds
  about 4 food at spring and, over the long gap, keeps about two thirds against the keeping smoke's third.
- **A constant share is the wrong shape anyway.** Preserved food keeps nearly whole for a while and then goes (mould, rancid fat,
  insects). The faithful model is a curve by the lot's age, which needs dated lots in stores; a store holds one quantity a good today
  (`night.py:176-197`). The processing unit already keeps lots with a day (§2.1); carrying the day into the store is the step that would
  allow it. I recommend keeping part 1's curve for the nights, reading "keeps d days" as **about a quarter lost by then** for now, and
  flagging the age curve for later with the stores (W80-Q1). If Zach keeps part 1's half, the walk says rules and salt matter more.

### 5.7 What the walk says about the design

- **For a household, D2-284's racks are ample and the hands mostly enough.** A glut binds on hands only on days above about 200 kg
  landed (7 units of hanging); on the racks only above 250 kg in a day. Hands, wood, salt and fire bind for a village sharing a hut and
  a weir-holding household; for an ordinary trap household **the bind is the keeping's shelf life, the wood and the salt**.
- **The wood binds now** on part 1's prices: 220 to 390 kg for a run's keeping, 7 to 13 units of gathering, as much again as the
  hanging. A household that has not stacked wood by the run smokes less. This is real (fuel was a smokehouse's main cost,
  smokehouse_capacity §4) and ties keeping to the woods (W-76).
- **Keeping is about 3 to 5% of the household's work over the run and winter**, about 6 to 10% with its wood; with the lifting and the
  weir the food work is about 15%, inside scenario_design's 30%.
- **Salt's value shows only if salted on purpose and over the spring and the long gap**: a design that wants inland salt trade (the
  brine spring, the saltmarsh) to matter needs the fisher's lore to say so and the long gap to be felt.
- **Rules matter most on the days the catch is unknown at dawn** and for the routine steps (tending, taking down); the tend matters
  most of all.

---

## 6. Alternatives considered, and why not

| Alternative | Why not |
|---|---|
| **Five bespoke mechanisms** (as today for the smokehouse and hearth rack, new code for retting and tanning) | §2.7: five capacity checks, night steps and failures; rules and signs special-cased; the engine already shares the rack pile between two |
| **Processes as timers on the goods, no container** ("becomes smoked fish on day N") | goods are quantities, not items; no capacity, so the hut never binds; no place for fire or spate; a shared smokehouse's ownership lost |
| **The container as a slowing store** (a smokehouse with fire keeps goods at a low rate, as `house_spoil` did) | the blanket multiplier D2-272 removed; processing must change the good, not slow it |
| **Salting fish as a lot of 1 night** (part 1 §2.4 lists 1 night of settling) | a wait with no failure and no capacity bind, since the tub is also the store; kept instant, meat at 3 nights (W80-Q8) |
| **Tending at real hours (5 to 16 units a night)** | treats duration work as quantity work; a keeping smoke would cost more tending than hanging; §2.5's rule instead |
| **Tending folded into the fuel, no labour** | the fire-dies rule makes the smoke a chore worth a rule; the runs show youths doing it (02zzy) |
| **Done lots go into the store at once** (today, `night.py:300-307`) | hides the choice of where cured goods go, and racks never block; simpler, and with D2-274's free move within a building it costs nothing to keep (W80-Q11) |
| **Rules fire on events only** (edge triggers) | a missed chore is lost; the agent must re-arm; states with a latch are robust |
| **Rules read the world's state** ("when the run begins") | an oracle: the river's signs and attention stop mattering (D4-35) |
| **Rules may do any act, production included** | the household runs itself and the turn becomes moot; what a run measures is the daily choice of work (standing_rules.md item 7) |
| **Chores take units from plans, or come before them** | D2-274: spare units only; and before the plans they could not see the day's catch |
| **The fallback before chores** (as now, by position) | the fallback fills every unit (L-142); chores would never run |
| **One good per fish with a cure attribute** | the engine's goods are flat names everywhere (ITEMS, EDIBLE, stores, trade); part 1 already adds hot-smoked and hard-cured fish as goods |
| **The hut's capacity kept low to make it bind** | D2-284 decided the real load |

---

## 7. Conflicts with decisions, with part 1 and part 4, and with the code

**Between decisions, parts and notes:**
1. **Part 1 §2.1 against this note (W80-Q1):** part 1 reads "keeps d days" as half lost by then; §5.6 shows that reading leaves a
   careful household 10 to 20 food of 112 and a careless one nothing; I recommend a quarter. Both use part 1's curve for the nights.
2. **Part 1 §2.4 against W80-Q8:** part 1 lists salting's settling as 1 night; I recommend salting fish at once (as now) and meat as a
   3-night lot.
3. **Part 1 §2.2, "fire out: the fresh rate in the open":** inside a smokehouse there is a roof, so I used the fresh base (0.37), not
   the open's x2; even so one missed tend loses about a third of the lot (§5.5). Part 1 should say which, and whether a first night out
   should be gentler.
4. **Part 1 §3.1, tending as "a named departure",** against §2.5's rule that duration work compresses with the duration (W80-Q4).
5. **D2-284 and part 1 §3.6 against smokehouse_capacity.md §8 and storage.md §11** (500 fish on 2 spaces; a timber house of 1,500): part
   1 follows D2-284 (250 on 1 space, 750 to 1,000 a small timber house), and so does this note; the notes need a line at the top saying
   so (part 1 §5.4 item 15).
6. **Part 4 §2.4's rules block** gives the grammar with `unless` only; D2-282's conditions need `when` and `if` in it (§4.1, about 20
   words).
7. **D2-272 against D2-212** (fresh fish twice as badly in a store): `DECAY["fresh fish"]["store"] = 2.0` (`data.py:126-127`),
   `night.py:347`. Part 1 §2.3 drops the x2, folding it into fresh fish's base. Agreed.
8. **D2-272 against the in-process factor:** `DECAY["drying meat"]["smoke"] = 0.25` (`data.py:122`, `night.py:331-334`) multiplies below
   the good's own rate; part 1's 0.03 in the smoke as the base fixes it (§2.4). Part 1 §2.3 also keeps `smoke` 0.25 "standing for"
   removing flies from stored goods: two uses of one factor, to be separated.
9. **D2-273 against `clocks.py`:** `TECHNIQUES.*.rack.nights` and `ITEMS.*.spoil` are listed on the day clock (`clocks.py:20`, `:23`).
   Under D2-273 process times and keeping are on the year clock: the nightly share stays a night's share but is derived from a
   year-clock shelf life, and rack nights from real durations at 1/11.4.
10. **D2-283 against the code:** `salt fish` and `salt meat` are 4 a unit and 1 to 4 salt for both (`data.py:639-642`).
11. **D2-284 against the code:** rack nights 3 (`data.py:625`, `:632`); capacity fittings x racks x batch (`keeping.py:39-47`); smoke racks
    3 spaces and 2 timber (`data.py:275-276`); the `does` and `manual` texts saying "40" and "3 nights" (`data.py:277`, `:627-629`,
    `:633-635`); keeping.py's docstring (`keeping.py:1-12`).
12. **D2-271's order of keeping against the shelf lives:** smoked fish 0.005 keeps longest (`data.py:55`), salt fish 0.01 (`:50`), salt
    meat 0.003 (`:93`); part 1 §2.2 restores the order.
13. **D2-272 against `house_spoil` and the fittings' `spoil`** (`data.py:776`; bins 0.5, granary 0.2, cellar 0.25; `night.py:346-347`):
    known (storage.md §7; part 1 §2.1).
14. **Fuel flat a night** (`data.py:835`, `keeping.py:186`) against fuel as a total by kg hung [p1 §3.1].
15. **Smoke fish at 1 unit whatever the batch** (`data.py:624`) against 30 a unit; whole-unit costs before the act (`verbs.py:116-150`,
    `run.py:1014`).
16. **Done lots do not block the racks today** (`keeping.py:28-31`, `:39-47` count only curing goods) against hunt_fish_materials Q10(d)
    ("the cost is full racks for the next catch") (W80-Q11).
17. **The fallback's place** (`run.py:1036-1057`, D4-76) against chores from spare units (D2-274): both claim the units left after the
    plan; the order is written nowhere (W80-Q13).
18. **The day's interleaved acts** (`run.py:995-1000`) make a same-day hand-off between people depend on their order; not a conflict with
    a decision, but the reason the chore phase sits after the plans.
19. **`here.party_container`** goes to the first-claimed building (`here.py:379-387`; store_rules' finding): work done for a household
    never reaches a later smoke hut or tub by default; `go` rules fix it, the default (D1) must too.

**With 37.4's areas (read, not edited):** standing_rules.md item 7 lists "the fire" for later rules ("keep it lit"), meaning the
hearth; §4's `tend` is the same verb for a container's fire, and the two should be one. The chore phase is a change to the day's loop
in `run.py`, 37.4's; to go to the board.

---

## 8. Couplings to other parts

- **Part 1 (W-77, final):** every price here; the shelf-life reading (W80-Q1) and the fire-out rate (§7 item 3) go back to it.
- **Part 2 (making, `wave2_making.md`, in progress):** how racks, tubs, troughs, barrels, tan pits and the retting pit are made; the
  cooper (salt's year); tanning's lime (part 1 assumes wood ash); leather's uses. Left to it.
- **Part 3b (W-81, taking):** the lift and its result line (a trigger reads it); the river's signs as triggers ("seen"); set and lift as
  two acts.
- **Part 4 (W-78, final):** the rules block (§7 item 6); the head's management lines (HH3 could carry "smoke for the winter, salt for
  the spring"; HH4 the containers); the fisher's lore; who knows the hard cure and the retting.
- **Stores (D2-279, storage.md, part 1 §2.3, §3.3):** racks, tubs and barrels as containers; the smoke loft; vermin on hanging goods; the
  scale gap (L-154, handed on to part 3 by part 1 §7).
- **The hard-cured meat good** (handed on by part 1 §7): bacon and ham are the hard cure of meat (salted 1 to 8, D2-283, then smoked); the
  same process row with meat as its input; I recommend it comes with the fish (W80-Q7).
- **Buildings and the building clock (D2-276, D2-281; 37.4's):** the hut room of 2 spaces, tiers and lofts, fire and spread by structure.
- **Withies and wood (W-76):** racks of withies and timber; firewood for the smoke, now a real bind.
- **Salt:** the brine spring and pans (`keeping.near_spring`; `data.py:608-616`), the saltmarsh; inland salt as a dependence.
- **Tanning (D2-281):** bark from coppice in late spring (peeling 1.5 bundles a unit [p1 §3.1]), wood ash, hides from hunters and
  herders; the pits' fouling.
- **Retting and flax:** the close, the pond, the fouling downstream (hunt_fish_materials §7.5).
- **Acts on owned things (Q-80):** taking another household's lot from a shared smokehouse is a choice, named and noticed.
- **Households as shared books (L-151), fallbacks (L-142):** the chore phase and its order.
- **Signs (the senses guide):** §2.6's bundle, to be checked through `perceive.chance_of`.
- Part 1 §7 also hands part 3 coin's weight and containers' protection against theft (L-156): neither is keeping; coin goes to the
  money owner, the locked chest stays deferred.

---

## 9. Questions for Zach

Each stands alone. Ids are this note's own (W80-Qn), not yet recorded as asks.

**1. What "keeps for d days" means as a nightly loss (W80-Q1).** The engine loses a fixed share of a good each night; part 1 turns
"keeps d days" into nights on a curve (a keeping smoke 9.7, a hard cure 25.5, salt 33.8) and reads that as the half-life: half gone by
then. Worked through a winter (§5.6), a household that catches 112 food of eel keeps, at spring: (a) half lost (part 1): 10 to 20 food
if careful, nothing after one missed tend; (b) a quarter lost: 28 to 34; (c) a tenth lost: 40 to 43, and salt barely matters before the
next run; (d) a curve by age (nearly whole until its time, then going fast), the real shape, needing dated lots in stores. **Recommend
(b) now, with part 1's curve for the nights, and (d) flagged for later.** With today's uncompressed rates salt makes a household worse
off, so the curve itself should stand. **Blocks:** every shelf life, the stores' calibration, and whether salt, brine and the timber
smokehouse are worth building.

**2. Processing containers as one engine unit (W80-Q2).** Smoke racks, a salting tub, drying racks, tanning pits and retting ponds as
one unit: a process table (in, out, nights by depth, ratio, inputs, capacity, load and unload work, tending, failures, what is left past
its nights, fouling, what it protects once done), lots in containers counting nights while conditions hold, one night step, one load,
one tend, one unload. Options: (a) one unit, today's smokehouse and hearth rack its first rows; (b) five bespoke mechanisms.
**Recommend (a)**, with the test that a process enters only if its wait, capacity or failure binds something. **Blocks:** the racks'
rebuild under D2-284, tanning (D2-281) and retting in this build, and the rule triggers.

**3. How conditional rules fire (W80-Q3).** D2-282 lets a rule fire on a state change. Proposed: (a) triggers are states that persist
("a cured lot is on the racks"), latched when they come true and held until the chore is done, so a missed chore is not lost; events
that leave no state latch for the day; (b) a trigger reads only what the household knows (its containers and stores, its acts' results,
the calendar, signs its members noticed), never hidden state such as the run's pulses; (c) chores run in a chore phase after everyone's
plans and before the fallback, from spare units, in the order tend, load the most perishable, take down, move; (d) a rule whose
condition holds counts as more specific than the same rule without. **Recommend all four.** **Blocks:** the standing rules build (37.4's
W-37), the store rules (D2-274), part 4's rules block.

**4. Work that runs through a compressed process (W80-Q4).** Tending a smoulder for a real fortnight is 11 to 33 real hours; at real
hours it would cost 5 to 16 units a smoke night; the engine charges 1, which part 1 keeps as a named departure. Proposed clock rule: work
that scales with the quantity (hanging, salting, scraping) is at real hours; work that scales with the duration (tending, feeding a pit,
watching) compresses with the duration, about 1/11.4; materials stay real totals. Options: (a) write that rule into the clocks spec; (b)
keep each case a named departure. **Recommend (a).** **Blocks:** tending, the tan pit's feeding, and any later chore through a long
process.

**5. A set of racks on one space, and the room caps (W80-Q5).** Part 1, following D2-284, puts a set at 250 fish on 1 space and a small
timber or stone room at 3 to 4 tiered sets (750 to 1,000); the earlier notes had 500 on 2 spaces. Options: (a) part 1's; (b) the notes'.
**Recommend (a)**, extended to a medium room at 8 to 10 tiered sets. **Blocks:** the smokehouse rebuild.

**6. What a rule may do (W80-Q6).** Options: (a) keeping only: go, keep, hold back, first, eat, move, load (hang, salt, sink, lay in,
spread), tend, take down; (b) also production (lift the traps, gather). **Recommend (a):** production, trade and travel stay the daily
choice a run measures. **Blocks:** the rules grammar.

**7. Hard-cured meat with the fish (W80-Q7).** Part 1 adds hot-smoked and hard-cured fish as goods and proposes hard-cured meat (bacon,
ham) beside them, for part 3 to confirm. Options: (a) hard-cured meat in the same build, the same process row with meat as input (salted
1 to 8, D2-283, then 2 to 3 nights in timber or stone); (b) later. **Recommend (a)**: it costs a row, and gives herders and hunters the
long keeper fishers get. **Blocks:** the hard cure's process row.

**8. Salting fish at once, meat over nights (W80-Q8).** Options: (a) salting fish stays an instant act (D2-283's rate), the tub or barrel
only a store; salting meat a 3-night lot in the tub; (b) both as lots of part 1's 1 night; (c) both instant. **Recommend (a).**
**Blocks:** the salting rebuild under D2-283.

**9. A brine container before the cooper (W80-Q9).** Salt fish reaches its year only in brine (part 1 §5.4 item 20); on a dry floor it
keeps at x1.5 on the hazard, out of salt at x2, and barrels wait for a cooper. Options: (a) a salting tub or trough of timber, basic,
about 120 kg in brine, now; barrels later for trade; (b) nothing until barrels. **Recommend (a)**: in the walk brine adds about 2.5 food
at spring and keeps half again as much salt fish over the year, and without it salt is hard to see the point of. Its making is part 2's.
**Blocks:** salt's value in this build.

**10. Drying racks (W80-Q10).** Options: (a) the hearth rack at 1 night (part 1) and its batch as now; an outdoor wind rack later, with
stockfish and the coast; fat and lean fish not told apart (a named departure: eels dry as well as cod); (b) the wind rack now and a fat
or lean trait on fish. **Recommend (a).** **Blocks:** the hearth rack's recost.

**11. Where a finished lot goes (W80-Q11).** Options: (a) it stays in the container, counts against its room, and comes down by rule or
act (free within the building); (b) as today, into the building's store at once if there is room. **Recommend (a):** where cured goods
go becomes a visible choice, and an untaken lot costs the next catch, which is real. **Blocks:** the processing unit's night step.

**12. Tanning's time on the year clock (W80-Q12).** Real pit tanning takes 6 to 18 months, 16 to 48 nights (part 1), so a hide laid down
in spring comes out the next year or later. Options: (a) 16 to 24 nights (lighter leathers, 6 to 9 months), heavy sole leather later;
(b) the full range; (c) shorter, a named departure. **Recommend (a).** **Blocks:** tanning in this build (D2-281).

**13. Chores before the fallback (W80-Q13).** Both claim the units left after the plan; the fallback fills them all (L-142). Options: (a)
chores first, then the fallback; (b) the fallback first. **Recommend (a).** (Part of W80-Q3 (c), asked alone in case L-142's redesign
moves the fallback.) **Blocks:** the chore phase in `run.py`.

**The five that matter most:** W80-Q1 (what "keeps for d days" means), W80-Q2 (one unit), W80-Q3 (how rules fire), W80-Q4 (duration
work compresses), W80-Q9 (brine before the cooper).

---

## Sources

- Part 1, `wave1_physical_basis.md` (§1.1 the food goods, §1.3 firewood's bundle, §2 shelf lives and the keeping curve, §2.3 penalties,
  §2.4 process times, §3.1 the day clock's recipes, §3.3 containers, §3.4 fittings, §3.6 the smokehouses, §5.4 contradictions, §7
  hand-ons); part 4, `wave4_people.md` (§2.4 the rules block, §3.4 the head's lines).
- The code (read 22 Nov): `cybertron2/engine/keeping.py`, `night.py:176-352`, `verbs.py:116-150`, `:755-840`, `run.py:990-1057`,
  `data.py:20-130`, `:234-300`, `:600-660`, `:776`, `:830-836`, `clocks.py:1-60`, `here.py:379-440`, `buildings.py:120-215`, `things.py:16`,
  `wild/runs.py:1-40`, `wild/kinds.py:58`, `:649`, `:873`, `bots_livelihood.py:164-192`.
- The records: D2-271, D2-272, D2-273, D2-274, D2-276, D2-279, D2-281, D2-282, D2-283, D2-284; Q-83 and Q-73 (closed by D2-284 and
  D2-283); L-142, L-151, L-154, L-155; the context pack for W-73.
- The notes: `smokehouse_capacity.md`, `storage.md`, `store_management.md`, `02zzx_salting_rates.md`, `02zzy_why_they_did_not_fish.md`,
  `02zzu_lookup.md` (each marks its own sources, mostly search summaries).
- Real figures marked (est.) here and not in part 1 or the notes (pit capacity, stockfish drying, eels' fat against drying, a smoulder
  half-drying fish before it goes out) are general knowledge, not checked against a source tonight.
- The walk's arithmetic: a script in the session's scratchpad (not kept in the repository), on §5.1's parameters.

*Current as of 22 Nov 2026.*
