---
id: docs/review/37_growth/02zzp_audit/replies_2_audit.md
kind: note
updated: "2026-11-19"
---
# Audit of 37.2's replies, 9 to 19 Nov 2026: commitments and switches

*note · `docs/review/37_growth/02zzp_audit/replies_2_audit.md`*


Source: `replies_2.md` (all 355 replies read), Zach's messages in `msgs_b.md` / `msgs_c.md`, `compactions.md` (compactions 7 to 12),
and the repository at `/home/user/cybertron2` (main at a38b1c7; all `origin/*` branches). Checked with `git log --all --grep/-S`,
WORK.md, OPEN.md, DECISIONS.md, proposal Status lines, and `python3 tools/hygiene.py` (run 19 Nov). Read-only: nothing edited.

Outcome key: **done**; **done (late)**; **done after reminder** (Zach had to ask); **by others / superseded**; **recorded, not done**
(a WORK row or OPEN ask/deferred row exists); **dropped** (not done, no record); **unsure**.

## 1. Commitments

| date | commitment (brief quote) | outcome (evidence) | recorded? |
|---|---|---|---|
| 9 Nov 00:30 | "Building that probe is next" (LLM probe of reading signs) | done: 28 runs, a5d9352 (02zp part six) | yes |
| 9 Nov 00:56 | "I'll write up the results when they finish" | done: a5d9352; first run withdrawn fa006c5 | yes |
| 9 Nov 00:56, 01:15 | merged waves "awaiting your confirmation (open question 8)" | superseded by wild_layer.md ([[D2-199 The wild layer is built on 37.2's own ecology branch|D2-199]]); Q8 still in wild_systems.md | in proposal only |
| 9 Nov 03:00 | "I'll finish those [bridge, scope, questions] when the survey reports" | done 03:04 (wild_layer.md) | yes |
| 9 Nov 05:01, 05:24 | climate calibration (long freezes in 40 to 70% of winters) "still has to come before the agent experiment" | **dropped**: never done; agent runs 1 to 6 went ahead; no WORK/OPEN row ever (the 19:48 sorting named it "paused", no row made); 16 Nov 02zzn found the climate too *mild* instead | no |
| 9 Nov 05:24 | "boar don't yet follow the mast; voles don't cycle" | voles: done 09:14 (a phase clock); boar and mast: not done, deferred only on 19 Nov as [[L-127 The ecology's calibration backlog|L-127]] | late (19 Nov) |
| 9 Nov 06:23 | "Next: analyse the second run, then the signs sweep ... then wave 3" | done 07:11 | yes |
| 9 Nov 07:16 | "I can rename the acts ... make the fire watch burn firewood" | done 09:14 | yes |
| 9 Nov 14:23, 14:25 | "the two immediate fixes (no hibernating bears met in winter hunts, and cutting the readings that claim behaviour nothing implements)" | **dropped**: no commit; hibernation still only skips eating (ecology.py:285, from 9d418ff); "the old sow ... she knows the gap and the fields" still in `cybertron2/wild/kinds.py:469` on main; not in compaction 8's summary | no |
| 9 Nov 14:25 | "Re-grade the audit (02zq) honestly ... real behaviour, multiplier only, sign only, missing" | **dropped**: 02zq not regraded (only a date fix in 442174d); wild_behaviour.md took over the topic | no |
| 9 Nov 15:59, 16:21 | drop sign withholding "from the revision"; "Your two principles will also go into the next revision of wild_behaviour.md" | not done: v3 never written | [[W-4 wild_behaviour.md v3|W-4]] "waiting" 10 days (on [[Q-32 02zv §6's decisions still open|Q-32]]) |
| 9 Nov 16:26, 18:25 | commit the critic's finished files and bring summaries | done: ea3b2b1, 89c9b74, 20bf5b5 | yes |
| 9 Nov 18:34 | (a) pointer lines on 02zr to 02zu; mark wild_behaviour v2 superseded; one build brief | done: 442174d | yes |
| 9 Nov 18:46 | "I'll ground every item in code and spec before writing any brief" | done: 02zw, db40459 | yes |
| 9 Nov 19:21, 19:33 | clear my own hygiene items: "[[D2-199 The wild layer is built on 37.2's own ecology branch|D2-199]] to [[D2-203 Each wild kind's behaviour is designed first, then built as a module…|D2-203]] into the spec, the stale scratchpad path in 02zp/sim.py" | **not done**: [[D2-200 Wild plant kinds replace the single plants stock in worlds with the…|D2-200]] to [[D2-203 Each wild kind's behaviour is designed first, then built as a module…|D2-203]] cited in no spec file (hygiene, 19 Nov); sim.py:15 still has the scratchpad path | [[W-5 37.2's own hygiene items|W-5]] "queued, not begun" 10 days |
| 9 Nov 19:57 | the drive's ×2.4: "run the old code with only the key renamed ... I'd ask 37.4 to do that before brief 2 builds on the drive" | not done: build log 02zx:87 still "not explained" | in [[Q-36 Brief 1 as built differs from the brief in 16 places|Q-36]] as unexplained; the test never run |
| 9 Nov 20:36 to 21:23 | Fable probe and paired-probe comparisons | done: 02zza, 02zzb, 02zzc; [[W-17 A Fable 5.2 probe in run 6's world|W-17]] to [[W-20 Paired probes, round 3|W-20]] done | yes |
| 9 Nov 20:53 | "bots need fixing before they're used as the background population" | not done by 37.2 (37.4 added a green-reap setting in brief 2) | [[Q-35 Run findings with no owner yet|Q-35]], "no owner", 10 days |
| 9 Nov 21:57, 22:02 | "shall I write up the animal encounters (`wild_encounters.md`, attacks on people as a fuse event) and send all three to 37.4?"; "aren't written yet" | **dropped**: no file, no row; carried in compaction 9's summary and still dropped | no |
| 9 Nov 22:19 | "I can write the forays brief now" | deferred by Zach (10 Nov) | [[L-105 Forays as their own track|L-105]] |
| 9 Nov 23:21 | "When the sweep finishes I'll set measured hunting ... against these" | done: 02zzd (10 Nov 00:15) | yes |
| 10 Nov 00:35; 07:53 | HF upload of 37.2's own runs (Fable probe, 18 paired probes, wild runs 1 to 6, llm_runs): "If you confirm, I'll stage ..."; "Want those uploaded the same way?" | **dropped**: no answer either time, never raised again; `publish_hf.py` lists only `wild_region_s7`; compaction 10 carried it | no |
| 10 Nov 00:45 | land_kept: "should I write my generator part now" | not done: no land hash/land file in landgen | [[W-25 Keeping each world's full 150 m land with it|W-25]] "waiting" 9 days |
| 10 Nov 02:26, 03:53, 12 Nov, 14 Nov | "I owe it two test worlds" (brief 5) | done (late, 6 days): [[W-47 Brief 5's worlds and the runs-only world|W-47]], `water-worlds` cc6f38d, 16 Nov | yes |
| 10 Nov 02:51 | rats down 21%: "It's in my code, so I'll look into it" | done 03:22 (02zzd addendum) | yes |
| 10 Nov 03:37 | "Should I note [catching and releasing live deer] in the wood-and-frontier brief's plan and the content list (02zv) now?" | **dropped**: Zach moved to hunting parties; no note in 02zv, OPEN or proposals | no |
| 10 Nov 03:59 | "Should I start designing the world and fixing the generator now" | done: 02zze, make_wild_region.py | yes ([[W-29 Writing up the 10 Nov wild-region live run|W-29]]) |
| 10 Nov 05:51 | fix the trade lines, regenerate younger, set the cast | done 06:12 | yes |
| 10 Nov 06:12 | generator speed: fixes "proposed and await Zach's go" (02zzf, b514a8c) | not done, never re-raised | only inside [[W-29 Writing up the 10 Nov wild-region live run|W-29]]'s text |
| 10 Nov 06:12 | the family-tree seeder: "A better design ..." | by others: c2viz session's generation_redesign.md ([[Q-45 The generation redesign|Q-45]]) | yes (not 37.2's) |
| 10 Nov 06:24 | firewood: "I'll check it" in the new run | done 06:26 (14% of acts) | n/a |
| 10 Nov 06:32 | "I'll check whether 'with' appears in the hunting act's description" | **unsure**: no evidence found | no |
| 10 Nov 06:52 | plough lent as a sale: "agents have no way to express renting out capital ... an engine gap worth flagging" | **dropped**: no row in OPEN or engine_gaps; "loan" appears only in 02zze as a question | no |
| 10 Nov 08:01 | fertile-window seeding "That's my mistake"; `ages: true` unset | by others: 37.4's [[Q-43 Fixes before a second peoples run|Q-43]]; later [[Q-60 The water worlds' people, and the runs world for the…|Q-60]] | yes (by 37.4) |
| 12 Nov 21:16 | "the status lines of briefs 1 to 3 still say 'to be built' ... Those files are mine to fix" | **dropped**: all three still "to be built" on main, 19 Nov | no |
| 12 Nov 22:08, 22:13 | [[L-106 MAJOR what the engine remembers and settles for agents, and…|L-106]] (memory and ledger revisit); brief 4c written | done: OPEN [[L-106 MAJOR what the engine remembers and settles for agents, and…|L-106]]; 893f6a1 | yes |
| 13 Nov 17:52 | 4c §7.1: "I check it before the build" (wolves and boar decline) | done 14 Nov 21:51 (8674eff) | yes |
| 13 Nov 18:33 | cats as animals: "Should I add it to 4c?" | folded into the kept-beasts offer (below) | — |
| 13 Nov 18:48 | tallow as food in 4c? | decided otherwise: dropped, [[L-107 Tallow's real uses|L-107]] | yes |
| 14 Nov 21:01 | the signs audit "as a systematic audit" from the journal's ~60,000 unattended changes | not done by 37.2; partly overtaken by 37.4's signs pass of 17 Nov (11 signs, 4c8d720) and 4c §6's own-house signs | no row of 37.2's |
| 14 Nov 21:18, 21:55 | "Should I write it up as a brief for 37.4: herds generalised into kept beasts"; "kept beasts next" | **not done**: no brief; only economy_web.md's open question and, from 19 Nov, [[L-119 Wildlife pack K6 keeping|L-119]] (K6) | late (19 Nov) |
| 14 Nov 21:39, 21:46 | write hunting-worth-learning and the rack into 4c; smokehouse into brief 5 | done: 50a5924 | yes |
| 14 Nov 23:08 | birth windows: "If you want it, I'll add it to 4c as §7.4" | waiting on Zach | [[Q-46 Brief 4c as built|Q-46]] (5 days) |
| 14 Nov 23:44; 16 Nov 19:59, 20:00, 22:05 | "Should I record [briefs 4, 4b, 4c] as built decisions?" (asked four times) | no DECISIONS rows; never answered; no default taken | [[Q-46 Brief 4c as built|Q-46]] (a) |
| 15 Nov 00:04 | rewrite 02zzh around chain shapes? | done: economy_web.md 4e89f29 | yes |
| 15 Nov 02:22 | "I'll go back over the unchecked figures in part 03 and write the overview" | overview done; **figures check dropped**: part 03 has one commit (3426b47) | no |
| 15 Nov 20:19 | "Shall I start the [[L-103 Crafting and discovering new things|L-103]] proposal on that basis?" (discovery as small grids) | **dropped**: Zach asked about Civilization; no proposal; [[L-103 Crafting and discovering new things|L-103]] is only the 9 Nov flag | no |
| 16 Nov 18:43, 19:01 | rebuild Flint to Fab, update the overview, close [[W-44 The missing domains and a linking pass|W-44]] | done 19:04 | yes |
| 16 Nov 18:51 | "When I draft the materials-and-gear brief, I'll put the self bow under wood and cord" | benched by Zach | [[L-111 The hunting and resources build, a soon follow-up|L-111]] |
| 16 Nov 19:01 | the "blade" mismatch into OPEN for 37.4 | done: [[C-11 Weapons specconflictcombat.md and D2-46 name a blade, but…|C-11]] | yes |
| 16 Nov 19:23 | "After that I'll write the waters proposal for discussion" | **done after reminder**: Zach 20:20 "you were gonna do the waters / envrionments proposal?"; environment_systems.md 20:28 | yes |
| 16 Nov 19:27 | "[[W-47 Brief 5's worlds and the runs-only world|W-47]] is my next job: brine springs, two test worlds, then the runs-only world" | done 19:59 | yes |
| 16 Nov 22:19 | the water prototype ("Logging it and starting now") | **done after reminder**: Zach 22:18 "Next u were gonna continue the hidden state etc one?"; 02zzn | yes |
| 16 Nov 22:50 | the flow-level rule ([[D2-218 Set traps in high water|D2-218]], 37.2's): "I'll set it once the weather is fixed" | not done; [[D2-218 Set traps in high water|D2-218]] also in no spec file | [[W-51 Testing the weather across dry, cold, coastal and mountain worlds…|W-51]] "active", untouched since 16 Nov |
| 16 Nov 23:11 | eels as fish: "I'll check it once they report it built" | done 23:16 (reported built) | yes |
| 16 Nov 23:43 | water-measure: "Before it merges, I'll check those species against real densities ... update one replay test" | **not done**: branch `water-measure` 4a0a98f untouched; [[W-62 Merging the water work from its twelve branches into main|W-62]] says it blocks the water merge | [[W-60 Fixing the ecology's water counted twice, then rechecking the…|W-60]] "active", untouched 3 days |
| 17 Nov 00:09 | climate from land, "Generator (mine, about half a day)" | not done; waits on [[Q-56 How the weather should follow each place's climate from the generated…|Q-56]] | [[W-51 Testing the weather across dry, cold, coastal and mountain worlds…|W-51]] |
| 17 Nov 00:55; 04:14 | lake fish constants "left for me to calibrate ... across the test-world suite" | not done | no explicit row ([[D4-120 A lake's fish by its size|D4-120]] calls it calibrate; listed only in the 19 Nov chat) |
| 17 Nov 03:52 | water per village (two-cell cap): "I'll add that to the generator audit ([[W-54 The twelve calibration worlds and an audit of the generator across…|W-54]])" | recorded | [[W-54 The twelve calibration worlds and an audit of the generator across…|W-54]] |
| 17 Nov 04:20 | founders' ages "in one remake after 37.4's branch lands" | done for the runs world 04:49; **unsure** for the river and lake worlds | partly |
| 17 Nov 04:49 | "The river and lake worlds ... still need remaking ... I'll do that next" | done 06:01 | yes |
| 17 Nov 04:53 | the generator's food check counts unreachable food: (19 Nov: "I said on 17 Nov I'd fix it to count only food within a day's work, and haven't") | **dropped**; the 17 Nov text where it was promised is cut off in the extract | no (old [[Q-28 The economy check counts crops that winter will clear|Q-28]] is a different overcount) |
| 17 Nov 04:49 to 06:01 | "I'll record them [[[Q-60 The water worlds' people, and the runs world for the…|Q-60]]'s relayed answers] as decisions once you confirm" (asked four times) | waiting; [[D2-230 Highpool's larder in the runs world|D2-230]], [[D2-231 The runs world's runs on set nights|D2-231]] also in no spec file | [[Q-60 The water worlds' people, and the runs world for the…|Q-60]] |
| 19 Nov 05:06 | "Stale records: ... I'll fix both" | done 05:15 ([[W-6 Merging the wild layer into main|W-6]] to Done; wild_layer.md) | yes |
| 19 Nov 05:15 | catch-up pass on my share (33 decisions into the spec, 7 replaced, 11 WORK rows, triggers) | proposed, not begun | [[W-63 The audit of work started and left, and the triage of open asks and…|W-63]] (the audit) |

## 2. Switches

| date | was doing | switched to | trigger | the set-aside work's fate |
|---|---|---|---|---|
| 9 Nov 02:45 | wave 1 as a standalone system plus the LLM probe | the wild layer in the engine (wild_layer.md) | Zach's critique ("plainly badly undesigned") | superseded; recorded in wild_layer.md |
| 9 Nov 05:12 | phase 0's climate calibration | the general hunting system | Zach asked about killing boar; assistant proposed the order | **lost**: no row ever; agent runs went ahead without it |
| 9 Nov 05:56 | the order hunting → cattle wave 2 → husbandry | an LLM run, then wave 2 | Zach's request | resumed |
| 9 Nov 07:26 | the round of animal layers | plants as parcel stocks ([[D2-200 Wild plant kinds replace the single plants stock in worlds with the…|D2-200]] to 202) | Zach's question on plants | resumed 08:21 |
| 9 Nov 14:25 | two immediate fixes and the 02zq regrade | a behaviour spec per kind, then facets | Zach's challenge; then compaction 8 (15:43) | **lost**: not in compaction 8's summary; no commit, no row |
| 9 Nov 15:16 | wild_behaviour.md v2 | a critic agent, then 02zs to 02zv, then briefs | Zach's request | recorded: [[W-4 wild_behaviour.md v3|W-4]] waits on [[Q-32 02zv §6's decisions still open|Q-32]], 10 days, no default taken |
| 9 Nov 19:12 | the briefs and their test worlds | process analysis, hygiene.py, WORK.md | Zach's request | own hygiene items [[W-5 37.2's own hygiene items|W-5]] "queued, not begun" 10 days |
| 9 Nov 20:36 | reviewing brief 1's gate (the drive's ×2.4) | Fable probes (four rounds) | Zach's request | the check never run; recorded as "unexplained" in [[Q-36 Brief 1 as built differs from the brief in 16 places|Q-36]] |
| 9 Nov 22:21 | animal encounters; shelter and cats proposals | hunting's value | Zach's question | wild_encounters **lost**; shelter_damage and cats "waiting" ([[W-21 Proposals for Q-37|W-21]]), 10 days |
| 10 Nov 00:15 | the hunting measurement | the descendants benchmark | Zach's idea | benchmark deferred ([[L-104 MAJOR the descendants benchmark|L-104]]); hunting resumed as brief 4 |
| 10 Nov 00:35 | brief 4 | the HF upload | a 37.4 message | **lost**: never answered, never recorded |
| 10 Nov 00:41 | brief 4 with forays | a land grid and keeping the land ([[D2-208 The world keeps the land it runs on|D2-208]]) | Zach's route-module idea | forays [[L-105 Forays as their own track|L-105]]; land_kept generator part [[W-25 Keeping each world's full 150 m land with it|W-25]] "waiting" 9 days |
| 10 Nov 03:59 | brief 5's owed test worlds ("I can make those while 37.4 builds 4b") | the four-village region and its live run | Zach's question | resumed 16 Nov (6 days later) |
| 10 Nov 06:12 | launching the run | generator speed (02zzf) | Zach ("why does it take infinite time") | fixes never taken up; no row of their own |
| 10 Nov 07:58 | run analyses (compaction 10) | trading and fertility | Zach's questions | the HF backlog dropped after the compaction carried it |
| 12 Nov 21:16 | status housekeeping (briefs 1 to 3) | snares, memory, the ledger, 4c | Zach's questions | **lost**: status lines still stale |
| 13 to 14 Nov | brief 4c (built by 37.4) | the peoples run's analysis, then the economy map and layers | Zach's questions | kept-beasts brief never written; birth windows in [[Q-46 Brief 4c as built|Q-46]] |
| 15 Nov 02:09 | economy_web's stage 1 design | 13-part research run, Flint to Fab | Zach's request | stage 1 stays discussion; part 03 check **lost** |
| 15 Nov 20:22 | discovery ([[L-103 Crafting and discovering new things|L-103]] proposal offered) | the Civilization comparison, then the border note | Zach's question | **lost**: offer never answered or recorded |
| 16 Nov 19:31 | the waters proposal ("after that I'll write") | brief 5's worlds | Zach "Start on your part now" | resumed only after Zach's reminder at 20:20 |
| 16 Nov 21:46 | the environment consolidation and its prototype | the weir's size, cost and upkeep ([[D2-210 The weir in sections, capped, with upkeep by the river|D2-210]] to 213) | Zach's questions | resumed only after Zach's reminder at 22:18 |
| 16 Nov 23:43 | the climate questions | the water-measure bug (from 37.4), then floodplains, water bodies | a 37.4 bug report, then new bugs | [[W-60 Fixing the ecology's water counted twice, then rechecking the…|W-60]] recalibration "active", untouched since 16 Nov; blocks the water merge |
| 17 Nov 04:21 | the floodplains handover | the runs world for the model-per-household run | 37.4 relaying Zach's answers | food-check fix **lost**; lake fish calibration unrecorded |
| 17 Nov 05:56 | (runs world handed over) | the salt-house bug | a 37.4 bug report | then idle to 19 Nov; [[W-51 Testing the weather across dry, cold, coastal and mountain worlds…|W-51]], [[W-54 The twelve calibration worlds and an audit of the generator across…|W-54]], [[W-60 Fixing the ecology's water counted twice, then rechecking the…|W-60]] untouched |

## 3. Counts

- **Commitments:** 65 rows (a few rows join two linked promises; the owed test worlds counted once).
  - done: 25; done only after Zach's reminder: 2; by others or superseded: 5; decided otherwise or deferred, with a row: 3.
  - recorded but not done: 16 (several only recorded on 19 Nov, or only as an unanswered ask).
  - **dropped, with no record: 12** (counting lake fish calibration, which has no explicit row); unsure: 2.
- **Switches:** 24. Resumed: 6 (2 only on Zach's reminder). Recorded as paused, deferred or waiting: 9. **Lost: 7** (climate
  calibration, the two immediate fixes, wild_encounters, the HF upload, the brief status lines, the part 03 check, the [[L-103 Crafting and discovering new things|L-103]] proposal).
  Two more lost partly (the food-check fix and lake fish calibration in the 17 Nov switch).
- **Triggers:** Zach's new request or question 17 of 24; a 37.4 message or bug report 4; bugs found mid-task 2; a compaction 1
  clearly (8, 9 Nov 15:43), and 2 more where an item was carried through a compaction summary and dropped anyway.
- **Records:** hygiene, 19 Nov: unfinished 31 in progress, 9 paused, 50 asks, 88 deferred, 176 chores (9 Nov: 6, 11, 30, 62, 122).
  `--record` last run 16 Nov. 37.2's [[D2-200 Wild plant kinds replace the single plants stock in worlds with the…|D2-200]] to [[D2-203 Each wild kind's behaviour is designed first, then built as a module…|D2-203]], [[D2-207 The three wild build briefs are built|D2-207]], [[D2-218 Set traps in high water|D2-218]], [[D2-230 Highpool's larder in the runs world|D2-230]] and [[D2-231 The runs world's runs on set nights|D2-231]] are cited in no spec file.

## 4. Patterns

1. **The latest question wins.** 17 of 24 switches came from a new question of Zach's. The assistant answers it fully and leaves its
   own stated "next" behind. Offers ending in "Shall I ...?" that Zach did not answer were never raised again: wild_encounters (asked
   twice), the HF upload (twice), the deer note, [[L-103 Crafting and discovering new things|L-103]], the kept-beasts brief.
2. **Bugs found mid-task chain into each other.** 16 to 17 Nov: prototype → floodplain bug → weather across conditions → lake-by-a-pond
   bug → water counted twice (37.4) → one-parcel fix (reverted) → water bodies → runs world → missing livestock → missing brine pan.
   Each was fixed and "handed over", and the checks owed on the earlier ones ([[W-60 Fixing the ecology's water counted twice, then rechecking the…|W-60]], lake fish, the food check) fell away.
3. **Messages from 37.4 open new work** (HF upload, water-measure, relayed answers for the runs world, the salt pan). Answers relayed by
   37.4 cannot be recorded as decisions, so they pile up as asks ([[Q-46 Brief 4c as built|Q-46]], [[Q-60 The water worlds' people, and the runs world for the…|Q-60]]) that the assistant re-asks 3 to 4 times instead of
   taking a stated default, which CLAUDE.md allows.
4. **Compactions are not the main leak.** Only the two immediate fixes clearly vanished at a compaction (8). wild_encounters and the HF
   upload were in the summaries (9, 10) and were dropped anyway. The leak is in what gets picked back up, not in memory.
5. **What gets lost:** small owed write-ups (wild_encounters, the deer note, [[L-103 Crafting and discovering new things|L-103]], the kept-beasts brief); checks and calibrations
   (climate, the drive's ×2.4, part 03's figures, [[W-60 Fixing the ecology's water counted twice, then rechecking the…|W-60]], lake fish, the food check); record upkeep (brief status lines, [[D2-200 Wild plant kinds replace the single plants stock in worlds with the…|D2-200]] to 203
   into the spec, the sim.py path); publishing (the HF runs). Building and research almost never get lost; upkeep and verification do.
6. **Zach has to catch the drops.** 16 Nov 20:20 ("you were gonna do the waters / envrionments proposal?"), 22:06 ("Did you write up the
   weir and hand over ...?"), 22:18 ("Next u were gonna continue the hidden state etc one?"), 17 Nov 05:04 ("Did u do it?").
7. **Status claims run ahead of the records.**
   - 9 Nov 08:21: "every specced layer the engine can support", withdrawn 14:20 as perception only.
   - 10 Nov 01:06: "shelter_damage.md and cats.md are marked as being built". Only a History line was added (9f26f7c); both Status
     lines still read "discussion (9 Nov). Nothing decided or built".
   - 16 Nov 19:59: "My part of brief 5 is done". Then came four generator faults in those worlds: the trench, the pond, two water
     parcels, the missing pan.
   - 17 Nov 04:49: "Every check passes". The world had no livestock (04:53) and no brine pan (05:56).
   - 19 Nov 05:06: "wildlife: built and on main". Nine of the 13 packs had never been briefed, six had no row anywhere, and the claim
     was withdrawn at 05:13.
8. **Rows that exist go stale.**
   - [[W-2 Build briefs 2 and 3, the 20 dry test arms, the spring live run|W-2]], [[W-27 Build brief 4|W-27]] and [[W-30 Build brief 4b|W-30]] are still "active" or "waiting", though those briefs were built and merged on 16 Nov.
   - [[W-22 Hunting against farming and gathering in generated worlds|W-22]] and [[W-29 Writing up the 10 Nov wild-region live run|W-29]] are "waiting", though the work is done.
   - [[W-3 Records restructure|W-3]] has been "active" since 9 Nov.
   - The tracking system built on 9 Nov was kept up for new rows, not for closing them.
9. **Long research tangents displace the build queue.** From 14 to 16 Nov, the economy research (18 parts, Flint to Fab, the border
   note) ran while these waited: 4c's records, the kept-beasts brief, birth windows, the hunting and materials brief (later
   benched), and [[W-5 37.2's own hygiene items|W-5]].
10. **"Waiting on Zach" goes unanswered.** Asks grew from 30 to 50. Rows have waited 9 to 10 days ([[W-4 wild_behaviour.md v3|W-4]], [[W-21 Proposals for Q-37|W-21]], [[W-25 Keeping each world's full 150 m land with it|W-25]], [[Q-32 02zv §6's decisions still open|Q-32]], [[Q-35 Run findings with no owner yet|Q-35]]) with no
    default taken and no re-raise, except when Zach asked for a list (16 Nov 23:47).
