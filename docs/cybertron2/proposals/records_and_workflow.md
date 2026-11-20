# Records and workflow: how the documents, the scripts and git carry the design

**Status:** discussion (OPEN Q-64). Takes in proposals/thread_tracking.md (W-65, Q-63) as its part on threads and commits.

**Owner:** 37.2 (WORK W-66). The engine's branches and merges are 37.4's to agree (§5).

## Summary

Three principles:
1. **Write each fact once, and derive the rest.** A proposal's status, a row's last touch and where its work is, whether a decision
   is built, the outcome log and the indexes are read from the item and from git, not copied by hand into four files.
2. **Every change of stage is a commit that says so.** Trailers name the agent, the thread and the ids opened and closed. Checks
   hold these claims against the diff before the commit (the agent's hook) and after the push (the Action).
3. **Zach reads views made for him; agents read the stores through a tool.** Nobody reads a 150 KB table to find out what is open.

The evidence is in docs/review/37_growth/02zzq_records_and_workflow.md (the process as measured, 20 Nov) and 02zzp (what was lost).

## 1. What the process is now

- **Volume:** 1,111 commits on main in 23 days (about 48 a day). The records are 141 proposals, 67 spec files and about 200 session
  notes.
- **The stores are too big to read.** DECISIONS.md is 150 KB, OPEN.md 86 KB, WORK.md 36 KB and BOARD.md 106 KB (1,106 lines).
  Agents grep them. Zach asks in chat instead ("List out the open questions to me with context for each").
- **Every stage change is written by hand in three to six places.** A decision needs:
  - its DECISIONS row;
  - the spec line and the spec file's "Current as of";
  - the proposal's status and a History entry;
  - the outcome log;
  - the ask closed in OPEN;
  - the WORK row.

  Since 1 Nov, WORK.md and OPEN.md are each in 123 commits, proposals/README.md in 96 and DECISIONS.md in 85. These are the writes
  02zzp found lost.
- **A proposal's status mixes two things:** whether it is decided and whether it is built. When a build lands, nobody updates it
  (02zzp pattern 4: 17 proposals say "not built" of code on main). Building usually comes before writing: 38 of 141 proposals are
  retrospective.
- **Code waits on branches.** Main has had one merge in 23 days: the wild layer on 16 Nov, after about ten days on stacked branches.
  The water work is now on 12 branches ahead of main, by 1 to 61 commits each. They are stacked (5-river, then ecology-water, then
  floodplains, water-bodies, lake-fixes and runs-models), and the live run runs on one of them. The records on main describe
  branch state, and a fix made on one branch is missing from the others.
- **Ids:** the decisions' series by session (D2-n, D4-n) have never collided. The shared W series has collided seven times.
- **Already right:** runs record their commit (`engine/journal.py`), and the session notes hold long analysis apart from the rules.

## 2. The stages

Every item has a kind, an id, a parent thread, and a few states. A move between states is one commit, with a trailer that says so.

| Kind | Id | States | What moves it | Evidence it needs |
|---|---|---|---|---|
| **Request** (Zach's message) | none | becomes a thread, an ask, an offer or an answer in the same turn | the stop check | a row, or a reply that answers it |
| **Thread** (work) | W-n | queued, active, waiting (on named ids), paused, then done, dropped or deferred | its owner | done: the checks it passed, named; dropped: the reason; deferred: an L id |
| **Ask** (for Zach or an owner) | Q-n | open, answered, then recorded or default taken, then closed | Zach's answer; a default's date | answered: his words and date; recorded: the D ids, or "no rule" |
| **Offer or promise** | O-n | open, then accepted, declined or defaulted, then done or dropped | Zach's reply, or the default date | done: the commit |
| **Deferred** | L-n | flagged (waits on something), then taken up (a W id) or dropped | its trigger arriving, or Zach | waits on: named |
| **Proposal** | its filename | discussion, then accepted, partly accepted, rejected, deferred or replaced by another | Zach's decision | the D ids |
| **Decision** | D2-n, D4-n | recorded, then in the spec, then replaced by another | Zach's own statement | his words; the spec line |
| **Build** | the thread's W id | briefed, then on a branch, then on main, then in a run | git | derived: the branch, the merge, the run's commit |
| **Run** | the run's name | planned, running, stopped or finished, then published, reported, then its issues triaged | the run | triaged: every issue in the report has an id or is dropped by name |

What this changes:
- **Decided and built are two axes,** and built is never typed by hand. It is read from git: the commits that name the thread, and
  whether they are on main.
- **A run is an item.** Its report's issue list must end with every issue made a row or dropped by name. 02zzp pattern 6 lost these
  lists: 38.78 §5 had 16 issues and none became rows.
- **A request is never a stored item;** it must become one of the others in the same turn. 02zzp pattern 1: "the latest message wins".

## 3. Storage, indexing and references

**The store.** Three ways to do it:

| | A: keep the tables | B: one file per item | C: one registry (what W-65 began) |
|---|---|---|---|
| How | OPEN, WORK and DECISIONS stay markdown tables; a tool derives and checks | `docs/cybertron2/items/Q-63.md`: a short header (id, kind, state, parent thread, dates, waits on) and the prose; OPEN.md, WORK.md and the decision log are rendered from these files | `threads.json` holds the fields; WORK.md is rendered from it |
| Writes per stage change | the same 3 to 6, but checked | 1: the item's header (the views are derived) | 1 to 2 |
| Conflicts between sessions | as now: four files in most commits | none on items; the views are only ever made by the bot | a new hotspot: one file in every commit |
| Reading | grep in large files | open the one item; `records show Q-63` | the tool |
| Cost | small | one mechanical migration of about 600 rows | medium |

**37.2 recommends B, and dropping C.** Derivation (principle 1) ends the lost upkeep whichever store is used. But only B also ends
the hot files and the 150 KB reads. The migration is a script and one commit. The old ids are kept, and every existing reference
still resolves.

**The views.** OPEN.md, WORK.md, the decision log and the proposals' index are rendered from the items:
- the Action renders them after each push to main, in a bot commit;
- agents never edit them (the commit hook refuses);
- a session that rebases over a bot commit has no conflict, since it never touched those files.

**References.** Any id in any text (W-n, Q-n, L-n, O-n, D2-n, a proposal's filename, a run's name) is a reference. The tool
resolves it, and the views link it. The "references" field is derived from mentions in the text; the parent thread is the one
link written by hand.

**Ids.** The series stay flat, never nested under threads (thread_tracking.md, "The ids"). A new id comes from `records new`
after a fetch. The commit hook refuses an id already on main, and the push check refuses a duplicate.

**The spec stays hand-written, and the tool writes its decided lines.** Each decision item carries its area
(`area: environment/land`) and its rule, stated as a rule. `records decide` appends that line, with its id, to the area file's
"Decided" section in the same call. When a decision is replaced, the tool marks the old line, and the check refuses the commit
until the line is rewritten. People may regroup and reword the lines freely; the check only needs every live decision cited
once.

This removes the most-lost write in 02zzp: about 50 decisions are in no spec file, and W-9 and W-10 have not been begun since 2
and 3 Nov. The rest of the spec is untouched (§11).

(Revised 20 Nov. The first draft rendered the whole spec from decisions. But the "Decided" sections are only 13% of the spec's
words: 6,900 of 52,300. The other 87% describe the mechanics as built, with their parameters and checks, and no decision is
their source.)

**The other layers keep their form:**
- **Proposals:** one file per idea, with its History. The status covers the decision axis only; the build axis is derived.
- **Session notes:** long analysis. A list of plans or issues in a note must tag each line with an id or "dropped"; a check finds
  untagged lines.
- **The board:** see §6.

## 4. What runs, and when

| When | What runs | What it does | Who sees it |
|---|---|---|---|
| A session starts, resumes or is compacted | `records brief` (hook) | this owner's live threads, each with its next step; Zach's asks waiting on them, with their age; offers past their default; branches that no thread names; what failed on the last push | the agent, in its context |
| Every commit by an agent | `records commit-check` (hook before `git commit`) | the trailers are present; the ids exist or are opened in the diff; Opens and Closes match the diff; no view is edited by hand; no scratchpad paths | the agent: a refused commit, with the reason |
| The end of every reply | `records stopcheck` (Stop hook) | a reply that promises, offers or leaves work, with no record changed in the turn, is sent back | the agent |
| Every push to main | the Action | every truth check (hygiene's and 02zzp's); the views rendered; the status page rebuilt; the ids whose code has just reached main listed (the merge checklist) | the run's summary; the next brief |
| Weekly | a scheduled task | a digest page: what moved, what is stuck and on what, asks older than a week with their defaults, the size of unfinished work against last week | Zach |
| Before any paid run or build handed over | `records sheet <world or brief>` | the settings against the defaults; what has been added or changed since Zach last looked; a map or picture where there is one | Zach, before he says go |
| On demand | `records new`, `close`, `move`, `show <id>` (the tree under a thread), `status` | the agent's verbs; every status answer comes from `status`, not memory | the agent, then Zach in chat |

**Zach runs nothing.** He reads the desk (the status page: his asks with context, recommendations and defaults; what moved; what is
stuck) and answers in chat, as now.

## 5. Git

- **Records go to main, always,** in the same commit as the work they describe. Docs already do.
- **Who changes code.** Any session may change code, on a short-lived branch named for its thread, with a row. The owner of the
  area (37.4 for the engine) is named on the merge, and their objection is an ask. This replaces "code under `cybertron2/` is
  changed only by 37.4", which Zach overrode on 1 Nov, 9 Nov and 17 Nov.
- **Code built without a decision opens an ask.** A commit that changes code under a thread with no decision behind it opens a
  "built without decision" ask, the retrospective proposal's trigger. Today 37.4 writes these and 37.2 almost never does (about 45
  against 1).
- **Code is merged early, with new behaviour switched off.** A branch per thread, named for it (`w62-water`), one level deep:
  nothing branches from an unmerged branch except a fix merged back within a day. The branch merges to main once the tests pass,
  with any new behaviour behind a world-spec switch that is off by default. **Zach's go then moves from "merge" to "switch on".**
  He still decides what any run or default world does. What changes is that unfinished work stops hiding on branches. This is
  his choice to make, and 37.4's to agree.
- **Runs only from a commit on main** (or a tag `run/<name>`). The journal already records the commit; publishing would warn
  when it is not on main.
- **Commits:** trailers as in thread_tracking.md; the subject `<id or area>: what changed`; small commits.
- **No pull requests.** Agents push to main and Zach does not review diffs. The commit hook is the gate before a commit, the Action
  the check after the push.
- **Merging records itself.** A merge commit's trailers close the build. The Action lists the decisions and proposals whose code
  has just landed, and their build axis changes with no hand edit.

## 6. How it fits the way Zach works

Measured in 02zzq §2, from Zach's messages since 22 Oct, the commits and the records. Each finding is followed by what the design
takes from it.

| What works, or fails, for Zach | Evidence | So the design |
|---|---|---|
| **Numbered asks, answered in terse numbered replies,** are the fastest route from a question to a recorded rule | the reply is committed 1 to 3 minutes after it; the 22 Oct to 2 Nov period, rich in numbered replies, gave 191 of the 231 D2 rows | makes the **ask digest the interface** (below) |
| A digest he asks for gets answered; asks never put to him stay open | "List out the open questions to me with context for each" (16 Nov): 25 asks, answered in 27 minutes, 8 decisions a minute later; 57 Q rows open; he never cites an OPEN id unprompted | shows the digest at the start of each burst and on demand; parses his numbered reply at once |
| **"Yes to all" on a long menu** records quickly but loses what was meant | the 22 to 24 Oct burst decided gates, ledgers, specialised tools and node raids, never built; "did you build the complex behavioral mechanisms… I thought the first was what you were adding?" (9 Nov) | keeps a digest to about 8 asks, each one choice; a decision gets its build axis, so "decided, not built" shows in the brief |
| **A record that is one row lands; prose owed elsewhere does not** | "flag", "defer", "add the rule": the row in the same minute; the spec: 84 commits by 2 Nov, 37 since; about 50 decisions in no spec file; W-9 and W-10 not begun since 2 and 3 Nov | records every event as **one item**; **the spec is rendered from the decisions**, not written out after them (§3) |
| **Measurements he can check** become decisions fast, and the decisions hold | "Why did it take them 24 times": model at 18:31, D2-162 built at 18:38 (29 Oct); the food table on 17 Nov gave D2-230 in 12 minutes; prototypes he could not judge went badly (9 Nov) | puts a measurement or a picture with any ask it can settle |
| **A brief handed to 37.4** gets built fastest, and nothing closes the records afterwards | Package F decided 05:52, built 06:13 (24 Oct); brief 1 in 50 minutes (9 Nov); briefs 4 to 4c built with no D rows; 17 proposals say "not built" of code on main | records closing itself at the merge (§5); the build axis derived |
| **Circling a topic** gives real work; the open stretch without asks gives most of the losses | ecology through four proposals in 30 hours, then built; 7 to 15 Nov: 289 messages, almost no numbered asks, 17 D2 rows, and "you just redescribed what we already have" | gives each area **one page of what already exists** (`records show area:<name>`: its proposals, decisions, code and rows), read before designing in it; offers a digest when a burst has gone a while with no asks |
| **A redirection loses nothing when the old thread is parked in the same turn** | kept: L-33, Package E, forays (L-105), the one-parcel revert; lost: four ecology proposals never marked replaced, the 3 Nov generator critique followed by 38 silent hours | has the stop check park the old thread (a row, or "replaced by"), keyed by its id in the commit trailers |
| **His probing questions** find what the records hide: done or not, promises dropped, things changed without telling him, what a claim rests on | about 39 "did you / you were gonna" questions; "Did u do it?"; Q-59; "I don't know why you changed that" (the lifespan) | puts each item's merge state, the open promises, **a sheet of changes from the defaults before any paid run or build**, and the checks behind any "done" in the desk |
| He reads **chat, pictures and run data,** not the registers | the board named 4 times, last "don't post anything more on the board for now" (8 Nov); three running records he asked for on 22 Oct stopped within a day; "Generate an image… so I can check it before running" caught the wild-node cap | sends nothing to Zach through a register; the desk page and the digest in chat are his views |
| **Bursts with long gaps,** about ten threads touched at once | 21 bursts of 0.1 to 17.6 hours, gaps up to 131 hours; 10 of 21 returns open with a status question, each answered from memory | answers every status question from `records status`; the brief opens each session; the weekly digest covers the gaps |
| **Records that carried weight** were one-row appends in a series of their own | DECISIONS (by session, never collided); the deferred table (each row quotes him); WORK (the only thing that carried items across compactions) | keeps these as items; drops what went stale by hand (Status lines, the board's status table, "Current as of", the outcome log) by deriving them |
| **The rule that only 37.4 changes code** is overridden and makes branches multiply | overridden on 1 Nov, 9 Nov and 17 Nov ("Make the changes yourself and tell them"); 13 branches ahead of main | replaces it with: any session changes code on a short-lived thread branch with a row, merged behind a switch; the area's owner is named on the merge (§5) |
| He needs **plain meanings** of the records' words | about 69 "what is…" messages: clappers, a spate wreck, the year's length; "wdym hen is a good?" exposed a design fault | names briefs and packages beside ids (he speaks in them: "brief 5", "package C"); keeps a glossary of world terms that the digest links to |

**The ask digest.** Numbered asks, at most about 8, one choice each. Each carries:
- its context in two or three lines, with a measurement or a picture where one can settle it;
- 37.2's recommendation;
- a default and the date it applies;
- its urgency (what waits on it).

It comes at the start of a burst, when he asks, and when a burst has gone a while without asks. His numbered reply is recorded
item by item in the same minute: a decision only where he states one; "default taken" where he says "sure" to a recommendation,
named as such.

## 7. The fail states, and what catches each

| 02zzp pattern | What catches it |
|---|---|
| 1. The latest message wins | the stop check (a request becomes an item in the turn); the brief (a thread set aside is listed with its next step) |
| 2. The tail falls out at each compaction | the brief after compaction, read from the items, not from the summary |
| 3. What gets lost is upkeep | derivation: one write per stage change, the rest read from it |
| 4. Nobody closes what the other session built | the build axis read from git; the merge's list of ids landed |
| 5. A redirection never closes the old path | a "replaced by" state, whose commit must close or move the old item's open questions |
| 6. Plans in session notes never become rows | the check on untagged plan and issue lines; a run's issue list as a stage |
| 7. Bug chains crowd out checks owed | "done" needs its checks named; a fix opens an O-row for the check it owes |
| 8. Status runs ahead of the truth | `records status` for every status answer; "done" with its checks |
| 9. Branches hide work | early merges behind switches; branches named by thread; a branch with no thread flagged |
| 10. Relayed answers pile up as asks | an answer's state "default taken, relayed, to confirm", with a date |
| 11. Housekeeping by age, not by truth | the truth checks on push |

## 8. Build order

1. **The items and the tool:** migrate the rows, then `new`, `close`, `move`, `show`, `status` and the rendered views. About a day.
2. **The hooks:** the commit check with the trailers, the stop check, the start brief. About a day.
3. **The Action and the page:** the checks, the bot's renders, the status page, the weekly digest. About a day.
4. **Git:** branch names and merging behind switches. This needs Zach's choice and 37.4's agreement; then the water branches are
   merged (W-62).

## 9. The items as a small graph, and the tool that writes them

(Revised 20 Nov after Zach: "can't threads branch, or be related to others ... Should any item like an open question potentially be
able to add an edge to another one if it seems potentially relevant to it? ... Should this be somewhat graph-like like obsidian?
... I don't want the software for this itself to be a big complex thing.")

**An item is a markdown file with a flat header.** `docs/cybertron2/items/Q-63.md`: a YAML front matter of flat keys and lists,
then the prose. This is the format Obsidian reads as properties and links, and GitHub shows as a table. Nothing nests, which keeps
the parser small and the metadata short.

**Every kind shares these fields:**

| Field | Holds |
|---|---|
| `id`, `kind` | Q-63, ask |
| `title` | one line in plain words, using the names Zach uses ("brief 5", "the runs world") |
| `owner` | 37.2, 37.4, Zach |
| `state` | one of the kind's states (§2) |
| `created` | the date |
| `parent` | the thread it belongs to (a thread's parent is a larger thread) |
| typed edges | see below, each a list of ids |
| `sources` | files, commits, quotes |

**Each kind adds a few fields:**

| Kind | Adds |
|---|---|
| thread (W) | `next` (the next step, one line); `branch`; at done, `checks` (what it passed) |
| ask (Q) | `to`; `recommend`; `default` and `default_on`; `answer` (Zach's words and the date) |
| offer or promise (O) | `default` and `default_on` |
| deferred (L) | `waits_on`: the trigger, as an id or in words |
| decision (D) | `rule` (stated as a rule, not as "replaces X"); `area` (the spec page); `quote` (Zach's words); `date` |
| run | `commit`; `world`; `models`; `report` |

**Read from git and from the text, never written:** last touched, commits, files changed, build state, and backlinks (every item
that mentions or links this one).

**The edges.** A small fixed set, each one used by a tool:

| Edge | Meaning | Used by |
|---|---|---|
| `parent` | part of a larger thread (threads branch into sub-threads) | the tree; the brief |
| `blocks` / `waits_on` | cannot move until the other does | the brief's "stuck on"; the digest's urgency |
| `replaces` | this supersedes that (a thread merged into another, a decision replaced) | the spec render; closing the old path |
| `decides` | a decision settles this ask | closing asks |
| `relates` | worth reading together, **with a one-line reason** | `show` lists it after the typed edges |

Any id mentioned in an item's text is already a weak link, derived like Obsidian's backlinks and costing nothing. So `relates` is
only for a link the text does not make. Its reason is required, because no check can tell whether a relevance link still holds.

**The query.** `records show Q-63` prints one bounded packet of about 40 lines:
- the item itself;
- its chain of parents up to the root thread (titles only);
- its open children;
- each typed edge with that item's state;
- the `relates` links with their reasons;
- the titles of the items that mention it;
- its last three commits.

Nothing is followed further than one step: a further step pulls in half the project.

**The tool.**
- One script, `tools/records.py`, in the standard library alone.
- Its verbs: `new`, `set`, `link`, `close`, `show`, `find`, `status`, `digest`, `brief`, `sheet`, `commit-check`, `stopcheck`.
- Each event is one call. For example, `records decide Q-63 --rule "..." --area process --quote "..."` writes the D item, closes
  the ask and links them.
- **A project skill** (`.claude/skills/records/SKILL.md`) holds the rules now spread through CLAUDE.md: decisions only on Zach's
  own statement, "default taken" for a "sure", a row for every commitment, the digest's form. It names the verb for each event.
- The hooks enforce what the skill teaches.

**Not built:**
- an MCP server (a process to run and configure in every session, where one shell call does the same);
- a database;
- search by meaning;
- links proposed by similarity;
- a graph picture as a working view.

**Size:** the script is about 600 to 800 lines, the hooks three short commands, the Action about 30 lines, the skill a page.

### Ideas borrowed

| From | The idea | Here |
|---|---|---|
| Architecture decision records | one file a decision, never edited, superseded by a later one | decision items with `replaces` |
| Issue trackers (Linear, GitHub issues) | few states; sub-issues; a few relation types (blocks, related, duplicate); "Closes #n" in a commit closes the issue | the states, the edges, the trailers |
| Event sourcing | an append-only log of events; views are derived | principle 1: items and commits as the log, views rendered |
| Zettelkasten and Obsidian | small notes, links in the text, backlinks for free | mentions as links; the item format |
| Getting Things Done | capture everything at once; every project has a next action; a weekly review | the stop check; `next` on every thread; the weekly digest |
| Kanban | a limit on work in progress makes the pile visible | the brief flags an owner with more than about 6 active threads (37.2 has 19 in progress) |
| Trunk-based development | merge daily, with unfinished work behind flags | §5 |

**The real alternative: GitHub Issues** (sub-issues, "blocked by", labels, closing from commits, a board for Zach), with no
software at all. Against it:
- the records leave the repository, so agents need a network call for each read and cannot grep;
- a record cannot change in the same commit as the work;
- the spec cannot be rendered from issues without a sync;
- the diff checks cannot see issue changes.

37.2 prefers the files, and this is Zach's to weigh (Q-64 (10)).

## 10. Keeping it light

Zach (20 Nov): "I also don't want the other fail-state, that every small ask i give you turns into a massive amount of updating
this and that and that and adds massive latency."

**Today, measured from 1 Nov to 20 Nov:**
- 651 commits; 275 (42%) touch at least one register (WORK, OPEN, DECISIONS, the index, the board);
- 80 (12%) touch nothing but registers;
- a commit that records a decision touches a median of 6 files.

Each write is a hand edit inside a large file: grep for the row, read around it, patch it. That costs time and tokens on every
event, and is the step that gets skipped.

**The design's rules for weight:**
1. **Record only what outlives the turn.** That is:
   - a decision;
   - something left open (an ask, a promise, a deferral);
   - a thread starting, pausing, ending or changing its next step;
   - a stage move (built, merged, run).

   A question answered in the turn, an explanation, or a fix made and committed needs no record beyond its commit. The stop check
   fires only on a promise or an offer left in the reply.
2. **One event is one call.** `records decide` writes the decision, its spec line and a dated line in the proposal's History, and
   closes the ask, in one call that reads nothing large. Today that is about six edits.
3. **Records ride in the work's commit.** The tool notes each event in a local pending file. `records commit "<subject>"`
   commits the work with the trailers written from those events. No separate commits for records, and no trailers typed by hand.
4. **Expensive work happens off the agent's turn.** The views, the status page and the full truth checks run in the Action after
   the push. The commit check looks only at the commit's own diff, in under a second. The brief runs once at the start.
5. **Nothing is copied.** The outcome log, proposal status lines, "Current as of", last touched, where the work is and the
   built state are all derived, so none is ever written.

**What a small ask costs, then:**
- a question answered: nothing;
- a fix: the commit;
- "flag it for later": one call (`records new L ...`);
- a numbered reply to the digest: one call per answer, in one commit.

## 11. Against today's proposals and spec

| Today | Holds | In this design | Gained | Lost or at risk |
|---|---|---|---|---|
| **Proposal** file (Status, Owner, Summary, The proposal, Why, Alternatives, Open questions, Affects, History, Sources) | the thinking: options, reasons, the record of revisions | kept as it is, as the narrative. Its Status covers the decision axis only; its open questions are its Q items (`parent:` the proposal), listed by the tool, not copied; its History gets a dated line from `records decide` | no more Status lines that lie about building (38 of 137 today); questions in one place, not in both the proposal and OPEN | nothing |
| **Outcome log** (proposals/README.md) | each idea's outcome by date | derived from the decision items and proposal states | no hand rows (96 commits touched the index since 1 Nov); no "?" dates | the log's one-line wording, written by hand today |
| **DECISIONS.md** | every decision, with source and what it replaces | the decision items; DECISIONS.md becomes their rendered view | a `rule` field written as the rule; `replaces` as an edge the tools follow | nothing: the same fields |
| **Spec "Decided" sections** (13% of the spec) | the current rules, citing decisions | still hand-written; the tool appends each new rule line and marks replaced ones | no decision left out of the spec | none, unless an agent never regroups the appended lines (cosmetic) |
| **Spec mechanics, parameters and checks** (87%) | how the engine works as built: tables, values, code pointers | untouched | (not addressed) | **still unchecked against the code.** A later check could hold the code pointers in these sections (`engine/renewal.py`) against the files, and the parameters against the data tables |
| **OPEN.md** (asks, conflicts, deferred) | one row each, grouped by area | items; OPEN.md rendered, grouped as now | one-step context from `show`; defaults with dates; parents | the convenience of one file to scan by hand, which the rendered view keeps |
| **WORK.md** | threads | thread items with `next`; WORK.md rendered | the next step, the branch and last touched, kept true | nothing |
| **Session notes** | long analysis | kept; plan and issue lists in them tagged with ids | lists that become rows | nothing |
| **The board** | talk between sessions | hand-offs only (Q-64 (4)) | | its status table, which was already stale |

**Improving?** On every point 02zzp measured: lost upkeep, untrue statuses, branches unseen, asks never put to Zach. The thinking
(proposals, session notes, the spec's mechanics) is untouched.

**The one real gap** is that the spec's mechanics can drift from the code with nothing to notice. That was so before as well,
and it is the next thing to check once this is built.

## 12. Documents in the web, and reading without losing things

Zach (20 Nov): "show the directly relevant things in full, show potentially connected things as summaries or at least small
descriptions / mentions of the edges so that you know they exist ... explore like a directory cd ls"; "I don't think everything
can be appropriately stored in short decision statements ... each contains the appropriate metadata so that when something
relevant is explored the existence of the doc pops up ... deeper documents are things pinned to and caught up in the web".

**One kind of node.** Spec files, proposals, session notes, run reports and briefs stay where they are, as long documents. Each
gains the same flat header as an item:
- `id` (its path);
- `kind` (spec, proposal, note, report, brief);
- `title`;
- `summary` (two or three lines on what it holds, not on its status);
- `threads`;
- `area`;
- for a proposal, its decision state.

The decisions a document reflects, and the documents and items that mention it, are read from its text. **A small node is an
item; a large node is a document. The schema is the same,** so a query about a thread or an area finds the documents pinned to it
as readily as the asks.

**What a query shows, by level:**

| Level | Shown | Why |
|---|---|---|
| the node asked for | in full if it is an item; if a document, its header, summary and outline (its headings), and its decided lines and open questions in full | prose is read by opening the file; what binds (rules) and what is open (asks) must never hang on a summary |
| its direct links | one line each: id, kind, state, title, and the edge type; grouped by edge type, with counts | to know they exist, and what they are, without reading them |
| what mentions it | titles, counted | the backlinks |
| further | nothing; `show` that node | stays bounded; exploring is a step at a time, like `cd` and `ls` |

**The verbs for exploring:**
- `records show <id>`: the node, as above;
- `records ls <id>`: its children and links, one line each;
- `records tree <thread>`: the sub-threads, items and documents under a thread;
- `records area <name>`: every live decision in the area, in full, and every document and open item in it, one line each;
- `records find <words>`: titles, summaries and text.

A list is never cut silently: past its limit it ends "and 12 more: `records ls W-62 --all`".

**So that decisions do not fall away.** Recall is made by construction and checked; it does not depend on the query being clever:
- every live decision has an area, and `area` lists all of them in full;
- every open ask and promise has a parent, and its thread's `tree` lists it;
- the push check flags **orphans**: a decision with no area, an item with no parent, a document with no thread or area;
- the push check flags **dead ends**: a thread whose decisions are not reachable from its documents.

**Summaries go stale too.** A summary says what a document holds, not its state; states are always derived. The push check flags
a document whose body has changed a lot since its summary was last edited ("summary may be stale"). The brief lists these for
their owner.

**Moving the existing documents across:** about 410 documents (67 spec files, 141 proposals, about 200 session notes).
- The spec files and proposals get headers in one pass: a script drafts each from the file's title, owner and the ids it
  mentions; the summaries are written by hand or by an agent and checked.
- Session notes get one when next touched. Until then the tool shows the first heading in place of a summary.

**Example** (`records show W-66`, from today's records):

```
W-66  thread  waiting  37.2  "The design of the records and the workflow"
  next: Zach's answers to Q-64 and Q-63; then W-65 builds it
  parent: (root)       touched: 20 Nov (9ce7011)     branch: none
  waits_on  Q-64 ask open "How the records, the scripts and git carry the design" (13 choices)
            Q-63 ask open "A commit schema and ids for threads"
  blocks    W-65 thread waiting "Tracking threads automatically"
  docs      proposals/records_and_workflow.md  proposal discussion  "How documents are stored, staged ..." 
            proposals/thread_tracking.md       proposal discussion  "A registry, hooks, checks and a commit schema"
            review/37_growth/02zzq_...md       note                 "The records as measured; how Zach works well"
            review/37_growth/02zzp_...md       note                 "What was started and left, 22 Oct to 19 Nov"
  mentioned by  3 (OPEN Q-61, Q-63, Q-64)
```

## 13. Freshness against the edges, typed commits, and how far from built

Zach (20 Nov): "Each thing should be clear when it was last updated vs comparison to the edges to it were last updated. And the
commits should have types: e.g building code could label which things it edits ... One derived measure could be like shortest
path to last built commit ... or is that too much?"

**Freshness.** Every node shows its last update, read from git. Each of its links shows the linked node's last update too, and
the node is flagged when a link is newer than the node itself:

```
proposals/climate_from_land.md  proposal  discussion   updated 17 Nov
  ! 2 links newer: engine/climate.py (built 19 Nov, 3 commits), D2-231 (19 Nov)
```

- **Not every newer link means stale.** The flag is a count shown at the place, not an error.
- **Reviewing clears it without editing.** An owner who has read the newer links and found nothing to change sets `reviewed:` in
  the header, and the flag counts only what is newer than that.
- **Documents name the code they describe.** A spec file's mechanics name their code (`describes: engine/renewal.py`), and the
  same freshness test applies. When the code has commits after its spec file, the file shows "code newer by 4 commits". This
  closes the gap left open in §11: the 87% of the spec that describes mechanics now notices when the code moves.

**Commit types.** The subject starts with a type and the main thread: `build W-48: the weir's gap downstream`.

| Type | Means | Must touch |
|---|---|---|
| `design` | proposals, session notes, briefs | docs |
| `decide` | decisions recorded | a new decision item |
| `build` | new code or data | `cybertron2/`, `c2viz/` or `specs/` |
| `fix` | a fault mended | code, and an item naming the fault |
| `run` | a run made, stopped or published | a run item |
| `record` | records only (asks, threads, offers, statuses) | items only |
| `upkeep` | hygiene, links, wording | anything; no thread needed |

- **Inferred, then corrected.** `records commit` takes the type from the paths changed (code means build, a new decision means
  decide, only items means record), and the agent corrects it where the intent differs (build or fix). The commit check holds
  the type against the paths.
- **`Builds:` says what the code implements.** A build or fix commit names the decisions and threads it implements (`Builds:
  D2-229, W-48`). A decision's built state is then a fact with a commit behind it, not an inference, and its "built" line shows
  the commit and whether it is on main.
- **Recent commits are a query.** "The latest commits in this thread or its direct links" is `records log <id>`, one line each:
  date, type, subject.

**How far from built.** Two plain measures, in place of a shortest path:
- **per decision:** built or not, by which commit, and whether that commit is on main;
- **per thread:**
  - the date of its last `build` commit;
  - how many of its decisions are unbuilt;
  - its branch's commits not on main.

A shortest path in hops measures how densely people link more than how far work is from code. A single `relates` edge would put
most things two hops from a build. The question behind it, "how much of what we decided is real", is answered directly by
unbuilt decisions per thread and area. That is the 22 to 24 Oct failure (gates, ledgers, tools decided, never built) made
visible. `records area` and the brief list unbuilt decisions with their age.

## Open questions

OPEN Q-64:
1. The store: one file per item (B, recommended), keep the tables (A), or the registry (C)?
2. Merge early behind switches, with Zach's go on switching on rather than on merging?
3. Views rendered only by the bot and never edited by hand?
4. The board for hand-offs between sessions only, with no status table (§6)?
5. The ask digest as Zach's interface: at most about 8 asks, each one choice with a recommendation and a default date, at the
   start of each burst and on demand (§6)?
6. The spec's decided lines written by `records decide` into the hand-written spec, with replaced lines marked and refused until
   rewritten (§3; revised from rendering the whole spec)?
7. Any session may change code on a thread branch, with the area's owner named on the merge (§5)? This replaces the 37.4-only
   rule.
8. A sheet of changes from the defaults before every paid run and every brief handed over (§4)?
9. The items as a small graph (§9): flat headers, five edge types (`parent`, `blocks`/`waits_on`, `replaces`, `decides`,
   `relates` with a reason), mentions as free links, `show` one step deep?
10. Files in the repository with one script and a skill (recommended), or GitHub Issues?
11. A soft limit on active threads for each owner, flagged in the brief (about 6)?
13. The rules for weight (§10): record only what outlives the turn; one call per event; records in the work's commit, with
    trailers written by the tool?
14. Documents as nodes (§12): a flat header with a summary on every spec file, proposal and session note; a query showing
    the node in full (a document's decided lines and open questions in full, its prose as summary and outline), its links one
    line each, nothing further; orphan, dead-end and stale-summary checks?
15. Freshness (§13): each node's last update against its links', a "links newer" count with `reviewed:` to clear it, and
    `describes:` on spec files so code newer than its spec shows?
16. Commit types in the subject (`build W-48: ...`; design, decide, build, fix, run, record, upkeep), inferred from the paths and
    corrected by the agent, with `Builds:` naming what code implements; "how far from built" as unbuilt decisions per thread and
    area and the last build's date, not a shortest path?
12. Ids written as `[[Q-63]]` in the items, so the folder opens in Obsidian with its links and graph, or as plain ids that only
    the tool links?

## Affects

Every session's habits (CLAUDE.md's work rules); `tools/` (hygiene folded into `records`); `.claude/settings.json`;
`.github/workflows/`; OPEN.md, WORK.md, DECISIONS.md and proposals/README.md, which become views; 37.4's branches and merges.

## History

- 20 Nov 2026: §13 added after Zach: freshness against links (with `reviewed:` and `describes:`, which also covers the spec's
  mechanics against the code), commit types with `Builds:`, and unbuilt decisions in place of a shortest path. Q-64 (15), (16).
- 20 Nov 2026: §12 added after Zach: documents are nodes with the same header as items; queries show by level (in full, then
  one line, then nothing); recall made by construction (areas, parents) and checked (orphans, dead ends, stale summaries); the
  example of `show`. Q-64 (14).
- 20 Nov 2026: §10 (keeping it light) and §11 (against today's proposals and spec) added after Zach's questions on latency and on
  what is lost. §3's spec rendering replaced by the tool writing decided lines into the hand-written spec, since the decided
  sections are 13% of the spec's words. Q-64 (6) revised; (13) added.
- 20 Nov 2026: §9 added after Zach's questions on a tool, edges and a graph: flat item headers, five edge types, a one-step
  query, one script and a skill (no MCP server, no database), the ideas borrowed, GitHub Issues weighed; Q-64 (9) to (12).
- 20 Nov 2026: §6 written from 02zzq §2 (how Zach works well). This added the ask digest, the spec rendered from decisions, the
  pre-run sheet, an area page before designing, code changed by any session on thread branches, and plain words.
- 20 Nov 2026: written by 37.2 at Zach's request, after 02zzp and thread_tracking.md.

## Sources

docs/review/37_growth/02zzp_audit_of_paths.md and 02zzp_audit/; 02zzq_records_and_workflow.md; docs/cybertron2/README.md;
tools/hygiene.py; `git log` and the branches on 20 Nov.
