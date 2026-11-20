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

## Sources

docs/cybertron2/proposals/records_and_workflow.md; proposals/thread_tracking.md; docs/cybertron2/README.md; CLAUDE.md.

*Current as of 20 Nov 2026: D2-232 to D2-240, D2-243, D2-244, D2-253, D2-254.*
