# Cybertron 2: notes for agents

A multi-agent LLM society engine on a graph of places (Python package `cybertron2/`, the engine in `cybertron2/engine/`, worlds in
`cybertron2/specs/`, visuals in `c2viz/`). Runs are published to the Hugging Face dataset `zachmacsmith/cybertron2-runs`.

This repository split from Cybertron 1 (https://github.com/zachmacsmith/cybertron) on 6 Nov 2026. The history before the split is
kept; the tag `archive/cybertron1-inherited` marks the last commit that still carries the Cybertron 1 package, docs and tests.
Model calls, the privacy scan and the dataset id that cybertron2 used from Cybertron 1 now live in `cybertron2/infra/`.

**Before designing any world or experiment, read `docs/scenario_design.md`** (lessons carried over from Cybertron 1): design from
leverage and dependence, never an all-Haiku society, goals as in-world aims and never scoring proxies, food binds without
dominating, and read any metric against a null arm and a qualitative end-state reading. The work packages for worlds that grow
are in `docs/review/37_growth/`.

## Work in progress, asks and what is left

Zach (9 Nov): "every time we start on something new it has to be added to the currently working and we can track how large the
unfinished work goes."

- **Starting anything new** (a task, a brief, a phase, a build, a review, a run): first add a row to `docs/cybertron2/WORK.md`, "In
  progress" (owner and session, started, where, what it is), then begin.
- **Stopping before it is done** (Zach turns to something else, a phase or a brief is left part-way, the session ends): update the
  row (state, last touched, what is done, what is left, where the work is), and move it to "Paused" if no one is on it.
- **Finished:** move the row to "Done" with the date. Dropped or deferred: say so there, and add a deferred row to OPEN.md.
- **A question for Zach** (a decision, an uncertainty, a choice made while building): a row in OPEN.md's open questions (asks). Going
  ahead on a default, write "default taken: ..." on the row and tell him.
- **A mechanic or system to flesh out later:** a row in OPEN.md's "Flagged for later (deferred)", with what it waits on.
- **Before designing in an area:** read its rows in OPEN.md and WORK.md, and the code that already does it; cite both.
- **Before ending a session:** run `python3 tools/hygiene.py`, fix what is yours, then `python3 tools/hygiene.py --record`.

## Visuals are drawn from the engine

Zach (24 Oct): any visualisation (maps, scenes, sprites, charts of a world) must be grounded in how the engine actually works.
Before drawing anything, study the physics it shows (places and the parcel graph, covers and resources, buildings, lots and
fittings, containers and goods, people and herds, verbs and their primitives, events, senses and noticing) from the code and
the spec, and build the visual framework from the general model up: a picture may only show what the state holds, at the
resolution the state has; anything the engine does not decide (a position inside a parcel, say) is a presentation choice,
named as one and kept deterministic. Take data tables (covers, items, fittings, techniques) from the engine, never re-invent
them. The c2viz grounding notes: `c2viz/ENGINE.md`.

## Senses are written to a guide

Before adding or changing what people can sense in cybertron2 (signs, bundles, noticing), read `docs/cybertron2/guides/senses.md`:
what senses are for, what makes a good sign (grounded in state, worth acting on, a change not a standing fact, a bundle across
senses, never an act or feeling the person did not choose), the checklist, and the measured evidence.

## cybertron2: where design work goes

Everything about cybertron2 (code, spec, proposals, notes) lives on `main` in this repository.
Full rules: `docs/cybertron2/README.md`.

| Layer | Holds | Where |
|---|---|---|
| **Spec** | only what Zach has **decided**, as current rules; never stale | `docs/cybertron2/spec/<area>/` |
| **Decisions** | every decision, numbered by session (D2-n, D4-n, ...), with what it replaces | `docs/cybertron2/DECISIONS.md` |
| **Proposals** | working thoughts: one file per idea, with a status and a dated history; kept after it is decided or rejected | `docs/cybertron2/proposals/` |
| **Open** | **asks**: open questions, decisions and uncertainties for Zach or an owner, and conflicts between documents; and **deferred** work: everything **flagged for later** (its own table), each with what it waits on | `docs/cybertron2/OPEN.md` |
| **Session notes** | long supporting material only: analyses, cost models, run reports, work logs | `docs/review/38_space_engine/` (37.4), `docs/review/37_growth/02*` (37.2) |
| **Work** | what is being worked on now, and what was started and left (in progress, paused, done) | `docs/cybertron2/WORK.md` |
| **Board** | talk between sessions, append only | `docs/coord/BOARD.md` |

**The path of an idea:**
1. **New idea:** write or extend a file in `proposals/` (status `discussion`; layout in `proposals/README.md`: Status, Owner,
   Summary, The proposal, Why, Alternatives considered, Open questions, Affects, History, Sources). Put long analysis or a model in
   your session notes and link it. If it touches another session's area, post on the board.
2. **Revised:** add a dated History entry saying what changed and why. Never rewrite history away.
3. **Zach decides,** in one commit:
   - add the decision to `DECISIONS.md` in your own series;
   - write the rule into the spec file you own, citing the decision number, and update the file's closing "Current as of" line;
   - mark the proposal `accepted: D-n` (or `partly accepted`), with a History entry;
   - add a row to the outcome log in `proposals/README.md`.
3a. **Built at Zach's request before it was written down** (he asks in conversation for something to be built now): build it, then
   in the same session write it up as a **retrospective proposal** (status `retrospective, accepted: D-n`): what was built, why (his
   words and the problem it answered), alternatives, what is still open, a dated History entry; then do step 3's records (DECISIONS,
   spec, outcome log). Nothing built is left without a proposal.
4. **Rejected or deferred:** mark the proposal `rejected` or `deferred` with the reason, add a History entry and a log row. Ideas
   for later go to a `deferred` proposal (economy: `proposals/economy_later.md`), never into the spec.
5. **Replaced by a later decision:** rewrite the spec text to the new rule (no struck-through history in the spec); mark the old
   row in `DECISIONS.md` "replaced by"; record the change in the proposal's History.

**Rules:**
- The spec says what, not why. Every spec rule cites a decision; parameters are `decided` or `calibrate`. Anything undecided goes in
  `proposals/` or `OPEN.md`, not the spec.
- Never edit another owner's spec section or proposal: propose on the board or add to `OPEN.md` under that owner. Code under
  `cybertron2/` is changed only by 37.4 unless agreed on the board.
- Ask Zach before treating anything as decided; a question he answers in conversation is a decision only when he states it.
- A session note that a proposal or the spec supersedes gets one line at its top pointing there; nothing is deleted.
- Small commits; `git pull --rebase` before every push. On a conflict in a shared log or index, keep both sides.
- Work logs record work, not decisions. Board posts stay short and cite decision numbers and file paths.
