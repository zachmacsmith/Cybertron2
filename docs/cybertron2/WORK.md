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
| W-2 | Build briefs 2 and 3, the 20 dry test arms, the spring live run (wild_raiders_and_works.md, carcass_and_decay.md, 02zy) | 37.4 | active | 9 Nov | 9 Nov | branch `ecology-raiders` (from `ecology-methods`) | brief 2 begun. Left: brief 2 and its gate, the 20 dry arms, the spring live run (D2-207); brief 3; the late-summer live run needs Zach's go |
| W-3 | Records restructure: WORK.md, OPEN.md's kinds, CLAUDE.md's rule, hygiene's stale checks, the sorting draft (02zz) | 37.2 (session "Thicker economy exploration") | active | 9 Nov | 9 Nov | main: docs/cybertron2/WORK.md, OPEN.md, CLAUDE.md, tools/hygiene.py, docs/review/37_growth/02zz_open_sorting.md | in this commit; left: Zach checks 02zz's sorting, then the rows move |
| W-4 | wild_behaviour.md v3 (the per-kind designs, from 02zv, 02zw and the briefs) | 37.2 | waiting | 9 Nov | 9 Nov | docs/cybertron2/proposals/wild_behaviour.md | waits on Q-32 (02zv §6, items still open) |
| W-5 | 37.2's own hygiene items: D2-199 to D2-203 into the spec; the scratchpad path in 02zp's sim.py | 37.2 | queued | 9 Nov | 9 Nov | spec/environment/wildlife.md; docs/review/37_growth/02zp_ecosystem_models/wildsys/sim.py | not begun |

## Paused

| # | Work | Owner | State | Started | Last touched | Where | Done so far; what is left |
|---|---|---|---|---|---|---|---|
| W-6 | Merging the wild layer into main | 37.2 with 37.4 | paused | 9 Nov | 9 Nov | branch `ecology` (24 commits each way from main; `climate-calibration` merged into it 8 Nov) | waits on briefs 1 to 3 and Zach; nothing merged yet |
| W-7 | The ecology branch's next steps: the calibration backlog, takes from the store, an engine experiment | 37.2 | paused | 8 Nov | 8 Nov | branch `ecology` | overtaken in part by the briefs; to sort after W-2 |
| W-8 | Couple the food web to 37.4's weather and climate | 37.2 | paused | 7 Nov | 8 Nov | branch `ecology` (wild/ecology.py reads the climate's values by place, D4-111, D4-113) | the hook is read; what is left to couple is to check after W-2 |
| W-9 | Compile the generator into spec/world/generation.md (OPEN L-101) | 37.2 | paused | 3 Nov | 3 Nov | docs/cybertron2/spec/world/generation.md | not begun beyond the flag; D2-173 to D2-191 are in no spec file |
| W-10 | 37.2's spec write-ups owed since 2 and 3 Nov (OPEN L-32, L-44, L-45, L-61) | 37.2 | paused | 2 Nov | 3 Nov | spec/economy/lodging.md, agreements.md, production.md, buildings.md | not begun |
| W-11 | Landscapes still to tune (OPEN L-100); the generator's `_spread` reach (L-51) | 37.2 | paused | 3 Nov | 3 Nov | cybertron2/landgen/ | not begun |
| W-12 | Forays (proposals/forays.md): the design's open questions; building after the core stages | 37.2 | paused | 9 Nov | 9 Nov | docs/cybertron2/proposals/forays.md | designed (discussion); waits on Q-33 and on briefs 1 to 3 |
| W-13 | Brookend survival world, rerun p2 (specs/make_plenty.py; D4-114's fixes) | 37.4 | paused | 8 Nov | 8 Nov | runs/p2_brookend (stopped at day 14, Zach); on the Hub | all lived to day 14; the harvest rotted unreaped (reaping 1/8 plot a unit). Left: rerun after the work costs fit the year (OPEN L-69, an ask) |
| W-14 | Claims and ownership by physics, part 2 (proposals/use_by_physics.md part 2) | 37.4 | waiting | 8 Nov | 8 Nov | docs/cybertron2/proposals/use_by_physics.md | the audit written (ten refusals, two physical gaps). Left: Zach's go on the small fixes (OPEN L-70) |
| W-15 | The land's fast stocks: soil water, snow, river flow, fuel dryness (D4-113's hook; 37.2's land fields) | 37.4 with 37.2 | waiting | 8 Nov | 8 Nov | names agreed with 37.2; land fields on `climate-calibration` | not begun. Left: Zach's go (OPEN L-71) |
| W-16 | The engine overhaul: phase 2's open decisions and phase 3's rest (review 38.64 §8; phase3_variance_and_risk.md) | 37.4 | paused | 8 Nov | 8 Nov | docs/review/38_space_engine/64_overhaul_breakdown.md | phases 1 and 2 built; phase 3: the weather scheduler, storms, place-required weather, base fertility, the renewal hook (D4-109 to D4-113). Left: OPEN L-72, L-73 |

## Done

| # | Work | Owner | Done |
|---|---|---|---|
| W-1 | Build brief 1: general methods (D2-204, D2-207); branch `ecology-methods`; gate and deviations in 02zx, defaults in OPEN Q-36 | 37.4 | 9 Nov |

## Size of unfinished work

Appended by `python3 tools/hygiene.py --record` (one line a run; counts: rows in progress, paused, open asks, deferred, and the
chores the report finds).

| Date | In progress | Paused | Asks | Deferred | Chores |
|---|---|---|---|---|---|
| 2026-11-09 | 5 | 7 | 27 | 62 | 122 |
