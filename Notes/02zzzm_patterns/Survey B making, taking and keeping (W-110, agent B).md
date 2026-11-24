---
id: docs/review/37_growth/02zzzm_patterns/B_making.md
kind: note
updated: "2026-11-24"
---
# Survey B: making, taking and keeping (W-110, agent B)

*note · `docs/review/37_growth/02zzzm_patterns/B_making.md`*

> **The area:** about 10,560 lines in 21 modules (verbs.py's handlers, gear, placed, process, stores, buildings, things, farm, herds, night, strips, fuse, yields and the small modules they call: wear, keeping, labour, needs, modifiers, tags, clocks, outcomes), against 7,620 in the same files at f728a3


Session 37.2, 24 Nov 2026. Brief: [brief.md](brief.md), area B, with the coordinator's three additions (a taxonomy, the history, what
in the process let ad hoc systems in) and Zach's framing of the verdict ([[D2-354 The architecture is a healthy balance, not a strict one|D2-354]]: a healthy balance, not a strict architecture). Read
from the code on `main` at 6b609f48. Line numbers are in `cybertron2/engine/` unless a path says otherwise. The wave's baseline is
f728a3b7. No model calls, no runs; one script, [B_branches.py](B_branches.py), counts the branches on named things (§2).

**Grades** (the brief's): **G** general over rows; **GF** general with fitted constants; **N** a special case by name; **T**
hand-written text; **W** a word-list parse; **S** a silent skip. A mechanism can carry two (a general rule with a named branch in it
is "G, N"); the summary counts both ways.

## Summary

**The area:** about 10,560 lines in 21 modules (verbs.py's handlers, gear, placed, process, stores, buildings, things, farm, herds,
night, strips, fuse, yields and the small modules they call: wear, keeping, labour, needs, modifiers, tags, clocks, outcomes), against
7,620 in the same files at f728a3b7. The set gear's night lives in `engine/wild.py` (area A's file) and is cited where it decides a
mechanism here.

**Mechanisms by fit** (§1, 98 mechanisms in the area; four more listed there belong to areas C and D):

| Fit | Count | Came in the wave |
|---|---|---|
| G: general over rows, nothing by name | 26 | 17 |
| GF: general, its constants fitted | 9 | 3 |
| a general rule with a named branch inside it (G, N or GF, N) | 23 | 3 |
| a general rule whose words are hand-written or parsed from a list (G, T or G, W) | 4 | 3 |
| N: a special case by name throughout (the act dispatch among them, with the one silent skip, S) | 23 | 9 |
| T: hand-written text is the mechanism | 6 | 3 |
| W: a word-list parse | 7 | 3 |

By worst grade alone: G 26, GF 9, N 43, T 10, W 9, S 1. The wave's own modules are mostly in the first row; its named branches
are at the joins (verbs.py) and in the set gear.

**Branches on named things** (§2): **345** string literals naming a row in function code (comparisons, lists of names, dict keys,
registry reads by a literal), against 256 in the same files at f728a3b7: 32.7 a thousand lines now, 33.6 then. Of the 345, about
**80 are legitimate** (39 dispatches on an act's yield kind, 20 on the core thing kind `set`, 20 reads of a table's own keys); about
**265 should be properties** of covers (53), gear and set methods (45), fittings (40), the camp structure (29), structure materials (25),
goods (21), seasons (15), monuments (12), wild kinds and resources (12), processes (7), tools (4), cattle roles (3). Beside them, **32**
word-list parses in verbs.py (21 at f728a3b7) and about **30 property tables keyed by name** at module level (stores' `DRY`, `CURED`,
`SALTED`; gear's `SET_GEAR`, `SET_MOST`, `TOOL_LIVES`; placed's `NOUN`, `WORDS`; things' `SET_NOUN`, `FLESH`; data's `GOES_OFF`,
`IN_PROCESS_OF`; night's `GOING_OFF`; farm's `ROLES`).

**What does not fit** (§3): six mechanics none of the hypothesis's patterns captures, each with several copies today:
1. **Works**: a change built up in units over days by several people, finishing with an effect: 9 copies (a building, a room, an
   upgrade, a tier, a fitting, a weir part, a weir's mending, a grave, field works), each with its own `units_left` record.
2. **Bodies with parts**: a building's rooms, storeys and fittings; a weir's sections; a field's holdings and strips; a set's laid
   pieces. Capacity, cost and wear derive from the parts, written four ways.
3. **Keeping by risk and remedy**: a good meets named risks (floor damp, flies, brine, the heap, frost, wet, fire, vermin), a place
   removes some; the rate is the base times what is not removed. Seven loss rules (§3.3) do this with the risks coded and the goods
   that meet them in name tuples.
4. **Drawing a need from ordered sources**: eating, fodder, a hearth's fuel, a smokehouse's fuel, an act's inputs, a gift's top-up:
   six loops with the same shape (a need, an order of containers, a worth a unit, what is held back, what a shortfall does).
5. **Capacity and room**: a store's portions, a building's floor, a parcel's ground, the racks' kg, a camp's 30 kg, a set's hold, the
   weir's hold, what one carries: eight capacity rules, each its own.
6. **Populations with classes**: the herd is cattle only, roles in code (`farm.py:24`, `herds.py:25`); a stock of S, K and r is too
   thin for it.

And two the hypothesis names but cuts too finely or too coarsely: **lives and wear** (3e) is right but has **nine** implementations;
**set gear** (3d) is in practice four named methods plus a weir on a separate path, and is better read as a placed body with parts
sampling a stock, wearing by lives, than as a mechanism of its own.

**The verdict for area B: too few, and in two places wrongly cut.** Of 98 mechanisms, 35 are general over rows and 27 more are
general rules with a named branch or hand-written words that would come out as properties; 36 are by name, text or word lists. The
hypothesis's set fits the newest code well: processes
(`process.py`), stores (`stores.py`'s spaces and containers) and gear's two lives (`gear.py`) are mostly general over rows, and they
are what the wave did best. It does not reach the acts' effects (a 33-branch dispatch with one handler per kind, `verbs.py:687-910`),
the works, the wear, the herds, or the names (twelve resolvers, §3.7). Nothing checks a registry at load: rows merge by `setdefault`
(`gear.py:133-141`, `stores.py:84-110`, `process.py:131-149`), and an unknown yield kind falls through the dispatch and reports a
yield of nothing (`verbs.py:860-862`). The balance [[D2-354 The architecture is a healthy balance, not a strict one|D2-354]] asks for, for this area, is §4: six general primitives own the behaviour
(acts' effects through a kind registry, works, parts and capacity, keeping, draws, lives), each with named extension points; the
systems that keep their own specifics (crop growth, the weir's share of a run, herd wandering, vermin) keep them inside their package
and reach the core through those points.

**The history** (§5): the area was general at its start (23 Oct: one handler from the data, `ce24b6f3`), went ad hoc in the wild and
river briefs (9 to 17 Nov: 13 wild yield kinds, shelter in levels beside breaks, the weir in sections), and was partly generalised
again by the wave (23 Nov: processes, stores, gear's lives). The trend is better inside the new units and worse at the seams: the new
modules carry 25 named branches a thousand lines against the old files' 34, but verbs.py gained 18 branches and 11 word lists, and
three new systems were built beside the old ones they could have replaced (`TOOL_LIVES` beside `LIVES`, stores' `SPACES` beside
data's `STORES`, `IN_PROCESS_OF` beside the process rows).

**What let ad hoc in** (§6): briefs named features, not mechanisms; the build plan keeps edits "to the seams" and tests "interfaces
and basic functioning only" ([[D2-298 Bot runs test interfaces and basic functioning only|D2-298]]); every stage's "done when" is one world; no registry is checked at load; live-run fixes patch
the words that failed ([[W-102 Fix the act shapes' interface faults found in live run 1's rebuilt arm|W-102]], [[W-104 Build the after-runs list from live run 1|W-104]]).

**The restructuring** (§7): about 3,500 to 4,000 lines touched in area B (plus about 400 in `engine/wild.py`'s set and weir code), 17
to 25 builder-days, most of it inside feature_packages.md's phase 4 (its "technique hub about 600" and "night into phases about 500"
are this area). A cheap first tier (a load check, a yield-kind registry, properties off names, one resolver) is 6 to 8 builder-days,
no schema change, golden journals byte-identical.

---

## 1. The mechanisms

Every behaviour in the area that reads or changes state. *Wave*: **w** came in f728a3b7..HEAD (`git log -S`, `git blame`); **p**
before; **w+** older, changed in the wave. *Pattern*: the hypothesis's (1 rows, 2 properties, 3a stocks, 3b pulses, 3c processes,
3d set gear, 3e lives, 3f acts, 3g signs, 3h book, 4 resolver) or a missing one from §3 (**works**, **parts**, **keeping**, **draw**,
**capacity**, **classes**).

### 1.1 Acts (verbs.py and the handlers it calls)

| # | Mechanism | Where | Pattern | Fit | Wave | Note |
|---|---|---|---|---|---|---|
| 1 | An act's units | `verbs.py:128-212` | 3f | G, N | w+ | general from `units`, `hours` and the clocks (`clocks.py:105-136`), then eight special branches by verb or kind: a day's guard (`:135`), a gap set (`:140-150`), gear set from the hands (`:151-154`), a build (`:155`), a move from a store or racks (`:157-172`), a grave and a burning (`:190-200`), a loading (`:201-205`), mending gear (`:186-187`) |
| 2 | The verb registry and its manual lines | `verbs.py:20-103` | 3f, 3g | T | w+ | args and docs hand-written, naming goods and kinds: "wicker traps \| snares \| a gill net \| a set line" (`:57`), "grain, rye, beans", "cow, ox, bull, calf" (`:23`) |
| 3 | Verb aliases and lifts | `verbs.py:2293-2297`, `:398-399` | 4 | W | p | `LIFT` is 5 verbs x 16 phrases of named gear (`:2295`), brief 4c |
| 4 | A good from words | `verbs.py:424-431` | 4 | W | p | a hard-coded alias dict (loaves, greens, ore, hides...) beside the rows |
| 5 | A party from words | `verbs.py:434-449` | 4 | W | p | "my household", "our household", "home"... |
| 6 | Inputs from hands, then stores (one-of inputs, held back) | `verbs.py:494-516` | draw | G | w+ | all or nothing; the book's holds (`:507`) came with u6 |
| 7 | Who drew what; why a good is short | `verbs.py:519-588` | 3f | G | p | the recipe that makes a short good found from the rows (`:584`) |
| 8 | Where an act is done | `verbs.py:595-646` | 3f | G, N | p | from `at`; the things and cairn branches by technique (`:597-618`) |
| 9 | **The act's effect: dispatch on yield kind** | `verbs.py:687-910` | 3f | N, S | w+ | 33 branches; four kinds go through `yields.dist` (stock, chance, fixed, pool: `yields.py:17-38`), the rest each a handler; `tech == "fell"` (`:779`), `dk == "willow"` (`:776`); an unknown kind matches nothing and the act reports 0 (`:860-862`) |
| 10 | Practice counted as done | `verbs.py:873-877` | 3f | N | w+ | a list of 19 kinds that count as success whatever they gave |
| 11 | The act's result line | `verbs.py:878-909` | 3f | T, N | w+ | slaughter's meat line by kind (`:888-891`), the shallows' own words (`:897-903`) |
| 12 | Mending gear | `verbs.py:914-963` | 3e | G | w | over `gear.LIVES` and the making's craft |
| 13 | Loading a processing container | `verbs.py:966-1029` | 3c | G, T | w | over `PROCESSES`; refusals hand-written ("done in still water or on the grass", `:998`) |
| 14 | Making (recipes, batches, try, a fitting's wear) | `verbs.py:1036-1137` | 3f, 3e | G, N | w+ | `process == "salting"` by name (`:1048`), `"water wheel" in fits` (`:1078`), the brine pan's rim by `spring` (`:1110-1111`) |
| 15 | A new building, room, upgrade, tier | `verbs.py:1186-1420` | parts, works | G, N | p | over `ROOMS`, `TIERS`, `SPACE`; the camp (`:1211`, `:1230`, `:1337`, `:1377`), stone as walling (`:1146-1163`, `:1414-1415`), storeys by words (`:1196-1198`) |
| 16 | A fitting | `verbs.py:1579-1673` | parts, works | G, N | w+ | `apart`, `spring`, `site`, `heavy`, `per` read from rows; `beds` and `hearth` named against `apart` (`:1596-1599`), the camp's beds and fire ring (`:1611`), `what == "smoke racks"` (`:1616`) |
| 17 | Works in progress: building, room, fitting | `verbs.py:1544-1576`, `:1646-1704` | works | N | p | three records (`unfinished`, `works`, `fitting_work`) of one shape |
| 18 | A monument, the weir's first section | `verbs.py:1273-1320` | works, parts | G, N | p | the river site and the crew by the weir (`:1277-1289`, `:1297-1313`) |
| 19 | A weir's further parts | `verbs.py:1433-1500` | works, parts | N, W | p | `WEIR_PARTS` (19 phrases, `:1433`); its own `weir_work` record |
| 20 | A weir's mending | `verbs.py:1507-1541` | works, 3e | N | p | its own `mending` record and level scale |
| 21 | Writing on buildings | `verbs.py:1707-1849` | (area C/D) | G | p | over `LINES`; stone named for carving (`:1743`, `:1799-1812`) |
| 22 | Moving between hands and stores; taking a lot down | `verbs.py:1852-2017` | capacity | W, N | w | `HOME_WORDS`, `RACK_WORDS` (`:1892-1895`, [[W-102 Fix the act shapes' interface faults found in live run 1's rebuilt arm|W-102]]), the hands words four times (`:1876`, `:1923`, `:1982`, `:1997`), the racks by three fitting names four times (`:163`, `:1870`, `:1907`, `:1959`) though fittings carry `process` |
| 23 | A container named by an act; tending its fire | `verbs.py:2036-2074` | 3c, 4 | W, N | w | `CONTAINER_WORDS` (`:2036`), suffixes " fire", " racks" (`:2055`) |
| 24 | Taking (stores, piles, set things, theft) | `verbs.py:2092-2186` | 3f | G, N | w+ | the set kind's branches (`:2096-2173`), traps in water by name (`:2173`) |
| 25 | Giving and putting down | `verbs.py:2188-2283` | 3f | G | p | |
| 26 | A lift or check as a tend | `verbs.py:2300-2330` | 4 | W | p | gear named by substring ("snare", "net", "set line", "trap", `:2306`) |
| 27 | Setting a gap or a door | `verbs.py:2496-2561` | 3d | N | p | `WATER_WORKS["weir" if WL.is_weir(b) else "mill"]` (`:148`) |
| 28 | Repair of a building | `verbs.py:2742-2776` | 3e | GF, N | p | its material by structure (`buildings.py:334-340`) |
| 29 | Clearing for a field, for building | `verbs.py:2779-2830` | works | GF | p | over `CLEARING`; whole-parcel (build_gaps G38) |
| 30 | Burying, a cairn, burning a carcass | `verbs.py:292-380` | works | GF, W | p | a grave's own `grave` record (`:324`); a carcass named by a set of phrases (`:373-374`) |

### 1.2 Gear and placed gear (gear.py, placed.py; the set's night in engine/wild.py)

| # | Mechanism | Where | Pattern | Fit | Wave | Note |
|---|---|---|---|---|---|---|
| 31 | The wave's goods, recipes and lives as rows, merged at load | `gear.py:33-155` | 1 | G | w | merged by `setdefault` (`:136`); no required fields checked |
| 32 | Pieces moved by the primitives | `gear.py:243-275` | 3e | G | w | one record for made and placed gear (basis §6) |
| 33 | A use's wear | `gear.py:277-285` | 3e | G | w | |
| 34 | Lay and unlay | `gear.py:288-346` | 3d | G | w | |
| 35 | A night set: worn, torn | `gear.py:380-409` | 3e | G | w | over `LIVES` count kinds |
| 36 | Torn away by a spate or the ice | `gear.py:412-446` | 3b, 3e | G | w | the chance is the caller's |
| 37 | Rot, wet and dry | `gear.py:449-534` | 3e, keeping | GF, N | w | wet covers named (`:458-459`: water, fen, saltmarsh) |
| 38 | The older tools' lives | `gear.py:120-121`, `:178-189` | 3e | N | w | `TOOL_LIVES`, a second life table beside `LIVES` |
| 39 | A set method's gear and most laid | `gear.py:124-125` | 3d | N | w | `SET_GEAR`, `SET_MOST` keyed by name; belong on the method rows |
| 40 | Mending's cost, units, uses | `gear.py:537-581` | 3e | G | w | |
| 41 | Gear's words (life, state, plural) | `gear.py:584-635` | 3g | T, N | w | `plural` a dict of 11 names (`:628-631`); "rotting" for nets and lines by name (`:612`) |
| 42 | A set method from words | `placed.py:19-41` | 4 | W | w | `WORDS` (`:23-28`), a resolver beside `KN.resolve` |
| 43 | Setting gear from the hands | `placed.py:123-172` | 3d | G, N | w | `WATER` by name (`:20`), water and fen named (`:142-143`) |
| 44 | The water tonight at a setting | `placed.py:175-193` | 3g | N, T | w | eels by name (`:181`) |
| 45 | Tending one's set | `placed.py:208-295` | 3d | G, T | w | fish or meat by `WATER` (`:224`), the otter's line hand-written (`:261`) |
| 46 | The tend act; the weir's traps | `placed.py:298-375` | 3d | N | w | the weir on its own path (`:315-316`, `:355-375`); only snares move, by name (`:319`, `:350`) |
| 47 | One who fishes | `placed.py:80-84` | 2 | N | w | seven techniques named; a tag would do |
| 48 | The set's night: catch, hold, ice, run, the water's fish | `engine/wild.py:975-1130` | 3d, 3a | N | w+ | by method name (`:1016`, `:1023`, `:1036`, `:1069`, `:1098`, `:1114`); `SET_HOLD_KG` keyed by name (`:920`) |
| 49 | Spate and flood on set gear | `engine/wild.py:3322-3400` | 3b | N | w+ | methods named (`:3322`, `:3326`, `:3355`) |

### 1.3 Processing, keeping and stores (process.py, stores.py, night.py's loss)

| # | Mechanism | Where | Pattern | Fit | Wave | Note |
|---|---|---|---|---|---|---|
| 50 | The process rows, merged at load | `process.py:39-149` | 1, 3c | G | w | four lot processes and two at once |
| 51 | A lot loaded; ground laid; the fire lit | `process.py:307-367` | 3c | G, T | w | the head and tail words by fire, inside, outside (`:325-340`) |
| 52 | Room on the racks | `process.py:207-224` | capacity | G | w | |
| 53 | A container's condition tonight | `process.py:454-503` | 3c | GF | w | three conditions coded (a tended fire, `cond: hearth`, `cond: ground`), not a declared condition |
| 54 | Retting's wash in a spate | `process.py:506-522` | 3b, 3c | GF | w | |
| 55 | A lot finished | `process.py:534-552` | 3c | G | w | |
| 56 | A lot's loss | `process.py:555-576` | keeping | G | w | |
| 57 | A smokehouse fire catching, spreading | `process.py:579-621` | 3b | GF | w+ | a pulse by structure (`PHYSICS.smokehouse`), not registered as one |
| 58 | A smokehouse's work floor and sets | `process.py:624-637` | capacity | N | w | a "hut" room (`:629`) that no `ROOMS` row has (build_gaps G24); `F["smoke racks"]` (`:636`) |
| 59 | What a household knows of its racks; the book's states | `process.py:640-700` | 3g, 3h | T, N | w | process names in the words (`:657-658`) |
| 60 | Salting at once | `process.py:703-741` | 3c | N | w | `PROCESSES["salting"]` by name, the tub and barrel by name (`:731-736`); called by name from `verbs.py:1048` |
| 61 | Taking a lot down | `process.py:406-451` | 3c | G | w | |
| 62 | Spaces and containers as rows | `stores.py:36-67` | 1, capacity | G | w | `suits`, `removes`, `adds`, `vermin` |
| 63 | The goods each risk meets | `stores.py:21-31` | keeping, 2 | N | w | name tuples (`DRY`, `CURED`, `SALTED`, `FLIES`, `WARM`, `ROOTS`, `NUTS`, `FRUIT`); only `VERMIN` is written onto the rows (`:88-90`) |
| 64 | Penalties by portion; the hazard | `stores.py:152-264` | keeping | GF | w | the risks coded in `factor` (`:152-172`); roots' heap by space names (`:170`); the cellar named (`:259`) |
| 65 | The sort (portions) | `stores.py:188-241` | capacity | G | w | |
| 66 | Vermin exposure, sudden illness | `stores.py:312-367` | keeping | G | w | |
| 67 | In hand: fresh foods without a creel | `stores.py:300-309` | keeping | N | w | creel and basket named (`:307`); "fresh" as `KEEP_DAYS <= 4` |
| 68 | The store's line | `stores.py:370-403` | 3g | T, N | w | tub, barrel, chest named (`:391-392`) |
| 69 | A good's loss in its container | `night.py:298-321` | keeping | G | w+ | dispatch by container kind to stores, processes, the open |
| 70 | A night's base loss | `night.py:327-339` | keeping | G | p | over `DECAY` tables |
| 71 | The night's spoiling loop | `night.py:196-224` | keeping | G, N | w+ | meat in a carcass (`:193-199`), traps in water skipped by name (`:201`), `GOING_OFF` by name (`:16`, `:216`) |
| 72 | Fresh fish and meat's base from the keeping curve | `data.py:138-176` | keeping | G, N | w | `KEEP_DAYS`, `GOES_OFF`, `IN_PROCESS_OF` keyed by name, written onto rows at load |

### 1.4 Buildings, things, fire and the night (buildings.py, things.py, night.py)

| # | Mechanism | Where | Pattern | Fit | Wave | Note |
|---|---|---|---|---|---|---|
| 73 | Floor, footprint, fittings' spaces, ground | `buildings.py:23-109` | parts, capacity | G, N | w+ | the camp (`:25`, `:96`); the woodshed by name (`:98-100`) though its row has `ground` |
| 74 | Where goods lie; overflow to the next store and the door | `buildings.py:132-188`, `:398-432` | capacity | G | w+ | |
| 75 | Costs of rooms, upgrades, tiers | `buildings.py:241-297` | works | G, N | p | the trade by structure (`:269`) |
| 76 | Two condition scales (condition 0-2, level 0-5) | `buildings.py:301-331` | 3e | N | p | `COND_OF_LEVEL`, `LEVEL_OF_COND`; camps a third (`:302`) |
| 77 | A vault safe from fire | `buildings.py:506-512` | keeping | N | p | by name, though its row has `fireproof` (`data.py:348`) |
| 78 | Stalls' share of a herd | `buildings.py:515-525` | capacity | N | p | stalls by name; `FITTINGS.stalls.fodder` and `dung` read by name in `farm.py:1488`, `:1534` |
| 79 | Seeded rooms | `buildings.py:343-389` | parts | G | p | |
| 80 | Things' own conspicuousness | `things.py:123-149` | (area D) | G | p | by kind, over `THINGS` |
| 81 | Describing a thing | `things.py:158-194` | 3g | T, N | w+ | process names in the words (`:171-173`) |
| 82 | Carcasses: size, fresh, flesh, bones, eaten, left | `things.py:197-279` | keeping | GF, N | p | `FLESH` by name (`:208`), meat named (`:275`) |
| 83 | Set things: owner, noun, state | `things.py:285-350` | 3d | G, N | w+ | `SET_NOUN`, `SET_WHAT` (`:310-313`), a third noun table |
| 84 | Graves: units, words | `things.py:751-782` | works | GF | p | |
| 85 | Fires in houses and camps (heat, fuel, warmth) | `night.py:47-80`, `:461-483` | draw | GF, N | p | the camp's fire (`:55-67`); `FIRE` from the rows' `fire` (`:13`) |
| 86 | Eating: the need, the order, the book's ration | `night.py:102-178`, `:486-613`; `needs.py:21-49` | draw | G | w+ | `eaten_worth`, `eat_order` over the rows |
| 87 | Starvation | `night.py:179-194` | (area C) | G | p | |
| 88 | Sleeping out: tent and bedroll | `night.py:342-358` | 3e | N | p | by name, though their rows carry `camp` (`data.py:132-133`) |
| 89 | Camps falling in; old breaks | `night.py:226-252` | 3b, 3e | GF, N | p | wattle's painted line by name (`:236`) |
| 90 | Shelter in levels: wear and damage | `night.py:694-760` | 3b, 3e | GF, N | p | weather causes coded; the structures' rules coded (`:747`: timber one less, stone at most two); the weir skipped by name (`:718`) |
| 91 | Regrowth by renewal rule | `night.py:620-660`; `renewal.py` | 3a | G, N | w+ | the shallows' ice and willow's spring by rule name (`:645-652`) |
| 92 | A carcass's night | `night.py:663-691` | keeping | GF | p | |

### 1.5 Farming and herds (farm.py, strips.py, herds.py)

| # | Mechanism | Where | Pattern | Fit | Wave | Note |
|---|---|---|---|---|---|---|
| 93 | Crops: growth, frost, ripening, rot | `farm.py:100-185`, `:1381-1448` | 3a/3c | G, N | p | over `CROPS`; winter by name (`:118`, `:1385`); a coupled layer on a holding |
| 94 | Soil: fallow, manure, a crop's step | `farm.py:190-224` | 3a | GF | p | |
| 95 | Holdings and plot shares | `farm.py:234-440` | parts | G | p | |
| 96 | The farm acts | `farm.py:737-807` | 3f | N | p | one branch per kind; `ready` by kind (`:1207-1270`); the plough by name (`:1110`, `:1135-1136`) |
| 97 | Field works' night | `farm.py:1353-1378` | works, 3e | N | p | "ditch" if wet else "terrace" (`:1361`) |
| 98 | Herds: graze, fodder, starve, breed, milk, dung | `farm.py:1465-1544` | classes, draw | GF, N | p | fodder by the rows' `fodder` (`:1496`); roles named (`:1512`); stalls by name (`:1488`, `:1534`) |
| 99 | Driving a herd | `farm.py:1275-1336` | (area C) | N | p | ten covers listed (`:1285`) |
| 100 | Strips below a plot | `strips.py:26-225` | parts, 3a | G | w | the crop's `strip` and `seed_kg` fields |
| 101 | Fences' night | `herds.py:60-90` | 3e, works | GF | p | a fourth level scale (`FENCES`) |
| 102 | Wandering, gadding, value of a parcel | `herds.py:97-192` | (animals) | GF, N | p | covers named (`:113`, `:142`, `:149`) |

The table has 102 rows; four (21, 80, 87, 99) belong to areas C and D and are not counted, leaving 98. The other small modules are general over their rows and are not listed one by one: `wear.py`
(a fitting's wear by use or time over `FITTINGS.wear`), `clocks.py` (the capital factor and conversions), `labour.py` (work's food,
fading), `modifiers.py` (ways of doing over `TECHNIQUES.modifies`), `tags.py`, `outcomes.py`, `keeping.py` (`near_spring` by kind),
`fuse.py` (a registry of urgent calls; the raid its one kind).

---

## 2. Branches on named things

Counted by [B_branches.py](B_branches.py) (`python3 -I docs/review/37_growth/02zzzm_patterns/B_branches.py --list`): an AST walk of each
module's functions for string literals that are the names of rows (items, techniques, fittings, rooms, blueprints, monuments, covers,
resources, crops, processes, gear lives, structures, seasons, cattle roles) in a comparison, a list of names, a dict key, a call's
list argument, a default argument, or a registry read by a literal. Refs such as `("herd", hid)` and fields such as `.get("herd")` are
left out. The same script over f728a3b7's files (with today's registries) gives the baseline. It undercounts names held in
module-level tables (counted by hand in §2.3) and in word lists (§2.4).

### 2.1 By file

| File | Now | At f728a3b7 | Lines now |
|---|---|---|---|
| verbs.py | 101 | 83 | 3,028 |
| farm.py | 62 | 62 | 1,544 |
| night.py | 43 | 38 | 760 |
| things.py | 33 | 25 | 782 |
| buildings.py | 20 | 20 | 525 |
| gear.py | 17 | (new) | 635 |
| herds.py | 17 | 17 | 533 |
| process.py | 17 | (new) | 741 |
| placed.py | 12 | (new) | 388 |
| stores.py | 12 | (new) | 403 |
| needs.py, modifiers.py, strips.py, keeping.py | 4, 3, 3, 1 | 4, 3, -, 4 | |
| **Total** | **345** | **256** | 10,559 (7,621) |

### 2.2 By what is named, and what it should become

| Named (count) | Where most | Legitimate? | It should become |
|---|---|---|---|
| A yield or work kind's value (39): sow, manure, slaughter, herd, bury, repair, fence, milk... | `verbs.py:782-889`, `farm.py:743-805`, `:1219-1265` | **yes** in kind: P3's "a new kind of change" is code. Wrong in form: an `elif` chain and lists of kind names (`verbs.py:874`) | a **yield-kind registry**: kind -> {handler, outcome (for the capacity model), counts as done, words}; the chain becomes one lookup, an unknown kind refused at load |
| The thing kind `set` (20) | `things.py`, `verbs.py:2096-2171` | **yes**: a core body kind (§2.1 of feature_packages) | the kind registry's `set` row, with its draw and noun fields |
| Table keys and record fields (20): `carcass_sizes`, `hidden`, the gap's `shut` | `things.py`, `verbs.py:2545-2558` | **yes** | (none) |
| Covers (53): built, field, water, fen, meadow, pasture... | `farm.py` (25), `herds.py` (10), `placed.py`, `gear.py:459` | no | cover properties: `wet` (gear's rot, setting in water: `gear.py:459`, `placed.py:142`), `grazing` (`herds.py:142`), `buildable` (exists as `ground`), `farmed` (`farm.py:315-447`), `herd_value` (`herds.py:113-149`), `drivable` (`farm.py:1285`) |
| Gear, containers, set methods (45): trap in water, snare, gill net, salting tub, barrel, tent... | `gear.py` (13), `things.py`, `process.py`, `placed.py` | no | set-method fields (`water`, `movable`, `hold_kg`, `gear`, `most`, `noun`, `plural`); container fields (`brine`, the rows already hold `removes: brine`); items' `camp` (exists) for the tent and bedroll |
| Fittings (40): hearth, smoke racks, beds, fire ring, stalls, woodshed, vault, cellar | `verbs.py` (13), `night.py` (9), `buildings.py` (8) | no | the fields the rows already carry or nearly do: `process` (the racks, `verbs.py:163` and 3 more), `fire` (exists), `fireproof` (exists, unused by `buildings.py:510`), `ground` (exists, unused by `buildings.py:98-100`), `houses` beasts (stalls), `sleeps` (beds), `cool` (cellar) |
| The camp structure (29) | `buildings.py` (10), `night.py` (9), `verbs.py` (7), `needs.py` (3) | no | a **structure row** `camp` with `floorless`, `store_kg`, `takes` (beds, fire ring), `levels` (its three), `lasts`, `fire` (in the weather), `upgradable: false`; there is no structures table at all today |
| Structure materials (25): stone, wattle, timber | `verbs.py` (15), `night.py` (5) | no | structure rows: `trade` (mason for stone, `verbs.py:1146-1163`), `repair` material (`buildings.py:339`), wear and damage multipliers (`night.py:747`), `storeys` (`verbs.py:1349`), `carve` (`verbs.py:1743`), `fades` paint (`night.py:236`) |
| Goods (21): meat, offal, rotting meat, hay, straw, salt... | `night.py`, `things.py` | partly: `meat` as a carcass's flesh is a core default of the carcass kind | item properties: `flesh` (`things.py:208`), `rots_to` (DECAY `becomes` exists), `smelt_when_off` (`night.py:16`) |
| Seasons (15): winter, summer, spring | `farm.py` (8) | borderline: a calendar's names | season rows with `slow_regrowth`, `warm`, `housed` (stalls), `breeding`; the crops already hold growth by season |
| Monuments and rooms (12): weir, cairn, hall, medium room | `verbs.py` (10) | no | the weir as a **work with parts** (§3.2); the cairn as a modifier (it is one: `method: cairn`); room size order from `floor` |
| Wild kinds and resources (12): willow, shallows, brine, rats, eel | `verbs.py:776`, `night.py:645-652`, `placed.py:181` | partly: a renewal rule's own context is the rule's | the rule's declared context (`renewal.context` already takes `**extra`); the willow's summer harm as the resource's `on_draw` hook |
| Processes (7): salting, keeping smoke, hard cure, retting | `process.py:657-658`, `things.py:171-173`, `verbs.py:1048` | no | process fields: `at_once` (salting and the hot smoke, today `lot: False` plus a branch), `words` (waiting, done, where) |
| Tools and techniques (4): plough, wooden plough, fell | `farm.py:1110-1136`, `verbs.py:779` | no | `brash` on the felling row; the plough's team and tool on the breaking row |
| Cattle roles (3) | `farm.py:1193`, `herds.py:495` | no | the population kind's classes (§3.6) |

So about **80 of 345** are legitimate as they stand or in kind, and about **265** should become properties of rows, most of them
properties the rows already carry or that one table (structures) would hold.

### 2.3 Property tables keyed by name

The same disease one step removed: a property held in a module's own table keyed by row names, not on the row. About 30:
`data.py`'s `KEEP_DAYS`, `GOES_OFF`, `IN_PROCESS_OF` (`:138-176`, written onto the rows at load: the least harmful); `stores.py`'s eight
goods classes and `WORDS` (`:21-31`, `:66`); `gear.py`'s `SET_GEAR`, `SET_MOST`, `TOOL_LIVES` (`:120-125`); `placed.py`'s `METHODS`,
`WATER`, `NOUN`, `WORDS` (`:19-28`); `things.py`'s `SET_NOUN`, `SET_WHAT`, `FLESH` (`:208`, `:310-313`); `night.py`'s `GOING_OFF`
(`:16`); `farm.py`'s `ROLES`, `ROLE_WORD`, `ROLE_OF`, `LAND` (`:24-26`, `:235`) and `herds.py`'s `ROLES` again (`:25`); `engine/wild.py`'s
`SET_HOLD_KG` (`:920`); data's `STORES.kinds` and `STORES.words` (`data.py:399-410`) beside stores' `SPACES`. The set gear's nouns are
held **four** times (`placed.NOUN`, `things.SET_NOUN`, `things.SET_WHAT`, `gear.plural`).

### 2.4 Word-list parses

32 in verbs.py (21 at f728a3b7), 4 in things.py, 4 in farm.py, 3 in placed.py, 2 in herds.py, 1 in stores.py (a grep for `in ("`,
`removeprefix(` and `endswith((` on input text). The new ones came from live run 1's replies ([[W-102 Fix the act shapes' interface faults found in live run 1's rebuilt arm|W-102]]: `HOME_WORDS`, `RACK_WORDS`,
`verbs.py:1892-1895`, commit 8018a85e) and the containers (`CONTAINER_WORDS`, `verbs.py:2036`, commit 0965a4d0).

---

## 3. What does not fit

### 3.1 Works (a change built up over days)

**The mechanic:** something is begun with its materials, worked in units by one or more people (each act's units, skill and
practice), kept between days, and finished with an effect.

**Copies today (nine):** a building (`unfinished`, `verbs.py:1676-1704`), a room, an upgrade or a tier (`works`, `:1544-1576`), a
fitting (`fitting_work`, `:1646-1673`), a weir's part (`weir_work`, `:1442-1500`), a weir's mending (`mending`, `:1507-1541`), a grave
(`grave`, `:292-327`), field works (`works` on the parcel, `farm.py:840-866`, `:1353-1378`), fences (`herds.py:60-90`), clearing
(`verbs.py:2779-2830`). The shared step is already one function for four of them (`_build_act`, `verbs.py:273-279`); the records, the
"one at a time" rules, the crews and the finishing are each their own.

**A pattern would need:** a work record `{kind, target, units_left, by, crew, began}` on any body or parcel; per kind (a row): how the
units and materials are set (from a cost function or a row), who may work (anyone, a crew, a trade at a level), whether several may run
at once, and the finishing effect as a compound primitive. The hypothesis's acts (3f) cover one act's cost; nothing covers the work
across acts.

### 3.2 Bodies with parts

**The mechanic:** a body made of typed parts, each with its own make-up and condition; the whole's capacity, cost and wear derive
from them. **Copies:** a building (rooms with floor and storey, fittings with spaces and stores: `buildings.py:23-109`); a weir
(sections by position and material, each with a level and a footing: `verbs.py:1442-1541`, `wild/gear.py`); a field (holdings by plot,
each with crop and soil; strips below a plot: `farm.py:234-440`, `strips.py`); a set thing (its laid pieces: `gear.py:288-346`). Each
writes its own parts list and its own sums. **A pattern would need:** a body kind declaring a parts field, each part a row reference
plus its state; capacities and costs as sums over parts by declared fields (`floor`, `spaces`, `holds`, `share`, `hold`); wear per
part (§3.8). feature_packages §2's "contents or make-up" on the body is the place; it is not yet a mechanism.

### 3.3 Keeping by risk and remedy

**The mechanic:** a good loses a share a night on its clock; the share rises with the risks its place leaves (a hazard, never a
share: `stores.py:244-247`). **Copies (seven loss rules):** a store's portions (`stores.py:250-297`), the night's base and the open
(`night.py:327-339`), a lot in a container (`process.py:555-576`), in hand (`stores.py:300-309`), gear's rot wet and dry
(`gear.py:449-534`), a carcass's flesh (`night.py:663-691`), a crop past its window (`farm.py:1426`). The vault's fire safety
(`buildings.py:506-512`) and vermin's exposure (`stores.py:175-182`) are the same shape with other risks. The risks are coded (floor
damp, flies, brine, the heap, frost in `stores.py:152-172`; wet in `gear.py:459`); which goods meet them is in name tuples
(`stores.py:21-31`). **A pattern would need:** risks as rows (name, multiplier, when it applies: a season, the frost, wet ground, out
of brine); goods declaring the risks they meet (`meets`); places, containers and conditions declaring what they remove or add (the
spaces and containers already do: `removes`, `adds`); one rate function. The hypothesis's processes (3c) are "becoming another good
over nights under conditions"; keeping is "becoming less", continuous, with the conditions as remedies. It could be cut as a process
with no end, but the remedy vocabulary is its own and wants its own rows.

### 3.4 Drawing a need from ordered sources

**The mechanic:** a need in some worth (food, heat, fodder, a recipe's inputs), met from an ordered list of containers, a good's worth
a unit from its row, what the book holds back left alone, a shortfall with a consequence. **Copies (six):** an act's inputs
(`verbs.py:494-516`), a gift's top-up (`verbs.py:558-568`), eating (`night.py:590-613`, `eat_order` `:491`), a herd's fodder
(`farm.py:1495-1505`), a house's fire (`night.py:60`, `forests.burn`), a smokehouse's fuel (`process.py:231-251`, `:476-486`). The
pack ox's hay (`herds.py:508`) is a seventh. Each loop orders, skips and records in its own way. **A pattern would need:** `draw(need,
worth_field, sources, order_key, held_back, why)` returning what was met and from where, with the record for the morning lines
(`_drawn`, `night._meal_record`). This is the "costs and needs from the registry" half of 3f made general, and it is not named.

### 3.5 Capacity and room

**The mechanic:** a container holds so much by a declared unit (kg, count, spaces of floor, ground), filled in an order, the rest
refused or overflowing. **Copies (eight):** a store's portions (`stores.py:188-241`), a building's floor (`buildings.py:150-188`), a
parcel's ground (`:86-109`), the racks' kg (`process.py:207-224`), a camp's 30 kg (`buildings.py:157-175`), a set's hold (`wild.py:920`),
the weir's hold (`data.py:461`), what one carries (`items.carry`). The hypothesis has no word for containers at all; feature_packages
§3 puts `core/goods.py` ("containers, the base columns of items, carrying") in the core, so this is the core's mechanism to name.

### 3.6 Populations with classes

**The mechanic:** a population counted by class (cows, oxen, bulls, young), with rules between classes (breeding needs a bull and
cows, the young grow, milk follows calving), fed from a stock and from stores, split and merged. **Today:** cattle only, its roles in
code (`farm.py:24-26`, `herds.py:25`), starvation's order a literal (`farm.py:1512`), a herd's `kind` read only to ask
whether it is cattle (`herds.py:139`), the slaughter's goods by role
(`TECHNIQUES.slaughter.yield.gives`). The hypothesis's stocks (3a: S, K, r) cannot hold it; feature_packages §2.3's population base
shape ("counts by class") and its acceptance test 1 (sheep as rows) are where it belongs. Not a new pattern so much as 3a too thin.

### 3.7 Names: twelve resolvers, not one

`KN.resolve` (techniques, `knowledge.py:24-37`) is the only resolver over rows' aliases. Beside it: `verbs.item_of`'s dict
(`verbs.py:424-431`), `placed.method_of` and `WORDS` (`placed.py:23-41`), `FITTING_ALIAS` and `MONUMENT_ALIAS` (rows' aliases, two
tables: `data.py:359`, `verbs.py:1142`), `STRUCTURE_WORDS` (`verbs.py:1140`), `WEIR_PARTS` (`:1433`), `UPGRADE` (`:1143`), the storey
words (`:1205`), `HOME_WORDS`, `RACK_WORDS`, `CONTAINER_WORDS` (`:1892-1895`, `:2036`), `LIFT` and `_as_tend` (`:2295`, `:2300-2319`),
`farm.ROLE_OF` (`farm.py:26`), `_thing_site`'s phrases (`verbs.py:364-381`). Pattern 4 is right and unbuilt for everything but
techniques.

### 3.8 Lives and wear: the right pattern, nine implementations

A gear piece's uses and rot (`gear.py`), the older tools' wear map (`TOOL_LIVES`, the `wear` primitive), a fitting's wear by use or
years (`wear.py`), a building's condition and breaks (`night.py:237-252`), a building's levels (`night.py:694-760`), a camp's
`lasts_until` (`night.py:226-236`), a weir section's level (`engine/wild.py:3142`), a fence's level (`herds.py:60-90`), field works'
decay (`farm.py:1353-1378`). Four level scales (`buildings.LEVELS`, `CAMP_LEVELS`, `COND_OF_LEVEL`; fences; weir sections; works).
Mending has six forms (§4). The hypothesis is right that this is one pattern; the code has not been brought to it.

### 3.9 The candidates the brief names, for this area

| Candidate | Here | Fits? |
|---|---|---|
| fire and heat | house and camp fires (`night.py:47-80`), open fires (`:429-458`), the smokehouse fire (`process.py`), the brine pan | a **draw** (§3.4) of heat, plus a **pulse** for catching fire (3b): fits once draws exist |
| eating and hunger | `night.py:102-194`, `needs.py` | a **draw** of food worth; hunger's effects are area C's |
| buildings with rooms and floors | `buildings.py` | **parts** and **capacity** (§3.2, §3.5) |
| theft and witness | `verbs._take`, `placed.tend_one(theft=True)` | rights (area C) read by acts; the act's effect is general; the witness is area D's noticing |
| travel and roads | herds on roads (`herds.py:244-330`) | area C |
| weather and the calendar | read by wear, keeping, crops, fires | the readers want declared conditions (risk rows, season rows), not named labels (`night.py:705-719`) |
| agreements, claims, households | `_against`, `may_take`, `_out` | area C; acts read them through `Here` |

---

## 4. The verdict for area B, in [[D2-354 The architecture is a healthy balance, not a strict one|D2-354]]'s terms

**The set is too few, and in two places wrongly cut.** Too few: works, parts, keeping, draws and capacity are mechanisms with six to
nine copies each and no pattern. Wrongly cut: set gear (3d) is not a mechanism of its own but a body with parts that samples a stock
and wears by lives; and stocks (3a) are too thin for the herds. The rest fits: typed rows (1), properties not names (2), processes
(3c), lives (3e), acts (3f), one resolver (4) are the right patterns; in this area they are built for processes, stores and gear and
missing for most else.

### Where a general primitive should own the behaviour

| Primitive | Owns | Its extension points (so a feature extends it, never bypasses it) |
|---|---|---|
| **Acts' effects** | every act's outcome | a yield-kind registry (handler, outcome for the capacity model, counts-as-done, result words template); techniques declare their kind; unknown kinds refused at load |
| **Works** | everything built up over days | a work-kind row: cost function or row, who may work, one at a time or many, the finishing compound primitive |
| **Parts and capacity** | buildings, weirs, holdings, sets, stores, racks, carrying | part fields declared on a body kind; capacity units (`kg`, `count`, `spaces`, `ground`) and fill order as rows; overflow rule per container kind |
| **Keeping** | every loss of goods by condition | risk rows; goods' `meets`; places' and conditions' `removes` and `adds`; the clock |
| **Draws** | eating, fodder, fuel, inputs | a worth field per need (`food`, `heat`, `fodder`); source order per need; the book's holds |
| **Lives and wear** | gear, tools, fittings, buildings, sections, fences, works | a life row (count by uses, nights, years or levels; causes as rows with multipliers; what wearing out does: half rate, broken, gone); the mend technique per life |
| **One resolver** | every noun an agent writes | aliases, nouns and plurals on rows (items, techniques, fittings, monuments, structures, set methods, containers, places' words) |
| **Load check** | every registry | required fields per category, known kinds and property names, unique aliases; a failed check stops the world loading |

### Where a system legitimately owns its specifics, and how to keep them there

| System | Its own specifics | Kept inside by |
|---|---|---|
| farming | crop growth by season, soil steps, plot shares (`farm.py:100-440`) | the crop's growth as its own rule on a declared layer (feature_packages §2.2); the farm acts as registered yield kinds; no cover or season named outside it |
| water and the weir | a section's share and hold by position, flow classes, ice (`wild/gear.py`, `data.WATER_WORKS`) | the weir as a work with parts whose part rows carry share, hold and wear; its specifics in the water package's handlers, reached through the parts and wear points; `verbs.py` and `night.py` never name it (today `verbs.py:140-146`, `:1402`, `night.py:718`) |
| animals | wandering, gadding, splits, the pack ox (`herds.py`) | the animals package's population kind with classes; covers' properties for the parcel's value |
| stores | the sort's order, vermin's exposure, sudden illness (`stores.py`) | already a unit; its goods classes move onto the item rows |
| processes | the lot's record, the fire's fuel and catching (`process.py`) | already a unit; its three condition kinds become declared conditions; salting's "at once" a row field, not a branch in `verbs._make` |

**The rule that keeps specifics inside:** a system's names appear only in its own package; anything outside it reaches the system's
behaviour through a property or a registry entry. Today 101 named branches sit in `verbs.py`, which is no system's own.

### From the history: ad hoc because the general system could not be extended, and ad hoc though it could have been

**Could not be extended (the general system had no extension point):**
- The 13 wild yield kinds (b7ade4d9, 9 Nov, and the waves after): the act dispatch was an `elif` chain; each kind had to add a branch.
- Shelter in levels (28fc06ff, 10 Nov): the building's condition had no wear model to extend; a second scale was added beside it.
- The weir in sections (c2f2ff46, 16 Nov; 099c9d38, 20 Nov): buildings had no parts beyond rooms and fittings, and no works model;
  the weir got `sections`, `weir_work`, `mending` and its own wear.
- The set gear's night by method (wild brief 2, 1f43911a; [[W-98 Build stage 2, taking and making|W-98]], 653737c4): the set thing declared only `base`, `line`, `holds`; water,
  ice, the run's reach and the catch's state were coded per method.
- Herds cattle only (6eaf51bb, 23 Oct): no population kind with classes existed.

**Could have been general (the property or the system was there):**
- The racks by three fitting names in `verbs.py` ([[W-99 Build stage 3, keeping, stores and the household book|W-99]], [[W-102 Fix the act shapes' interface faults found in live run 1's rebuilt arm|W-102]], 23 Nov) though `FITTINGS.process` was written in the same wave.
- `TOOL_LIVES` beside `LIVES` (8ad7c50f, 23 Nov): `LIVES` has `count: acts`; the older tools were left out "in this stage"
  (`gear.py:20-21`).
- The vault by name (956a9935, 1 Nov) though its row says `fireproof`; the woodshed's ground by name though its row says `ground`.
- Stores' goods classes as name tuples (3a1962e3, 23 Nov) in the same module that writes `vermin` onto the item rows.
- `SET_GEAR` and `SET_MOST` (8ad7c50f) though the set methods are technique rows with a `set` block (`wild/methods.py:101-107`).
- The smokehouse (5be6fa30, 16 Nov) and the hearth's rack (572151b5, 10 Nov) as their own code in keeping.py and verbs.py: later
  folded into `process.py` (0965a4d0, 23 Nov), which proves the general form was within reach.
- `item_of`'s alias dict (p) though techniques and fittings carry `aliases`.

---

## 5. Taxonomy of the area

### 5.1 Categories and kinds of row

| Category (feature_packages §2) | Registry | Rows | Kinds within |
|---|---|---|---|
| Type: goods | `ITEMS` (`data.py:20`, plus gear's 20, process's 1, stores' 1) | 96 | food, fodder, fuel (`heat`), materials, tools (`tool`), weapons, gear (pieced, by `LIVES`), containers (`container`), carriers (`carry`), shelter (`camp`), waiting goods |
| Type: techniques | `TECHNIQUES` (`data.py:504` and registered rows) | 161 | by verb: gather 25, work 34, make 54, build 25, modifier 23; by yield kind 37 (§2.2) |
| Type: fittings | `FITTINGS` (`data.py:308`) | 18 | stores (`holds`), fires (`fire`), workplaces (`process`, `wear`), beds and stalls (`per`) |
| Type: rooms, blueprints, monuments, tiers | `ROOMS`, `BLUEPRINTS`, `MONUMENTS`, `TIERS` | 3, 4, 4, 4 | the weir a monument with a site and a crew |
| Type: structures | **none** | (wattle, timber, stone, camp in code) | |
| Type: crops, fences | `CROPS`, `FENCES` | 4, 2 | strip crops (`strip`) |
| Type: processes | `process.PROCESSES` | 6 | lot (4), at once (2) |
| Type: lives | `gear.LIVES`, `gear.TOOL_LIVES`, `FITTINGS.wear` | 15, 7, 4 | by nights, acts, used up, rot only; by use or years |
| Type: spaces and containers | `stores.SPACES`, `stores.CONTAINERS`; `data.STORES` | 8, 5 | |
| Type: decay tables | `DECAY` | 10 | |
| Type: covers, resources | `COVERS`, `RESOURCES` (area A's) | 12, 15 + wild | read here by name (§2.2) |
| Body kinds | `things.KINDS` | 4 | pile (with `lot`), remains, carcass, set; buildings and herds are bodies outside it |
| Population | herds (`s.herds`) | | cattle only, four roles in code |
| Parameters | `PHYSICS` sub-tables (farming, cattle, heat, wear, smokehouse, repair...), `THINGS`, `HERDS`, `SPACE`, `CAPITAL`, `WATER_WORKS` | | |

### 5.2 Properties, grouped

| Group | Properties carried or read |
|---|---|
| **Quantities** | weight, food, heat, fodder, carry, holds, holds_kg, per_space, spaces, floor, ground, room, units, hours, batch, inputs, gives, materials, load, base, range, p, share, hold, most (side table), seed_kg, yield |
| **Rates and clocks** | spoil, keep days (side table), rot (wet, dry years), life, uses, count (nights, acts, used, none), renewal, r, growth by season, nights, in_rate, fuel a kg, wear life or years, clock (capital, day), takes, restores, torn |
| **Conditions** | cook, raw, at (covers, fittings, building, things), needs (a fitting), structure, structures, site, spring, apart, heavy, by_season, fire or cond, covers (a process), suits, removes, adds, decay class, hardy, needs_winter, ice, the goods classes (side tables) |
| **Capabilities** | tool grade, weapon, camp, track, seen, fire, fireproof, process, container, mends, set, crew, trade, basic, class, untaught, modifies, mend_gear, batch |
| **Links to other rows** | gives, inputs (with one-of), seed and gives (a crop), green, draws, draws_else, needs, wear.mend (a technique), process -> fittings, in (input -> waiting -> output), decay table, becomes, pack, set method -> gear (side table) |
| **Words** | label, does, words, aliases, ambient, low and high, manual, note; nouns and plurals only in side tables (§2.3) |

The groups are clean on the rows; what is missing is a declared schema per category (required fields, types, units, clock) and the
properties now in side tables and code: wet, grazing (covers); flesh, meets (goods); noun, plural, water, movable (set methods);
houses beasts, sleeps, cool (fittings); every structure property.

### 5.3 Families of mechanisms that could be generalised

| Family | Members today | What they share | What a general version would read |
|---|---|---|---|
| Act effects | 37 yield kinds | site, shortfall, skill and tool multipliers, a draw or a change, practice, an event, a line | the kind's row: handler, outcome, success rule, words |
| Works | 9 (§3.1) | units left, materials at the start, crew, practice per act | the work-kind row |
| Lives and wear | 9 (§3.8) | a count on a clock, causes, a worn state, mending | the life row and its causes |
| Mending | 6: gear (`verbs.py:914`), a fitting (`:804-812`), a building (`:2742`), the weir (`:1507`), fences (`herds.py:60`), works' upkeep (`farm.py:1370`) | materials a share of the build, units, a level or uses back | the life row's `mend` |
| Keeping | 7 (§3.3) | base rate, multipliers by condition, hazard form | risk rows, `meets`, `removes` |
| Draws | 6 to 7 (§3.4) | need, order, worth, held back | worth field and source order |
| Capacity | 8 (§3.5) | units, fill order, overflow | capacity rows |
| Goods becoming goods | process lots (4), salting and the hot smoke at once, crops on a holding, meat to rotting meat (`DECAY.becomes`), green crops | input, condition, nights, output and ratio | the process row, with `nights: 0` for at once and `becomes` as a loss process |
| Placed things sampling a stock | 4 set methods, the weir's traps, the mill's race trap, a herd grazing | a hold, a share of what passes or stands, a catch rule | the set method's row: what it samples, hold, catch, wear |
| Pulses | smokehouse fire, old breaks, serious damage, trap wreck, gear torn, blight, a herd lost on the road, a split | a nightly chance from conditions, an effect | pulse rows (3b) with their conditions |
| Name resolution | 12+ (§3.7) | words to a row | one alias table from rows |
| Words of a result | each handler's own lines | what was done, got, where, why short | the yield kind's words template, with the drawn record |

---

## 6. History: how the area was built

From `git log --all` on the area's files (the history before the split is reachable through `archive/cybertron1-inherited`). Commits on
the area by day: 23 Oct 32, 24 Oct 13, 1 Nov 20, 2 Nov 8, 7 Nov 7, 8 Nov 10, 9 Nov 16, 10 Nov 3, 13 to 17 Nov 23, 20 Nov 3, 23 Nov 20,
24 Nov 9.

### 6.1 Three ways a mechanism came in

**A new ad hoc system** (its own records, its own code, names in function code):
- 23 Oct, 1dbbf0a5 (Package C): fences round a parcel as field works with their own levels and decay: the first separate wear scale.
- 1 Nov, 956a9935 (building package 1): wear by structure as breaks; the vault and the woodshed by name; `STRUCTURE_WORDS`.
- 9 Nov, b7ade4d9 and the wild waves: `wild_take` and twelve more yield kinds, each a branch in `verbs._technique` and a handler in
  `engine/wild.py`.
- 10 Nov, 28fc06ff (wild brief 4 stage B): shelter in levels beside the old breaks, gated by `levels_on` (`buildings.py:307`), so two
  wear systems run by world.
- 16 Nov, f8e97336 and c2f2ff46 (brief 5): the weir: a monument with sections, `weir_work`, `mending`, its own wear in `wild.py`, the
  gap's cost by `"weir" if ... else "mill"`; the water wheel by name in `_make`.
- 23 Nov, 8018a85e ([[W-102 Fix the act shapes' interface faults found in live run 1's rebuilt arm|W-102]] fixes): `HOME_WORDS`, `RACK_WORDS` from live run 1's replies.

**Built into an existing general system** (a row, or a registered kind, on a general rule):
- 23 Oct, ce24b6f3: "Techniques, recipes, blueprints and fittings are data: one handler for gathering and work, one for making, one
  for building" (`verbs.py:1-3`).
- 7 Nov, bfd76c3d and a02acab5 ([[D4-103 The engine overhaul goes ahead, in phases|D4-103]] overhaul phase 1): the renewal registry; gathering yields as outcome distributions
  (`yields.py`); the night's food need as `needs.food`.
- 7 Nov, cfd79789: fishing, salt and salting as the water system's rows.
- 23 Nov, eff4c7e9 ([[W-98 Build stage 2, taking and making|W-98]]): the wave's recipes as rows at real hours; the flax strip as a crop row with `strip`.

**Generalised and extended an existing system:**
- 7 Nov, 5a85a95e: the night's rules as pure functions read by the engine and the capacity model alike.
- 23 Nov, 0965a4d0 ([[W-99 Build stage 3, keeping, stores and the household book|W-99]]): the hearth's rack (572151b5, 10 Nov) and the smokehouse (5be6fa30, 16 Nov) folded into one process shape
  (`process.py`); keeping.py cut from 245 lines to 17 (`git diff --stat f728a3b7`).
- 23 Nov, 3a1962e3 ([[W-99 Build stage 3, keeping, stores and the household book|W-99]]): stores as spaces and containers removing named risks, replacing the stores' spoil multipliers ([[D2-58 Grain spoils a little|D2-58]]) by
  `removes` (`stores.py:98-100` pops the old `spoil`).
- 23 Nov, 8ad7c50f ([[W-98 Build stage 2, taking and making|W-98]]): gear as pieces, one record for made and placed gear, carried by the primitives.

### 6.2 The trend

Better inside the new units, worse at the seams, flat overall:
- The new modules (gear, placed, process, stores, strips: 2,392 lines) carry 61 named branches, 25 a thousand lines; the old files
  carry 34 a thousand. Over the whole area the density went from 33.6 to 32.7.
- verbs.py gained 18 named branches (83 to 101) and 11 word lists (21 to 32) in the wave: the seam is where each new unit is joined to
  the acts.
- Three new systems were built beside the old ones they could replace: `TOOL_LIVES` beside `LIVES`, `SPACES` beside data's `STORES`
  (both read: `buildings.py:203` reads `STORES["words"]`), `IN_PROCESS_OF` beside the process rows.
- The wild layer's 13 kinds (9 Nov) are the largest ad hoc addition and have not been generalised; the wave did not touch them.

---

## 7. What in the process let ad hoc systems in

| Cause | Evidence |
|---|---|
| **Briefs named features, not mechanisms** | brief 5's sections are "the smokehouse", "the brine pan", "the weir" (commit subjects 5be6fa30, f8e97336); each built its own path. The [[W-73 Fishing, hunting and their materials developed together|W-73]] design set did the opposite for processing ("Every way of keeping a glut ... has one shape", `process.py:3-5`) and that unit came out general |
| **Edits kept to the seams; the new beside the old** | "edits to the old files are kept to the seams the specs name" (`w73_design/build_plan.md:11-12`); [[D2-244 The engine's reworking into feature packages|D2-244]]'s feature units. A unit self-contained with its names passes; the old special cases stay and the join is written in verbs.py |
| **Tests for interfaces only** | "unit tests and bot runs for interfaces and basic functioning only ([[D2-298 Bot runs test interfaces and basic functioning only|D2-298]])" (`build_plan.md:15`); no test that a new row works without code; feature_packages §8's acceptance tests 1 and 2 are not built |
| **Done means one world works** | every stage's "done when" is Eelmouth or the runs world (`build_plan.md:24-30`); the first generality audit ([[W-108 The waters calibrated across many generated environments|W-108]], `02zzzl_waters_calib/generality.md`) came the day after the wave |
| **No registry checked at load** | rows merged by `setdefault` (`gear.py:136`, `stores.py:86`, `process.py:133`); a misspelt field is ignored; an unknown yield kind falls through `verbs.py:860-862`. The only check is a test (`tests/test_cybertron2_capacity.py:31-34`, every yield kind read by the capacity model) |
| **Live-run fixes patch the words that failed** | [[W-102 Fix the act shapes' interface faults found in live run 1's rebuilt arm|W-102]] (8018a85e: `HOME_WORDS`, `RACK_WORDS`), [[W-104 Build the after-runs list from live run 1|W-104]] (5117e9e8: "your a hand line"), [[W-97 Build stage 1, the basis in code|W-97]] (a24dbf8e: "a place's name is the place"): each a list of phrases, not an alias on a row |
| **Audits ask "built as designed?", not "built generally?"** | build_gaps.md ([[W-73 Fishing, hunting and their materials developed together|W-73]]'s audit) classifies designed against built (partly, later, nowhere, decided); it has no column for a named branch or a parallel system |
| **No structures table** | with nowhere to put a structure's property, 54 branches name wattle, timber, stone and the camp (§2.2) |

---

## 8. The restructuring's cost for area B

In feature_packages.md §9 and §10's terms. Lines are of area B's 10,560 unless said; builder-days as §10's (a refactor slower per line
than new code, each step checked against golden journals).

| Step | Lines touched | New | Builder-days | Risk | Saves |
|---|---|---|---|---|---|
| **Load check** over every registry (required fields, known kinds, known properties, unique aliases) | 0 | about 200 | 0.5 to 1 | low; finds errors at once | the silent skip; every misspelt row |
| **Yield-kind registry** for `verbs._technique` and `farm.act` | about 300 | about 100 | 1 to 1.5 | low (byte-identical journals) | a new kind is a registration; the capacity model reads every kind |
| **Properties off names** (§2.2's ~265 branches; a structures table; cover, fitting, item, set-method fields) | about 450 | about 80 row fields | 2 to 3 | low | most of §2; acceptance test 1's way in |
| **One resolver** (aliases, nouns, plurals on rows) | about 300 | about 60 | 1.5 to 2 | medium: parses agents' text; needs live run 1's replies as a fixture | 12 resolvers to 1; [[W-102 Fix the act shapes' interface faults found in live run 1's rebuilt arm|W-102]]-style patches become alias rows |
| **Keeping by risk and remedy** | about 350 | about 60 | 1.5 to 2 | low to medium (calibrated rates must come out the same) | 7 loss rules to 1 |
| **Draws from ordered sources** | about 250 | about 80 | 1.5 to 2 | medium (the meal order and the book's holds) | 6 loops to 1 |
| **Works** (9 records to one) | about 800 | about 150 | 3 to 4 | medium: world schema change, in-flight works migrated | 9 copies to 1; stage 5's works (u7) built on it |
| **Lives and wear** (9 to one, with mending) | about 700 | about 150 | 3 to 5 | medium to high: the weir's wear ([[D2-210 The weir in sections, capped, with upkeep by the river|D2-210]]) and shelter levels are calibrated | 9 to 1; the oven, millstones, weir, house and fence mended by one act |
| **Parts and capacity** (buildings, weir, holdings, sets) | about 500 | about 150 | 2 to 3 | medium | the weir off its own path; smoke huts and new works as rows |
| **Herds as a population kind with classes** | about 1,000 (with herds.py) | about 200 | 3 to 4 | medium | feature_packages phase 3 and acceptance test 1 |
| **Set gear by rows** (`engine/wild.py`'s set night, `placed.py`) | about 400 (in wild.py) + 150 | about 50 | 1 to 1.5 | low to medium | four methods' branches to rows; the weir's traps a set like any other |
| **Total** | **about 3,500 to 4,000** in area B, plus about 400 in wild.py | **about 1,300** | **17 to 25** | | net shrink of about 1,000 to 1,500 lines |

**Against feature_packages §10:** phase 4 already counts "the technique hub about 600" and "night into phases about 500" rewritten
lines for this area, and phase 3 the animals (about 2,000 moved, 500 rewritten). Done during those moves, the pattern work is about
half again on top of what phase 4 touches anyway, and it saves touching these files twice. Done before them (the cheap tier: the load
check, the yield-kind registry, properties off names, one resolver: about 1,050 lines, 6 to 8 builder-days), it needs no schema
change, keeps the golden journals byte-identical, and makes phase 4's moves smaller, since a package then registers rows and handlers
instead of carrying named branches into its folder.

**What it costs not to:** every new feature in this area is today written as stage 5 and 5b are planned (`build_plan.md:30-31`: the
smoke hut, works in sections, border fences, mending several levels): each a new record kind and a new branch in verbs.py. With works,
parts and wear as primitives, stage 5's list is mostly rows.
