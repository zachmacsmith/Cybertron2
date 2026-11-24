# The fault table, checked against the engine (session stable, W-111, 24 Nov 2026)

The fault table of `proposals/stable_engine_for_runs.md` §2, each row checked against `main` at a6a8d855 and against this thread's
branch (`claude/busy-turing-v54rhu`). "Fixed" names the commit and its test. Probes are those of
`docs/review/37_growth/02zzzh_hunt_fish/wave_regressions_probes/`, run from the repository root with `PYTHONPATH=.`.

| Area | Fault | On main | Now | Record |
|---|---|---|---|---|
| Interface | acts and options not shown; techniques without what they do; one rules grammar; gear line; waiting today | confirmed (prompt_compare.md) | **fixed** by W-109, on main (c64c16f9) | W-109 |
| Interface and parse | World 0b's refusals ("sleep ... None", "to my hands", "wild food", "for my household", burial, "say", a lesson) | confirmed by 37.2's builder's probe ("sleep: there is no building called None here") | **fixed** by W-109 (c64c16f9) | L-189 (closed) |
| Old worlds | old water worlds cannot set traps | confirmed: river, lake, runs all "You have no wicker traps in hand" | **fixed** 07a58063: the five old water worlds seeded (D2-330 C5); `old_fishing_worlds.py` on runs.yaml "You set 6 wicker traps"; M6 gone from river's gate | Q-100 |
| Old worlds | `World()` runs worlds the gate refuses | confirmed | **fixed** e69a8979: refused at a run's start where anyone acts by a model (default taken: not in `World()` itself; Q-100's notes); waivers and `--ungated` said in the first line and run.json | Q-100 |
| Founders | other villages' households seeded as neighbours, also across unexplored places | confirmed (`wanted` gave an NB line for every household in the world) | **fixed** 26db8874 (D2-349): neighbours in one's village; a line of their own in a known village; none for an unknown one | D2-349 |
| Founders | fisher lines assume an eel run on any water | confirmed (`_runs_here(c, "eel")` returned True everywhere) | **fixed** 26db8874: the runs read from the world's land as the engine runs them, at a water parcel on the river; salmon, lamprey and the mill's line reachable at last. Eelmouth's lines unchanged | L-187 |
| Founders | the farmer's seed lines set seed per plot too high | **not an engine fault**: FA3 and HH2 state the engine's `plot_seed` (16 kg a plot). World 0b holds 32 grain against six plots' 96 | closed (agent), for World 0b's design | L-185, Q-105 |
| Herds | an unnamed slaughter fell on a neighbour's herd | confirmed by bench | **taken** 7bf7b180 with bench's other fixes (reviewed; tests) | L-189 (closed) |
| Building | the cairn free | fixed on main before this thread (cfc21ab7) | probe `cairn.py`: "it needs 6 stone" three times | L-186 (closed) |
| Building | the wattle roof free (site material removed without its work) | not yet checked | stage 5's proper fix (D2-357: the work of getting it added to the units); open | D2-357 |
| Waters | the lamprey dies out at world build | confirmed: Eelmouth 18 of 19 spawning stretches with spawners, the runs world 20 of 21 (worse on longer rivers, sweep.md) | **fixed** 6584e3a1: pulses in flight at the history's end spawn where bound; 19 of 19, 21 of 21 | Q-101 |
| Waters | the lamprey's run sized by head waters only (bug 2) | confirmed in the data (`spawn` unset) | left; an ask (Q-106) | Q-106 |
| Waters | shallows 11.4 times too rich | not checked: benched by Zach, who doubts the figure | benched | L-191 |
| Waters | resident fish only from makers | confirmed (sweep.md bug 5) | W-112 (the overhaul) | W-108 |
| Signs | false ambient lines (cattle lowing with no herds, picks with nobody quarrying) | confirmed (`data.py` COVERS, emitted for every parcel of the cover) | **fixed** (D2-346): the pasture's and the rock's lines dropped (the herd's bundle and the quarrying rows say it when true); water over its stones only on a brook or river at low or normal flow; voices only with three or more there | D2-346 |
| Signs | an attend that finds nothing falls back to the ambient lines | confirmed (`resolve_target` returned "the place in general") | **fixed** (D2-346): a name inside the sentence is found (a person, a building, a parcel, a herd); nothing found shows nothing but one's own line. The design's own sentence waits on prompt.py (W-109) | D2-346 |
| Signs | river signs hand-written and Eelmouth-tuned | confirmed (wave_regressions 5) | open; W-103's design | L-187 |
| Checks | the gate check fitted and swallowing exceptions | confirmed | **in part** e69a8979: "in hand" passes only gear one can get; `_first_run_day` raises; the dead test gone. Left: M3 for traps only, M7's numbers written in, P14 reads the founders' words | L-187 |
| Bots | generic bots no longer work or make on old worlds | confirmed (wave_regressions 12) | **in part** b65d91ab: `run.bot_plan` by verb (valley_s5: 42 work acts and 6 makes in 2 days, against 0); `knowledge.doable`'s site filter left | L-188 |
| Small | smokehouse fire risk untold in the old prompt; plural household names; crumbs in the meal line; "about 1 meal" at the least | confirmed by the audits | **fixed**: the fire told (23c649bd), the Marshes and crumbs (b6369fe0), a take's meals (b68f86ba) | L-178, L-179 (closed), L-188 |

## Not in the table, found while checking

- World 0b's own gate report refuses it on P6 and P20, both from the graded goal line that D5-1 decided. With the gate now at a
  run's start, World 0b's files need `gate: {waive: {P6: ..., P20: ...}}` with the reason (sent to bench).
- World 0b's makers and specs are only on bench's branch, and bench reads World 0b as unfair as a benchmark (a late-summer start,
  the fishing village starving first in every arm): Q-105.

*Current as of 24 Nov 2026.*
