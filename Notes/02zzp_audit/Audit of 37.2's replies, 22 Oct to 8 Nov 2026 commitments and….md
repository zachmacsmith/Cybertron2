---
id: docs/review/37_growth/02zzp_audit/replies_1_audit.md
kind: note
updated: "2026-11-19"
---
# Audit of 37.2's replies, 22 Oct to 8 Nov 2026: commitments and switches

*note · `docs/review/37_growth/02zzp_audit/replies_1_audit.md`*


Source: `replies_1.md` (314 replies), with Zach's messages (`msgs_a.md`, `msgs_b.md`) for what each reply answered. Evidence checked
in `/home/user/cybertron2` (all branches), `docs/cybertron2/OPEN.md`, `WORK.md`, `DECISIONS.md`, the proposals, `docs/review/37_growth/`,
and the coordination board (last copy in git history). Read-only. Notes on method: WORK.md did not exist until 9 Nov (93fbe74), so for
this period "recorded" means an OPEN row, a proposal's status or a session note. "Late" means done only after Zach asked again, or
more than a week later. Where I could not be sure, the row says so.

Outcome key: **done** · **done late** · **recorded, not done** (a row exists, work still open on 19 Nov) · **dropped** (neither done
nor recorded when it was left) · **superseded**.

## 1. Commitments

| # | date | commitment (brief quote) | outcome (evidence) | recorded? |
|---|---|---|---|---|
| 1 | 22 Oct 17:18 | Post 1 reply: "I'll draft it here with you first and post it only once you approve" | superseded: board row said "replies to Post 1 pending" (21:10); answered indirectly 23 Oct 00:50 by agreeing to [[D4-23 Holding is a recognised claim|D4-23]] (holding.md) | board |
| 2 | 22 Oct 20:08 | game inflow "a porting bug I introduced" | done: 77e7f2d ("run-1 fixes (game inflow, partial meals...)") | n/a |
| 3 | 22 Oct 20:13 | "You told Hal" cut at 80 chars: "I'll fix that with the next round" | done: 77e7f2d removes the `[:80]` | n/a |
| 4 | 22 Oct 21:00 | "I'll move cybertron2 to its own branch" | done: `wp/cybertron2` | n/a |
| 5 | 22 Oct 21:03 | run 2: "When it finishes I'll commit the logs" | done: 4e359b1, `38_space_engine/03_hills_run.md` | n/a |
| 6 | 22 Oct 21:09 | space runs to Hugging Face, own folder | handed over: no token; f9ce953 stages `experimental/cybertron2`; task posted to 37.4 (board 21:55). 02zl (2 Nov) found a partial Hub copy | board |
| 7 | 22 Oct 21:16 | stale docs, incl. CLAUDE.md not naming cybertron2 | done: CLAUDE.md section 23 Oct 00:20 | n/a |
| 8 | 22 Oct 21:34 | "Agreed on coin, debt and seeding merchants. I'll record those." | done: 02g, 21:36 | n/a |
| 9 | 22 Oct 21:53 | travel/combat preferences "as proposals for 37.4 ... a pointer on the board" | done: 02g §2c, §3c, §5b; board | n/a |
| 10 | 22 Oct 23:03 | "I'm adding a pruning rule" | done: 02j | n/a |
| 11 | 23 Oct (board 00:50) | "I will rescale 02l to [[[D4-23 Holding is a recognised claim|D4-23]]'s plot]" | probably superseded by [[D2-59 The plot's numbers|D2-59]] (1c5578e); 02l itself never revised after 1bb4f3f. **Unsure** | no |
| 12 | 23 Oct 00:18 | 14 helper-drafted proposals: "I haven't read all 14 line by line" (a check owed) | done late: the 5 Nov sweep (ca51032) found 34 of 92 proposals stale and 37 missing from the index | no (until 5 Nov) |
| 13 | 23 Oct 04:34 | staleness check as a script: "Want me to add it?" | unanswered; done late as `tools/hygiene.py` (a8e7850, 9 Nov) after Zach's 9 Nov ask | no |
| 14 | 23 Oct 06:43 | "I'll bring their results together and come back with recommended numbers" | done: 06:50 (02n, 02o, 02p) | n/a |
| 15 | 23 Oct 07:27 | "If you agree, I'll add this to the mill ladder in the recipes proposal" | done: [[D2-60 The food ladder|D2-60]] to [[D2-62 Dried meat|D2-62]], recipes.md §16 | n/a |
| 16 | 23 Oct 08:41 | herds on edges: "I'll raise both on the board when you want this built" | done: [[D2-123 Herds wander on the node|D2-123]] to [[D2-125 searching is a travel modifier known to all|D2-125]], built (OPEN [[L-8 Herds wandering onto edges|L-8]] done) | [[L-8 Herds wandering onto edges|L-8]] |
| 17 | 23 Oct 20:15 | "Nothing yet sets each day's weather inside a spell. I'll spec that" | done: [[D2-99 Visibility per place and sense|D2-99]], scheduler.md | n/a |
| 18 | 23 Oct 23:51 | pack ox: "I'll write it as spec and add it to 37.4's queue after Package C" | done: built by 37.4 (24 Oct 00:04) | n/a |
| 19 | 24 Oct 00:27 | "I can write the children spec for 37.4" | done: Package D (38.27) | n/a |
| 20 | 24 Oct 05:00 | "Should I re-run the transport check on region_c1?" (two winters double the fuel to carry) | **dropped**: unanswered, never run, no row. 38.26 (region_c1 r1, same day): 17 of 58 died, 12 "with food in reach and no fire", limited by carrying, the failure the check predicted | no |
| 21 | 24 Oct 05:08 | fitting-work bug: "I haven't reported it yet"; 05:26 "left unfixed for now" | done late: still "unfixed" on 1 Nov 19:14; fixed ab971ff (1 Nov, brief 02zg). Never an OPEN row | no |
| 22 | 24 Oct 05:26 | buildings-integration questions before Package E | done: buildings_integration.md "mostly settled"; building package 02zh built 1 to 3 Nov | proposal |
| 23 | 24 Oct 06:13, 06:22 | takeover/1984 benchmark: "should I write the gap analysis and plan ... ?" ("still waiting on you") | **dropped**: no answer, 5-day gap, never written; resurfaced only as [[L-74 What Cybertron 2 lacks for a society richer than Cybertron 1's|L-74]] (flagged 9 Nov from an 8 Nov conversation, owner 37.4) | no (until 9 Nov, indirectly) |
| 24 | 29 Oct 17:26 | "Once it reports back, I'll write the per-system overview" | done: 02zc (0362a07) | n/a |
| 25 | 29 Oct 18:20 | "I can correct [\"24 times\"] in both" | done: c185154 (02zc line 345) | n/a |
| 26 | 29 Oct 18:27 | (Zach) note fertility rates for the future; more modelling | done: [[L-27 Replacement and fertility rates over lifespans against how often…|L-27]], 02ze, proposals/fertility.md | [[L-27 Replacement and fertility rates over lifespans against how often…|L-27]] |
| 27 | 29 Oct 18:33-18:39 | fertility questions (scaling, vulnerable young, "youth", cost) | recorded, not answered: fertility.md "soft limits open", [[L-27 Replacement and fertility rates over lifespans against how often…|L-27]] | proposal, [[L-27 Replacement and fertility rates over lifespans against how often…|L-27]] |
| 28 | 29 Oct 19:07 | "I won't send anything to 37.4 to build ... until you ask in so many words" | done: README rule 10 (19:48); kept on 1 Nov 21:36 | README |
| 29 | 1 Nov 00:21 | customs: "I can turn the flag into a full proposal" | **dropped** offer: no answer, not written; beliefs_and_values.md still "flagged for later (24 Oct)" | [[L-25 Beliefs, values and customs|L-25]] (area only) |
| 30 | 1 Nov 19:45 | towns flagged | done: [[L-33 Growth to towns fixed nodes, faster edges, reach by place|L-33]] | [[L-33 Growth to towns fixed nodes, faster edges, reach by place|L-33]] |
| 31 | 1 Nov 21:07 | "Once you answer the three, I'll record them, update the specs and send them" | mostly done: [[D4-84 A camp keeps little|D4-84]] to [[D4-86 Beds (D2-165), the defaults confirmed|D4-86]] in buildings.md and lodging.md (3 Nov); spoilage by fitting capacity still open as [[Q-24 Built for the building package|Q-24]] (6); [[Q-24a Q-24 settled in part by Zach|Q-24a]] never closed though done | [[Q-24 Built for the building package|Q-24]], [[Q-24a Q-24 settled in part by Zach|Q-24a]] |
| 32 | 1 Nov 21:36 | camp store limit (10 weight) | done: [[D2-176 (Replaced by D4-84.)|D2-176]], [[D4-84 A camp keeps little|D4-84]], spec | n/a |
| 33 | 1 Nov 21:45 | "I'll add this [places split on use] to generator.md §7" | done: generator.md §8a (outlined, deferred) | proposal |
| 34 | 1 Nov 21:49 | [[D4-83 A fire under no roof in the night's weather|D4-83]] into lodging/goods: "I haven't done that yet ... Say if you want them updated" | **recorded, not done**: [[L-32 D4-83 (a fire under no roof in the night's weather|L-32]] open; WORK [[W-10 37.2's spec write-ups owed since 2 and 3 Nov|W-10]] "not begun" | [[L-32 D4-83 (a fire under no roof in the night's weather|L-32]], [[W-10 37.2's spec write-ups owed since 2 and 3 Nov|W-10]] |
| 35 | 1 Nov 22:19 | "Build stage 1, then generate a world and run it on today's engine" | part: bot dry run 3 Nov (02zn); no LLM run of a generated world in this period; cheap ladder waits ([[L-50 Calibrate the carrying burden|L-50]]) | [[L-50 Calibrate the carrying burden|L-50]] |
| 36 | 1 Nov 22:19 | stage 2 "needs numbers ... a small calibration model" before it is specced | not done; never a row of its own; pieces later in [[L-71 The land's fast stocks|L-71]] (fast stocks), [[W-49 Environment systems|W-49]] (16 Nov). Partly superseded | partly |
| 37 | 1 to 2 Nov | spec for [[D2-173 The generator fills in around what a world file gives|D2-173]] to [[D2-191 The generator designs within one envelope|D2-191]] (generator decisions), required by CLAUDE.md step 3 | **recorded, not done**: [[L-101 Compile the generator into specworldgeneration.md|L-101]] (flagged 5 Nov), [[W-9 Compile the generator into specworldgeneration.md|W-9]] "not begun beyond the flag; [[D2-173 The generator fills in around what a world file gives|D2-173]] to [[D2-191 The generator designs within one envelope|D2-191]] are in no spec file" | [[L-101 Compile the generator into specworldgeneration.md|L-101]], [[W-9 Compile the generator into specworldgeneration.md|W-9]] |
| 38 | 2 Nov 19:37 | stage-1 leftovers "already deferred (supply-chain checks, the sampling mesh, ... kin between villages)" | partly true: supply chains are [[L-49 Automated supply-chain and dependence checks for generated worlds|L-49]]; mesh, fine detail and kin are only in the 02zj build note, not OPEN | session note |
| 39 | 2 Nov 19:31 | flag the carrying-burden measure; transport later | done: [[L-52 The carrying burden is an incomplete measure|L-52]], [[L-53 Transport and traders, built out|L-53]] | [[L-52 The carrying burden is an incomplete measure|L-52]], [[L-53 Transport and traders, built out|L-53]] |
| 40 | 2 Nov 19:51 | [[L-61 D4-97's parts in 37.2's files|L-61]] ([[D4-97 Decisions on 38.51's list|D4-97]] into production, buildings, lodging): "I'll make those edits after we settle the forest question" | **recorded, not done**: [[L-61 D4-97's parts in 37.2's files|L-61]] open; no [[D4-97 Decisions on 38.51's list|D4-97]] in spec/economy; [[W-10 37.2's spec write-ups owed since 2 and 3 Nov|W-10]] "not begun" | [[L-61 D4-97's parts in 37.2's files|L-61]], [[W-10 37.2's spec write-ups owed since 2 and 3 Nov|W-10]] |
| 41 | 2 Nov 21:13 | cheap ladder, 3 runs ($75 to $90), "still waiting on you" | recorded, waiting on Zach; never run | [[L-50 Calibrate the carrying burden|L-50]] |
| 42 | 3 Nov 04:14, 20:30 | varied landscapes: "whether to write up or build the varied-landscapes plan" | **mostly dropped**: never answered or written up; only a line in 02zo §B (5 Nov). Floodplains done much later ([[D2-226 Floodplains in the generator, now|D2-226]], [[W-53 Floodplains in the generator now|W-53]], 17 Nov); ponds as parcel features and wood share by world not done, no OPEN row | 02zo only |
| 43 | 4 Nov | water ecosystems: "Shall I write that proposal now?" | done late: "slipped behind the sweep"; written only when Zach asked (7 Nov, water_and_preservation.md); its Q1 to Q5 never in OPEN (later partly answered via brief 5) | no |
| 44 | 4 Nov 18:34 | make rot visible ("it will rot in about 3 days") before the next runs | in the 5 Nov ranking (item 4, 37.4's lane); whether built not found. **Unsure** | 02zo ranking |
| 45 | 5 Nov 05:06 | sweep, index, open-decisions list, message 37.4, re-rank | done: ca51032, 02zo | n/a |
| 46 | 8 Nov 02:41 | retest the cut kinds; rebuild the generator on absolute physics | done: b4fb26c; ba0f2da | n/a |
| 47 | 8 Nov 03:14 | interim patches kept as a patch file, tree reverted | done: generator_interim.patch | n/a |
| 48 | 8 Nov 03:15 | plan: hook, generator, "calibrate the climate on generated worlds against real British climate figures", couple the web | part: hook ([[D4-113 Renewal rules are handed the weather where the stock is|D4-113]]) and generator done; climate calibration never done; coupling [[W-8 Couple the food web to 37.4's weather and climate|W-8]] "paused" (9 Nov) | [[W-8 Couple the food web to 37.4's weather and climate|W-8]] (from 9 Nov) |
| 49 | 8 Nov 03:52 | "I'll carry on ... fix bears and outbreaks, calibrate the climate on the branch, run the eras" | part: bears done; outbreaks and eras went to 02zp §16 backlog when the assistant recommended consolidating (04:09); backlog became OPEN only on 19 Nov ([[L-127 The ecology's calibration backlog|L-127]]) | late ([[L-127 The ecology's calibration backlog|L-127]], 19 Nov) |
| 50 | 8 Nov 04:31 | [[Q-29 scheduler.md and the weather scheduler (D4-109)|Q-29]], [[Q-30 livestock.md's fence upkeep (D2-130) and D4-114|Q-30]] spec fixes: "Shall I do them now?" | **recorded, not done**: Zach asked another question; both rows open 19 Nov; scheduler.md and visibility.md still describe region-wide weather | [[Q-29 scheduler.md and the weather scheduler (D4-109)|Q-29]], [[Q-30 livestock.md's fence upkeep (D2-130) and D4-114|Q-30]] |
| 51 | 8 Nov 04:30 | 02zp §17's five decisions for Zach | superseded the same day by part three (node first); never an OPEN row | no |
| 52 | 8 Nov 23:27 | "When the research returns I'll write the full design" | done: wild_systems.md (0ff5379, 23:39) | proposal |

## 2. Switches

| # | date | was doing | switched to | trigger | the set-aside work's fate |
|---|---|---|---|---|---|
| S1 | 22 Oct 19:47 | economy design (02a to 02e) | building cybertron2 phase 0 and two LLM runs | Zach's idea of a new engine | resumed: handed to 37.4 (Post 3), back on the economy 21:22; worklog records it |
| S2 | 22 Oct 20:44 | perception design | implementing it in cybertron2, run 2 | Zach | completed; then handed over |
| S3 | 23 Oct 07:56 | economy: ditches, terraces, camps ([[D2-66 Field works in the first worlds, before weather exists|D2-66]] to [[D2-68 Camps and portable shelter|D2-68]]) | the environment scheduler and catalogue | Zach: take over 37.4's environment work | economy items posted to 37.4 as ready to build; built later |
| S4 | 23 Oct 08:20 | children review | hidden variables of the land | Zach ("we'll come back to this") | resumed 24 Oct at Zach's ask; Package D built; [[L-12 Children and life (we'll come back to this)|L-12]] |
| S5 | 24 Oct 05:04 | region world, children | buildings, then Package E | Zach | E deferred at his word, recorded; rebuilt as 02zh on 1 Nov |
| S6 | 24 Oct 05:27 | buildings integration | forests, fuel, warmth (Package F) | Zach | F built; integration questions kept in a proposal, revisited 1 Nov |
| S7 | 24 Oct 05:00 to 06:11 | region_c1 transport re-check offered | buildings, forests, then the takeover benchmark | Zach's new questions | **lost**: the re-check never ran (C20); the run failed as predicted (38.26) |
| S8 | 24 Oct 06:11 to 29 Oct | takeover/1984 benchmark gap analysis offered | (session pause), then the systems overview and v2 justification | session gap, then Zach's new requests | **lost** (C23); surfaced as [[L-74 What Cybertron 2 lacks for a society richer than Cybertron 1's|L-74]] only on 9 Nov |
| S9 | 1 Nov 19:11 to 20:27 | buildings and land | space levels, towns, building types, then the generator | Zach | towns flagged [[L-33 Growth to towns fixed nodes, faster edges, reach by place|L-33]]; building package and plot shares sent and built |
| S10 | 1 Nov 23:14 | speccing the generator | building it itself, merging into 37.4's branch | Zach | done (98bdc3f); cross-village kin left to 37.4, recorded only in 02zj |
| S11 | 2 Nov 19:39 to 20:11 | stage 1 finished; stage 2 and the cheap ladder next | forest kinds, ecosystems, a planet, temperate landscapes (built) | Zach's questions | stage 2 never specced (C36); cheap ladder waits ([[L-50 Calibrate the carrying burden|L-50]]); temperate landscapes built |
| S12 | 3 Nov 04:12 | gate check and fixes | varied-landscapes plan, after Zach's critique of over-fitting | Zach | **mostly lost**: never written up (C42) |
| S13 | 3 Nov 20:30 | (idle) | replying to Zach's question relayed by 37.4 | cross-session message | done; the assistant answered for itself without Zach in the loop |
| S14 | 4 Nov 18:21 to 5 Nov | water ecosystems, fishing, smoking | "best next things", then the proposals sweep | Zach | **lost until Zach asked** (7 Nov): proposal written late (C43) |
| S15 | 7 Nov 23:41 to 8 Nov 06:30 | water and preservation questions (Q1 to Q5) | living populations, wildlife, then a deep dive on regional food webs | Zach | water questions not in OPEN; the deep dive ran at a scale villages cannot touch (admitted 06:31, 06:34) |
| S16 | 8 Nov 02:41 to 03:13 | generator rebuild | weather and climate | Zach's interrupt ("did you see the new weather?"), then 37.4's message | rebuild resumed and done on `climate-calibration` (b4fb26c), merged |
| S17 | 8 Nov 03:52 to 04:09 | calibrating the climate against real statistics; eras through the web | consolidation (02zp part two) | the assistant's own recommendation, Zach "yeah" | climate calibration **lost** (no row); eras and outbreaks to the 02zp backlog, OPEN [[L-127 The ecology's calibration backlog|L-127]] only on 19 Nov; [[W-8 Couple the food web to 37.4's weather and climate|W-8]] paused |
| S18 | 8 Nov 04:31 | [[Q-29 scheduler.md and the weather scheduler (D4-109)|Q-29]]/[[Q-30 livestock.md's fence upkeep (D2-130) and D4-114|Q-30]] spec fixes offered | "do the ecosystems have relevant relationships ...?" | Zach's new question | recorded (by 37.4), never done |
| S19 | 8 Nov 06:34 to 23:39 | 02zp §17 decisions | node-first model, interface experiments, wild_systems.md | Zach's critique | §17 superseded; the new design written (0ff5379) |

## 3. Counts

- **Commitments: 52.** Done 29 (including 2 handed over or superseded on record). Done late 4 (C12, C13, C21, C43). Recorded but
  still not done on 19 Nov 10 (C27, C31 part, C34, C35, C37, C40, C41, C48, C49, C50). Dropped, neither done nor recorded when left: 4
  clear (C20, C23, C29, C42). Partial or unsure 4 (C11, C36, C38, C44). Superseded 1 (C51).
- **Offers left with no answer from Zach: 7** (C13, C20, C23, C29, C42, C43, C50). Of these, 2 were done later, both only after
  Zach raised the matter again (C13 on 9 Nov, C43 on 7 Nov), and 5 were never done.
- **Switches: 19.** Resumed or completed 12. Recorded as deferred or paused 2 (S5, S18). Lost or lost until Zach asked 5 (S7, S8, S12,
  S14, S17).
- **Triggers of the 19:** a new request or question from Zach 14; a cross-session message from 37.4 3 (S13, S16, part of S18); the
  assistant's own recommendation 1 (S17); a session gap 1 (S8). No reply in this window was cut by a compaction mid-commitment that I
  could find. Compactions (23 Oct 09:13, 29 Oct, 2 Nov, 8 Nov) fall at points where the open offers had already been left.

## 4. Patterns

1. **Offers at the end of a reply die when the next message changes topic.** "Should I re-run the transport check on region_c1?",
   "should I write the gap analysis ...?", "I can turn the flag into a full proposal", "write up or build the varied-landscapes plan",
   "Shall I do them now?" ([[Q-29 scheduler.md and the weather scheduler (D4-109)|Q-29]]/30): each went unanswered because Zach's next message was a new question, and none became an OPEN ask.
   The CLAUDE.md rule (an ask goes in OPEN) did not exist yet, but OPEN's asks table did.
2. **Spec write-ups of decisions are the most lost kind of work.** [[D2-173 The generator fills in around what a world file gives|D2-173]] to [[D2-191 The generator designs within one envelope|D2-191]] (19 generator decisions, 1 to 2 Nov) are in no
   spec file ([[L-101 Compile the generator into specworldgeneration.md|L-101]], [[W-9 Compile the generator into specworldgeneration.md|W-9]] "not begun"); [[D4-83 A fire under no roof in the night's weather|D4-83]], [[D4-93 One room, one fire|D4-93]], [[D4-94 Acts made to work as they read|D4-94]], [[D4-97 Decisions on 38.51's list|D4-97]] owed to 37.2's economy specs ([[L-32 D4-83 (a fire under no roof in the night's weather|L-32]], [[L-44 D4-93 (one room, one fire|L-44]], [[L-45 D4-94's parts in 37.2's files|L-45]], [[L-61 D4-97's parts in 37.2's files|L-61]], "not begun");
   [[Q-29 scheduler.md and the weather scheduler (D4-109)|Q-29]] and [[Q-30 livestock.md's fence upkeep (D2-130) and D4-114|Q-30]]. The assistant twice said it would do these "after" something else (2 Nov 19:51; 1 Nov 21:49). Each "after" came, and
   the next design topic replaced it.
3. **37.4's messages land in the middle of other work and leave chores that the assistant accepts but does not do.** The camp limit
   got done because Zach and 37.4 settled it; [[L-61 D4-97's parts in 37.2's files|L-61]], [[D4-83 A fire under no roof in the night's weather|D4-83]] and [[Q-29 scheduler.md and the weather scheduler (D4-109)|Q-29]]/30 were accepted ("I'll make those edits") and left.
4. **Follow-up checks on runs are the costliest loss.** The region_c1 transport re-check named the failure in advance ("the cause would
   be the 38.23 one again"); the run that day lost 17 of 58 to fuel that could not be carried.
5. **Long research tangents move from the purpose.** The 8 Nov deep dive (seven models, 144 villages, four rounds) was at regional and
   decade scale; the assistant admitted "most of the ecosystem work was designed at a scale the AI society can't touch" (06:31) and,
   later, "I didn't build an interface, and I should be plain about that" (22:46). The climate calibration it promised that morning
   was dropped when it recommended consolidating instead.
6. **Bugs found in passing are named but not tracked.** The fitting-work bug (24 Oct) was reported in chat three times ("I haven't
   reported it yet", "left unfixed", "still unfixed") and never given an OPEN row; it was fixed 8 days later only because a brief for
   another purpose took it in.
7. **"Ready" and "done" were said before they were true, then walked back when asked.** "Yes, stage 1 is ready to build" (1 Nov
   22:19), then "More than I implied when I called it ready" (22:23); "Is all of stage 1 finished?" "No." (2 Nov). On 3 Nov: "I tuned
   toward the reported symptoms with blunt rules and made the checks pass". On 2 Nov the stage-1 leftovers were called "already
   deferred", though three of them were only in a build note.
8. **Records decayed between sweeps, and the assistant found it only when asked.** By 5 Nov 34 of 92 proposals were stale and the
   index missed 37 ("partly my fault"); the helper-drafted proposals of 23 Oct were never read line by line; [[Q-24a Q-24 settled in part by Zach|Q-24a]] stayed open after
   its work was done. Closed work is not always closed in the records, and open work not always opened.
9. **The assistant's reading of a "yes" overreached once and then swung to caution.** It took "yes, write it up" as approval to send
   fertility values to 37.4 to build (29 Oct); after rule 10 it held even a small fix (the camp limit) until told.
10. **Claims checked against the records were mostly accurate.** Things said to be flagged were flagged ([[L-14 Clothing|L-14]] clothing, [[L-33 Growth to towns fixed nodes, faster edges, reach by place|L-33]] towns,
    [[L-52 The carrying burden is an incomplete measure|L-52]], [[L-53 Transport and traders, built out|L-53]], [[L-27 Replacement and fertility rates over lifespans against how often…|L-27]]); what the assistant said it had written into spec ([[D4-84 A camp keeps little|D4-84]] to [[D4-86 Beds (D2-165), the defaults confirmed|D4-86]]) is there. The gaps are in what it said it
    *would* do, not in what it said it *had* done. One mis-statement: commit 66702b9's message described work it did not hold
    (admitted 23 Oct 03:00).
