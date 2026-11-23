# U4. Processing containers: lots that become the next good over nights

**Status:** discussion (component spec of the integrated design, W-85). The parts decided are cited; nothing built.
**Owner:** 37.2 (the unit, its data rows, its night step). 37.4 is named on the merge for what lands in its areas: the `make` verb's
loading branch (`verbs.py`), the building cap on sets (`buildings.py`), the fittings' costs (U7), and the house lines in the prompt.
**Thread:** the integrated design (W-85), under the network (W-73); the earlier note's thread is W-80 (keeping).


> **Decisions since this spec was written (binding over its text; the build reads this table first):**
> - **D2-313:** 37.2 owns every engine file this wave changes (read every '37.4' in the code tables as 37.2 for this wave).
> - **D2-327:** tanning and leather deferred until the wave is tested (frame, harness and bellows in leather, tanning's pollution with it).
> - **Default corrected (B10):** hard-cured meat keeps the salt meat's food: 0.57 / 0.85 = about 0.67 food a kg (salt meat is 0.57).

## Extends

Each read in full, not from a summary:

- **D2-271** (three depths of smoke by building; racks of withies and timber), **D2-272** (a store never slows a food below its base),
  **D2-273** (three clocks; process times on the year clock, floored at a night), **D2-283** (salting 20 kg an hour with gutting,
  salt 1 to 4 for fish, 1 to 8 for meat), **D2-284** (capacity from racks; the building caps the sets; material sets depths, life,
  fire; a keeping smoke holds its racks 1 night, a hard cure 2 to 3), **D2-288** (handling units, recipes in kg), **D2-289** (a
  shelf life read as a quarter lost by then), **D2-290** (fuel at real weight), **D2-291** (a set is 250 kg on 1 space; Q-83's 500 on
  2 corrected), **D2-295** (each depth its own good; a lot becomes the next good when its nights are counted), **D2-282** (rules fire
  on state changes: "a cure finished"), **D2-298** (bots test interfaces only).
- **hunt_fish_materials.md §7.3** (the keeping paths) and **open question 10** (the smokehouse as a store; racks as containers; (e)
  processing containers in general), **§7.5** (pollution: retting and tanning), **§7.6** (tanning).
- **wave3_keeping.md §2 to §3** (the strongest draft: one unit for every processing container; the in-process good's base; quantity
  and duration work; the smokehouse table). Its §5 walk is not carried (see Departures).
- **wave1_physical_basis.md §1.1** (the goods and ratios), **§2.2 to §2.4** (the keeping curve, the penalties, process times), **§3.1**
  (day-clock work rates), **§3.6** (the smokehouses).
- **basis.md** §1 (process times, quantity and duration work, the floor), §2 (firewood bundle, timber load), §3 (food unit, smoking
  fuel, the keeping order, depths, salting, racks, hanging, gutting), §5 (moving within a building).
- **The code as it stands** (read 22 Nov): `keeping.py` (the smokehouse and racks), `night.py:77-78` (the smokehouse's night),
  `:176-207` (spoilage and the rack's end), `:286-308` (`_dried`), `:311-352` (`decay_rate`, `spoil_rate`), `verbs.py:760-845`
  (`_make` and its rack branch), `:669-672` (`smoke_tend`), `data.py:49-58`, `:92-95` (the fish and meat goods), `:117-130` (DECAY),
  `:238`, `:248`, `:272-277` (racks on hearth, fire ring, smoke racks), `:618-650` (the smoking, salting and drying techniques),
  `:835` (PHYSICS smokehouse), `clocks.py:20-23`, `here.py:423-470`, `prompt.py:572-650` (`house_food`, `house_known`).

## Departures

| # | From | This spec | Why |
|---|---|---|---|
| 1 | wave3_keeping §5 (the night-by-night winter on a 243 kg catch and the half-lost reading; its conclusions "the hut never binds", "17 food at spring", "salt makes no difference unless salted on purpose") | not carried. §5 below re-derives a worked season on the bot catch basis (D2-293, D2-297) and D2-289's quarter-lost rates | the catch was invented and the reading replaced (brief rule 3) |
| 2 | wave1 §2.1 and wave3 §2.4 rates (fresh fish 0.37, a keeping smoke 0.069 a night) | D2-289's rates: fresh fish 0.17, keeping smoke 0.029, hard cure 0.011, salt 0.0085, dried 0.0069 (Basis rows needed, 1) | D2-289 replaced the half-lost reading |
| 3 | hunt_fish_materials §7.3 ("about 500 fish a set of racks on 2 spaces"; fuel "1 firewood per 60 fish") and storage.md §11 (a hut of 500, a timber house of 1,500) | a set is 250 kg on 1 space (D2-291); fuel 0.15 bundles a kg hung (basis §3) | D2-284, D2-291, D2-288; wave_conflicts C1, C21 |
| 4 | D2-271 "a timber or stone smokehouse ... holds more a space (tiers, an upper storey)" read by wave3 as tiered sets that hold the same 250 kg | a set holds 250 kg on 1 space in any building (D2-291); "more a space" is met at the building: a hut room loses 1 of its 2 spaces to the fire and the work (125 kg a space of floor), a small timber or stone room 2 of 6 (167), a medium room 2 of 12 (208); the loft or upper storey of a timber or stone house is a store for cured goods (U5) | D2-291 fixes the set; the building-level reading keeps D2-271 without a second rack number nobody has a source for. Stated so Zach can say otherwise (Q-U4-4) |
| 5 | hunt_fish_materials Q10(c): with a fire, hanging on deepens "unsalted fish to the long end of a keeping smoke" | a done keeping smoke under a continued fire stays smoked fish; only salted fish deepens, to a hard cure, in timber or stone | D2-295: each depth is its own good with one shelf life; there is no "long keeping smoke" good |
| 6 | the code: a done batch goes into the building's store at once (`keeping.done_into_store`, `night.py:298-307`) | a done lot stays in its container, counts against its room by the kg loaded, and comes down by an act or a rule (default taken: Q-U4-2) | where cured goods go becomes a choice the book can make (D2-282's example "move smoked fish to the cellar once cured"); full racks then cost the next catch (hunt_fish_materials Q10(d)); wave_conflicts C28 |
| 7 | wave3_keeping §2.2 (W80-Q8): salting meat a 3-night lot | salting fish and meat both at once (a row with no nights); the tub or barrel is then the store | a wait with no failure and little bind on room adds a state for nothing; the hard cure already carries meat's long wait (bacon); Q-U4-3 |
| 8 | basis §5 "taking down is quantity work" with no rate | taking down at 120 kg a unit (est.; Basis rows needed, 4) | a rate is needed to build; wave_conflicts C23 |
| 9 | basis §3 gutting "never paid twice" with no rate for hanging a gutted fish | hanging salt fish or gutted fish for a hard cure at 60 kg a unit (est.; Basis rows needed, 3) | C25: the hanging rate includes splitting |
| 10 | today's in-process factor `DECAY["drying meat"]["smoke"] = 0.25` (`data.py:123`) | the in-process good's base is its rate in the container's conditions, 0.03 a night in the smoke (wave1 §2.2, est.); a failed night takes the input's base | D2-272 (no factor below a good's own rate); wave_conflicts §7 item 8 |
| 11 | today's fuel, 0.5 heat a night burning whatever hangs (`data.py:835`, `keeping.py:186`) | fuel is a total by the kg loaded (basis §3), burned evenly over the lot's nights | an almost empty set burned as much as a full one |
| 12 | today's smoking at 1 unit whatever the batch (`data.py:624`) | hanging at 30 kg a unit (basis §3), the make act's `qty` of units | basis §3; D2-288 |

Nothing in D2-271, D2-284, D2-291 or D2-295 is departed from.

## Purpose

A run's glut is food for a few nights unless it is turned into something that keeps. Every way of turning it (smoking, salting,
drying, and the materials' processes, retting and tanning) has the same shape: goods go into a container, wait some nights while a
condition holds, fail if it does not, and come out as a different good. One engine unit for that shape gives each process a data
row instead of its own code, gives the book (U6) one vocabulary of states to read ("cured", "has room", "the fire out"), and gives
the signs (U8) one place to read from. The unit changes goods; stores (U5) only remove risks (D2-272).

## The design

### 1. Three things: a process, a container, a lot

- **A process** is a data row (`PROCESSES`, §2): what goes in, what it is while it waits, what comes out and at what ratio, nights,
  inputs at loading and over the nights (salt, fuel, bark), the work to load, tend and take down, the conditions a night must meet,
  the failure when it does not, what a lot left past its nights does, its fouling, and what the container protects once the lot is
  done.
- **A container** is where lots wait: a fitting in a building (a set of smoke racks, a hearth's or fire ring's rack, a salting tub),
  or a work on a parcel (a tan pit, a retting pit), or ground of a cover (a meadow for dew retting). Its row in FITTINGS (or WORKS)
  names the processes it runs (`process`), its capacity in kg (`holds_kg`), and its spaces.
- **A lot** is one loading: a thing (today's rack pile, `kind: "pile"`) with a `lot` record in place of today's `rack`:

```
lot = {"process": "keeping smoke", "by": person, "household": id, "day": day loaded, "kg": kg loaded (counts against room),
       "nights": nights needed, "had": nights counted, "out": last night failed or None, "done": day done or None}
```

  The lot's goods are its in-process good while it waits (`smoking fish`) and its output good once done (`smoked fish`). Each
  loading is its own lot with its own nights, as now.

### 2. The process rows

All numbers cite basis.md or are marked; nights are whole nights (D2-273); kg are the goods' ITEMS weights (food goods about 1 kg a
unit, basis §2). Columns are the row's fields.

| Row | In → while waiting → out | Ratio (kg out a kg in) | Nights | Inputs | Load (kg a unit) | Tend | Container, where | Conditions | Failure |
|---|---|---|---|---|---|---|---|---|---|
| `keeping smoke` (fish) | fish → smoking fish → smoked fish | 0.5 (wave1 §1.1) | 1 (D2-284) | fuel 0.15 bundles a kg (basis §3) | 30 (basis §3, hanging) | 1 unit a night for the building (basis §1, duration work) | smoke racks; a hut, timber or stone smokehouse (D2-271) | the fire tended today and the night's fuel burnt | the night not counted; the lot keeps at fresh fish's base that night; the building may burn with it |
| `keeping smoke` (meat) | meat → smoking meat → smoked meat | 0.5 | 1 | as fish | 30 | as fish | as fish | as fish | as fish, at fresh meat's base |
| `hard cure` (fish) | salt fish → salt fish → hard-cured fish | 0.4 of salt fish (wave1 §1.1: 0.4 of the fresh weight; salt fish keeps the weight) | 3 (Basis rows needed, 2) | fuel 0.25 bundles a kg (basis §3) | 60 (Basis rows needed, 3) | as above | smoke racks in a timber or stone smokehouse only (D2-271) | as above | the night not counted; the lot keeps at salt fish's base out of brine |
| `hard cure` (meat) | salt meat → salt meat → hard-cured meat | 0.85 (Basis rows needed, 5) | 3 | as fish | 60 | as above | as above | as above | as above |
| `salting` (fish) | fish → salt fish | 1.0 (wave1 §1.1: the weight kept) | 0: at once | salt 0.25 kg a kg (D2-283) | 40, gutting included (D2-283) | none | a salting tub or barrel if one has room, else the store, packed in its salt | none | none (out of brine it keeps worse: U5) |
| `salting` (meat) | meat → salt meat | 1.0 | 0 | salt 0.125 kg a kg (D2-283) | 40 | none | as fish | none | none |
| `hearth rack` (fish, meat) | fish → drying fish → dried fish; meat → drying meat → dried meat | 0.5 (wave1 §1.1) | 1 (wave1 §2.4; Basis rows needed, 6) | the house's own fire | 8 a rack, 1 unit (wave1 §3.1; the 1-unit floor) | none | a hearth inside, a fire ring at the door (`racks: 1`, as now) | inside: the hearth lit tonight; at a fire ring outside: a dry night | the night not counted; the lot keeps at the input's base, in the open's penalties outside |
| `hot smoke` | fish → hot-smoked fish; meat → hot-smoked meat | 0.67 (wave1 §1.1: 1 from 1.5) | none: an act on the day clock | fuel 0.15 bundles a kg (wave1 §3.1: 1 to 2 bundles for 10 fish) | 10 a unit (wave1 §3.1) | none | a hearth, fire ring, or a fire in the open (D2-271) | none | none |
| `liming` (U10's) | hide + wood ash → liming hide → limed hide | 1.0 | 2 (U10's row; basis §1) | ash (U10) | in the hide's 1.5 units (wave1 §3.1) | none | a lime pit (a work by water; U10) | water in the pit | U10 |
| `tanning` (U10's) | scraped hide + bark → tanning hide → leather | 3 leather a 6 kg hide (wave1 §3.1) | 16 light, 32 heavy (U10's rows; basis §1) | 2 bark a hide (wave1 §3.1) | in the 1.5 units | the pits fed at each stage (U10) | tan pits (U10) | the pits fed | the hides rot a share a night (U10) |
| `retting` (U3's) | flax → retting flax → retted flax | 1.0 | water 1; dew 3 (basis §1) | none | 1 unit to lay, 1 to lift a pit's hold (wave1 §3.1) | none | a retting pit or the river (water); a meadow (dew) | water: no spate at the parcel; dew: none | a spate washes a share away (the traps' `wreck` 0.5, wave3 §2.2); left past its nights, fibre lost (U3) |

Notes on the rows:

- **Hot smoke is an act, not a lot.** It is in the table because it is a depth (D2-271, D2-295). Its keeping alone buys little
  (2.4 nights against fresh fish's 1.5: wave_conflicts K2). Its reasons in the engine are two the state already holds: it is
  cooked, so it is eaten without a fire (fresh fish is `cook: True`, `data.py:49`), and it carries 0.69 food a kg against fresh
  fish's 0.46. That is road food and food sold nearby, which is what D2-271 says it is for.
- **Salting is a row with no nights** (Departure 7). It is quantity work at once, and its container is a store: the tub or barrel
  in brine (U5) or, without one, the store packed in its salt.
- **The hard cure loads salt fish or salt meat**, so a hard cure is two acts or two rules (salt, then hang). Gutting is paid in the
  salting (basis §3), so hanging the salted lot is at the faster rate (Departure 9).
- **Liming, tanning and retting are U10's and U3's rows.** Their shape is given here so that they are rows of this unit, not code
  of their own; their numbers (capacity, failures, fouling in numbers, wave_conflicts G3) are U10's and U3's to set.
- **The wind rack** (fish dried in the open; stockfish) is not a row now (Gaps, 4).

### 3. The goods (D2-295)

Each depth is its own good. New rows marked ★; the rest exist and change. Keeping is basis §3's keeping order; food a kg is
conserved through the ratio (fresh fish 0.46 a kg × ratio = the output's food a kg × 1).

| Good | Food a kg | Keeps (real, well kept) | Curve nights (basis §3) | Base a night (D2-289) | Pack (D2-244) |
|---|---|---|---|---|---|
| fish (fresh) | 0.46 (basis §2) | 1 to 2 days | 1.5 | 0.17 | water |
| smoking fish, drying fish (in process) | 0.46 | | | 0.03 in the smoke or at the hearth (wave1 §2.2, est.) | water |
| ★ hot-smoked fish | 0.69 | about 7 days (wave1 §2.2) | 2.4 | 0.11 | water |
| smoked fish | 0.92 | about a season | 9.7 | 0.029 | water |
| ★ hard-cured fish | 1.15 | most of a year | 25.5 | 0.011 | water |
| salt fish | 0.46 | about a year in brine | 33.8 | 0.0085 | water |
| dried fish | 0.92 | a year and more, kept dry | 41.3 | 0.0069 | water |
| meat (fresh) | 0.6 (`data.py:61`) | 2 to 4 days | 2.1 (wave1 §2.2) | 0.13 | core |
| smoking meat, drying meat (in process) | 0.6 | | | 0.03 | core |
| ★ hot-smoked meat | 0.9 | about 7 days (est., as fish) | 2.4 | 0.11 | core |
| smoked meat | 1.2 | about a season | 9.7 | 0.029 | core |
| ★ hard-cured meat (bacon, ham) | 0.67 (Basis rows needed, 5) | about a year (wave1 §2.2) | 33.8 | 0.0085 | core |
| salt meat | 0.57 (`data.py:93`) | about a year in brine | 33.8 | 0.0085 | core |
| dried meat | 1.2 | a year and more, kept dry | 41.3 | 0.0069 | core |

The rates are D2-289's formula, 1 − 0.75^(1/nights), on basis §3's nights; they are not on basis.md yet (Basis rows needed, 1).
Hard-cured meat keeps no longer than salt meat in brine; what it buys is keeping **out of brine** (salt meat out of brine takes
U5's penalty, about 0.0127 a night) and travelling, as bacon and ham did. Hard-cured fish does the same and is also 2.5 times
lighter a meal than salt fish.

### 4. The smokehouse: racks, the building's cap, fire

| Smokehouse | Room (ROOMS, U7) | Floor kept to work and keep the fire | Sets at most | On the racks at most | Depths (D2-271) | Fire a burning night (`data.py:835`) |
|---|---|---|---|---|---|---|
| wattle smoke hut | a hut room, 2 spaces (wave1 §3.5; U7) | 1 | 1 | 250 kg | hot (at its fire), keeping | 0.02 |
| timber, small room | 6 | 2 | 4 | 1,000 kg | hot, keeping, hard cure | 0.008 |
| stone, small room | 6 | 2 | 4 | 1,000 kg | all three | 0.0003 |
| timber or stone, medium room | 12 | 2 | 10 | 2,500 kg | all three | as its structure |

- **A set** is the `smoke racks` fitting: 250 kg on 1 space (D2-291). In timber or stone it is built as a tiered set (wave1 §3.6:
  3 withies, 3 timber; a hut's 2 and 2); its making and cost are U3's and U7's.
- **The cap** is one rule in `buildings.py`: a building with smoke racks keeps 1 space of floor free in a hut room and 2 in any
  other room; the sets fit in the rest. A fitting that would break it is refused at building ("the Smoke Hut's floor takes one set
  of racks: it needs a space free to work and keep the fire").
- **The fire** is the building's, one a night for all its lots: tended once a day (1 unit; today's `tend the smoke`), it burns
  tonight if the night's fuel is there (its store, then the woodpile at its door, as now, `keeping.fuel_cids`). The night's fuel is
  the sum over its lots still in process of (kg loaded × the row's fuel ÷ the row's nights). While it burns, the keyed fire chance
  by structure (`keeping.py:192`, kept).
- **Nothing in process: no fire, no tending, no fuel.** The house is then a store at base (U5: hung goods out of the flies and off
  the floor).
- **A done lot under a continued fire** gains nothing; the fuel is spent and the chance rolled. The house line says so as a fact
  (§7).
- **A salted lot in a wattle hut** is refused at loading (§6).

### 5. The night step: one function

`process.night(w, rec)` replaces `keeping.night` (called at `night.py:77-78`, after the hearths' fires are set) and the rack end in
the spoilage loop (`night.py:203-207`, `_dried` at `:286-308`). For each building (and work) with lots not done, in sorted order:

1. **Read tonight's conditions** for each process its lots run: for a fire row, tended today (`b["smoke"]["tended"] == w.d`) and the
   night's fuel burnt (`forests.burn` from `fuel_cids`, all or none); for the hearth rack, the building's fire lit tonight
   (`b["fire"]`, set in the heat loop above); at a fire ring outside, a dry night (`environment.wet` false); for water rows, no spate
   at the parcel (U1's water state); for fed rows, fed this stage (U10).
2. **Met:** each lot of that process counts a night (`had += 1`). A fire row rolls the building's fire chance once
   (`w.rng("smokehouse fire", w.d, bid)`, as now); a fire burns the building and its lots (`keeping.catch`, `burn_building`, kept).
3. **Not met:** the lot does not count; `out = w.d`; a destroying failure (a spate) destroys its share (`w.apply("destroy", ...,
   why="washed away")`).
4. **Spoilage** runs in the general loop (`night.py:176-202`). `decay_rate` reads the lot's row: in process and not failed tonight,
   the in-process good at the row's in-process base (0.03); failed tonight, the input good's base (fresh fish 0.17), with the
   penalties of where the container is (a roof removes the open's; outside, the open's); done, the output good as a stored good
   (U5: the racks remove flies and floor damp).
5. **Done:** a lot with `had >= nights` becomes its output: its in-process good destroyed and the output created at the ratio
   (`why="cured"` or the row's word), `done = w.d`. It **stays in the container** (Departure 6) and raises the state "done" for its
   household (U6 §3).
6. **Recorded** for the morning lines and the book: `rec["lots"][bid] = {lot id: {"process", "had", "nights", "done", "out"}}`.

A salting row (no nights) never makes a lot: its act turns the goods at once (§6). A done lot under a continued fire is not
touched by step 5 again. Every draw is keyed (`w.rng`) and every write goes through `w.apply`: replay-safe.

### 6. The acts and their results

Loading is the `make` act as now (`verbs._make`), its `rack` record replaced by the row's name (`"process": "keeping smoke"`) and
its batch by the row's load rate: `make smoke fish` with `qty` units hangs up to 30 kg a unit, as much as the racks have room for
and one has (D2-263's "up to"); the 1-unit floor (basis §1) holds for a part batch. Smoking is thus a make technique whose output is
a lot in a container: wave4 §5.1 and wave3 §2 describe the same act (wave_conflicts C27), and wave4's lore lines that read
`smoke_batch` and `smoke_nights` read the row's `load` and `nights` instead (U9).

| Act | Result (exact wording; numbers from the state) |
|---|---|
| `make smoke fish` (hang for a keeping smoke) | "You hung 90 kg of fish on the smoke racks in the Smoke Hut (3 units): a keeping smoke, done after 1 night of fire. The fire is lit for tonight and wants about 14 bundles of firewood (40 there). The racks have room for 160 kg more." |
| the same, no fuel there | "... The fire is lit for tonight, but there is no firewood in it or at its door: it will die tonight unless some is brought." (as now) |
| the same, racks full | "Refused: the smoke racks in the Smoke Hut are full: 160 kg of fish smoking, done tomorrow; 90 kg smoked, waiting to be taken down." |
| `make hard cure` (salt fish, timber or stone) | "You hung 60 kg of salt fish on the smoke racks in the Fish House (1 unit) for a hard cure, done after 3 nights of fire. The fire is lit for tonight and wants about 5 bundles (40 there)." |
| `make hard cure` in a wattle hut | "Refused: a hard cure needs the long cool smoke of a timber or stone smokehouse; the fire in the Smoke Hut hangs too close and hot." |
| `make salt fish` with a tub | "You salted 40 kg of fish with 10 kg of salt (1 unit): 40 kg of salt fish, in brine in the salting tub at Reed House (room there for 80 kg more)." |
| `make salt fish`, no tub | "You salted 40 kg of fish with 10 kg of salt (1 unit): 40 kg of salt fish, packed in its salt in Reed House's store." |
| `make salt fish`, short of salt | "You salted 12 kg of fish with the 3 kg of salt you had (1 unit): 12 kg of salt fish, ... It takes 1 kg of salt to 4 of fish." |
| `make hot smoke` | "You hot-smoked 10 kg of fish over the hearth in Reed House (1 unit, 1.5 bundles of firewood): 6.7 kg of hot-smoked fish, cooked, to eat cold or carry." |
| `make dry fish` (hearth rack) | "You hung 8 kg of fish on the rack in the smoke of the hearth inside Reed House (1 unit), dry after 1 night of its fire." |
| `tend the smoke` | as now (`keeping.tend`), its fuel line in bundles: "You tended the fire in the Smoke Hut and banked it for the night: 160 kg of fish smoking, done tomorrow; firewood there for tonight (14 bundles of 40)." |
| `tend the smoke`, nothing in process | "Refused: nothing is smoking in the Smoke Hut: what hangs there is done, and needs no fire." |
| `move` from a container (taking down) | "You took down 61 kg of smoked fish from the racks in the Smoke Hut into its store (0.5 units)." (U6 owns `move`'s fields; the rate is Basis rows needed, 4) |
| `move` another household's lot | as Q-80: unnamed, refused, naming whose it is ("the smoked fish on the racks is Agnes's, of Reed House"); named, done, and seen as taking |

### 7. What the household knows of its containers (without a roll)

`keeping.house_lines` and `prompt.house_known` (`prompt.py:593-649`) become one generator over every container a household holds,
read from the lots and the building (brief 4c §6.4's rule kept: one's own house is known). Facts, never advice. Lower case, joined
as now.

- in process: "on the smoke racks: 160 kg of fish smoking, done tomorrow" / "salt fish on the racks for a hard cure, 2 nights left"
- the fire: "the fire tended today" / "the fire not tended today: it dies tonight unless someone tends it" / "firewood for tonight's
  fire (14 bundles needed, 40 there)" / "not enough firewood for tonight's fire (14 bundles needed, 6 there)"
- a failure: "the fire died last night: the fish lost a night's smoke and spoiled a little"
- done: "on the smoke racks: 61 kg of smoked fish, done two nights ago, waiting to be taken down; room for 90 kg more"
- a fire on a done lot: "the fish on the racks have had their smoke: more fire does them no good"
- the tub: "in the salting tub: 80 kg of salt fish in brine; room for 40 kg more"
- room: "the racks are full" / "the racks are empty"

What others sense (smoke rising from a lit hut, the smell, the burnt hut, a wet outdoor rack, the pits' and ponds' stink and the
water below) is U8's bundle (wave3 §2.6), reading these states: a lit fire tonight, a fire caught (D4-74's bundle), a rack outside
on a wet night, U10's fouling. Nothing about a lot "being cured" goes to others: it is not visible.

### 8. A worked season, re-derived

On the bot catch basis (D2-293, kept by D2-297) and D2-289's rates. **The household:** the weir household of catch_basis.md §1 (the
Marshs: 3 adults, 2 children, about 4.4 food a night), landing about 915 units in one autumn (the weir's 364 of eel and 551 of
salmon, its traps' share small). **The run's shape is mine** (est.): ten run nights of 40, 60, 90, 150, 330, 120, 50, 40, 25 and
10 units (summing to the basis; the 330 is the village's peak night of D2-293). A unit of fish is read at its ITEMS weight, 1 kg
(U0 settles the eel's 0.86). **Assumed** (est.): 12 spare units a run day for keeping after the weir and the lifts; 140 bundles of
firewood stacked before the run; the household eats fresh first, hangs what it can, salts what is left while salt lasts; nothing
else eaten. Arithmetic in a scratchpad script, not the engine.

| Case | Food at the run's end | At winter's end (8 nights on) | At the next run (22 nights on) | Lost to spoiling | Keeping work | Wood burned |
|---|---|---|---|---|---|---|
| A. wattle hut (1 set), no salt | 309 | 213 | 91 | 178 | 40 units | 121 bundles |
| B. the hut, 60 kg of salt, two salting tubs | 317 | 223 | 104 | 165 | 40 | 112 |
| B'. the hut, 60 kg of salt, no tub | 316 | 222 | 102 | 168 | 40 | 112 |
| C. timber smokehouse (4 sets), 60 kg of salt, salted fish hung for a hard cure | 313 | 227 | 117 | 146 | 39 | 140 |
| C'. timber smokehouse (4 sets), no salt | 313 | 216 | 93 | 176 | 41 | 123 |
| The weir's eels alone (364 units), the hut, no salt | 102 | 50 | runs out 17 nights after the run | 41 | 19 | 41 |

What it says, as far as an invented run shape lets it:

- **The hut binds on one night only**, the 330-unit peak (80 kg left unhung); the timber house's four sets add about 2 food at the
  next run. D2-284's racks are ample for a household; they bind for a village sharing one hut.
- **The wood binds.** About 120 bundles (1,200 kg) a run, about 40 units of gathering at 3 a unit (wave1 §3.1): as much work as all
  the hanging, salting and tending together. A household that has not stacked wood by the run smokes less (wave3's finding holds on
  the corrected fuel).
- **The hands do not bind** at 12 spare units (about 4 units a day of keeping work), except on the peak night (11 units of hanging
  and a tend; wave_conflicts K1).
- **The hard cure and salt matter over the long gap,** not the winter: about 13 food more at the next run with 60 kg of salt and a
  tub, about 24 more with a hard cure (C against C'). With salt only 60 kg, the gain is bounded by the salt, which is the inland
  salt trade's lever.
- **One missed tend on a full set** costs about 36 kg of fish (about 17 food: the lot at fresh fish's base against the smoke's, one
  night) and a night more on the racks, its fire and its fuel.
- **The weir household banks the gap; its eels alone feed the winter but not the gap**, as catch_basis §4 found. This is a reading of
  arithmetic, not of behaviour (D2-298); the live runs carry the signal.

## Code changes

| File, line | Change | Owner |
|---|---|---|
| new `engine/process.py` (from `keeping.py:1-245`) | the lot record; `room(w, bid, process)` by `holds_kg` less lots' `kg`; `night(w, rec)` (§5); `house_lines` generalised (§7); `load(here, ...)` called by `_make`; `fuel_tonight`; `catch` and `burn_building` kept; `done_into_store` removed | 37.2 |
| `keeping.py:247-252` (`near_spring`) | stays (salt, not processing) | 37.2 |
| `data.py` new `PROCESSES` (after TECHNIQUES) | the rows of §2, each with its `pack` | 37.2 |
| `data.py:49-58`, `:92-95`, ITEMS | the goods of §3: four new rows (★), spoil rates from D2-289 (U0's table), weights in kg (U0) | 37.2 (U0) |
| `data.py:123` DECAY `drying meat.smoke` | removed; the in-process base is the row's `in_rate` | 37.2 |
| `data.py:238`, `:248`, `:275-277` FITTINGS | `racks: 1` on hearth and fire ring becomes `process: ["hearth rack"], holds_kg: 8`; `smoke racks` gains `process: ["keeping smoke", "hard cure"], holds_kg: 250, spaces: 1` (was 3), its `does` text; costs are U7's | 37.2 (data), 37.4 named (fittings) |
| `data.py:618-650` TECHNIQUES | `smoke fish`, `smoke meat`: `process` in place of `rack`, inputs 30 a unit; new `hard cure fish`, `hard cure meat`, `hot smoke fish`, `hot smoke meat`; `salt fish`, `salt meat` at 40 a unit and D2-283's salt; `dry fish`, `dry meat` 1 night; `manual` texts rewritten from the rows (D2-263) | 37.2 |
| `data.py:835` PHYSICS `smokehouse.fuel` | removed (fuel by the row); `fire` kept | 37.2 |
| `night.py:77-78` | `PROC.night(w, rec)` | 37.2 |
| `night.py:203-207`, `:286-308` | the rack end and `_dried` folded into `process.night` step 5 | 37.2 |
| `night.py:311-337` `decay_rate` | a lot's goods by its row (§5 step 4); the `rk.get("smoke")` branch replaced | 37.2 |
| `verbs.py:776`, `:791-831` `_make` | the rack branch calls `process.load`; result wording of §6; refusals by the row (structure, room, input) | 37.2 code in 37.4's verb, named on the merge |
| `verbs.py:669-672` `smoke_tend` | `process.tend` | 37.2 |
| `here.py:430-445` (`rack_room`, `smoke_fuel_nights`), `:466` (`hung_by_household`) | read the lot record | 37.2 |
| `buildings.py` (new check beside `fitting_spaces`, `:62`) | the smokehouse's work floor (§4) | 37.4 (buildings) |
| `prompt.py:572-650` (`house_food`, `house_known`) | lots by container; the lines of §7 | 37.4 (prompt), lines from `process.house_lines` (37.2) |
| `wild.py:2780-2786` `_racks_in`, `kinds.py` LEFT_OUT | read lots (the in-process goods by row) | 37.2 |
| `clocks.py:20-23` RATES | `PROCESSES.*.nights` on the year clock (derived from real days at 1/11.4, floored, D2-273); `PROCESSES.*.in_rate` on the day clock; `TECHNIQUES.*.rack.nights` removed | 37.2 (U0) |

## Tests

Interface tests (bots or unit tests; D2-298: they test the interfaces, not behaviour):

1. A lot loaded on a set counts a night only when tended and fuelled; untended, `out` is set and the lot spoils at fresh fish's base
   that night; done after its nights, it becomes smoked fish at 0.5 and stays on the racks.
2. Room: 250 kg a set; a done lot counts by its kg loaded until taken down; loading over room loads what fits and the result says
   the rest.
3. Fuel: a 250 kg keeping smoke burns 37.5 bundles in its night; a 100 kg hard cure burns about 8 a night for 3 nights; short fuel
   kills the night.
4. The cap: a hut room takes one set and refuses a second; a small timber room takes four.
5. A hard cure is refused in wattle with §6's words, and in timber turns 60 kg of salt fish into 24 kg of hard-cured fish after 3
   nights.
6. Salting with and without a tub: the salt fish lands in the tub when it has room, else in the store; 1 kg of salt to 4 of fish.
7. Hot smoke: 10 kg of fish to 6.7 kg of hot-smoked fish, eaten at night with no fire lit.
8. A fire catching (forced by a keyed seed) destroys the lots inside and the house line and the D4-74 signs follow.
9. Replay: a run replayed from its journal gives the same lots, nights and goods (every draw keyed).
10. The book's states (U6): `done`, `has room`, `full`, `fire out` read true and false on the right nights.

**What live runs should read** (against a null arm without the smokehouse and salt): how much of a glut is kept and in what depth;
where done lots go (taken down by rule, by hand, or left up); whether households stack wood before the run; missed tends; whether
salt is bought or boiled for the long gap; the qualitative end state (who holds the smokehouse, who sells hard cure).

## Basis rows needed

| # | Row | Value | Mark |
|---|---|---|---|
| 1 | Base rate a night of each kept good (§3's column) | 1 − 0.75^(1/nights) on basis §3's nights: fresh fish 0.17, fresh meat 0.13, hot smoke 0.11, keeping smoke 0.029, hard cure 0.011, salt 0.0085, dried 0.0069 | follows D2-289 (arithmetic) |
| 2 | The hard cure's nights | 3 (within D2-284's 2 to 3: "three weeks to a month and more" at 1/11.4, rounded up) | default |
| 3 | Hanging a salted or gutted fish | 60 kg a unit (gutting paid in salting) | default, est. |
| 4 | Taking down from a container | 120 kg a unit | default, est. |
| 5 | Hard-cured meat | 0.85 of the salt meat's weight; 0.67 food a kg (food conserved) | default, est. (wave1 §1.1 had 0.6 at about the same weight) |
| 6 | The hearth rack's nights | 1 (wave1 §2.4) | default |
| 7 | The in-process base in the smoke or at the hearth | 0.03 a night (wave1 §2.2, "a few per cent", est.) | default, calibrate |
| 8 | The smokehouse's work floor | 1 space in a hut room, 2 in any other | default |

## Gaps

1. **The salting tub before the cooper (G10): designed.** A basic container now (U5 §2: 120 kg in brine), made without a cooper
   (U3: a hollowed or boarded tub); barrels with the cooper later, for trade (they travel; a tub stays where it is).
2. **Depth as a good or a state (G5): decided** (D2-295); built as §3.
3. **Smoking as an act or a container (C27): resolved** in §6: the make act is the load, the lot is the container's.
4. **The wind rack: deferred.** It waits on fat and lean fish told apart (eels are fat and were smoked or salted, not air-dried; est.),
   on the coast and stockfish, and on wet-weather failure for an outdoor rack (`open_wet`). Until then fish dries only at a hearth.
5. **Liming, tanning and retting in numbers:** the rows' shape is here; capacity, failure rates and fouling are U10's (G3) and U3's.
6. **Fire risk against a real record:** the engine's 0.02, 0.008 and 0.0003 a burning night are kept unchecked (no rate found,
   smokehouse_capacity §6). Calibrate in live runs.
7. **A curve by a lot's age** (D2-289: "a curve by a lot's age comes later with dated lots in stores"): a lot carries its day, so
   the age is known while it is a lot; carrying it into the store is U5's later step.

## Open questions for Zach

1. **Where a done lot goes** (Q-U4-2; wave3 W80-Q11; wave_conflicts C28). (a) It stays in its container, counts against the room,
   and comes down by an act or a rule (taking down at 120 kg a unit); (b) as today, straight into the building's store if there is
   room. Recommend (a): where cured goods go becomes a visible choice the book can make, and untaken racks cost the next catch.
   Default taken: (a). Blocks: the night step's step 5.
2. **Salting meat at once or over nights** (Q-U4-3; W80-Q8). (a) Both fish and meat at once, the tub the store; (b) meat a 3-night
   lot in the tub. Recommend (a). Default taken: (a). Blocks: the salting rows.
3. **Hard-cured meat's numbers** (Basis rows needed, 5): 0.85 of the salt meat's weight, 0.67 food a kg, keeping about a year out of
   brine. Recommend as stated; it gives herders and hunters the travelling keeper fishers get. Blocks: the hard cure (meat) row.
4. **"Holds more a space" in a timber or stone smokehouse** (Q-U4-4; Departure 4). (a) Read at the building: every set 250 kg on 1
   space, the timber or stone room losing less of its floor to the fire and having a loft; (b) a tiered set holds more on its space
   (a number nobody has sourced, perhaps 375 kg). Recommend (a). Blocks: the smokehouse table.
5. **Tanning's nights:** U10's rows (lime 2, light hides 16, heavy 32), aligned 22 Nov by 37.2.

## Sources

wave3_keeping.md §1 to §3, §6, §7 (and §5 read, not carried); wave1_physical_basis.md §1.1, §2.1 to §2.4, §3.1, §3.6;
hunt_fish_materials.md §7.3, §7.5, §7.6, open question 10; wave_conflicts.md C1, C21, C23, C25, C27, C28, G5, G10, K1, K2, K12, E1, E8;
catch_basis.md §1, §4 (the bot basis); smokehouse_capacity.md (through wave1); basis.md; README.md; DECISIONS D2-271 to D2-298 as cited;
the code as listed under Extends. The worked season: a scratchpad script on §8's parameters (not kept in the repository).

## History

- **22 Nov 2026:** written by a 37.2 design subagent for W-85 from the sources above.

*Current as of 22 Nov 2026: D2-263 to D2-298.*
