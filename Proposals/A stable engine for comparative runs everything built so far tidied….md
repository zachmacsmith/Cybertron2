---
id: docs/cybertron2/proposals/stable_engine_for_runs.md
kind: proposal
updated: "2026-11-24"
---
# A stable engine for comparative runs: everything built so far tidied, usable and pinned

*proposal · discussion (24 Nov); scope settled by Zach (Q-101, Q-100); being built on W-111 · `docs/cybertron2/proposals/stable_engine_for_runs.md`*

> the engine as it stands tidied, usable and pinned for comparative runs between models: faults fixed with module tests, no silent failure, other sessions' fixes merged, the records reconciled, a tag


**Status:** discussion (24 Nov 2026), opened at Zach's ask; scope settled by Zach ([[Q-101 The two priority threads' scope|Q-101]], [[Q-100 Old water worlds|Q-100]]); acceptance for him to confirm.
**Owner:** session stable (from 24 Nov; 37.2 handed over). **Thread:** [[W-111 Priority thread a|W-111]] (priority thread a).
**Runs it serves:** comparative, longer-term monoculture runs between models (session bench's World 0b, W-201 to W-203, and others).

## Start here (for the agent taking this thread)

1. Read CLAUDE.md, `docs/scenario_design.md`, `docs/cybertron2/spec/process/how_we_work.md` (the process rules, [[D2-353 Everything new in the engine is built within the agreed architecture…|D2-353]] to [[D2-357 D2-306 as meant|D2-357]]
   among them), and this file.
2. `python3 tools/records.py surface [[W-111 Priority thread a|W-111]]` and `records status`: everything tagged to this thread.
3. The evidence of what is broken, in order of use: the wave's regression audit
   (`docs/review/37_growth/02zzzh_hunt_fish/wave_regressions.md`), the act-by-act prompt comparison (`.../prompt_compare.md`),
   the gaps audit (`.../build_gaps.md`), session bench's World 0b failures (branch `claude/fervent-carson-601q18`,
   `docs/review/39_monoculture/prompt_audit.md` and `w0b_failures.md`), the waters reads (`docs/review/37_growth/02zzzl_waters_calib/
   generality.md`, `sweep.md`), the signs survey (`docs/review/37_growth/02zzzk_signs_audit/survey.md`).
4. What is in flight: the interface rebuild ([[W-109 The prompt's interface restored|W-109]], branch `w109-interface`, brief `.../iface_brief.md`) is being finished by a
   37.2 builder; it is the first item of this thread and 37.2 reviews and merges it, then hands over.

## Summary

Zach (24 Nov): "Everything that has been built so far needs to be tidied up and usable so that I can run experiments on the
current engine version as desired." The fishing, hunting and materials wave ([[W-73 Fishing, hunting and their materials developed together|W-73]]) left the engine with an interface that hid acts,
regressions in old worlds, half-built decisions and fitted mechanisms, several found only by chance. This thread makes the engine
as it stands trustworthy for experiments, without new content: fix what is broken, finish what was half built where a run would
meet it, stop silent failures, and pin a version that runs use while the architecture overhaul ([[W-112 Priority thread b|W-112]]) proceeds.

## The proposal

### 1. Freeze new content
No new features until this thread's acceptance is met. Stage 5 (works, [[W-106 Stage 5 of the wave, works|W-106]], paused on `w85-s5-works`) and stage 5b's feature
parts ([[W-107 Stage 5b of the wave, the gaps closed|W-107]]) wait; stage 5b's fault parts move here (below). Live run 2 waits.

### 2. Fix what is broken (each with a test of the module it touches, [[D2-355 Tests a change runs only the tests of the modules it touches|D2-355]])

| Area | Fault | Source | Record |
|---|---|---|---|
| Interface | acts and options not shown; techniques without what they do; sowing refused for an argument never shown; one rules grammar; gear line, source line, waiting today | prompt_compare.md; wave_regressions 2, 3, 10, 11 | [[W-109 The prompt's interface restored|W-109]] (in flight), D5-2, [[D2-350 Every act and every technique a person can take is registered with…|D2-350]] to [[D2-352 Familiarity and the interface|D2-352]], [[D2-356 A technique's name, what it does, what it needs and its working hints…|D2-356]] |
| Interface and parse | World 0b's refusals: "sleep ... None" made with no sleep asked, "to my hands" read as racks, "wild food" storing refused, "for my household" unread, burial unreachable, "say" among the acts, a lesson without fields | bench's w0b_failures.md | [[L-189 Interface and resolver faults from World 0b's refusals|L-189]] (in [[W-109 The prompt's interface restored|W-109]]'s brief) |
| Old worlds | old water worlds cannot set traps (nobody holds or can make one); `World()` runs worlds its gate check refuses | wave_regressions 1 | [[Q-100 Old water worlds|Q-100]] |
| Founders | other villages' households seeded as neighbours, also across unexplored places | [[D2-349 Founders' seeded lines about other households follow where they live…|D2-349]]; bench's L-202 | stage 5b part 3 item, moved here |
| Founders | fisher lines assume an eel run on any water | wave_regressions 8 | [[L-187 Regressions from the wave for stage 5b|L-187]] |
| Founders | the farmer's seed lines may set seed per plot too high (World 0b kept 96 grain against 32 held) | bench | [[L-185 The farmer's seed lines|L-185]] |
| Herds | an unnamed slaughter fell on a neighbour's herd; [[D2-304 An unnamed act on several of one's own things at a place|D2-304]] built only for several of one's own | bench, branch 1e799387 | [[L-189 Interface and resolver faults from World 0b's refusals|L-189]] note; review bench's fix |
| Building | site material removed without its work (the cairn, now 6 stone again; the wattle roof free) | [[D2-357 D2-306 as meant|D2-357]] | [[L-186 A cairn costs nothing since the wave|L-186]] |
| Waters | the lamprey dies out at world build (history's end clears runs in flight); shallows 11.4 times too rich (wrong clock, [[D2-273 Three clocks, each system on one|D2-273]]); resident fish only from makers | generality.md; sweep.md; ecosystems.md | [[W-108 The waters calibrated across many generated environments|W-108]] |
| Signs | false ambient lines (cattle lowing with no herds); an attend that finds nothing falls back to them; river signs hand-written and Eelmouth-tuned | signs survey; wave_regressions 5 | [[W-103 Signs and what people can know of the state of things|W-103]], [[D2-346 The signs design|D2-346]] |
| Checks | the gate check fitted to Eelmouth and swallowing exceptions; never run at world build | wave_regressions 9; build_gaps G70, G71 | [[L-187 Regressions from the wave for stage 5b|L-187]] |
| Bots | generic bots no longer work or make on old worlds (smoke coverage) | wave_regressions 12 | [[L-188 Smaller regressions from the wave|L-188]] |
| Small | smokehouse fire risk untold in the old prompt; wording bugs (plural household names, crumbs in the meal line); "food worth about 1 meal" at the least | wave_regressions 7; [[L-178 Wording bugs|L-178]]; [[L-179 Every take's line says 'food worth about 1 meal' at the least|L-179]] | [[L-178 Wording bugs|L-178]], [[L-179 Every take's line says 'food worth about 1 meal' at the least|L-179]], [[L-188 Smaller regressions from the wave|L-188]] |

The list is a starting point: the first task is to confirm each against main and add what the run worlds meet that is not here.

### 3. Merge what other sessions fixed in this code
Session bench's branch `claude/fervent-carson-601q18` (W-201 to W-203) holds fixes in 37.2's files: `verbs._try` (the partner read
from "target"), `book.py` GRAMMAR's `keep` wording and `_voice` (an orphaned household), `livelihoods.fill` (a specialism read
only from the living that has it), `farm._herd_on` (the slaughter's target). Review and merge them with bench.

### 4. No silent failure
- `World()` refuses a world its gate check refuses (or says so in the run's first line), never runs it silently.
- Every silent skip found (founders' skipped ids, an unknown cue key, a raising sign condition dropped, an attend's fallback)
  either raises or is reported where a person reads it.
- The interface coverage test ([[W-109 The prompt's interface restored|W-109]]) stays: every act and option shown to someone who can use it.

### 5. The records reconciled
Every "Not done" item in the stage reports (stage1 to stage5, fix_shapes, after_run1, lines, iface) is an open record; the 48
open asks triaged (`records digest`): answered, defaulted with Zach told, or moved to [[W-112 Priority thread b|W-112]].

### 6. A pinned version for experiments
When acceptance is met: tag the engine (`engine-runs-1`), record the tag in every run's metadata, and keep a maintenance branch for
fixes to it, so the overhaul on `main` does not change a running experiment. Each later fix to the tag says which runs it
invalidates.

## Acceptance (for Zach to confirm)

1. The run worlds Zach names (World 0b and its arms; Eelmouth; whichever else) each run a 6-day bot pass with no refusal the
   prompt does not explain, and a short live check (one model, a few days) whose refusals are read and each explained or fixed.
2. Every act and option is shown to someone who can use it (the coverage test); the replay of live run 1's and World 0b's replies
   parses as before or better, each difference explained.
3. Old worlds load, run and render as before the wave, or refuse with a reason.
4. The fault table above is closed or recorded with Zach's word.
5. The full suite passes once, at the tag.

## Why

Comparative runs between models are only worth their cost if the engine does not change under them and does not hide acts from
some models' agents. Today it does both.

## Open questions for Zach

Answered 24 Nov ([[Q-101 The two priority threads' scope|Q-101]], [[Q-100 Old water worlds|Q-100]]):
1. The experiment worlds are World 0b (its arms) and Eelmouth.
2. The freeze as written: stage 5, stage 5b's feature parts and live run 2 wait.
3. Old water worlds: both: their trappers seeded with traps and the craft as Eelmouth's fill does, and `World()` refuses what
   the gate check refuses (default taken: the recommended option chosen).
4. The waters: the lamprey is fixed here; the shallows' richness is benched: Zach doubts the figure ("I can't believe the
   shallows are 11.4 times too rich so maybe bench that"), so the claim is checked before any fix ([[L-191 The shallows' richness|L-191]]).

Still open: the acceptance list below.

## Affects

The engine's interface (`prompt.py`, `core.py`, `shapes.py`, `view.py`, `verbs.py`'s registry), `founders.py`, `livelihoods.py`,
`farm.py`, `world.py` (the gate at build), `landgen/gates.py` and `gate_check.py`, `signs.py`, `wild.py` (the history's end),
`wild/water.py`, the old world specs.

## History

- **24 Nov 2026:** opened by 37.2 at Zach's ask, from the week's audits, as one of two priority threads (with [[W-112 Priority thread b|W-112]]).
- **24 Nov 2026:** taken by session stable. Zach settled the scope: World 0b and Eelmouth are the experiment worlds; the freeze
  as written; old water worlds seeded and gate-refused worlds refused by `World()`; the lamprey fixed, the shallows benched ([[L-191 The shallows' richness|L-191]]).
- **24 Nov 2026:** built on [[W-111 Priority thread a|W-111]] (branch `claude/busy-turing-v54rhu`): the gate at a run's start, where anyone acts by a model,
  with waivers and `--ungated` said in the first line (default taken: at the run's start, not in `World()`, [[Q-100 Old water worlds|Q-100]]); the old water
  worlds' traps; the lamprey's spawners kept at the history's end; the founders' lines by the runs and by village ([[D2-349 Founders' seeded lines about other households follow where they live…|D2-349]]); the
  signs' bug fixes ([[D2-346 The signs design|D2-346]]); M7 firing; the engine tag in the run record (§6). The fault table checked:
  `docs/review/40_stable_engine/fault_table.md`; a first acceptance pass: `acceptance.md` there.

## Sources

The files named in "Start here"; `docs/cybertron2/proposals/w73_design/` (the wave's design set); `live1_report.md`;
`spring_gap.md`; `after_run1_report.md`; `lines_report.md`; `stage1_report.md` to `stage4_report.md`.
