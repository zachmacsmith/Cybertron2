# cybertron2: work in progress and unfinished work

What every session is working on now, and what was started and left. Zach (9 Nov): "every time we start on something new it has to
be added to the currently working and we can track how large the unfinished work goes." The rules are in CLAUDE.md
("Work in progress"); `python3 tools/hygiene.py` reports what has gone stale here, and `--record` adds a line to the size log below.

**The four places for things not done:**

| Kind | Where | What moves it |
|---|---|---|
| **In progress**: started, and someone is on it (or waiting on an ask) | here, "In progress" | its owner carrying on |
| **Paused**: started and stopped, with something already made (a branch, a draft, half a phase) | here, "Paused" | a choice to resume, defer or drop it |
| **Asks**: questions and decisions for Zach (or another owner), uncertainties, conflicts needing a ruling | [OPEN.md](OPEN.md), open questions and conflicts | the answer; an agent going ahead on a default writes "default taken: ..." on the row |
| **Deferred**: mechanics and systems to flesh out properly later, not started | [OPEN.md](OPEN.md), flagged for later | Zach taking it up, or its trigger ("waits on") arriving |

Chores (spec write-ups owed, replaced decisions unmarked, rows done but not struck through) are not kept by hand: the hygiene
report lists them.

**A row:** `| W-n | what | owner (session) | state | started | last touched | where (branch, files) | done so far; what is left |`.
States: `active`, `waiting` (on an ask, named), `queued` (agreed, not begun), `paused`. When a row is finished, move it to "Done"
with the date; when it is dropped or deferred, say so there and, if deferred, add an OPEN row with its trigger. New rows take the
next number; 37.2 and 37.4 share the series (check before adding).

## In progress

| # | Work | Owner | State | Started | Last touched | Where | Done so far; what is left |
|---|---|---|---|---|---|---|---|
<!-- records:in_progress -->

## Paused

| # | Work | Owner | State | Started | Last touched | Where | Done so far; what is left |
|---|---|---|---|---|---|---|---|
<!-- records:paused -->

## Done

| # | Work | Owner | Done |
|---|---|---|---|
<!-- records:done -->

## Size of unfinished work

Appended by `python3 tools/hygiene.py --record` (one line a run; counts: rows in progress, paused, open asks, deferred, and the
chores the report finds).

| Date | In progress | Paused | Asks | Deferred | Chores |
|---|---|---|---|---|---|
| 2026-11-09 | 6 | 11 | 30 | 62 | 122 |
| 2026-11-12 | 13 | 11 | 33 | 64 | 122 |
| 2026-11-14 | 18 | 11 | 37 | 69 | 129 |
| 2026-11-16 | 26 | 11 | 43 | 70 | 155 |
| 2026-11-20 | 30 | 4 | 31 | 99 | 181 |
| 2026-11-21 | 30 | 4 | 34 | 99 | 185 |
| 2026-11-22 | 41 | 4 | 36 | 114 | 205 |
