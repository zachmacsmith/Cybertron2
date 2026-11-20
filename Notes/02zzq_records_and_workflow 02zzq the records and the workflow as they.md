---
id: docs/review/37_growth/02zzq_records_and_workflow.md
kind: note
updated: "2026-11-20"
tags: [note, open]
---
# 02zzq: the records and the workflow as they are, and how Zach works well

## Text
# 02zzq: the records and the workflow as they are, and how Zach works well

37.2, 20 Nov 2026. WORK [[W-66 The design of the records and the workflow (Zach, 20 Nov scope ou|W-66]]. Supports docs/cybertron2/proposals/records_and_workflow.md. Zach: "scope out the desired design of
how documents are stored, indexed, referenced, updated, tracked ... what scripts automatically run ... how does this relate to the
git workflow ... informed based on the process of how I have been actually designing cybertron with you so far and especially its
fail states, but also how I seem to work well". The fail states are in 02zzp. This note gives the measurements (§1) and the other
side, what works (§2).

## 1. The process as measured, 20 Nov

| Measure | Value |
|---|---|
| Commits on main, 22 Oct to 20 Nov | 1,111 in 23 days with commits |
| Merges into main | one: the wild layer, 16 Nov (34 merge commits in all, the rest between branches) |
| Branches ahead of main | 13 (water work on 12: runs-models 61, floodplains 46, water-bodies 44, lake-fixes 42, ecology-water 36, water-measure 34, 5-fowl 33, lake-on-mere 32, 5-river 29, 5-keep 4, water-worlds-2 3, water-worlds 1; plus wip-weather-senses 1) |
| Proposals, spec files, session notes | 141; 67; 99 in 37_growth and 98 in 38_space_engine |
| Proposal statuses | 38 retrospective, 29 accepted, 21 partly accepted, the rest scattered |
| Store sizes | DECISIONS.md 150 KB (394 lines), OPEN.md 86 KB, WORK.md 36 KB, BOARD.md 106 KB (1,106 lines) |
| Commits touching the stores since 1 Nov | WORK.md 123, OPEN.md 123, proposals/README.md 96, DECISIONS.md 85, BOARD.md 22 |
| Ids in use | D2 231, D4 124, Q 64, L 99, W 66 |
| A run's commit | recorded (`engine/journal.py`, `git rev-parse HEAD`) |

## 2. How Zach works well

Read-only review by an agent of the 02zzp tables, `git log` (1,814 commits on all branches), the records, and Zach's messages in
the transcript (563 kept by its filter, against 02zzp's 629, so its counts are approximate). M is measured, I is inferred.

1. **Numbered asks, answered in terse numbered replies, are the fastest route to a recorded rule (M).**
   - About 37 numbered replies, 32 of them between 22 Oct and 2 Nov: the period of 191 of the 231 D2 rows.
   - From answer to commit takes 1 to 3 minutes: 23 Oct 01:53 to 35b8f6e at 01:54; 16 Nov 19:25 to cc796c0 at 19:27; 17 Nov
     00:15 to 6ab73ba at 00:16.
   - The failure: "yes to all" on long menus (1 Nov, 9 Nov) recorded quickly what was never built (gates, ledgers, specialised
     tools, node raids). Then: "did you build the complex behavioral mechanisms… I thought the first was what you were adding?"
     (9 Nov).
2. **A digest he asks for works best (M).**
   - "List out the open questions to me with context for each" (16 Nov 23:47): 25 asks with recommendations, answered in 27
     minutes, 8 decisions committed a minute later.
   - "First ask me the key gating road layout questions" (23 Oct) gave [[D2-104 Roads have stretches (one per day of the edge) and landmarks, k|D2-104]] to [[D2-108 Building on landmarks later|D2-108]] in 12 minutes.
   - 57 Q rows are open. He never cites an OPEN id unprompted. He speaks of briefs and packages.
3. **A one-row record lands at once; prose owed elsewhere does not (M).**
   - "Flag", "defer", "add the rule": the row lands in the same minute ([[L-33 Growth to towns fixed nodes, faster edges, reach by place|L-33]], 1 Nov 19:44; [[D2-208 The world keeps the land it runs on|D2-208]], 10 Nov 00:44).
   - The spec had 84 commits from 22 Oct to 2 Nov and 37 since. About 50 decisions are in no spec file. [[W-9 Compile the generator into specworldgeneration.md (OPEN L-101)|W-9]] and [[W-10 37.2's spec write-ups owed since 2 and 3 Nov (OPEN L-32, L-44, L-|W-10]] have not
     been begun since 2 and 3 Nov.
4. **Checkable measurements become decisions fast, and the decisions hold (M).**
   - "Why did it take them 24 times" (29 Oct 18:18): model c185154 at 18:31, [[D2-162 Shorter waits for children, a higher chance|D2-162]] built at 18:38.
   - The calibration checks on 16 Nov gave [[D2-211 Fresh fish keep as meat in hand, and alive in a trap or a weir|D2-211]] and [[D2-212 Fresh fish keep twice as badly as meat in a store|D2-212]] within minutes. The food table on 17 Nov gave [[D2-230 Highpool's larder in the runs world|D2-230]] in 12 minutes.
   - Prototypes he could not judge went badly (9 Nov 00:28; the 8 Nov deep dive, interrupted about a dozen times).
5. **A brief handed to 37.4 is built fastest; nothing closes the records after (M).**
   - Package F was decided at 05:52 and built at 06:13 (24 Oct). Brief 1 was built in 50 minutes (9 Nov).
   - Briefs 4, 4b and 4c have no D2 rows. 17 proposals say "not built" of code on main.
6. **Retrospective proposals are a 37.4 habit (M).** About 45 retrospective rows are 37.4's and one is 37.2's, though 37.2 built
   landgen stage 1 (98bdc3f) and the wild layer (9d418ff).
7. **Circling a topic gives real work; the open stretch gives most losses (M counts, I cause).**
   - Ecology went through four proposals in about 30 hours and was then built and merged. The economy web became a 1,335-node
     research folder.
   - From 7 to 15 Nov: 289 messages, almost no numbered asks, 17 D2 rows (none from 12 to 15 Nov). The same stretch holds "Wtf
     were you building?" and "you just redescribed what we already have".
8. **A redirection loses nothing when the old thread is parked in the same turn (M).**
   - Kept: [[L-33 Growth to towns fixed nodes, faster edges, reach by place|L-33]], Package E, forays ([[L-105 Forays as their own track|L-105]]), the one-parcel revert ([[D2-229 One fish stock per water body|D2-229]]).
   - Lost: the old ecology proposals never marked replaced; economy_web.md with no History entry; the 3 Nov generator critique
     followed by 38 silent hours.
9. **His probing questions find what the records hide (M).** About 39 "did you / you were gonna" messages. They catch:
   - whether something is done ("Did u do it?", 17 Nov);
   - promises dropped ("You were gonna…", 16 Nov);
   - things changed without telling him ([[Q-59 (Closed 17 Nov D2-229.)|Q-59]]; the lifespan; "so many random tools I didn't know you added");
   - what a claim rests on ("Did you just fix for these worlds?").
10. **He reads chat, pictures and run data, not the registers (M).**
    - The board is named 4 times, the last "don't post anything more on the board for now" (8 Nov).
    - Three running records he asked for on 22 Oct stopped within a day.
    - "Generate an image… so I can check it before running" caught the wild-node cap and the missing traders.
    - He carries findings between sessions by pasting them (37.4's economics critique, 23 Oct; a run report, which reached 37.2
      only because he pasted it).
11. **Bursts with long gaps (M).** 21 bursts of 0.1 to 17.6 hours, with gaps of up to 131 hours. 10 of the 21 returns open with a
    status question, each answered from memory. 37.2 holds 19 in-progress and 6 paused rows. About 10 threads were touched in 10
    hours on 16 and 17 Nov. D2 rows by day: 91 on 23 Oct, 48 on 24 Oct, 23 on 16 and 17 Nov, none from 12 to 15 Nov.
12. **What carried weight (M):**
    - DECISIONS (append-only, a series per session, written in the same minute);
    - the deferred table (each row quotes Zach);
    - WORK (124 commits in 11 days, and the only thing that carried items across compactions, though 21 of its rows contradict
      the repository and W numbers collide).
13. **What went stale (M):**
    - the spec's "Current as of" lines after 2 Nov;
    - proposal Status lines (38 of 137 untrue);
    - the outcome log;
    - the board's status table (37.2's row dates from 22 Oct);
    - `hygiene --record` (5 runs, the last 16 Nov);
    - the "decisions for Zach" lists in session notes.
14. **The code-ownership rule is overridden and makes branches multiply (M, I).** It was overridden on 1 Nov, 9 Nov and 17 Nov
    ("Make the changes yourself and tell them"). 13 branches are ahead of main.
15. **Plain meanings (M).** About 69 "what is…" messages ("what are clappers?", "What is a spate wreck?"). "Wdym hen is a good?"
    exposed a design fault.

The design's answer to each is in records_and_workflow.md §6.

