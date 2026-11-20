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

**The spec is rendered from the decisions.** Each decision item carries its area (`spec: environment/land`) and the rule as
stated. A spec page is its area's live decisions in order, with the replaced ones left out. Hand-written prose stays possible
for structure (headings, a table that groups rules), but a decision is in the spec the moment it is recorded. This removes the
most-lost write in 02zzp: about 50 decisions in no spec file, and W-9 and W-10 not begun since 2 and 3 Nov.

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

## Open questions

OPEN Q-64:
1. The store: one file per item (B, recommended), keep the tables (A), or the registry (C)?
2. Merge early behind switches, with Zach's go on switching on rather than on merging?
3. Views rendered only by the bot and never edited by hand?
4. The board for hand-offs between sessions only, with no status table (§6)?
5. The ask digest as Zach's interface: at most about 8 asks, each one choice with a recommendation and a default date, at the
   start of each burst and on demand (§6)?
6. The spec rendered from the decisions (§3), with hand-written prose only for structure?
7. Any session may change code on a thread branch, with the area's owner named on the merge (§5)? This replaces the 37.4-only
   rule.
8. A sheet of changes from the defaults before every paid run and every brief handed over (§4)?

## Affects

Every session's habits (CLAUDE.md's work rules); `tools/` (hygiene folded into `records`); `.claude/settings.json`;
`.github/workflows/`; OPEN.md, WORK.md, DECISIONS.md and proposals/README.md, which become views; 37.4's branches and merges.

## History

- 20 Nov 2026: §6 written from 02zzq §2 (how Zach works well). This added the ask digest, the spec rendered from decisions, the
  pre-run sheet, an area page before designing, code changed by any session on thread branches, and plain words.
- 20 Nov 2026: written by 37.2 at Zach's request, after 02zzp and thread_tracking.md.

## Sources

docs/review/37_growth/02zzp_audit_of_paths.md and 02zzp_audit/; 02zzq_records_and_workflow.md; docs/cybertron2/README.md;
tools/hygiene.py; `git log` and the branches on 20 Nov.
