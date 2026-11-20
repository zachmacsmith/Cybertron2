---
id: docs/review/37_growth/02zzr_triage.md
kind: note
updated: "2026-11-20"
---
# 02zzr: the triage of the open asks and 37.2's threads

*note · `docs/review/37_growth/02zzr_triage.md`*


37.2, 20 Nov 2026. WORK [[W-63 An audit of what was started and left|W-63]], OPEN [[Q-61 What was started and left, and the mechanisms to catch it|Q-61]] (1). Zach: "Let's do triage now of main open threads / questions to dig into".

**What it covers:**
- every ask waiting on Zach (35);
- every live 37.2 thread (24);
- each one read in full against DECISIONS, the commits and the later records (`python3 tools/records.py show <id>`).

**Not covered:** 37.4's 13 threads and its own asks; those are 37.4's to triage.

**What it gives:** a recommendation for each item, and the shortlist worth digging into. Nothing is closed until Zach answers.
Closures will carry `by: zach` where he decides, and `by: agent` or `by: default` where he only confirms a batch ([[D2-236 Every resolution names who made it|D2-236]]).

## 1. Asks

### A. Already answered or overtaken: close (by agent)

| Ask | Why it can close |
|---|---|
| [[Q-14 (Closed 2 Nov|Q-14]] | Its own text says "Closed 2 Nov: replaced by review 38.51". It was never struck through |
| [[Q-25 Zach's decisions now open, in one list|Q-25]] | The 2 Nov "one list" (38.51). Its items went to [[Q-21 Built for Package C|Q-21]] to [[Q-23 Built for Package F|Q-23]] and later decisions; the digest ([[D2-239 Zach's views and the hand-offs|D2-239]]) replaces lists like it |
| [[Q-40 Brief 4 as built, and its gate|Q-40]], [[Q-41 Brief 4b as built, and its gate|Q-41]] | Answered 16 Nov in Zach's words, as quoted in [[L-113 Briefs 4, 4b and 4c's deviations, to revisit|L-113]]: "flag these deviations for me to revisit later but still merge". Briefs 4 and 4b are on main; the deviations live in [[L-113 Briefs 4, 4b and 4c's deviations, to revisit|L-113]] |
| [[Q-44 Brief 4c before the build|Q-44]] | Brief 4c before the build. It was built and merged (6190b4d). Its open parts are [[Q-46 Brief 4c as built|Q-46]] (b) to (e) |
| [[Q-32 02zv §6's decisions still open|Q-32]] | 02zv §6's plan. Briefs 1 to 5 were built in its place; the packs never briefed are [[L-117 Wildlife pack K3 forays, methods and knowing|L-117]] to [[L-127 The ecology's calibration backlog|L-127]]; traits and general methods ([[D2-204 People answer the wild by general methods, not a technique per kind|D2-204]]) replaced per-kind modules ([[D2-203 Each wild kind's behaviour is designed first, then built as a module…|D2-203]]) |
| [[Q-33 forays.md's open questions|Q-33]] | Forays' questions. Forays are already deferred ([[L-105 Forays as their own track|L-105]]); the questions move there |
| [[Q-50 One grid or several|Q-50]] | One grid. In effect answered by [[D2-222 The environment's places|D2-222]]: the cells are the source, and parcels and areas hold the stocks. The "how" is [[W-25 The world keeps its land|W-25]]'s and [[Q-48 The engine as feature packages|Q-48]]'s |
| [[Q-61 What was started and left, and the mechanisms to catch it|Q-61]] | (2) answered by [[D2-232 The records as items|D2-232]] to [[D2-240 The Obsidian vault is a local folder Zach opens whenever he likes…|D2-240]] (built). (1) is this triage, and closes with Zach's answers |

### B. Built weeks ago with a default taken, unchallenged since: close by default

| Ask | What it is | Since |
|---|---|---|
| [[Q-21 Built for Package C|Q-21]] | Package C's 16 built choices (herds, fences, finding) | 24 Oct |
| [[Q-22 Built for Package D|Q-22]] | Package D's 12 (birth, children, succession) | 24 Oct |
| [[Q-23 Built for Package F|Q-23]] | Package F's 10 (woods, fuel, fires) | 24 Oct |
| [[Q-24 Built for the building package|Q-24]] | The building package's 9 readings | 3 Nov |
| [[Q-26 Built without decisions, found by the 5 Nov sweep of 37.4's proposals|Q-26]] | Built without decisions: the household verbs, the knowledge counts, private notes, clearing for building, steal folded into take | 5 Nov |
| [[Q-34 Defaults taken under D2-207|Q-34]] | Three defaults under [[D2-207 The three wild build briefs are built|D2-207]] | 9 Nov |
| [[Q-36 Brief 1 as built differs from the brief in 16 places|Q-36]], [[Q-37 Brief 2 as built, and what its gate found|Q-37]], [[Q-38 Brief 3 as built, and its gate|Q-38]] | Briefs 1 to 3 as built (16, 18 and 11 deviations) | 9 to 10 Nov |
| [[Q-39 Brief 4's open questions|Q-39]] | Brief 4's four questions (meat scale, novice target, rack) | 10 Nov |
| [[Q-31 Does guard the field become D2-21's watch|Q-31]] | Guard the field against [[D2-21 The watch|D2-21]]'s watch: keep the two acts with merged costs, as built | 8 Nov |

- **[[Q-26 Built without decisions, found by the 5 Nov sweep of 37.4's proposals|Q-26]] carries rules built without a decision.** Closing it by default makes them the rules. Each could become a D row if
  Zach prefers.
- **The points still alive in them** move to one deferred row beside [[L-113 Briefs 4, 4b and 4c's deviations, to revisit|L-113]] (the briefs' deviations), so they are not lost:
  - houses break fast, so a shut house soon lets the fox in ([[Q-37 Brief 2 as built, and what its gate found|Q-37]] (a), [[W-21 Proposals for Q-37|W-21]]'s proposal);
  - a carcass left out does not raise a pack's losses on the herd ([[Q-38 Brief 3 as built, and its gate|Q-38]] (a), [[Q-41 Brief 4b as built, and its gate|Q-41]] (c));
  - the carrion pool's balance ([[Q-38 Brief 3 as built, and its gate|Q-38]] (b)).

### C. Owned by 37.4, or belonging elsewhere

- [[Q-27 The verb list|Q-27]] (the verb list) folds into [[Q-48 The engine as feature packages|Q-48]]: a cut into feature packages redraws the verbs.
- [[Q-42 The peoples benchmark before any run|Q-42]] and [[Q-43 Before the second peoples run|Q-43]] (the peoples benchmark and its second run) go to 37.4 to triage: are peoples runs still planned, and which of
  [[Q-43 Before the second peoples run|Q-43]]'s engine findings are fixed?

### D. Quick answers, one line each

| Ask | 37.2 recommends |
|---|---|
| [[Q-65 Delete the 16 empty branches|Q-65]] | delete all 16 empty branches |
| [[Q-58 The calibration worlds|Q-58]] | the first seven calibration worlds (lowland, dry east, coast under mountains, upland, high mountains, fen, chalk and clay), the rest later; no people except where a check needs them |
| [[Q-52 Environment systems|Q-52]] (6) | the river frequencies as targets (a spate a year, a flood every three or four, about 12 low days), re-measured across the suite |
| [[Q-51 Brief 5 (river and water)|Q-51]] (5) | the mill grinds at half its rate with the gap open |
| [[Q-57 Fishing, from the lake run|Q-57]] (a), (b) | fishing reaches the ring's water as the hunt reaches the wood around (traps and weirs still on a water parcel); a rod's line of cord or hair as well as hide. (c), the brook fished out, goes to the calibration worlds |
| [[Q-60 The water worlds' people, and the runs world for the…|Q-60]] | confirm the runs world as built and run (lifespan 64 and 16 years of history, [[D4-20 One agent, one model, for life|D4-20]] heirs, fields on the floodplain, the spring and the mill, three places to expand into); record as D2 rows |
| [[Q-53 Brief 5 as built|Q-53]] (a), (b) | keep the defaults (one rack batch per hearth; the rack's loss as built). (d) the live run is done (the runs world). (c), the merge, is in E |
| [[Q-46 Brief 4c as built|Q-46]] (d), (e) | birth windows and young of the year as their own class; the boar's field rows into autumn: yes (37.2's data) |

### E. Worth digging into: they shape the next weeks

1. **The water merge** ([[W-62 The water work is on eight unmerged branches, none on main|W-62]], [[Q-53 Brief 5 as built|Q-53]] (c)). Twelve branches, up to 61 commits ahead. It blocks [[W-60 The ecology's water measure counted each lake and the large river…|W-60]], [[W-53 Floodplains in the generator now|W-53]], [[W-56 One fish stock per water body, the engine half|W-56]] and [[W-59 The runs world for the model-per-household run|W-59]], and
   keeps the live run off main. Under [[D2-238 Branches|D2-238]]: merge with new behaviour behind switches. Needs Zach's go and 37.4's merge.
2. **Hunting against farming** ([[Q-46 Brief 4c as built|Q-46]] (b), (c), with [[W-22 Hunting against farming and gathering in generated worlds|W-22]]). A master hunting one wood daily does not deplete it and out-earns
   farming on unbroken ground (2.5 against 1.8 food a unit). This decides whether villages farm at all, in every run.
3. **Climate from the land** ([[Q-56 The land the engine reads|Q-56]]; [[W-49 Environment systems|W-49]], [[W-51 The weather across conditions|W-51]], [[W-8 Couple the food web to 37.4's weather and climate|W-8]]). The environment line: the weather, then the soil's water, then what
   farming reads. The generator's fields the engine never reads come in this order.
4. **The engine's shape** ([[Q-48 The engine as feature packages|Q-48]] feature packages, with [[Q-27 The verb list|Q-27]] and [[W-25 The world keeps its land|W-25]]). The largest long-term choice: 26 to 39 builder-days for
   the whole migration, or the cheaper path.
5. **Generation redesign** ([[Q-45 Generation redesign|Q-45]]). The people generator; it would settle the founders' ages problem ([[Q-60 The water worlds' people, and the runs world for the…|Q-60]] (a)).
6. **The border and the economy web** ([[Q-47 The border for now|Q-47]], [[W-39 The economy's layers and trees of dependence across the domains|W-39]]). How far the economy goes, and what to brief next.

## 2. 37.2's threads

| Thread | Recommendation |
|---|---|
| [[W-3 Records restructure|W-3]] records restructure (9 Nov) | close: replaced by [[W-65 Tracking threads automatically|W-65]] |
| [[W-4 wild_behaviour.md v3|W-4]] wild_behaviour v3 | close: replaced by [[D2-204 People answer the wild by general methods, not a technique per kind|D2-204]] (traits); with [[Q-32 02zv §6's decisions still open|Q-32]] |
| [[W-7 The ecology branch's next steps|W-7]] the ecology branch's next steps | close: overtaken by the briefs; the backlog is [[L-127 The ecology's calibration backlog|L-127]] |
| [[W-12 Forays (proposalsforays.md)|W-12]] forays | close as deferred ([[L-105 Forays as their own track|L-105]]) |
| [[W-5 37.2's own hygiene items|W-5]], [[W-9 Compile the generator into specworldgeneration.md|W-9]], [[W-10 37.2's spec write-ups owed since 2 and 3 Nov|W-10]] | merge into one spec catch-up thread: about 52 decisions in no spec file, [[D2-173 The generator fills in around what a world file gives|D2-173]] to [[D2-191 The generator designs within one envelope|D2-191]] for the generator, [[L-32 D4-83 (a fire under no roof in the night's weather|L-32]], [[L-44 D4-93 (one room, one fire|L-44]], [[L-45 D4-94's parts in 37.2's files|L-45]], [[L-61 D4-97's parts in 37.2's files|L-61]]. Queued, to size first |
| [[W-11 Landscapes still to tune|W-11]] landscapes to tune | merge into [[W-54 The calibration worlds|W-54]] (the calibration worlds) |
| [[W-8 Couple the food web to 37.4's weather and climate|W-8]] couple the food web to the weather | merge into [[W-49 Environment systems|W-49]] (climate from the land) |
| [[W-21 Proposals for Q-37|W-21]] graded damage to houses | deferred, with [[Q-37 Brief 2 as built, and what its gate found|Q-37]] (a) |
| [[W-29 A multi-village wild region and its live run|W-29]] the wild region run (10 Nov) | a one-page write-up against the null arm, then publish on Zach's go; or drop. 37.2 recommends the write-up: the run cost $75 and found two engine gaps |
| [[W-22 Hunting against farming and gathering in generated worlds|W-22]] | E2 |
| [[W-25 The world keeps its land|W-25]] | E4 |
| [[W-39 The economy's layers and trees of dependence across the domains|W-39]] | E6 |
| [[W-49 Environment systems|W-49]], [[W-51 The weather across conditions|W-51]] | E3 |
| [[W-53 Floodplains in the generator now|W-53]], [[W-59 The runs world for the model-per-household run|W-59]], [[W-60 The ecology's water measure counted each lake and the large river…|W-60]], [[W-62 The water work is on eight unmerged branches, none on main|W-62]] | E1 ([[W-59 The runs world for the model-per-household run|W-59]] also [[Q-60 The water worlds' people, and the runs world for the…|Q-60]]) |
| [[W-54 The calibration worlds|W-54]], [[W-64 Shared units for food, weight and work|W-64]] | after [[Q-58 The calibration worlds|Q-58]] |
| [[W-63 An audit of what was started and left|W-63]] | this triage |
| [[W-65 Tracking threads automatically|W-65]] | carries on (headers, run threads) |

**After it:**
- 37.2's live threads go from 24 to about 14;
- asks waiting on Zach go from 35 to about 12, of which six are the shortlist and the rest quick answers.
