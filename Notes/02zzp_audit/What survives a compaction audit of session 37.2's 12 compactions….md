---
id: docs/review/37_growth/02zzp_audit/compactions_audit.md
kind: note
updated: "2026-11-19"
---
# What survives a compaction: audit of session 37.2's 12 compactions (22 Oct to 16 Nov 2026)

*note · `docs/review/37_growth/02zzp_audit/compactions_audit.md`*


**Method.** `compactions.md` is cut at about 6,000 characters a section, so it never reaches sections 7 ("Pending tasks") and 9
("Optional next step"). I took the full summaries from the session transcript
(`(the session transcript) `isCompactSummary` entries). The extract is
`pending_next.md` and the full text is `full_summaries.md`; both are in this folder. Fates were checked against
`git log --all` of /home/user/cybertron2 (and /home/user/cybertron for the board), the current WORK.md, OPEN.md, DECISIONS.md and
proposals, and against the replies (the transcript) after each compaction. WORK.md only exists from 9 Nov 19:54 (93fbe74), so
compactions 1 to 8 could only be recorded in OPEN.md (Q-n, L-n).

**Fates.** *done*: done, with evidence. *carried*: the item is in the next summary's pending list, and its later fate is given
there. *recorded*: a WORK, OPEN or DECISIONS row holds it (the date is given when it came late). *vanished*: not done, not
carried, and not in WORK or OPEN. Items that survive only as a proposal's "Open questions" are counted as vanished and marked
*(proposal only)*.

## Table

| compaction (date) | pending item | fate |
|---|---|---|
| 1 (22 Oct) | Decisions awaiting Zach (02f §6, 02g §7, 02h §9, 02i §8, 02j §5) | done: [[D2-6 One livestock system, bred not made|D2-6]] to [[D2-79 Windfalls have no rule of their own|D2-79]], 22-23 Oct |
| 1 | Board Post 1 replies (plot interface) held | done: answered on the board (holding.md [[D4-23 Holding is a recognised claim|D4-23]] "answers Post 1's plot questions") |
| 1 | HF upload of the space runs (assigned to 37.4) | done: f9ce953 publisher; 48 runs under experimental/cybertron2 by 2 Nov |
| 1 | (next-step option) extend 02j to the remaining end uses (food, transport, meeting space, force, information delivery) | **vanished**: no later 02j work; the conversation moved to stone houses and defence |
| 2 (23 Oct) | journeys.md Q1-3 | done: [[D2-88 Traces left by passers|D2-88]], [[D2-89 Signs of slow change on long journeys later, flagged|D2-89]], [[D2-97 Daily notices on the road|D2-97]] (23 Oct) |
| 2 | hidden_ways.md Q1-4 | done: [[D2-90 Each edge end is tied to a side of the node and one or more parcels|D2-90]] to [[D2-92 How hidden a way is follows its land|D2-92]], [[D2-98 Hidden ways are found by the noticing rule|D2-98]] |
| 2 | road_encounters.md Q1-4 | done: [[D2-81 Which events have a fuse in the first worlds|D2-81]], [[D2-104 Roads have stretches|D2-104]], [[D2-110 A meeting on the road is a fuse event with a short conversation|D2-110]] |
| 2 | environment_state.md Q1-6 | recorded: [[L-23 Water as a need, and the land's hidden state|L-23]] (24 Oct) |
| 2 | Fences, for later | recorded: [[L-11 Fences, hedges and walls for herds|L-11]], [[L-24 Fences on the borders between parcels|L-24]] |
| 2 | Recipes §8 (tool effects by method); great trees | done: 0c0e16f; built in data.py |
| 2 | Buildings numbers, livestock numbers (02o), transport capacities ([[C-1 Carrying capacity|C-1]]) | done: [[D2-135 Carrying capacities (OPEN C-1)|D2-135]] to [[D2-137 The next region world|D2-137]] ([[C-1 Carrying capacity|C-1]] resolved), [[D4-41 Oxen are a role within cattle, not a kind|D4-41]] to [[D4-45 Cattle eat|D4-45]], [[D2-154 One unit of space at every level|D2-154]]/165/166/168 |
| 2 | Children and life (deferred) | done: [[D2-138 A child only by choice|D2-138]] to [[D2-149 Old age is tuned to a chosen life expectancy under each health regime|D2-149]] (24 Oct) |
| 2 | Disease ([[Q-13 D4-37 (whoever is owed may release a debt|Q-13]]) | recorded: [[Q-16 Disease mortality, the units of the sick, immunity, nursing, a healer|Q-16]], [[L-9 Disease (mortality, the sick, immunity, nursing, a healer)|L-9]] |
| 2 | Household-budget model of the first region, its layout, measurement | **vanished** (the budget model): the layout became region_c (02t, [[D2-137 The next region world|D2-137]]), but the model ("my proposed next job") was never built or flagged |
| 2 | Waiting on 37.4: [[Q-12 Decisions made with 37.2 that belong in 37.4's spec areas and are not…|Q-12]], [[Q-14 The whole agenda of open decisions in the proposals, by what each…|Q-14]], Q-15 | recorded: [[Q-12 Decisions made with 37.2 that belong in 37.4's spec areas and are not…|Q-12]] closed; [[Q-14 The whole agenda of open decisions in the proposals, by what each…|Q-14]] replaced by [[Q-25 Zach's decisions now open, in one list|Q-25]] (2 Nov) |
| 3 (29 Oct) | The per-system description (the current task) | done: 0362a07, 02zc |
| 3 | The Explore agent's run-behaviour report | done: used in 02zc |
| 3 | Unanswered offer: the takeover/1984 gap analysis and plan; who designs institutions and law | **vanished**: never answered; the theme came back on its own as [[L-74 What Cybertron 2 lacks for a society richer than Cybertron 1's|L-74]] (9 Nov, from an 8 Nov conversation) |
| 3 | forests Q4 (poles from young growth) | **vanished** (proposal only): forests.md status "Q4 open" |
| 3 | [[Q-22 Built for Package D|Q-22]] and [[Q-23 Built for Package F|Q-23]] confirmations | recorded: [[Q-22 Built for Package D|Q-22]], [[Q-23 Built for Package F|Q-23]] (still open) |
| 3 | Buildings items (stone costs, beds, fire ring, clearing, upgrades) | done: [[D2-154 One unit of space at every level|D2-154]], [[D2-165 Household members need beds too|D2-165]], [[D2-166 Large capital costs village-scale work|D2-166]], [[D2-168 Wear varies by structure and repair by size|D2-168]] |
| 3 | buildings_integration questions | done: "mostly settled"; replaced by the building package (02zh) |
| 3 | Timing of the fitting-work bug fix | done: 02zg brief, fdbb50e (1 Nov) |
| 4 (2 Nov) | Rerun the economy.check validation | done: 16:54; 3ca5d99 |
| 4 | Write up the findings (02zl) | done: 3ca5d99 |
| 4 | Wire economy.check into the generator's checks | done: 3ca5d99 (write.py) |
| 4 | Tests for economy.py | done: 3ca5d99 (tests/test_cybertron2_landgen.py) |
| 4 | Commit 02zk and economy.py | done: 3ca5d99 |
| 4 | Read the board replies from 37.4, 37.1 and 37.3 | **vanished** (in part): 37.4 answered and was answered (ac46e5b, ed00682); 37.1 and 37.3 never replied and were never chased |
| 4 | Check describe2.log (descriptions from the improved prompt) and report on quality | **vanished**: tailed at 17:00, never reported |
| 4 | Report to Zach, with [[L-41 Herds on the new covers Done decided D2-189|L-41]] and L-42 | done: 17:01 and 17:51 replies; [[D2-189 Rough grazing on the waste covers|D2-189]]; L-42 became [[L-49 Automated supply-chain and dependence checks for generated worlds|L-49]] |
| 5 (8 Nov 00:19) | living_populations questions 1-7 and the mechanism decision | **vanished** (proposal only): still "discussion, nothing decided"; overtaken by wild_layer and the ecology branch, never marked |
| 5 | wildlife Q6 (§11 candidates) | done: wild plants into wave 1 ([[D2-200 Wild plant kinds replace the single plants stock in worlds with the…|D2-200]]); waves built (§11 itself still discussion) |
| 5 | wild_plants Q1-4 | done in part: [[D2-200 Wild plant kinds replace the single plants stock in worlds with the…|D2-200]] to [[D2-202 The wild kinds and the people draw the same stocks on a village's land|D2-202]] (9 Nov) |
| 5 | husbandry Q1-4 | recorded late: [[L-119 Wildlife pack K6 keeping|L-119]] (pack K6, keeping), 19 Nov |
| 5 | water_and_preservation Q1-5 | done in substance: brief 4 stage D (drying, salting), brief 5 ([[D2-209 Brief 5 (river and water) is built|D2-209]]); the proposal's status is stale |
| 5 | 02zo §A and §B decisions | recorded: [[Q-31 Does guard the field become D2-21's watch|Q-31]] (A2), 9 Nov; nothing else from §A or §B traced |
| 5 | Approval to run the cheap ladder | recorded: [[L-50 Calibrate the carrying burden|L-50]] |
| 6 (8 Nov 23:36) | Commit wild_systems.md; History line in node_ecology; rebuild the index | done: 0ff5379 |
| 6 | 02zp part four and the iface files | done: 5beb55d |
| 6 | The node-scale prototype | done: bcdd716 (02zp part five) |
| 6 | Align specs with [[Q-29 scheduler.md and the weather scheduler (D4-109)|Q-29]] and [[Q-30 livestock.md's fence upkeep (D2-130) and D4-114|Q-30]] (offered) | recorded: [[Q-29 scheduler.md and the weather scheduler (D4-109)|Q-29]], [[Q-30 livestock.md's fence upkeep (D2-130) and D4-114|Q-30]] (open since 8 Nov) |
| 6 | Task #21: couple the web to the climate | recorded: [[W-8 Couple the food web to 37.4's weather and climate|W-8]] (paused) |
| 6 | Update the artifact page with the later parts | **vanished**: no later Artifact call |
| 7 (9 Nov 06:26) | Analyse run 2 | done: 767041b |
| 7 | The signs sweep (_wild_traces, eaten, mast, hunt notices, tests, records) | done: 767041b |
| 7 | Waves 3, 4 and 5 | done: 767041b, c9b6259, b32f092 |
| 7 | One more small LLM run | done: runs 3 to 6 |
| 7 | Climate calibration (task 28) | **vanished**: dropped from the lists; "summer too cool" (C9) was never recorded; it came back as [[W-51 The weather across conditions|W-51]] at Zach's request (16 Nov) |
| 7 | The calibration backlog | recorded: [[W-7 The ecology branch's next steps|W-7]]; later [[L-127 The ecology's calibration backlog|L-127]] (19 Nov) |
| 7 | Capacity under a harvest (37.4's) | **vanished** (proposal only): living_populations step 2a, wild_layer §3.3 |
| 7 | Husbandry: sheep, poultry and hounds as beasts | recorded: [[L-36 Livestock kinds beyond cattle and herds moved with the seasons|L-36]] (1 Nov); [[L-119 Wildlife pack K6 keeping|L-119]] (19 Nov) |
| 7 | wild_layer.md History after each milestone | done: 81a2d87 through 4167a61 |
| 8 (9 Nov 15:43) | Share the critic's takes with my own view | done: 15:45 reply |
| 8 | Commit 02zr | done: 0221c22 |
| 8 | Revise wild_behaviour.md | recorded: [[W-4 wild_behaviour.md v3|W-4]] (waits on [[Q-32 02zv §6's decisions still open|Q-32]]) |
| 8 | Whether guard becomes the [[D2-21 The watch|D2-21]] watch | recorded: [[Q-31 Does guard the field become D2-21's watch|Q-31]] |
| 8 | Where [[D2-200 Wild plant kinds replace the single plants stock in worlds with the…|D2-200]] to [[D2-202 The wild kinds and the people draw the same stocks on a village's land|D2-202]] go in the spec | recorded: [[W-5 37.2's own hygiene items|W-5]] (queued since 9 Nov, not begun) |
| 8 | Flag the life model's elder deaths | recorded: [[Q-35 Run findings with no owner yet|Q-35]] (still "to assign") |
| 8 | Flag that the wild layer's nights depend on the seed | **vanished**: said to Zach at 09:14, in no record |
| 9 (9 Nov 23:26) | Finish the [[W-22 Hunting against farming and gathering in generated worlds|W-22]] measurement | done: eb593f0 (02zzd) |
| 9 | Answer the per-unit question | done: 10 Nov 00:15 |
| 9 | Relay 37.4's live-run and brief 3 results | done: 10 Nov 00:15; the carrion findings are in [[Q-38 Brief 3 as built, and its gate|Q-38]] |
| 9 | Side-by-side of live_spring_seed7 against run 6 | **vanished** |
| 9 | Tweak list to 37.4 once Zach confirms | done: became brief 4 (hunt_and_fixes.md, [[W-24 Build brief 4 written (hunt_and_fixes.md)|W-24]]); the "summer too cool" item was lost |
| 9 | Write proposals/wild_encounters.md (animal attacks on people as a fuse event) | **vanished**: last said "not written yet" (9 Nov 22:02) |
| 9 | The forays build brief | recorded: [[L-105 Forays as their own track|L-105]], [[W-12 Forays (proposalsforays.md)|W-12]], [[Q-33 forays.md's open questions|Q-33]] |
| 9 | [[Q-37 Brief 2 as built, and what its gate found|Q-37]] decisions | recorded: [[Q-37 Brief 2 as built, and what its gate found|Q-37]], [[W-21 Proposals for Q-37|W-21]] |
| 9 | 02zv §6 decisions ([[Q-32 02zv §6's decisions still open|Q-32]]) | recorded: [[Q-32 02zv §6's decisions still open|Q-32]] |
| 9 | The 02zz sorting check | recorded: [[W-3 Records restructure|W-3]] (still "active" since 9 Nov) |
| 9 | [[W-5 37.2's own hygiene items|W-5]] | recorded: [[W-5 37.2's own hygiene items|W-5]] |
| 10 (10 Nov 07:58) | Report the trade and children investigation | done: 08:01 |
| 10 | Check whether elders can conceive | done: 08:00 ("you must both be grown adults") |
| 10 | Write up the run against the bot null arm | recorded: [[W-29 A multi-village wild region and its live run|W-29]] "Left" (not done; last touched 10 Nov) |
| 10 | Fix: loans or rentals of goods | recorded: [[W-29 A multi-village wild region and its live run|W-29]] |
| 10 | Fix: hunting odds for the unskilled; how visible parties are | done: brief 4c (hunt_calibration.md); whether parties are visible in the manual was not traced |
| 10 | Fix: Stanmoor's isolation and the charcoal knowledge | **vanished** |
| 10 | Fix: debts of the dead | **vanished** |
| 10 | Fix: Haiku repeating failing actions | **vanished** |
| 10 | Seeder redesign proposal for 37.4 (age structure, partnering) | **vanished** as 37.2's: never written; the ground was covered by other sessions ([[Q-43 Before the second peoples run|Q-43]], [[W-46 Do agents in the runs form new partnerships, pair up when grown, or…|W-46]], generation redesign [[W-38 Generation redesign|W-38]]/[[W-39 The economy's layers and trees of dependence across the domains|W-39]]) |
| 10 | Zach's go on the generator speed fixes (02zzf) | carried |
| 10 | Brief 5's go, and the two test worlds owed | carried |
| 10 | HF upload of the other runs (Fable probes, pair runs, wild_run1-6) | **vanished**: only a standing rule in C11; not uploaded or recorded (logs in the scratchpad) |
| 10 | [[Q-39 Brief 4's open questions|Q-39]], [[Q-40 Brief 4 as built, and its gate|Q-40]], [[Q-41 Brief 4b as built, and its gate|Q-41]] | recorded ([[Q-40 Brief 4 as built, and its gate|Q-40]] and [[Q-41 Brief 4b as built, and its gate|Q-41]] answered 16 Nov) |
| 10 | Run hygiene before ending | done: --record rows of 12, 14 and 16 Nov |
| 11 (15 Nov) | Write the 02zzj README | done: 15 Nov 02:39 |
| 11 | [[W-40 Economy research, hunter-gatherers to the 21st-century urban economy|W-40]] to done; task #41 | done: WORK Done |
| 11 | Report to Zach | done |
| 11 | [[Q-46 Brief 4c as built|Q-46]] | carried ((b) to (d)) |
| 11 | economy_web.md open questions | recorded: [[W-39 The economy's layers and trees of dependence across the domains|W-39]], [[L-111 The hunting and resources build, a soon follow-up|L-111]] |
| 11 | Stage 1 materials brief; kept-beasts brief | recorded: [[L-111 The hunting and resources build, a soon follow-up|L-111]] (16 Nov); [[L-119 Wildlife pack K6 keeping|L-119]] (19 Nov) |
| 11 | Brief 5's go | done: [[D2-209 Brief 5 (river and water) is built|D2-209]] (16 Nov) |
| 11 | The merge questions | done: merged 16 Nov (6190b4d, 7ddc1c8; [[W-6 Merging the wild layer into main|W-6]], [[W-36 Build brief 4c, then the merge of the wild layer|W-36]]) |
| 11 | Generator speed fixes (02zzf) | recorded: only in [[W-29 A multi-village wild region and its live run|W-29]]'s "Left"; dropped from C12; not done |
| 11 | Brief 5's two test worlds | done: [[W-47 Brief 5's worlds and the runs-only world|W-47]], cd41833 |
| 11 | The signs audit | carried |
| 11 | The berries-line repetition fix | carried |
| 11 | Memory and agreements proposal ([[L-106 MAJOR what the engine remembers and settles for agents, and…|L-106]]) | carried (row [[L-106 MAJOR what the engine remembers and settles for agents, and…|L-106]] exists) |
| 11 | Hygiene | carried |
| 12 (16 Nov) | The environment prototype ([[W-49 Environment systems|W-49]], 02zzn) | done: 16 Nov 22:30 |
| 12 | [[Q-52 Environment systems|Q-52]] | recorded: answered 17 Nov ([[D2-221 The land in three speeds|D2-221]] to [[D2-228 Calibrate across a distribution of worlds|D2-228]]); (6) open |
| 12 | [[Q-46 Brief 4c as built|Q-46]] (b)-(d) | recorded: [[Q-46 Brief 4c as built|Q-46]] |
| 12 | Record briefs 4, 4b and 4c as decisions | recorded: [[Q-46 Brief 4c as built|Q-46]] (a) and [[Q-39 Brief 4's open questions|Q-39]], answered 16 Nov "accepted as built"; no DECISIONS rows written |
| 12 | [[Q-47 The border for now|Q-47]], the border | recorded: [[Q-47 The border for now|Q-47]] |
| 12 | The hunting and resources build brief | recorded: [[L-111 The hunting and resources build, a soon follow-up|L-111]] |
| 12 | The waters' fish groups | done: [[D2-229 One fish stock per water body|D2-229]], [[W-56 One fish stock per water body, the engine half|W-56]] |
| 12 | The signs audit | **vanished**: never in OPEN or WORK; 37.4's signs pass of 17 Nov (signs_pass_17nov.md) overlaps in part |
| 12 | The berries-line fix | **vanished**: never recorded, not done |
| 12 | The [[L-106 MAJOR what the engine remembers and settles for agents, and…|L-106]] proposal | recorded: [[L-106 MAJOR what the engine remembers and settles for agents, and…|L-106]] |
| 12 | Respond to 37.4's calibration results | done: [[W-60 The ecology's water measure counted each lake and the large river…|W-60]], 4a0a98f (16 Nov 23:43) |
| 12 | Hygiene | done in part: the last --record row is 16 Nov |

**Counts (each summary's pending list counted on its own, 111 items):** done 51, carried 7, recorded 33, vanished 20 (3 of them
proposal only).

### Next step against what was done right after

All 12 matched. The first action after each compaction was the summary's next step: present 02j; report journeys and
hidden_ways; write 02zc; rerun the validation; tell Zach about 37.4's review; commit wild_systems, part four, then the
prototype (after first finishing the lags revision in the kept messages); rewrite _wild_traces; commit 02zr and give the
takes; the sweep; the trade and children report; the README; the environment prototype. The session moved on only after that
step was done, each time at Zach's next message (after C1 to stone houses, after C2 to which proposals to build, after C3 to
the v1 justification). After C10 it sat idle until 12 Nov.

## The items that vanished

1. C1: extend 02j's costing to the other end uses (food, transport, meeting space, force, information delivery).
2. C2: the household-budget model of the first region.
3. C3: the takeover/1984 gap analysis and who designs institutions and law (an offer never answered; the theme came back later as [[L-74 What Cybertron 2 lacks for a society richer than Cybertron 1's|L-74]]).
4. C3: forests Q4, poles from young growth (proposal only).
5. C4: the board replies from 37.1 and 37.3 (asked, never came, never chased).
6. C4: the quality of the improved descriptions (describe2.log).
7. C5: living_populations questions 1 to 7 and the mechanism (proposal only, its status left stale).
8. C6: updating the ecosystems artifact page.
9. C7: climate calibration (task 28); "summer too cool" was lost from the C9 tweak list too.
10. C7: capacity under a harvest, a regional simulation (37.4's; proposal only).
11. C8: the wild layer's nights fixed by the world seed (same kills on the same nights across runs).
12. C9: the side-by-side of the spring live run against run 6.
13. C9: wild_encounters.md (animal attacks on people as a fuse event).
14. C10: Stanmoor's isolation and the charcoal knowledge gap.
15. C10: debts of the dead.
16. C10: Haiku repeating failing actions.
17. C10: the seeder redesign proposal for 37.4 (others later covered the ground).
18. C10: the HF upload of the earlier runs (Fable probes, pair runs, wild_run1-6).
19. C12: the signs audit (carried twice, never recorded).
20. C12: the berries-line repetition fix (carried twice, never recorded).

## Patterns

- **Each summary rebuilds its pending list from the current segment.** From C1 to C9 no pending item reappears in the next
  summary. Carrying starts only at C10 to C12 (the speed fixes, brief 5, [[Q-46 Brief 4c as built|Q-46]], the signs audit, the berries line, [[L-106 MAJOR what the engine remembers and settles for agents, and…|L-106]]), after
  WORK.md existed. Anything not written to a record before the next compaction was gone from working memory.
- **Long-tail follow-ups vanish most:** secondary checks and small fixes found on the way. Examples: describe2.log, the
  side-by-side, the artifact update, the seed-fixed nights, the Stanmoor, debts and Haiku fixes, the berries line. They are
  never the "current task", so no summary keeps them.
- **Offers waiting on Zach's yes vanish** when he never answers: the takeover gap analysis, extending 02j, the budget model,
  wild_encounters.md. An unanswered offer has no row type, and OPEN.md holds questions, not offers.
- **Cross-session asks with no reply drop out:** the 37.1 and 37.3 board replies, capacity under a harvest for 37.4, the seeder
  proposal for 37.4. [[Q-35 Run findings with no owner yet|Q-35]]'s findings are still "to assign".
- **Questions kept only in a proposal's Open questions are lost to tracking:** forests Q4, living_populations Q1-7, husbandry
  Q1-4 (until the 19 Nov sweep added [[L-117 Wildlife pack K3 forays, methods and knowing|L-117]] to [[L-127 The ecology's calibration backlog|L-127]]). Proposal statuses go stale ("discussion" after the work moved on).
- **Write-ups owed are the most fragile.** Of five owed (the null-arm write-up, wild_encounters, the seeder proposal, the
  takeover gap analysis, the briefs 4 to 4c DECISIONS rows), none is written. The null-arm write-up and the decision rows are
  recorded ([[W-29 A multi-village wild region and its live run|W-29]], [[Q-46 Brief 4c as built|Q-46]]) but stuck.
- **Recorded does not mean moving.** [[W-3 Records restructure|W-3]] is "active" and [[W-5 37.2's own hygiene items|W-5]] "queued" since 9 Nov, [[W-29 A multi-village wild region and its live run|W-29]]'s "Left" is untouched since 10 Nov,
  and [[Q-29 scheduler.md and the weather scheduler (D4-109)|Q-29]] and [[Q-30 livestock.md's fence upkeep (D2-130) and D4-114|Q-30]] have been open since 8 Nov. Recording stops the loss but not the drift.
- **The summaries did not grow steadily.** In total length they run 17k to 32k characters, peaking at C9 (32k, 35 pending
  bullets), then 29k, 26k and 23k. Their pending sections run 0.4k to 2.4k. They replace older items rather than build on them,
  so old items are lost by omission, not crowded out by length. The next step was always kept (12 of 12): the loss is in the
  tail, not the head.
