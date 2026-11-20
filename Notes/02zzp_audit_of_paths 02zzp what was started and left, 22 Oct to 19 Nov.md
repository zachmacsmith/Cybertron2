---
id: docs/review/37_growth/02zzp_audit_of_paths.md
kind: note
updated: "2026-11-19"
tags: [note, open]
---
# 02zzp: what was started and left, 22 Oct to 19 Nov, and how to notice it sooner

## Text
# 02zzp: what was started and left, 22 Oct to 19 Nov, and how to notice it sooner

37.2, 19 Nov 2026. WORK [[W-63 An audit of what was started and left (Zach, 19 Nov what differen|W-63]]. Zach: "what different paths of building things have we gone down and then ended up doing something
else, and how much of this has been documented vs missed entirely? What sorts of mechanisms would help us better notice what is
being missed so I have a better sense of always what has been partially worked on and how much progress and you do too"; "look at
patterns ... Can you also look through your transcript as well."

**How it was done.** Seven read-only audits, each against the repository's full history (1,800 commits on main from 4 Oct, every
branch) and the records (WORK, OPEN, DECISIONS, proposals, spec, session notes, the board):
- three audits of Zach's 629 messages, one period each, each request followed to what happened and its record;
- two audits of 37.2's 669 replies, for commitments ("next I'll", "left", offers) and for switches (work set aside for something else);
- one audit of the 12 context compactions: each summary's pending list followed forward;
- one audit of the records against the repository.

The tables are in `02zzp_audit/` (period_a, period_b, period_c, replies_1_audit, replies_2_audit, compactions_audit, records). The
audits overlap: the same item is often found by two or three of them, and the counts below are each audit's own, not deduplicated.

## 1. The counts

**Zach's requests (176 initiatives):**

| Class | 22 Oct to 3 Nov | 4 to 11 Nov | 12 to 19 Nov | All |
|---|---|---|---|---|
| done, recorded | 29 | 20 | 25 | 74 |
| partial, recorded | 12 | 17 | 25 | 54 |
| partial, unrecorded | 10 | 5 | 3 | 18 |
| redirected | 3 | 4 | 3 | 10 |
| dropped silently | 1 | 3 | 2 | 6 |
| stale record | 3 | 9 | 2 | 14 |

About 42% done and recorded, 31% unfinished but recorded, and 27% (48) lost, redirected without a record, or recorded wrongly.

**37.2's own commitments (117):** 54 done, 6 done late or only after Zach reminded, 26 recorded but not done, **16 dropped with no
record**, 6 uncertain, the rest superseded or done by others. **Offers left unanswered:** 7 in the first period alone, 5 never done.
**Switches (43):** 18 resumed, 11 recorded as paused or deferred, **12 lost** (some only until Zach asked).

**Compactions:** 111 pending items across 12 summaries: 51 done, 7 carried, 33 recorded, **20 vanished**.

**The records against the repository:**
- 38 of 137 proposals have a status that is no longer true (17 say "not built" or "not merged" of work on main);
- 15 planned lists exist only in a session note;
- 13 of 30 branches hold work not on main, 2 with no record anywhere;
- 21 WORK rows contradict the repository, and at least four W numbers are used twice;
- the hygiene report holds 285 items (176 chores);
- unfinished work grew from about 230 items on 9 Nov to about 350 on 19 Nov, and the size log was last recorded on 16 Nov.

## 2. The paths taken and left

The largest redirections, each one a design path begun and then replaced:

| Path | Replaced by | Recorded? |
|---|---|---|
| Cybertron 1's engine and its running records (the work log, the board's status row, porting.md) | Cybertron 2 (22 Oct) | no: all three stopped within a day, none points to its successor |
| Ecology as living_populations.md, then node_ecology.md, then wild_systems.md | wild_layer.md ([[D2-199 The wild layer is built on 37.2's own ecology branch|D2-199]], built and merged) | no: the first three were never marked replaced; two still say "nothing decided" |
| Per-kind behaviour modules ([[D2-203 Each wild kind's behaviour is designed first, then built as a m|D2-203]], wild_behaviour.md) | traits and general methods ([[D2-204 People answer the wild by general methods, not a technique per|D2-204]], 02zv) | no: [[D2-203 Each wild kind's behaviour is designed first, then built as a m|D2-203]] not marked replaced; [[W-4 wild_behaviour.md v3 (the per-kind designs, from 02zv, 02zw and th|W-4]] waiting 10 days |
| The wildlife pack plan, K0 to K12 (02zv §4) | briefs 1 to 5 took K0, K1, K2, the hunting and K4; the rest was never briefed | not until 19 Nov ([[L-117 Wildlife pack K3 forays, methods and knowing|L-117]] to [[L-127 The ecology's calibration backlog|L-127]]) |
| The engine overhaul's phases 3 to 5 ([[D4-103 The engine overhaul goes ahead, in phases|D4-103]]) | the wildlife briefs, then brief 5 | phase 3's proposal in discussion; phases 4 and 5 had no rows |
| The economy web (economy_web.md) after Zach's critique of 15 Nov | the economy research folder (02zzj) | no: the proposal was never revised and has no History entry |
| The runs-only test world (brief 5 §8, cc6f38d) | the model-per-household runs world with fields (dd54509) | in part: [[Q-60 The water worlds' people, and the runs world for the model-per-ho|Q-60]] (c) asks to confirm; the runs-only run was never made |
| Climate calibration against real weather (promised 8 and 9 Nov) | consolidation, then the briefs; it came back as [[W-51 The weather across conditions (Zach, 16 Nov try test the weather|W-51]] on 16 Nov | no row for a week |
| Stage 1 of the generator, "ready to build" (1 Nov) | parts built, parts left; the 3 Nov critique (flat forest, vanished lakes, water's paths) | no: partly met only on 17 Nov ([[D2-226 Floodplains in the generator, now|D2-226]]) |
| A large set of 22 to 24 Oct decisions (gates, ledgers, specialised tools, node raids, room bookings) | the packages that built some of them | no: the spec states the rest as if they hold |

## 3. The patterns: when work gets lost

1. **The latest message wins.** 31 of the 43 switches were set off by a new question from Zach. Work in hand was set aside and, unless
   it already had a row, not resumed. Offers at the end of a reply ("Shall I ...?") that Zach did not answer were never raised again:
   OPEN holds questions, not offers, so an unanswered offer had nowhere to live.
2. **The tail falls out at each compaction.** In the first nine compactions no pending item carried into the next summary: each was
   rebuilt from the latest segment. The next step was kept every time; the long tail (checks, small fixes, write-ups owed, publishing)
   was not. Carrying began only once WORK.md existed (9 Nov).
3. **What gets lost is upkeep, almost never building.** Spec write-ups for decided rules (the single most-lost kind of work: about 50
   decisions are in no spec file), statuses after a build, follow-up checks on runs, small fixes found in passing, write-ups owed,
   publishing to the dataset. Design and building are rarely dropped; their records are.
4. **Nobody closes what the other session built.** When 37.4 builds and merges a 37.2 brief, its proposal keeps "to be built", its
   WORK row keeps "waiting on the merge", and no decision row is written. Briefs 4, 4b and 4c are on main with no decisions.
5. **A redirection starts a new file and never closes the old one.** Four ecology proposals in a row; the economy web; the behaviour
   modules.
6. **Plans in session notes never become rows.** The pack plan, the calibration backlog (02zp §16), the run reports' issue lists (38.78
   §5: 16 issues; 38.71 §4: 12 world-building features), the 02zp §17 decision lists: rows only when Zach says "flag".
7. **Bug chains crowd out the checks owed on earlier fixes.** 16 to 17 Nov: trench, pond, water counted twice, a one-parcel fix
   reverted, water bodies, missing livestock, missing brine pan; each handed over, and the recalibration owed on the first ([[W-60 The ecology's water measure counted each lake and the large river|W-60]])
   untouched since.
8. **Status runs ahead of the record, and of the truth.** "Stage 1 is ready to build" (1 Nov), "every specced layer" (9 Nov), "My
   part of brief 5 is done" (16 Nov, before four generator faults), "Every check passes" (17 Nov, before no livestock and no brine
   pan), "wildlife: built and on main" (19 Nov, with 9 of 13 packs unbriefed). The claims about work already done mostly hold; the
   gaps are in what was said would be done, and in "done" said before the checks that would have shown otherwise.
9. **Branches hide work.** Thirteen branches are ahead of main; the water work is on eight. Nothing checks that a branch has a row,
   or that a live run's engine has the fixes it should.
10. **Relayed answers pile up as asks.** Answers that come through 37.4 are re-asked three or four times instead of being recorded
    with "default taken" as CLAUDE.md allows.
11. **Housekeeping is by age, not by truth.** The hygiene tool flags old rows, but not a "not built" status on built code, a row
    waiting on an answered question, or a branch with no row.

## 4. Mechanisms

Ordered by how much of the loss each would have caught, cheapest first where they tie.

1. **Every commitment is a row in the same turn.** Any "next I'll", "left:", "I'll fix", "owed", and every offer ("Shall I ...?"),
   becomes an OPEN row before the reply ends: a new kind, **O-n (offers and promises)**, with the owner, the date and a default ("if
   no answer in 3 days: do it" or "drop it"). Hygiene lists O-rows past their default. Catches patterns 1 and 2: about half of all
   losses found.
2. **Status answers come from a status tool, not memory.** `tools/status.py` prints, per owner: WORK rows with age and what is left;
   O, Q and L rows with age; every branch ahead of main with the row naming it (or "no row"); and the hygiene counts. Every "what is
   in progress", "what is left", "is X done" is answered from its output, and any disagreement with memory is said. Catches pattern
   8, and gives Zach the same view.
3. **Hygiene checks truth, not age.**
   - A proposal saying "not built" or "not merged" whose named commits or files are on main.
   - A WORK row whose state is "waiting" on an ask already answered in DECISIONS.
   - A branch ahead of main with no WORK row naming it.
   - A plan list in a session note ("Left:", "Next:", "Later:", "issues", "open questions") with an item not tagged with a row.
   - A decision in the owner's series not cited in a spec file, shown first to the owner.
   - Duplicate W, Q and L numbers.
   Catches patterns 4, 6, 9 and 11.
4. **A merge checklist.** Merging a branch prints the proposals, WORK rows and OPEN rows that name it; their statuses are updated in
   the merge commit, and the DECISIONS rows for what it built are written (or a "built without decision" ask is made). Catches pattern
   4 at its source.
5. **A redirection closes the old path.** When work is replaced, the old proposal's status says "replaced by X" and its open questions
   move to OPEN or are dropped by name, in the same commit as the new one. Catches pattern 5.
6. **"Done" needs its checks named.** A WORK row moves to Done only with the checks it passed listed (for a world: world_checks, the
   economy's food over the run by village, succession, the standard settings, the null arm where one applies); a hand-over says which
   checks were not run. Catches pattern 7 and most of pattern 8.
7. **A carry file read before work starts, written before it stops.** Each session keeps one short file of its live threads (one line
   each: what, where, what is next, the row), updated whenever a thread is opened or set aside, and read first after a compaction or a
   gap. WORK.md is the long record; this is the working memory that survives a compaction. Catches pattern 2.
8. **A weekly digest for Zach.** Generated from the status tool: what moved, what is stuck and on what, the asks older than a week
   with their defaults, and the size of unfinished work against last week. Published as a page, so the partial work and its progress
   are visible without asking.
9. **Defaults on relayed answers.** An answer relayed by another session is recorded at once as "default taken, relayed, to confirm"
   and acted on; it is confirmed once, not re-asked.

**What would not help:** more rules in CLAUDE.md without checks behind them. The existing rules (a row before starting, a row for
everything deferred, a decision row and a spec line for everything built) would have caught most of this. They were not followed
under the pressure of the next request, and nothing noticed. The checks are what matter.

## 5. What to do with what was found

The audits found, across their overlaps, roughly 70 to 90 distinct items that are lost, unrecorded or stale. The tables in
`02zzp_audit/` list each with evidence. Proposed:
1. **Triage, once:** each item to keep (a row), drop (said so), or already done (status fixed). 37.2 drafts the triage; Zach confirms
   the drops (OPEN [[Q-61 What was started and left, and the mechanisms to catch it|Q-61]]).
2. **Then the catch-up**: 37.2's share of the stale statuses, decision rows and spec lines (about 50 decisions in no spec file, 33 of
   them D2), and the briefs 4 to 4c decision rows.
3. **Build mechanisms 1, 2, 3 and 7 first** (rows for commitments, the status tool, hygiene's truth checks, the carry file): small,
   and together they would have caught most of what is above.

