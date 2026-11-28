# How we work: the process and its mechanisms

## Summary

Every rule Zach has set about how the work is done, in one place (D2-253): how things are recorded and tracked, how he is asked and
shown things, how code, commits and branches go, what may be built or run without him, where documents go. Each line cites its
decision, or the rule it was first written in. A new process decision is added here by `records decide --area process/how_we_work`.

## Decided

### Recording and tracking
- D2-232: asks, threads, offers, deferrals and decisions are items, one file each; OPEN, WORK and DECISIONS are views rendered from them, never edited by hand; ids flat, with a parent link.
- D2-233: one tool records them (`tools/records.py`) with a skill beside it; only what outlives the turn is recorded; one event is one call; the records go in the work's commit.
- D2-234: documents are nodes in the same web, with a summary, threads and area; a query shows the node in full, its links one line each, nothing further; freshness against the links; orphans, dead ends and stale summaries checked.
- D2-236: every resolution names who made it (Zach, agent, default, relayed); an agent may resolve the obvious, marked as its own; the last three are provisional until Zach confirms; any item may be marked to revisit; a thread closes only when its open items are moved, closed or marked; decisions stay live by area.
- CLAUDE.md (Zach, 9 Nov): everything started gets a row first ("every time we start on something new it has to be added to the currently working and we can track how large the unfinished work goes"); stopped work says what is done and left; finished work moves to Done; questions go to OPEN; later work is flagged with what it waits on.

### Asking Zach, and showing him things
- D2-254: everything shown to Zach names each question, proposal, thread or decision by a short plain description of what it is, with its id in brackets after it, never a bare id.
- D2-239: his questions come as a digest of at most about 8, one choice each, with a recommendation and a default; a sheet of changes from the defaults comes before any paid run or brief handed over; the board is for hand-offs between sessions only; about 6 active threads per owner is a soft limit, flagged so threads are revisited; a tool packs the context for any hand-off.
- D2-240: the Obsidian vault is a local folder kept up to date automatically, with nothing to download.
- CLAUDE.md rules: a question Zach answers in conversation is a decision only when he states it; going ahead on a default is written "default taken" and he is told.

### Code, commits and branches
- D2-235: a commit's subject starts with its type and thread; its trailers name the agent, the threads and the ids opened, closed, decided and built, checked against the diff.
- D2-237: code changes live under a thread; any session may change code, named for its thread; the area's owner is named on the merge.
- D2-238: merge to main early, not to an extreme; a branch is fine for a distinct thread or for exploring, and branches are revisited; runs go from main unless a purpose-run needs its own branch, labelled as a run thread, and few of those; no empty or stale branches.
- D2-244: the engine's rework into feature packages is postponed and kept in mind: every engine change meanwhile keeps to its seams.
- D2-243: the verbs and livelihood archetypes are reshaped first, as their own work, before that rework.

### What waits on Zach's word
- README rule 10 (Zach, 29 Oct): nothing is built until Zach asks for it to be built; a decision recorded is not permission to build it.
- Carried by the sessions, not yet in Zach's own words (to confirm, OPEN Q-67): live runs only on his go; publishing to Hugging Face only on his go; run logs kept out of the repository.

### Where things go
- docs/cybertron2/README.md: the layers (spec for what is decided, proposals for what is thought, session notes for long material, OPEN for asks and later work, WORK for what is in hand), the path of an idea, retrospective proposals for what is built first.
- D2-253: the rules about the process are kept together in this file.
- CLAUDE.md (Zach, 24 Oct): visuals are drawn from how the engine works, at the state's own resolution.
- CLAUDE.md: senses are written to docs/cybertron2/guides/senses.md.
- D2-277: Every idea explored in conversation is written down before moving on: into its thread's proposal, or, if it is not part of it, into its own proposal marked exploration (or speculation), linked to the thread; nothing explored is left only in the conversation
- D2-280: Commits carry no Claude-Session line (the repository is public and the link names a private session); the Co-Authored-By line stays
- D2-285: The records brief is run by hand after each compaction for now, since the project hooks do not load when a session starts outside the repository.
- D2-287: Reviewing past runs: every finding is checked against the fixes made since that run (the commits and decisions after its date, and the world's settings, e.g. view: beliefs) before it is taken as evidence of a current fault; a fault already fixed is reported as fixed, with the fix.
- D2-298: Bot runs test interfaces and basic functioning only; they make no decisions except those built into them, so they are not read as evidence of behaviour or of whether a world is too rich or too poor. Live runs carry that signal (starving included).
- D2-300: Every item Zach defers or flags is tagged with the prospective threads it most likely bears on (benched threads kept for that purpose), so that when work on a thread begins, every past item put off for it surfaces with one tool call.
- D2-313: For this wave (W-73, W-85), 37.2 owns every engine file its design changes, including those 37.4 owns (verbs and their registry, the standing rules, the prompt core, clocks, spoilage, buildings and their cost code, senses); 37.4 is told on the board.
- D2-353: Everything new in the engine is built within the agreed architecture without being asked each time: features are data on the core's general mechanisms (feature_packages.md P3), behaviour attaches to declared properties of rows and never to a thing's name, interface and signs are rendered from data, and every registry is checked when it loads. Every brief states it, every review checks it (named branches, hand-written text, word lists, silent skips, maker patches), and a guard test fails on new branches on a named thing.
- D2-354: The architecture is a healthy balance, not a strict one: most of the world is data acting on general, shared primitives that are extended when a new feature needs it; a system may own its specifics where they truly belong to it; the aim is that the engine can change quickly without falling into a tangle of ad hoc fixes or becoming so rigid that ad hoc fixes are the only fast way to build. Refines D2-353.
- D2-355: Tests: a change runs only the tests of the modules it touches (and a short bot smoke run where an interface changed); the full suite runs only when a whole stage merges or before a live run. Every brief says so.
- D5-11: A suspected engine fault found while reading runs is not sent to another session to fix until Zach has confirmed it is a bug: it is shown to Zach first, with the evidence, and sent on only on his word.

## Sources

docs/cybertron2/proposals/records_and_workflow.md; proposals/thread_tracking.md; docs/cybertron2/README.md; CLAUDE.md.

*Current as of 20 Nov 2026: D2-232 to D2-240, D2-243, D2-244, D2-253, D2-254.*
