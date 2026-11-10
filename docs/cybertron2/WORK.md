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
| W-2 | Build briefs 2 and 3, the 20 dry test arms, the spring live run (wild_raiders_and_works.md, carcass_and_decay.md, 02zy) | 37.4 | active | 9 Nov | 9 Nov | branches `ecology-raiders` (`f290e2c`) and `ecology-carcass` (`cc4d342`, from it) | brief 2 built and gated, 61 dry arms read, the spring live run done ($9.87); brief 3 built and gated (503 tests). Left: Zach's answers to Q-37 and Q-38; merging to `ecology` (Zach's go); the late-summer live run (needs Zach's go); brief 3's own live run if he allows one |
| W-3 | Records restructure: WORK.md, OPEN.md's kinds, CLAUDE.md's rule, hygiene's stale checks, the sorting draft (02zz) | 37.2 (session "Thicker economy exploration") | active | 9 Nov | 9 Nov | main: docs/cybertron2/WORK.md, OPEN.md, CLAUDE.md, tools/hygiene.py, docs/review/37_growth/02zz_open_sorting.md | in this commit; left: Zach checks 02zz's sorting, then the rows move |
| W-4 | wild_behaviour.md v3 (the per-kind designs, from 02zv, 02zw and the briefs) | 37.2 | waiting | 9 Nov | 9 Nov | docs/cybertron2/proposals/wild_behaviour.md | waits on Q-32 (02zv §6, items still open) |
| W-5 | 37.2's own hygiene items: D2-199 to D2-203 into the spec; the scratchpad path in 02zp's sim.py | 37.2 | queued | 9 Nov | 9 Nov | spec/environment/wildlife.md; docs/review/37_growth/02zp_ecosystem_models/wildsys/sim.py | not begun |
| W-21 | Proposals for Q-37 (a) and (d): graded damage to houses and camps by structure and weather, camps' shelter, growth and animals (proposals/shelter_damage.md); cats that choose where to live (proposals/cats.md) | 37.2 (session "Thicker economy exploration") | waiting | 9 Nov | 9 Nov | main: docs/cybertron2/proposals/ | written and sent to 37.4; waiting on Zach's decision (Q-37 a and d) |
| W-22 | Hunting against farming and gathering in generated worlds: food per unit of work by method, range, skill, familiarity and season (37.4's code on `ecology-raiders`), against the targets of 9 Nov; what needs calibrating | 37.2 (session "Thicker economy exploration") | waiting | 9 Nov | 10 Nov | docs/review/37_growth/02zzd_hunting_farming_ev.md | measured in four generated worlds (unarmed) and three (armed), with depletion runs; written up with seven calibration changes. Left: Zach's go on the changes (02zzd table), then 37.4's code and 37.2's ecology (pressure, game near people), then a rerun |
| W-27 | Build brief 4 (hunt_and_fixes.md, W-24): stage A the hunt over time, B shelter in levels, C the gates' fixes, D drying and salting; the gate | 37.4 | active | 10 Nov | 10 Nov | branch `ecology-calibrate` (`58bb2d3`, from `ecology-carcass` with `ecology` 6132861) | built and gated: 521 tests; 02zzd's harness on target in the wood around; losses x0.86; older worlds replay exactly (02zx, brief 4; OPEN Q-40). Left: Zach on Q-40 (and 37.2's Q-39); merging to `ecology` (his go); a live run if he allows one |
| W-26 | Build brief 5: river and water (K4 without fen and boats) | 37.2 (session "Thicker economy exploration") | waiting | 10 Nov | 10 Nov | docs/cybertron2/proposals/river_and_water.md | written (draft). Left: Zach's go after brief 4; 37.2 makes its two test worlds (two villages on one river; a lake village) with the land kept |
| W-25 | The world keeps its land (D2-208): the generator writes land.npz with every world and its hash; the engine loads it, keeps the run's changes on top; runs and the dataset keep it | 37.2 (generator) with 37.4 (engine, record, publish) | waiting | 10 Nov | 10 Nov | docs/cybertron2/proposals/land_kept.md | decided and written. Left: Zach on the how (tile size, past runs); 37.2's generator part; 37.4's engine and record part |
| W-28 | The Cybertron 2 website: home, runs page, run explorer with each day's messages; viewer files on the Hub so it runs with no server (static on Netlify) | site (c2viz, session "Cybertron website") | waiting | 6 Nov | 10 Nov | main: c2viz/site/ (viewer_publish.py, static.py, server.py, run.html, web/), netlify.toml; the Hub: `runs/<run>/viewer/`, `viewer/catalog.json` | built and pushed; viewer files for all 64 published runs uploaded (c2viz code_key ef4c0aa36282). Left: Zach sets up the Netlify site and the subdomain; `python -m c2viz.site.viewer_publish` after each publish (calling it from cybertron2/publish_hf.py is 37.4's to agree) |

## Paused

| # | Work | Owner | State | Started | Last touched | Where | Done so far; what is left |
|---|---|---|---|---|---|---|---|
| W-6 | Merging the wild layer into main | 37.2 with 37.4 | paused | 9 Nov | 9 Nov | branch `ecology` (24 commits each way from main; `climate-calibration` merged into it 8 Nov) | waits on briefs 1 to 3 and Zach; nothing merged yet |
| W-7 | The ecology branch's next steps: the calibration backlog, takes from the store, an engine experiment | 37.2 | paused | 8 Nov | 8 Nov | branch `ecology` | overtaken in part by the briefs; to sort after W-2 |
| W-8 | Couple the food web to 37.4's weather and climate | 37.2 | paused | 7 Nov | 8 Nov | branch `ecology` (wild/ecology.py reads the climate's values by place, D4-111, D4-113) | the hook is read; what is left to couple is to check after W-2 |
| W-9 | Compile the generator into spec/world/generation.md (OPEN L-101) | 37.2 | paused | 3 Nov | 3 Nov | docs/cybertron2/spec/world/generation.md | not begun beyond the flag; D2-173 to D2-191 are in no spec file |
| W-10 | 37.2's spec write-ups owed since 2 and 3 Nov (OPEN L-32, L-44, L-45, L-61) | 37.2 | paused | 2 Nov | 3 Nov | spec/economy/lodging.md, agreements.md, production.md, buildings.md | not begun |
| W-11 | Landscapes still to tune (OPEN L-100); the generator's `_spread` reach (L-51) | 37.2 | paused | 3 Nov | 3 Nov | cybertron2/landgen/ | not begun |
| W-12 | Forays (proposals/forays.md): the design's open questions; building after the core stages | 37.2 | paused | 9 Nov | 10 Nov | docs/cybertron2/proposals/forays.md | designed (discussion); split off as its own track (OPEN L-105, 10 Nov): the route module on the kept land (D2-208); waits on Zach |
| W-13 | Brookend survival world, rerun p2 (specs/make_plenty.py; D4-114's fixes) | 37.4 | paused | 8 Nov | 8 Nov | runs/p2_brookend (stopped at day 14, Zach); on the Hub | all lived to day 14; the harvest rotted unreaped (reaping 1/8 plot a unit). Left: rerun after the work costs fit the year (OPEN L-69, an ask) |
| W-14 | Claims and ownership by physics, part 2 (proposals/use_by_physics.md part 2) | 37.4 | waiting | 8 Nov | 8 Nov | docs/cybertron2/proposals/use_by_physics.md | the audit written (ten refusals, two physical gaps). Left: Zach's go on the small fixes (OPEN L-70) |
| W-15 | The land's fast stocks: soil water, snow, river flow, fuel dryness (D4-113's hook; 37.2's land fields) | 37.4 with 37.2 | waiting | 8 Nov | 8 Nov | names agreed with 37.2; land fields on `climate-calibration` | not begun. Left: Zach's go (OPEN L-71) |
| W-16 | The engine overhaul: phase 2's open decisions and phase 3's rest (review 38.64 §8; phase3_variance_and_risk.md) | 37.4 | paused | 8 Nov | 8 Nov | docs/review/38_space_engine/64_overhaul_breakdown.md | phases 1 and 2 built; phase 3: the weather scheduler, storms, place-required weather, base fertility, the renewal hook (D4-109 to D4-113). Left: OPEN L-72, L-73 |

## Done

| # | Work | Owner | Done |
|---|---|---|---|
| W-28 | Build brief 4b written (hunt_followups.md): wariness, history by distance, recovery with a lag, births through the season, carrion drawing eaters; declared hunting parties, led beasts | 37.2 | 10 Nov: written, revised with Zach, sent to 37.4 |
| W-24 | Build brief 4 written (hunt_and_fixes.md) | 37.2 | 10 Nov: written and handed over; built by 37.4 as W-27 |
| W-23 | A benchmark by living descendants on a ladder of worlds (proposals/descendants_benchmark.md) | 37.2 | 10 Nov: proposal written; deferred by Zach as a major item to come back to (OPEN L-104) |
| W-20 | Paired probes, round 3: Fable 5.1 (docs/review/37_growth/02zzc_fable_versions.md) | 37.2 | 9 Nov: six runs ($24.71) and reported |
| W-19 | Paired probes, round 2: a full LLM cast, Fable 5.2 (02zzc) | 37.2 | 9 Nov: six runs ($16.86) and reported |
| W-18 | Small paired probes, Fable 5.2 against Opus 5.5, three situations (docs/review/37_growth/02zzb_fable_opus_pairs.md) | 37.2 | 9 Nov: six runs ($5.33) and reported |
| W-17 | A Fable 5.2 probe in run 6's world (docs/review/37_growth/02zza_fable_probe.md) | 37.2 | 9 Nov: run ($10.81) and reported |
| W-1 | Build brief 1: general methods (D2-204, D2-207); branch `ecology-methods`; gate and deviations in 02zx, defaults in OPEN Q-36 | 37.4 | 9 Nov |

## Size of unfinished work

Appended by `python3 tools/hygiene.py --record` (one line a run; counts: rows in progress, paused, open asks, deferred, and the
chores the report finds).

| Date | In progress | Paused | Asks | Deferred | Chores |
|---|---|---|---|---|---|
| 2026-11-09 | 6 | 11 | 30 | 62 | 122 |
