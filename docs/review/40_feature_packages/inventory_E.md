# Inventory E: the day loop, the call, social, roads, fuse, generate, exchange

Slice: `cybertron2/engine/` run.py (1306 lines), evening.py (216), fuse.py (219), settle.py (247), agreements.py (441), roads.py (851),
generate.py (465), exchange.py (252). Interfaces only: journal.py, branch.py, api.py, converse.py. Callers: landgen/gates.py, capacity/model.py.
All line numbers are from the files as they stand on 16 Nov 2026. "F:" tags a feature; "K" means kernel. Read-only: nothing in the repo was changed.

Feature tags used below:
- K-sched: day scheduler and step keys
- K-call: model calls and responders
- K-jrnl: journal, checkpoints and branching
- K-rng: keyed randomness
- F-speech: say, tell and the talk waves
- F-know: explain, look_up, teach, learn and mentions
- F-notes: notes, open, pin and forget
- F-trade: offers, agreements and settlement
- F-house: households, join, admit, found and leave
- F-lodging: host, grant, revoke and sleep
- F-claims: claims and land legs
- F-theft: take, theft and thefts seen
- F-combat: attack, raid, guard, duel and settle_fights
- F-roads: roads, transit, stretches, landmarks, notices, finds, meetings and traces
- F-herds: herds and pack oxen on roads
- F-life: growing up, partner, try, care, births and children's work
- F-evening: the evening at the hearth, the meeting, `evening: plan`
- F-labour: units, overwork, fatigue and the walk
- F-percept: perception, the per-mind today and the signs
- F-memory: stretch memories, kept lines and memory_at_evening
- F-sched: world incidents and signs (environment/scheduler)
- F-layout: routes, hidden ways and parcels
- F-fuse: urgent night and road calls
- F-tags: names and tags (TG.render)
- F-view: the beliefs view (VW.turn)
- F-cap: day-0 capacity

---------------------------------------------------------------------------------------------------------------------------------

## 1. THE DAY

### 1.1 Module surface of run.py

| Lines | Name | What it is | K or F |
|---|---|---|---|
| 26-28 | `MAX_SAY=3`, `MAX_ACTIONS=10`, `WAVES=2` | caps on speech items, plan length, talk waves | K-sched (MAX_SAY is F-speech) |
| 38-40 | `blank_today()` | the shape of `w.s["today"]` (19 keys, see 1.3); also imported by landgen/gates.py:40 | the keys are F; the reset is K |
| 44-65 | `bot_plan` | scripted day plan (smoke tests). It knows verbs, items, roads and offers | K-call responder, with F knowledge inside |
| 68-84 | `bot_fuse` | scripted answer to an urgent call; an if-chain on the event kind (meeting, find, crossing, herd, split, else raid) | F-fuse |
| 87-117 | `Stopped`, `HumanTurn(turns)`, `UsageStop`, `Abandoned` | control-flow exceptions | K |
| 104-113 | `_week_stop(spec)` | reads `infra.llm.USAGE["windows"]["seven_day"]` against `llm.week_stop` or env `CYBERTRON2_WEEK_STOP` (default 0.9) | K-call |
| 120-133 | `Tally(frac, planned)` | counts calls and failures; raises `Abandoned` at `fail_stop_fraction` (0.5) of max(planned, calls) | K-call |
| 136-148 | `_recorded(...)` | answers a request from the journal; rebuilds the conversation; `J.check_message` | K-call/K-jrnl |
| 151-196 | `decide(w,name,text,opening,system,backend,conv,talk,schema,fuse,transit,kind)` | the one request function | K-call |
| 199-218 | `_parallel(fn, jobs, workers, tally)` | thread pool; collects errors; aggregates `HumanTurn` | K-call |
| 222-235 | `_guardian(w, child, names, node)` | who takes an offer made to a child (D4-55) | F-life/F-trade |
| 238-327 | `talk(w, names, replies, results)` | delivers say, tell, explain, offers, open and look_up; returns the boxes of those woken | F-speech/F-know/F-trade/F-notes |
| 330-359 | `_mentions(...)` | hearing a place, a hidden way or a craft named | F-percept/F-layout/F-know |
| 363-422 | `dawn(w)` | incidents (stray, death, fire), goods `left` found, `LF.dawn`, arrivals, spec signs | F-sched/F-life/F-roads |
| 425-439 | `arrive(w,name,t,dawn)` | a traveller comes in: RD.arrived, prims arrive and set, HD.arrive_with, LY.learn_way and wear_way, an event | F-roads/F-herds/F-layout/F-evening |
| 442-454 | `morning_departures(w,today)` | evening worlds: set off in the morning (D4-67) | F-roads/F-evening |
| 457-464 | `arrive_evening(w)` | those with `by_day` whose arrival day has come get in at nightfall | F-roads/F-evening |
| 467-553 | `evening_step(w,names,results,budget,used,talk_log,openings,systems,backend,conv,workers,tally)` | 12 arguments; the hearth call, then one answer wave; `memory_at_evening` folding; `plan_next` | F-evening/F-memory |
| 556-607 | `meeting_step(...)` | 11 arguments; a meeting called for the morning, up to `MEETING_WAVES=3` (set at line 610, after its use) | F-evening |
| 613-677 | `night_lines(w, rec)` | the night narration from the night record's keys | F-night/F-life/F-labour/F-fire |
| 681-716 | `fuse_calls(...)` | 12 arguments; urgent calls, meeting waves, `FU.answer`, `RD.settle_meeting` | F-fuse/F-roads |
| 720-722 | `CARRY` | the 27 local variable names of run() that are checkpointed as the runner's carry | K-jrnl (it names F state) |
| 725-738 | `_runner(J,cost,conv,scope)` | the runner checkpoint: cost, conversations (blobs above 200 chars), carry | K-jrnl |
| 741-759 | `_abandon` | fail-stop: `J.abandon_day`, writes STOPPED.md | K |
| 762-777 | `day0_capacity(spec)` | imports `capacity.model` inside the function; analyse on a deep copy; result to `J.meta("capacity")` | F-cap |
| 780-1163 | `run(spec_path,out_dir,backend,days,workers,bots,seed,until,mode,responders)` | modes: start, resume, replay, continue | K plus inline F |
| 1166-1306 | `main` | CLI: run, resume, replay, rewind, fork, continue, branches, export, import, publish, fetch, context, frames, play, serve, dump | K |

`TECHNIQUES` is imported at line 22 and never used.

### 1.2 The day, step by step (run.run, lines 861-1139)

Every step is `J.open_step(day, name)`, the step's work, then `J.commit(w.s, _runner(J,cost,conv,locals()))`. A step key is `d<day>.<name>`.

**Run setup (785-859). K.**
1. **Load the spec.**
   - `start`: `load_spec`. Applies `--seed`, `--days` and `--bots` (every model set to `"bot"`). `--as NAME=human|bot|model:<id>` sets `spec["agents"][n]["model"]`.
   - Other modes: the spec comes from `meta.spec` in the journal.
   - `continue`: `JN.checkpoint(src, at)` restores the world and the runner.
   - `replay`: copies run.db to a temp directory (WAL checkpoint first).
2. `w = World(spec)`. `World.__init__` installs `AG.install` (world.py:235), the after-hook on transfer that credits debts, and `BL.install` (overflow).
3. Initial `systems`. Writes run.json and opens the jsonl files (turns, days, perception, memory). `Conversations(out, chunk=memory.chunk or 3, backend)`.
4. Journal.
   - `start`: unlinks run.db, `J.start(spec, seed, responders)`, `J.meta("capacity", day0_capacity(spec))`.
   - `continue`: `J.meta("spec")` if `--days` was given.
   - Otherwise `J.resume(strict=replay)`.
5. `J.after_commit = lambda step: BR.after_commit(w,J,step)`. After each commit this applies the fork's salt and responders and the interventions.
6. `continue` also restores `cost`, `conv.c` (without sessions) and `last_system`.

**Per day:**

| # | Step key | Lines | In order | Feature | K or F |
|---|---|---|---|---|---|
| 0 | (before) | 862-865 | `_week_stop` unless replaying a committed dawn; raises UsageStop | K-call | K |
| 1 | `dawn` | 866-872 | `w.s["day"]=day`; `w.s["events"]=[]`; `today = w.s["today"] = blank_today()`; `dawn(w)`; `PC.dawn(w)` (perception of dawn events); commit | K-sched, F-sched/F-life/F-roads/F-percept | the reset is K; the rest is F |
| 1a | | `dawn()` 364-402 | `spec.incidents` for this day, an if per kind. **stray**: herd parcel set, crop drawn per holding (imports farm), stray event. **death**: `die` prim, event. **fire**: stock destroyed except vaulted (imports buildings), condition and `fire_hit` set, event | F-sched (it holds herds/farm/buildings/life logic) | F |
| 1b | | 403-407 | `w.s["left"]` from yesterday: "X left N item at B" events, dawn=True | F-trade/F-house (gifts at the door) | F |
| 1c | | 408-410 | `LF.dawn(w)`: growing up, coming of age, succession; appended to `w.s["life"]` | F-life | F |
| 1d | | 411-417 | arrivals: carried infants `apply("arrive")`; others `arrive(w,n,t,dawn=True)` | F-roads | F |
| 1e | | 418-422 | `spec.signs` for this day: `w.event(..., dawn=True)` per node | F-sched | F |
| 2 | `decide` | 873-903 | see the rows below | | |
| 2a | | | `names = w.agents_acting()`; `at_day` | | K |
| 2b | | | `systems` per name (`PR.system_prompt`) | | K-call |
| 2c | | | `turn = VW.turn if VW.on(w) else PR.turn_prompt` | F-view | |
| 2d | | | openings and users, each through `TG.render` | F-tags | |
| 2e | | | if `EVN.on`: `EVN.meeting_block` is spliced into openings and users by string-replacing "Plan your day. Reply with JSON only." | F-evening | F |
| 2f | | | if `EVN.plans_at_hearth`: those whose `people[n].plan_next.day==day` and not `EVN.needs_morning` are planned without a call; `today["skipped_morning"][n]=users[n]` | F-evening | F |
| 2g | | | `Tally`; `_parallel(decide)` for the others | | K-call |
| 2h | | | `first` is the replies; `results` starts with the error line; `PC.apply_notes` | F-notes | |
| 2i | | | commit | | |
| 3 | `talk.0`, `talk.1` | 904-935 | `woken = talk(...)`; for wave < `waves` (1 if evening, else WAVES=2): commit and open `talk.{wave}` when wave>0; `PR.talk_prompt`; `_parallel(decide, kind="talk")`; replies merged (actions replaced); `PC.apply_notes`; `late` is say, tell, explain and offers; `woken = talk(late)` | F-speech/F-trade/F-know | K: the waves; F: delivery |
| 3a | (in the last talk step) | 936-937 | if `EVN.on`: `meeting_step` (kind "meeting"; its calls are keyed under the last talk step) | F-evening | F |
| 3b | | 938 | commit | | |
| 4 | `work` | 939-1047 | see 4a to 4l | | |
| 4a | | 940-947 | `attend`, `plans` (MAX_ACTIONS); `spec.script` acts put first (dry runs) | K-sched | |
| 4b | | 948-949 | `order` shuffled by `w.rng("order", day)` | K-rng | K |
| 4c | | 950-955 | budget = `w.units_for(n)` - say units; `over_ok` from `replies[n].overwork` capped by `labour.over_units` | F-labour/F-speech | F |
| 4d | | 959-995 | interleaving by index then by order. Skip if dead, travelling tonight (`today.travel`), in `heavy`, or `travel_morning`. Morning travel must be the first act (evening). A refused signature is not tried again (D4-97). `V.cost` then `V.do`. `"Refused: travel: you carry"` goes to `heavy` | K-sched loop; F-evening, F-roads, F-labour checks inline | mixed |
| 4e | | 996-1018 | units left over go to the `fallback` acts (max 3, no travel) | K-sched (D4-76) | |
| 4f | | 1019-1034 | `heavy`: `PR.lighten_prompt`, `_parallel(decide, kind="lighten")`, then only give, leave, move and travel are done | F-roads (transport D4-32) | F |
| 4g | | 1035-1042 | tidy results: repeats, "units unused", "pushed on" | F-labour | |
| 4h | | 1043-1044 | `morning_departures` if `today.travel_morning` | F-roads/F-evening | F |
| 4i | | 1045-1046 | `LY.routes(w, today)` sets `today["route"]` (function-level import of layout) | F-layout | F |
| 4j | | 1047 | commit | | |
| 5 | `evening` (only `evening:` worlds) | 1048-1057 | `PC.evening(w, attend, today)` (the day's noticing) gives `today["day_seen"]` and perception.jsonl `phase: day`; `evening_step(...)` gives `folded` memories to memory.jsonl; commit | F-evening/F-percept/F-memory | F |
| 5x | (between steps) | 1058-1059 | `LA.close_day(w, today, used, budget, names)` runs after the work or evening commit and before `open_step(settle)`. Its `set` changes are journaled under the already-committed step | F-labour | F |
| 6 | `settle` | 1060-1068 | see 6a to 6f | | |
| 6a | | | `today["partners"] = LF.settle` (D2-140) | F-life | F |
| 6b | | | `today["children_work"] = LF.children_work` (V.do for children) | F-life | F |
| 6c | | | `settled = AG.settle(w)` | F-trade | F |
| 6d | | | `ST.settle_teaching` and `ST.settle_joins` lines appended to results | F-know, F-house | F |
| 6e | | | `ST.settle_thefts(w, today, attend)` | F-theft | F |
| 6f | | | `w.s["left"]` rotated (direct write, not a prim); commit | F-trade | F |
| 7 | `night` | 1069-1091 | see 7a to 7i | | |
| 7a | | | `N.departures(w, today)`: depart prim, `home_seen`, pack ox, infants carried, `today["_departed"]` | F-roads/F-herds/F-life | F |
| 7b | | | `road_rec = RD.night(w, today)`: `today["road"]` = meetings, finds, crossings, herds, splits, fed, camp | F-roads | F |
| 7c | | | `woke = FU.plan(w, today)` | F-fuse | F |
| 7d | | | `last_system.update(systems)`; if woke: `fuse_calls(...)` | F-fuse | K-call inside |
| 7e | | | `rec = N.night(w)`. Inside: `ST.settle_fights` (reads the fuse's today keys) → sleeping → fires → eating → `LF.night` → decay → breaks → grow → `LA.fade` → `FM.night` → **offers lapse** (night.py:203-208) → `s["log"].append(rec)` | F-night (many) | F |
| 7f | | | `rec["fuse"] = FU.record(today)`; `rec["road"] = road_rec` | | |
| 7g | | | `per = PC.evening(w, attend, today, skip=day_seen)` | F-percept | |
| 7h | | | `nights = night_lines(w, rec)`; cost summed from meta and talk_log usage; turns.jsonl per name; `PC.close_day(w,n,results,nights)` | K (log) + F-percept | |
| 7i | | | commit | | |
| 8 | `memory` | 1092-1133 | see 8a to 8h | | |
| 8a | | | `ending` = alive, `conv.ends(n, day)`, not the last day, not `today.memory_done` | F-memory | |
| 8b | | | prompt: `MEM.request` (rewriting) or `PR.memory_prompt`, plus `MEM.kept_request` | F-memory | |
| 8c | | | `decide(kind="memory", schema=the frozen conv schema, transit=True)` | K-call | |
| 8d | | | `MEM.keep` or `PC.own_memory`; `MEM.kept_apply`; memory.jsonl | F-memory | |
| 8e | | | perception.jsonl | | |
| 8f | | | `rec.update(cost_usd, talked, offers, agreements_made, settled, teaching, learning, joins, admits, watch, thefts, attend, errors)` | K-log with F keys hard-coded | |
| 8g | | | `extra_cost` added; road turns; days.jsonl; flush; commit | | |
| 8h | | | print a summary line (missed, deaths, agreements, taught, thefts, born) | F names hard-coded | |
| 9 | | 1138-1139 | `break` if no one is living | K | |

The exceptions at 1141-1152: `JN.Paused` prints. `Abandoned` calls `_abandon`. `HumanTurn` gives a "waiting for" message. `UsageStop` writes STOPPED.md. Then at 1153-1163: save state.json unless stopped, `J.meta("ended")` if finished, close everything, and return the replay report or the out path.

Which steps are named where: run.py uses dawn, decide, talk.N, work, evening, settle, night, memory. Request kinds in the journal: decision, talk, meeting, lighten, evening, fuse, memory. execution.md:17 and round.md list no `evening` step, and `branch.STEPS` (branch.py:24) lacks it too (see section 10).

### 1.3 The `today` record (`w.s["today"]`, checkpointed world state, reset at dawn)

`blank_today()` keys come first (marked "init"); then the keys that are added during the day. `here.today()` (here.py:483) returns `w.s["today"]`.

| Key | Init | Written by | Read by | Feature |
|---|---|---|---|---|
| `worked` {n:[keys]} | init | verbs `_site`/`_technique` 447-518, `_at_work` 928 | perceive 477-559, things 26-41/293, layout 82, settle_thefts (at_home) | F-work/F-percept |
| `thefts` [{by,building,item,qty,door}] | init | verbs `_take` 1307 | ST.settle_thefts; run 1124 (rec); print | F-theft |
| `left` [{by,item,qty,building}] | init | verbs `_into_store` 1384 | run 1067, which copies it to `w.s["left"]` for tomorrow's dawn | F-trade |
| `joins` [{by,household}] | init | verbs `_join` 1484 | ST.settle_joins; EVN._requests; rec | F-house |
| `admits` [{by,person,household}] | init | verbs `_admit` 1496 | ST.settle_joins; rec | F-house |
| `sleep` {n:bid} | init | verbs `_sleep` 1586; evening.apply 152 (host guest) | night.sleeping_places; evening.gathering | F-lodging |
| `travel` {n:to} | init | verbs `_travel` 1638 | run work loop; EVN.who_is_called; FU raid detect; N.departures; morning_departures | F-roads |
| `watch` {n:who} | init | verbs `_watch` 1659 | perceive 361-499; settle_thefts; rec | F-know/F-percept |
| `teach` / `learn` | init | verbs `_teach` 1672 / `_learn` 1683 | ST.settle_teaching; rec; print | F-know |
| `fights` [{kind,by,target or building,aim,node}] | init | verbs `_attack` 1692/1699 | fuse `_raids`; ST.settle_fights (night.py:28) | F-combat |
| `guards` {n:bid} | init | verbs `_guard` 1708; fuse `_defend` | fuse detect; settle_fights; labour | F-combat |
| `fire` {n:True} | init | verbs `_fire` 1725 | night.open_fires; roads.leave_traces (ashes) | F-fire/F-roads |
| `partner` [{by,with}] | init | verbs `_partner` 1839 | LF.settle; EVN._requests | F-life |
| `try` [{by,with,units}] | init | verbs `_try` 1866 | life `_conceive` 357; EVN._requests | F-life |
| `care`, `care_by`, `care_gift` | init | verbs `_care` 1893-1900 | life.care_gifts 184 and others | F-life |
| `route` {n:[parcels]} | init | LY.routes (run 1046) | labour.close_day; layout.passed; views.frames | F-layout |
| `travel_morning` {n:to} | added | verbs `_travel` 1636 | run 961, 987, 998, 1043; morning_departures | F-evening/F-roads |
| `travel_choices` {n:{...}} | added | verbs `_travel` 1641 | N.departures | F-roads |
| `skipped_morning` {n:text} | added | run 893 | evening_step 499 | F-evening |
| `day_seen` {node:[texts]} | added | run 1051 | run 1079 (PC.evening skip) | F-percept/F-evening |
| `memory_done` {n:True} | added | evening_step 535 | run 1094 | F-memory |
| `partners`, `children_work` | added | run 1061-1062 | nothing in the slice (kept for the record) | F-life |
| `drawn` [...] | added | verbs `_drawn` 334 | verbs (what was taken from stores, D4-96) | F-work |
| `turned`, `green_cut` | added | farm 1089, 1144 | farm | F-farm |
| `units` {n:{used,over}} | added | labour.close_day 65 | night (labour.work_need) | F-labour |
| `road` {meetings,finds,crossings,fed,camp,herds,splits} | added | RD.night 141-142 and its helpers | FU sources; night (`fed`); world.company 402 | F-roads |
| `soaked` [n] | added | roads.apply_choice 290 | night | F-roads |
| `fuse` [events] | added | FU.plan 66 | FU.record | F-fuse |
| `awake`, `fled` | added | fuse `_defend`/`_alarm`/`_flee` | ST.settle_fights | F-combat/F-fuse |
| `_departed`, `_floor` | added | night.departures 244, sleeping_places 310 | night 31, 363 | F-roads/F-lodging |

Also per mind: `PC.store(w,n)["today"]` (perceive.py:42, `_blank`) holds `heard`, `dawn`, `concerned`, `notice`, `glimpse`, `attended`, `felt` and `learned`. The run loop writes `heard` directly (run 261, 280, 297, 341, 352, 359, 587; evening 117, 129; settle 245). This is a second "today", per agent, kept by F-percept.

Other per-day state outside `today`:
- `w.s["day"]` and `w.s["events"]` are reset at dawn (run 867-868).
- `w.s["left"]`: run 1067.
- `w.s["log"]`: night rec, appended in night.py. `EVN.needs_morning` reads `w.s["log"][-1]`.
- `w.s["life"]`: run 410.
- `w.s["fuse_calls"]` {n:last day}: fuse.py:63.
- `w.s["traces"]`: p_traces.
- `w.s["offers"]` and `w.s["agreements"]`.

Runner-only state is not in the world: it is the `CARRY` locals (720-722). These are today, names, at_day, systems, openings, users, replies, meta, errors, first, results, woken, talk_log, talked, attend, plans, budget, used, rep, heavy, settled, road_rec, woke, rec, nights, last_system and extra_cost.

### 1.4 Ordering dependencies (must hold in any redesign)

1. `today` reset comes before `dawn()`, because dawn's events go into a fresh `w.s["events"]`. `RD.arrived` (in `arrive`) comes before `PC.dawn` and the morning prompt, so "On the way" shows. `LF.dawn` comes before arrivals: a coming of age changes `agents_acting`.
2. `w.s["left"]` is written at settle on day d and read at dawn on d+1. Its window is `day >= day-1`.
3. Decide → talk. `talk` reads `replies` (say, tell, explain, offers, open, look_up). Talk replies replace `actions`. The meeting (evening worlds) comes after talk and before the work commit, and may replace `actions` again.
4. Budget is computed from the say count in `results` before work. That is why speech has to be delivered before work.
5. Work is interleaved by index in one shuffled order. Rivalry for the same stock depends on this order (K-rng `order`).
6. Lighten, then morning departures, then `LY.routes`. Routes must see the final position.
7. The evening needs `today.sleep` from the work, `travel` (excludes) and `route`. `arrive_evening` comes before the hearth call. `PC.evening(day)` comes before the hearth prompt (`saw_day`).
8. `LA.close_day` runs after the evening (an evening `try` spends units) and before the night (`today.units` feeds the night's eating).
9. Settle order:
   1. `LF.settle` (partners).
   2. `children_work`, done before AG.settle, so a child's goods can pay a leg.
   3. `AG.settle`. Work legs count `w.s["acts"]`, so all the day's acts must be done first.
   4. teaching, then joins.
   5. thefts. These need `attend` and `watch`.
10. The night needs this order:
    1. **departures** come before `RD.night`, so leavers are on stretch 1, and before `FU.plan`.
    2. `RD.night` comes before `FU.plan`, because the sources read `today.road`.
    3. `FU.plan` and `fuse_calls` come before `N.night`, because `settle_fights` reads `guards`, `fled`, `awake` and `fight.handed`, which the fuse choices write.
    4. `N.night` reuses `today._departed` so it does not depart twice.
    5. `FU.plan` calls `night.sleeping_places`, which writes `today._floor`.
    6. Offers lapse at the end of `N.night`, after the fuse and after `AG.settle`.
11. `PC.evening(skip=day_seen)` comes after the night (only what came after the evening). Then `night_lines(rec)` needs the full night rec. `PC.close_day` comes after that.
12. Memory needs `nights` and `results`. `conv.ends` decides who writes. Folding at the evening sets `memory_done` so that memory is not asked twice.
13. `J.after_commit` runs interventions after any commit, so a step's checkpoint is taken before the interventions of that step.

### 1.5 Kernel versus feature logic inside run.py

**Kernel (irreducible):**
- the step sequence and its commits (`open_step`/`commit`, CARRY, `_runner`)
- `decide`, `_recorded`, `_parallel`, `Tally`, `_week_stop`, `_abandon`
- `HumanTurn`, `Stopped`, `UsageStop` and the mode handling (start, resume, replay, continue)
- the keyed `w.rng` (`order`)
- the calls to `Conversations`
- the turns, days, perception and memory jsonl writers
- cost accounting
- the CLI `main`
- the generic parts of the work loop: interleaving, budget, cost check, refused dedupe and fallback.

**Feature logic embedded in run.py (to move out):**
- **talk()**:
  - say costs units (`say_units`) and needs building access
  - private-message cap (`people[n].messages`)
  - explain (KN levels)
  - offers via AG, with **child guardians** (`_guardian`, D4-55)
  - notes open (`notes.open`)
  - look_up cards (KN.card)
- **_mentions()**: place knowledge (PC store places), hidden ways (LY.learn_way, roads ends), crafts heard (KN.mentions → learn prim).
- **dawn()**: three incident kinds (stray: farm and herds; death: life; fire: buildings with vault), `left` found, spec signs, LF.dawn.
- **arrive, morning_departures, arrive_evening**: travel, evening (D4-67), herds, layout.
- **evening_step / meeting_step**: the whole F-evening flow, including the `plan_next` set prim and `memory_at_evening`.
- **night_lines()**: narration of 15 or more night rec keys (food, fire, work, births, care, deaths, breaks).
- **fuse_calls()**: meeting waves (`RD.ROADS["waves"]`), "On the road: " and "In the night: " prefixes, `RD.settle_meeting`.
- **Work loop**: the morning-travel rule, `heavy` keyed on the string `"Refused: travel: you carry"`, lighten (allowed verbs give, leave, move and travel are hard-coded), `over_ok` (labour), "pushed on" text, scripted acts.
- **The settle step**: partners, children_work, teaching, joins, thefts and the `left` rotation are all named in run.py.
- **The night rec update (1121-1124)** and the day's print (1134-1137) name offers, agreements, teaching, learning, joins, admits, watch, thefts and births.
- **bot_plan / bot_fuse**: these know verbs, items, roads and fuse kinds.

---------------------------------------------------------------------------------------------------------------------------------

## 2. THE CALL

### Building the request
1. **System prompt.** `PR.system_prompt(Here, Mind)` is built per day (run 876). It is frozen per conversation by `Conversations` (converse.py:37 `system()`, 42-60 `message()`). Fuse calls use `conv.system(n, last_system[n])`.
2. **Message.**
   - Morning: `turn(Here,Mind,opening=False)` is the user text. The opening is `turn(...,opening=True)`, a self-contained text used when a conversation (re)starts. Both go through `TG.render` (tags).
   - Later calls send `openings[n] + "\n\n" + text` as the opening.
   - Fuse uses `PR.road_opening` for travellers with no opening (run 687).
3. **Schema.** `PR.schema_for(Here(transit=...), Mind)` (prompt.py:68-114). Its properties are actions, fallback, say, tell, explain, offers, attend, look_up, note, pin, forget, overwork and others.
   - `actions.do` enum = verbs where `V.verb_here` is true, plus **every FUSE choice and also** (prompt.py:75). It is one schema for day and night, so an urgent call continues the conversation (D2-84).
   - The enums come from what the mind knows (people, buildings, parcels, herds, holds, techs).
   - It is conditional on settings: `tags` (free text), `labour.over_units` (overwork), `evening` (`when`).
   - The memory call passes `schema=json.loads(conv.c[n]["schema"])` (run 1102) so the conversation is not restarted.
4. **Conversation.** `Conversations.message(name, day, system, schema, text, opening)`:
   - It restarts the conversation if there is none, the schema key changed, or `starts(name, day)` (stagger `crc32(name) % chunk`).
   - On restart the text becomes `opening`.
   - It returns either a flattened string or an `llm.Turn` (cached `claude -p` session, with history and fallback). `after(ctx, raw, usage)` appends the exchange.
   - `ends(name, day)` decides memory night.
   - The runner checkpoint stores `conv.c` without sessions (`_runner` 736).

### decide() (151-196): responder dispatch (execution.md "Responders")
1. `key = J.request_key(name)`, which gives `d<day>.<step>.<agent>.<n>` with n counted per (step, agent) (journal.py:246).
2. `rec = J.answer(key)` → `_recorded`. **Recorded** responder: the conversation is replayed through `conv.message`/`after`, and `J.check_message` compares the message sha (a replay mismatch goes to `J.mismatches`).
3. `J.strict` (replay) with no record raises `Stopped`.
4. **bot**: `J.request(..., "bot")`, then `bot_fuse` (if `fuse`) or `bot_plan`. `J.response` (an error is recorded and re-raised).
5. **human**: build the schema and the message, `J.request(..., "human")`, raise `HumanTurn([(key,name)])`. api.py answers it later in the journal: `api.answer` checks against the schema (jsonschema, with a fallback key check) and writes `J.response(..., "human")`. `api.advance` then runs `R.run(mode="resume")` and the recorded answer is used.
6. **model**: function-level `from cybertron2.infra import llm` (a lazy import of the heavy CLI or SDK wrapper; it also keeps `bots` and `replay` light). `J.request(..., f"model:{model}")`, then `llm.call(backend, model, system, sent, schema, thinking_budget=llm.thinking_budget or 2000, attempts=attempts)`. Raw output from the last good attempt, `conv.after`, `J.response(key, attempts, out, reasoning, usage, transport)`.
7. Returns `(reply dict, meta{model, usage, seconds, thinking, sent, opening, key})`.

### Parallelism and stops
- `_parallel(fn, jobs, workers=12, tally)`: a ThreadPoolExecutor. `_error` replies and exceptions become `{"actions": []}` plus `errors[n]`. Every `HumanTurn` is collected; the others' answers are kept (already journaled), then one `HumanTurn(sorted)` is raised. `tally.add(len(jobs), errors)` may raise `Abandoned`.
- The journal is thread-safe through `RLock` (journal.py:96). `Conversations` uses its own lock.
- **Request kinds** by call site:

| Kind | Site |
|---|---|
| decision | 895 |
| talk | 917 |
| meeting | 572 |
| lighten | 1021 |
| evening | 506, 543 |
| fuse | 688 |
| memory | 1103 |

- **Usage stop**: before each live day (`_week_stop`). **Fail stop**: `Tally`, then `_abandon` → `J.abandon_day` (journal.py:131) moves the failed responses to `abandoned`, so a resume asks them again.
- **Cost**: `usage.cc_equiv_usd` summed at night (1082-1084) and at memory (1113-1114). Road-traveller fuse costs go through `extra_cost` (692).
- **Determinism**: `__main__.py` re-execs with `PYTHONHASHSEED=0`. Every draw is `w.rng(*parts)` (world.py:335, seed plus an optional fork salt).

### Interfaces in the four files skimmed for interfaces only
- **journal.py**:
  - Tables: meta, data, segments, steps, requests, responses, blobs, checkpoints, events, changes, interventions, abandoned (21-36).
  - `Journal`: `open_step`, `commit(state, runner)`, `request_key`, `request`, `response`, `answer`, `check_message`, `event`, `change`, `blob`, `meta`, `start`, `resume(strict, until)`, `abandon_day`, `interventions_after`, `applied`, `close`.
  - Module functions: `read`, `checkpoint(path, step)`, `unslim`, `unblob`, `differences`, `provenance`, `frozen_tables`.
  - `World.apply` calls `journal.change`; `World.event` calls `journal.event`.
- **branch.py**:
  - `STEPS` (24); `order`; `step_of`; `_cut`.
  - `rewind`, `fork(run, at, out, interventions, responders, salt)`, `replicates`, `continue_`.
  - `after_commit(w,J,step)` applies the salt, responders as a `set` prim on `person.model`, and interventions through `w.apply(op, place, **args)` or `w.event`, inside `w.cause(verb="intervention")`.
  - `branches`.
- **api.py**: `pending`, `context` (views.context), `check`, `answer`, `status`, `advance` (calls run.run resume), `play` (terminal), `verbs()` (from `V.VERB`), `serve` (HTTP plus play.html).
- **converse.py**: `Conversations(out_dir, chunk, backend)` with `offset`, `starts`, `ends`, `system`, `message`, `after`, `end`, `close`. It depends on `infra.llm` (`Sessions`, `Turn`, `flatten`).

---------------------------------------------------------------------------------------------------------------------------------

## 3. SOCIAL (households, membership, claims, offers, agreements, settlement, hosting, thefts)

### State (world.py:100-101 init; schema world.py:18)
- `institutions{iid: {kind:"household", name, members[], offices{head}, rules{admit:"head", grant:"members"}, order?}}`
- `claims{cid: {thing[kind,key], claimant, rights[], grounds (built, claimed, granted, cleared, found, custom, sold...), until?, by?, plots?...}}`. Read by `w.claims_on` and `w.rights`.
- `offers{oid: {node, by, for, to, give[legs], get[legs], lots, taken, until, open, closed?}}`
- `agreements{aid: {node, day, status, parties, legs, witnesses, offer, made_by, seeded?}}`
- `acts[]`: the action record. `w.record` (world.py:457) is read by AG.settle work legs.
- `left[]` (goods left at doors).
- building fields `theft`, `raided`, `meeting`; parcel `fight`.

### Primitives (world.py:1038-1074 `PRIMITIVES`)

| Primitive | Lines | Place refs |
|---|---|---|
| `admit` | 720 | person |
| `leave` | 731 | person |
| `found` | 740 | person |
| `claim` | 753 | thing (parcel, building, herd); for a parcel it calls `FM.sync` |
| `end_claim` | 761 | |
| `plots` | 784 | parcel; land legs |
| `offer` | 1000 | by; id `O{seq}` |
| `close_offer` | 1007 | |
| `agree` | 1013 | none, "checked by the verb"; id `A{seq}` |
| `leg` | 1025 | none |
| `close_agreement` | 1020 | none |
| `office` | 953 | head, heir and order |
| `partner` | 939 | |
| `set` | | used for building `theft`, `raided`, `meeting`, `door`; person `plan_next` |

Hook: `AG.install` registers `("after","transfer") → _credit` (agreements.py:367-409). When the cause verb is give or leave, it credits the arrears and prepaid on the payer's open legs toward the payee (a person in hands or a holder's stock), oldest first. It is installed in `World.__init__` (world.py:235).

### Verbs (verbs.py VERB 17-89, HANDLERS 2003-2008, `do` 206-225)

| Verb | Handler | Lines |
|---|---|---|
| accept | `_accept` → `AG.accept` | 1729 |
| withdraw | `_withdraw` → `AG.withdraw` | 1739 |
| release | `_release` → `AG.release` | 1734 |
| host | `_host` (a claim granted until today, feed means withdrawal) | 1436 |
| grant | `_grant` | 1450 |
| revoke | `_revoke` (end_claim) | 1465 |
| join | `_join` (`today.joins`) | 1478 |
| admit | `_admit` (rule `admit`=head; `today.admits`) | 1488 |
| leave_household | `_leave_household` | 1500 |
| found | `_found` | 1510 |
| claim | `_claim` / `_claim_plots` | 1519, 1547 |
| sleep | `_sleep` | 1580 |
| take | `_take` (theft goes to `today.thefts`) | 1266 |
| give | `_give`/`_into_store` (`today.left`, "leave" alias) | 1318 |
| set | door | |
| name | heir or head | 1924 |
| order | children's standing work | |
| meet / come | evening meeting | 1960 / 1977 |
| partner / try | | 1833 / 1853 |
| watch, teach, learn, attack, guard | | 1655-1720 |

The `for` party is resolved for gather, work, make, build, give, accept and claim (`do` 216).

### Talk-side social (not a verb)
`offers` in the talk reply → `AG.make_offer(here, mind, o)` (agreements.py:137):
- legs are parsed from words by `parse_legs` (42-74, regexes for goods, promises, every-n, work and plots, with the season-date translation `_season_days`)
- `_land`, `_offer_goods` (availability through `KN.available`; land needs `alienation`)
- same-offer dedupe; `until` (a person: today; on the road: the meeting; anyone: while the offerer stays or until a day)
- `here.new_offer` → the `offer` prim

Text helpers: `offer_text`, `_leg_short`, `leg_text`; `lines(here,mind)` gives the open agreements shown to agents.

### Accept (180-243)
1. Checks: the offer is open, it was made to me, it is not my own, the offerer is here, lots, the now-legs are available both ways, land holdings.
2. Builds the legs with `from`/`to` = giver/getter (a party via `for`) and multiplies by lots.
3. Pays the now-legs with `_pay`: payer's hands, then the party container, then takeable stores, then transfer to the payee's hands or party container.
4. Moves land with the `plots` prim.
5. Bumps `taken` and closes the offer if all lots are taken. `new_agreement` (open if any leg stays open). A `trade` event. `here.record("accept")`.

### Settlement `AG.settle(w)` (321-364), engine side, in the settle step
For each open agreement leg:
- **Work legs** count the distinct days in `w.s["acts"]` where actor=from and `for`=to.
- **Goods legs**: `_due` (now, by, every; plus arrears). Paid only if the payer (`_person_for`: a person, or a household member with the head first) is at a node and the payee is present there (`_present_for`: a person there, or a building the party holds there). The payment runs inside `w.cause(actor=payer, verb="settle", node=node)`. Otherwise it goes into arrears. An instalment advances `paid`/`next`.
- The agreement closes when all legs are met (`_met`).

`release` (275): the creditor counts the debt as paid (the `leg` prim, then `close_agreement`). Offers lapse at night: night.py:203-208 (the `close_offer` prim, why "lapsed").

### Membership and settle.py
- `settle_joins(w,today)` (198-218): a join matches an admit, same household, same node, then the `admit` prim and a `household` event. Unmatched joins and admits get result lines.
- `settle_teaching` (165-195): a teach matches a learn at one node, then the `learn` prim (capable, or known for a youth) and a **direct** `r["skill"]` write (176-187, not a prim).
- `settle_thefts(w,today,attend)` (221-247):
  - the building `theft` set prim (D4-74)
  - for each agent at the node: the `TH.spot_chance` noticing rule (`NOTICING["theft"]`; inside if at home and not working; attending if attend or watch names the building) and the draw `w.rng("steal-seen", d, x, by)`
  - a `theft` event concerning the witnesses
  - the thief's `heard` line

### Hosting and lodging
host and grant write granted claims. Evening `host` also sets `today.sleep[guest]` directly (evening.py:147-152). `night.sleeping_places` reads `sleep`, homes and grants.

### Households in prompts and evening
`EVN._requests` (47-70) shows the pending try, partner, join (to the head) and offers-to-me asks at the hearth.

### Where the code lives
- agreements.py: offers, agreements, settlement, the credit hook
- verbs.py: the social verbs
- settle.py: joins, teaching, thefts, fights
- night.py: offers lapse
- world.py: prims, `household_of` (503), `members`, `head`, `homes` (552), `rights` (529), `claims_on`, `_claim`
- here.py: `offers`, `agreements`, `party_container`, `takeable`, `new_offer`, `new_agreement`, `households`, `institution`, `claim_records`
- run.py: talk offers, guardian, settle-step orchestration

Seeded state: `spec.agreements` gives the `agree` prim in World init (world.py:232). `generate.build` writes seeded debts with `seeded: True` (excluded from `agreements_made`).

---------------------------------------------------------------------------------------------------------------------------------

## 4. ROADS AND TRAVEL

### State
- `w.s["roads"][rid] = {a, b, days, track, terrain, bare?, stretches[{terrain, landmarks[{kind, state?}]}], ends{node: {parcels, hidden, worn, used}}}`. `RD.build(extra, days)` (27-39) makes the terrain and stretches from the spec. A road with no terrain is a farm track (D2-122).
- `people[n].transit`: created by `p_depart` (world.py:808) as `{road, from, to, left, arrive}`. Extended by the `transit` prim (882) with `choices`, `notices`, `notices_first`, `last_pos`, `by_day`, `carried_by`. Also mutated **directly** with `stopped`, `stop_until`, `arrive` (roads 193-194), `from`, `to`, `arrive`, `turned` (turn_back 305), and `from`, `to`, `arrive`, `left`, `with` (travel_with 311).
- `people[n].arrived`, `arrived_by`, `came_from` (evening worlds), `home_seen`.
- `w.s["traces"]` [{road, pos, day, kind (tracks, ruts, ashes), n, toward, by}] via the `traces` prim (fading by `ROADS.trace_days`).
- `w.s["mind"][n]`:
  - `landmarks{key: {crossed, words, road, pos, kind}}`, written directly by `_learn` (113)
  - `on_the_way{day, lines}`, written directly by `arrived` (851)
  - `found[]`, directly (726)
  - `ways{rid@node}`, written directly by `LY.learn_way`
- Road ends `worn`/`used`: written directly by `LY.wear_way`.
- herds: `node` (a road id when on a road), `pos`, `with`, `pack`, `lost`.
- things on roads: containers with `node==rid` and a `stretch`.

### Primitives used
`depart`, `arrive` (no place check: "checked by arrival"), `transit`, `traces`, `set` (person and herd fields), `create` (wild food gathered on the way), `destroy` (lost at the ford), `die` (the pass), `transfer` (take, give, find), `claim` (a found herd, `_hold_found`), `set_thing` (buried), `split_herd`.

### Verb
`travel` (verbs.py:1610-1652). It checks the road (`here.road_to`), the pack ox (`lead`, harness) and load against capacity (the refusal string starts "you carry"). Then it sets `today.travel` or `today.travel_morning` (evening worlds, `when: morning`) and `today.travel_choices`: on trouble, stop at, gather, days, meeting, searching, lead. A `depart` event. Its `"when": "roads"` gating is in `verb_here` (verbs.py:95-98).

### The day of travel
1. **Departure at nightfall**: `N.departures(w, today)` (night.py:213-246), run at the start of the night step.
   - It finds the road by matching ends, sets `home_seen`, picks the pack ox (`HD.pack_ox_for`), applies `depart`, `LY.wear_way`, and `transit` with choices.
   - `HD.lead_ox(...)` splits off an ox that carries. Infants are departed and `carried_by` is set.
   - `today._departed`.
2. **Departure in the morning** (evening worlds): verbs `_travel` sets `travel_morning`. In the work loop the first act is the travel; the rest of the plan is skipped and `used=budget`. Then `morning_departures` (run 442-454): `N.departures` with a temporary today, `transit{by_day:True, arrive: d+days-1}` for the traveller and its carried infants, then `arrive_evening`.
3. **The roads at night**: `RD.night(w, today)` (138-162).
   - `today.road` = meetings, finds, crossings, fed, herds, splits.
   - `ps = parties(w)` groups travellers by (road, from, to, left, arrive) on active roads.
   - `HD.follow` and `rec.pack = HD.feed_pack`.
   - For each party: `_landmark`, `_notices`, `_finds`, `_herd_finds`, `_driven_splits`. Then `_meetings(ps)`, then `leave_traces` for each party.
4. `_landmark` (184-236):
   - **Good places**: a stop by choice where the place is known (delay plus wild food), seasonal feeding (`today.road.fed`) or gathering, then `_learn`.
   - **Challenge** (`challenge()` 72-84, an if-chain on `high`, `down`, `snowed` reading the weather through `EV`): with the leader's experience (D2-106) and `_risk` (death or cart loss), a serious or minor draw combined with a "noticed" draw gives a fuse `crossing`. Otherwise `apply_choice` by the departure choice or the landmark default: wait, go round, turn back, or push on (load loss, soaked, death).
5. `_notices` (315-359): the bundles in `signs.py` (ROAD, THING, TRACE, GRAND_AHEAD, TRAVELLER) are rolled by the one rule (visibility times the eye), then `_note` adds the transit `notices` (what happened is put first).
6. `_finds` (368-386): things on the stretch that are worth taking; the finder by draw gives a `find` event.
7. `_herd_finds` and `_driven_splits` (410-446): F-herds on roads, giving `herd` and `split` events.
8. `_meetings` (450-484): parties on one road going opposite ways at the same position, or which crossed since `last_pos`. The meeting chance is the landmark's `meet` or the terrain's, halved in fog. A party set to "pass by" gets `pass_by` notes and no call. Otherwise a `meeting` goes into `today.road.meetings`. Then `last_pos` is set.
9. `turn_back`, `travel_with`, `_delay`: journey changes.
10. **Arrival**: at dawn (`dawn()` 411-417) if `arrive <= d`, or at nightfall for `by_day` (`arrive_evening`). `arrive()` (425-439):
    - `RD.arrived` turns the notices into `mind.on_the_way`, capped at `ROADS.notices`
    - the `arrive` prim and `arrived` set; `arrived_by` and `came_from` set if evening
    - `HD.arrive_with` (a pack ox stays led; other herds go `off_road`)
    - `LY.learn_way` (the end one came in by) and `LY.wear_way`
    - an `arrive` event
11. **Pack oxen** (F-herds, D2-136): `HD.pack_ox_for`, `lead_ox`, `feed_pack`, `pack_oxen`, `led_by` and `let_go`. Capacity is extended with `oxen` in `here.capacity`.
12. **Encounters and trouble as fuse kinds**: see section 5 for the crossing, meeting, find, herd and split choices registered in roads.py (516-799). `meeting_talk` (802-820) is one wave: say and tell to all, offers through AG with the road as the place. `settle_meeting` (823-842): the meeting is noted on arrival, attacks go to `ST.duel` on the road, `flee` has a chance from `ROADS.flee`.
13. **Data**: `TERRAIN`, `LANDMARKS`, `ROADS` and the road `FUSE` rows (data.py:784-834). `TECHNIQUES` modifiers for travel choices: "on trouble", "meeting" and others (data.py:836 on).

The world core reads roads state in `World.company` (world.py:395-405): `today.road.meetings`, so that those in a meeting are company.

---------------------------------------------------------------------------------------------------------------------------------

## 5. FUSE (urgent calls)

**Registry** (fuse.py:17-38):
- `SOURCES[kind]` (`@source`): which events tonight, from `today`.
- `DETECT[kind]` (`@detector`): returns {name: sign text}.
- `CHOICES[(kind, choice)]` (`@choice`): returns a result line.
- `WORDS` is declared and unused.
- Data row: `data.FUSE[kind]` = sense, label, detect chances, `acts` by structure, riders, `choices`, `also` (ordinary verbs allowed through `V.do`).

**Flow:**
1. `plan(w,today)` (60-89):
   - `gather` runs every SOURCE. Ties in start time are broken by `w.rng("fuse-start", d, kind, id)`.
   - `acts_for(e)` is the acts for the event's structure, capped by riders.
   - It detects; there is one call per agent per night (`w.s["fuse_calls"][n] = d`). An agent's events are merged into `{events, signs, acts=max}`.
   - `with`: on the road, its party; at a node, those sleeping in the same place (`night.sleeping_places`).
2. `fuse_calls` (run 681-716):
   - `PR.fuse_prompt` and decide with kind "fuse".
   - Meeting waves: up to `ROADS.waves`-1 more, each wave fed by `RD.meeting_talk` with `PR.meeting_wave_prompt`.
   - `FU.answer` per woken agent: each act goes to the `CHOICES[(kind, do)]`, or to `V.do` if it is in `also`, or is refused. `_event_for` matches by label or by the choice.
   - `RD.settle_meeting`.
3. `record(today)` gives `rec["fuse"]`.

**Kinds and their registration points:**

| Kind | Source | Detector | Choices | Writes |
|---|---|---|---|---|
| raid | fuse.py:137 (today.fights kind raid, attacker present) | fuse.py:149 (watcher, inside with dog or structure, neighbour by sound; `TH.spot_chance`; `SG.NIGHT` signs) | defend 179, flee 186, alarm 192, hand over 204, stay 217; also move, take, give | today guards, awake, fled; `e.fight.handed`; alarm event; transfer |
| meeting | roads 517 | roads 662 | go on 741, turn back 747, change course 755, attack 763, flee 772, give 778, accept 791 | e.attacks, fled, deals; transit; agreements |
| find | roads 522 | roads 673 | take 707, bury 732, go on 741 | transfer; set_thing; mind.found |
| crossing | roads 527 | roads 678 | push on, wait, turn back, go round 692 (`apply_choice`; settled once per party) | delays, loss, death |
| herd | roads 532 | roads 557 | drive on, drive back 578, accompany 597, leave 616 | herd `with`; claim `found`; delays |
| split | roads 537 | roads 564 | go after them 622, let them go 640 | herd counts set |

**What wakes agents mid-day: nothing.** Fuse calls happen only in the night step, after departures and the roads. A mid-day wake is the talk step (messages and offers to one person, `talk()`), the meeting (evening worlds) and the evening answer wave (`EVN._requests` and names said at the hearth). `here.py:20` refuses a `Here` on the road unless `transit=True` ("only for an urgent call").

**Registration points to keep:**
- the decorators (import-time side effects: roads.py must be imported for its kinds to exist, and run.py imports RD for this)
- `data.FUSE` rows
- `bot_fuse` (run 68-84, an if-chain on kind)
- `PR.fuse_prompt` words dict (prompt.py:786-801, a word per choice)
- `PR.schema_for` adds all FUSE choices to the `do` enum (prompt.py:75)
- `night.settle_fights`, which consumes the raid choices

---------------------------------------------------------------------------------------------------------------------------------

## 6. GENERATE AND EXCHANGE

### generate.py: a seeded society with a past (D4-21, 09 §3c). An offline spec tool, not part of the run
- `python -m cybertron2.engine.generate BASE --seed N --out SPEC` (main 443-461; `node_from` merges a node file).
- `Tree` and `simulate(lines, rng, ...)` (67-151): yearly demography (deaths, hard winters, births, marriage, leaving to `OUTSIDE="Ashby"`). It uses `random.Random(f"{seed}|tree|...")`, not `w.rng`.
- `kin(T,a,b)` (155-197): kin terms derived from the tree.
- `build(base, seed)` (201-440):
  - It retries trees until `bounds` fit (per line, acting count, children, youths).
  - It writes `spec.tree`, `spec.history`, `spec.generated` and `spec.agents{household, born (negative day via to_days and LF.spans), stage, sex, relations, memories, knows, aware_of, holdings, concerns, parents, partner, role, model, born_line, trade, aim}`.
  - Heads are the eldest adult man.
  - Ties: a feud adds a contested claim `grounds: custom` to `spec.claims`; seeded debts go to `spec.agreements` with `seeded: True`, plus friendships and an old love.
  - Models: Opus heads, Sonnet adults, Haiku youths, through `cast` and `household_models`, with `opus_extra`/`sonnet_extra` spreading. The model ids are hard-coded by full id.
  - House beds, size and stock are scaled to mouths.
  - Side effect: it mutates `base["lines"][*]["place"]`.
- Engine dependencies: `life` (lifespan, spans, stage_of, MINOR) and `data.TECHNIQUES` only.
- Users:
  - the generated specs (combe, valley_s5, wide_s7, hollins_s7, hollins2_s8 headers)
  - proto/peoplegen/write.py (GEN.MALE, FEMALE, to_days, winters, born_day, stage, kin)
  - tests/test_cybertron2_package_d.py
- In a redesign it belongs to the F-life and F-house "population generator" package (37_growth "generated populations"). It registers nothing with the run kernel; it writes the spec keys that World init and `KN.seed` and `PC.seed` read.

### exchange.py: export, import, publish and fetch of a run (spec/record/exchange.md; D1-1, D1-3 to D1-5)
- `export(run, out, redact)` (58-96): every `JN.TABLES` table to `journal/<table>.parquet` (lossless; `blobs.z` and `checkpoints.z` are decompressed, redacted and recompressed when redacting), plus `views/*.parquet`, `manifest.json` (rows, columns, types, sha256) and `run.json`.
- `view_tables(run)` (99-138): from each `.memory` checkpoint it builds people_days, holdings, buildings, parcels (`FM.main_crop`, `FM.field_fertility`), claims, and **messages, parsed from the runner carry `results` lines "You told "/"You said ("**, plus `VW.calls`, `layout` and `frames`.
- `import_(src, out)` (142-166): checks shas, creates an empty Journal, inserts rows, checks counts.
- `scan(root, strings)`: the privacy gate over parquet and text. `_private()` reads the `CLAUDE_CODE_*` id env vars.
- `publish(runs, staging, push, repo)` (200-243):
  - **It imports the legacy `cybertron2/publish_hf.py` as `LEGACY` (line 201)** for three things:
    - (a) `LEGACY.FILES` (publish_hf.py:33) to copy the files of runs with no run.db
    - (b) `LEGACY.SUMMARIES` (publish_hf.py:66), the per-run one-line summaries for the index rows
    - (c) `LEGACY.CARD` (publish_hf.py:37), the dataset card template, to which the journal section is appended
  - publish_hf.py itself says (lines 3-5) that it is only for runs from before the journal.
  - The upload uses `huggingface_hub.HfApi` and `infra.publish.default_repo()`; it needs `HF_TOKEN`.
- `fetch(run_id, out, revision, repo)`: `snapshot_download` (pinned revision), then `import_`.
- Users: the run.py CLI (1269-1280), c2viz/touch.py:193,198, tests/test_cybertron2_exchange.py.
- Dependencies: `journal` (TABLES, SCHEMA, checkpoint, unslim), `views` (steps, calls, layout, frames), `farm` (one F dependency for the parcels view), `infra.publish`, pyarrow, huggingface_hub.

---------------------------------------------------------------------------------------------------------------------------------

## 7. EXTENSION POINTS (existing and implicit)

### Dispatch dicts and registries that already exist
- `world.PRIMITIVES` (world.py:1038-1074): name → (fn, refs-for-place-check). `World.hook(when, prim, fn)` (419) gives before and after hooks. Two users: `AG.install` (transfer), `BL.install` (create, transfer).
- `verbs.VERB` (17-89, args, cost, doc, `when`), `verbs.HANDLERS` (2003-2008, with an assert that both have the same keys) and `ALIASES`. `verb_here` gates `when` ∈ {roads, herds, children, evening} with a hard-coded if-or-chain (95-98). `verb_units` reads costs from `w.p` paths.
- `fuse.SOURCES`, `DETECT`, `CHOICES` (decorators) and `data.FUSE`.
- The data tables in data.py: FUSE, TERRAIN, LANDMARKS, ROADS, HERDS, NOTICING, TECHNIQUES, ITEMS and others.
- `CARRY` (run 720): the names of the runner state.
- `JN.TABLES`.
- The `branch.STEPS` tuple.
- `TG.render`, `VW.on`/`VW.turn` (view mode switch), `EVN.on`/`plans_at_hearth`, `MEM.rewriting`, `CL.on`, `LF.on`: on-switches read from the spec.

### If and elif chains on a kind
- `run.dawn`: `inc["kind"]` ∈ stray, death, fire (368, 384, 390), with no registry and no else.
- `run.bot_fuse`: event kind (72-84).
- `roads.challenge`: `LANDMARKS[kind]["challenge"]` ∈ high, down, snowed (75-83). data.py:792 says "one function in roads.CHALLENGES", which does not exist.
- `roads.apply_choice`: choice prefixes wait, go round, turn back, else push (261-297). `push` dict keys cart_loss, foot, death.
- `fuse.answer`: CHOICES, else `also`, else refused.
- `settle.settle_fights`: `f["kind"]=="raid"` or attack; `aim=="hurt"`; `handed`.
- `verbs.verb_here`: `when` values.
- `evening.apply`: `verb=="host"` special case (147); `NIGHT_VERBS` tuple (19-20).
- `run.decide`: model == "bot" / "human" / else model.
- `run.main`: cmd chain (1249-1306); `dump` table dict (1299).
- `agreements`: leg type by key presence (`"work" in leg`, `"plots" in leg`, `"item" in leg`), repeated in `leg_text`, `_leg_short`, `_met`, `accept`, `release`, `settle`, `_credit`, `lines`.
- `exchange.publish`: run.db present or legacy files.

### Hard-coded feature names in the run loop (run.py)
- **imports**, top level (18-24): forests, agreements, fuse, knowledge, life, night, perceive, prompt, roads, settle, verbs, branch, evening, journal, memory, tags, view, converse, data (EDIBLE, TECHNIQUES), here and world.
- **settle step**: `LF.settle`, `LF.children_work`, `AG.settle`, `ST.settle_teaching`, `ST.settle_joins`, `ST.settle_thefts` (1061-1066).
- **night step**: `N.departures`, `RD.night`, `FU.plan`, `fuse_calls`, `N.night`, `FU.record`, `PC.evening`, `night_lines`, `PC.close_day`.
- **today key names**: `travel`, `travel_morning`, `travel_choices`, `skipped_morning`, `memory_done`, `day_seen`, `partners`, `children_work`, `left`, `teach`, `learn`, `joins`, `admits`, `watch`, `thefts`.
- **reply keys**: say, tell, explain, offers, open, look_up, note, pin, forget, attend, actions, fallback, overwork, memory.
- **strings matched**:
  - "You said (", "You told ", "Refused", "Refused: travel: you carry", "You offered "
  - "Plan your day. Reply with JSON only." and " Reply with JSON only." (prompt splicing in run 884-885, 496-501, 503, 1100)
  - "(your fallback)"
  - exchange reads the same "You told "/"You said (" lines.
- **verb names**: travel, come, give, leave, move (lighten filter 1027).
- **world params**: `say_units`, `notes.open`, `labour.over_units`, `people[n].messages`, `llm.*`, `memory.chunk`, `memory_at_evening`, `evening`, `script`, `incidents`, `signs`, `bot_travel`, `bots`.

### Function-level imports and why

| Where | Import | Why (stated or apparent) |
|---|---|---|
| run 106, 181 | `cybertron2.infra.llm` | a heavy model client; kept off the bot, replay and import paths |
| run 342, 1045; arrive 434 | `layout` (and `herds`) | a cycle risk (layout and herds import roads, perceive and others) or load order |
| run 372 / 393 | `farm` / `buildings` | only for one incident kind |
| run 767 | `capacity.model` | heavy and optional; wrapped in try |
| run 811-814 | `shutil`, `tempfile`, `sqlite3` | replay only |
| run 1058 | `labour` | |
| run 1257, 1270, 1282, 1292 | `yaml`, `exchange`, `views`, `api` | CLI only. api also imports run lazily (`advance` 74, `start` 136): a mutual import |
| evening 68 | `agreements` | only for offers |
| fuse 80, 152, 157, 174, 194 | `night`, `things`, `signs` | a cycle: night imports settle, and roads imports fuse |
| fuse 101-102 | `verbs`, `here` | `answer` |
| settle 82, 177, 223, 234-235 | `things`, `data.LEVELS`, `perceive`, `NOTICING` | |
| agreements 28, 65, 103, 113, 124, 139, 198, 324, 344 | `verbs.item_of`, `farm`, `knowledge`, `verbs._party`, `here` | verbs imports agreements back (verbs 1730 and others) |
| roads 144, 317, 346, 380, 405, 411, 425, 581, 599, 632, 648, 795, 805, 826 | herds, perceive, signs, layout, farm, agreements, here, settle | a cycle: herds imports roads |
| night 27, 33, 40, 171-180 | settle, climate, buildings, forests, herds, layout, roads, life | |
| world 233-245 | agreements, knowledge, perceive, things, buildings | World init installs features |
| exchange 201, 239, 248, 34 | `publish_hf`, `infra.publish`, `huggingface_hub`, `pyarrow` | optional dependencies |

### Long parameter lists, which mean the runner state is passed by hand
- `evening_step(w, names, results, budget, used, talk_log, openings, systems, backend, conv, workers, tally)`: 12 arguments.
- `fuse_calls(w, today, woke, results, talk_log, openings, systems, backend, conv, workers, extra_cost, tally)`: 12.
- `meeting_step(w, names, replies, results, talk_log, openings, systems, backend, conv, workers, tally)`: 11.
- `decide(w, name, text, opening, system, backend, conv, talk, schema, fuse, transit, kind)`: 12.
- `_recorded(...)`: 13.
- `run(spec_path, out_dir, backend, days, workers, bots, seed, until, mode, responders)`: 10.
- `EVN.prompt(w,n,results,left,place,others,arrived,saw)`: 8.
- `EVN.apply(w,n,reply,gather,names,results,left,box)`: 8.
- `_break_in_to_hurt(w,node,by,bid,b,inside,gd,holders,P,X,rng)`: 11.
- `apply_choice(w,rec,members,t,pos,lm,ch,choice,exp,by_call)`: 10 (`by_call` is unused).
- `PR.talk_prompt` takes 8.

Most of these are the same bundle: (backend, conv, workers, tally, openings, systems, talk_log, results), a "call context" object waiting to be made.

### Globals and module state
- run: `MAX_SAY`, `MAX_ACTIONS`, `WAVES`, `MEETING_WAVES` (set after use), `CARRY`.
- evening: `NIGHT_VERBS`, `MAX`.
- fuse: `SOURCES`, `DETECT`, `CHOICES`, `WORDS` (mutable, filled at import).
- roads: `CHALLENGE_WORDS`.
- generate: `MALE`, `FEMALE`, `OUTSIDE`, `KNOTS`.
- exchange: `FOLDER`, `SQL_TYPES`, `ID_VARS`, `COMPRESSED`.
- branch: `STEPS`.
- journal: `TABLES`, `SCHEMA`.
- `infra.llm.USAGE` (global usage, read by `_week_stop`).
- data tables mutated at import (`FUSE.update`, `TECHNIQUES.update` in data.py).
- `os.environ` `CYBERTRON2_WEEK_STOP`, `LLM_BACKEND`, `HF_TOKEN`, and `PYTHONHASHSEED` in `__main__`.

### State writes that bypass World.apply
These are not in the `changes` table; they are captured only by checkpoints.
- run: `w.s["day"]`, `events`, `today` (867-869); `w.s["life"]` (410); `w.s["left"]` (1067); `today[...]` throughout.
- evening: `today.sleep` (152); `PC.store` `saw_day`, `evening_shown`, `lasting` (witness 215).
- fuse: `w.s["fuse_calls"]` (63); `e[...]` on today's events.
- settle: `know[...]["skill"]` (187).
- roads: `transit.update` (194, 305, 311); `mind.landmarks` (113-119); `mind.on_the_way` (851); `mind.found` (726).
- layout: `mind.ways`, ends `worn`/`used`.
- perceive stores throughout.

---------------------------------------------------------------------------------------------------------------------------------

## 8. WHAT EACH FEATURE FOLDER WOULD REGISTER WITH THE CORE

**Irreducible kernel** (core/):
- World: state dict, `apply`, PRIMITIVES registry, hooks, cause, event, record, rng, place_of
- the step scheduler: an ordered list of day phases with commit points, CARRY or runner state, `today` reset
- the call layer: `decide`, `_parallel`, `Tally`, responders (recorded, bot, human, model), `Conversations`, schema assembly, cost and usage stops
- the journal: tables, request keys, checkpoints, resume and replay
- branching: rewind, fork, interventions, `after_commit`
- `Here`/`Mind` base facades
- the verb registry (`VERB`/`HANDLERS`/`do`/`cost`)
- the fuse registry (`SOURCES`/`DETECT`/`CHOICES` plus the night phase that runs them)
- the CLI and api shell
- the generic work loop (interleave, budget, cost, dedupe, fallback)

Proposed registration surface:

```
feature.register(core):
  data:          tables merged into data (FUSE rows, LANDMARKS, verbs' param paths in w.p)
  state:         top-level keys of w.s with initialisers and spec loaders (World init today does them inline)
  today:         {key: initial value} added to blank_today, plus a per-day reset
  primitives:    {name: (fn, refs)} plus hooks [(when, prim, fn)]
  verbs:         {name: {args, cost, doc, when-predicate, handler}}; night-allowed flag (evening NIGHT_VERBS)
  reply keys:    schema fragments ({"offers": ..., "explain": ...}) and their handlers in the talk step
  phases:        [(phase, order, fn)], phase ∈ dawn | decide.pre | talk | pre-work | work.post | evening | settle | night.pre |
                 night.roads | night.fuse | night.main | night.post | memory; order numbers make the dependencies in §1.4 explicit
  fuse kinds:    source, detector, choices, prompt words, bot answer
  prompt lines:  sections for system, turn, talk, evening, fuse and night_lines (narration from the night rec keys)
  record keys:   what goes into the day record (days.jsonl) and the print line
  bot policy:    contributions to bot_plan and bot_fuse
  views:         view_tables fragments (exchange)
```

### Per feature (from this slice)

**F-speech / talk**
- **Reply keys**: say, tell (MAX_SAY, the messages cap, `say_units`).
- **Phase**: talk (the delivery in `talk()`), which needs to be a kernel loop with pluggable deliverers that return "woken" boxes.
- **Prompt**: `PR.talk_prompt`.
- **Hearing**: hearing a name or place, via `_mentions` hooks registered by F-percept, F-layout and F-know.
- **Evening**: evening say and tell (`EVN.apply` 111-130).

**F-know (teach, learn, explain, look_up, mentions)**
- **Reply keys**: explain, look_up.
- **Verbs**: watch, teach, learn.
- **Today**: watch, teach, learn.
- **Phase**: settle (`settle_teaching`, after work).
- **Primitive**: `learn`.
- **Hearing**: hearing a craft (`KN.mentions`).
- **Record keys**: teaching, learning, watch.

**F-trade (offers and agreements)**
- **State**: offers and agreements; `left` (doorstep gifts).
- **Primitives**: offer, close_offer, agree, leg, close_agreement; plus the after-transfer hook `_credit`.
- **Verbs**: accept, withdraw, release; give and leave credit through the hook.
- **Reply keys**: offers (talk, meeting, road meeting).
- **Phases**:
  - settle (`AG.settle` after children_work)
  - night.post (offers lapse; now in night.py)
  - dawn (`left` found events; now in run.dawn)
- **Today**: left.
- **Prompt**: `AG.lines`, `offer_text`, evening `_requests` offers.
- **Fuse**: `meeting.accept`.
- **Record keys**: offers, agreements_made, settled.
- **Seed**: `spec.agreements`.
- **Also**: the child-guardian redirect (with F-life).

**F-house (membership)**
- **Primitives**: admit, leave, found, office.
- **Verbs**: join, admit, leave_household, found, name, order.
- **Today**: joins, admits.
- **Phase**: settle (`settle_joins`).
- **Evening asks**: join requests to the head.
- **Record keys**: joins, admits.
- **Seed**: institutions from the spec.
- **Generate**: households, heads, cast.

**F-lodging (host, grant, sleep)**
- **Verbs**: host, grant, revoke, sleep, set (door).
- **Today**: sleep.
- **Night**: `sleeping_places` (night.py).
- **Evening**: a host also books the guest's bed (evening.py:147-152), an evening hook.
- **Primitives**: claim and end_claim, with grounds "granted".

**F-claims**
- **Verbs**: claim, the land legs of offers.
- **Primitives**: claim, end_claim, plots, set_share, shares.
- **Seed**: spec.claims (and generate's feud claim).

**F-theft**
- **Verb**: take (theft branch).
- **Today**: thefts.
- **Phase**: settle (`settle_thefts`, needs `attend` from the runner and `watch`).
- **Signs**: building `theft`.
- **Record key**: thefts.
- **Noticing**: `NOTICING.theft`.

**F-combat**
- **Verbs**: attack, guard.
- **Today**: fights, guards, plus awake, fled and handed (from the fuse).
- **Fuse kind**: raid (all of fuse.py:136-219).
- **Phase**: night.main (`settle_fights` before sleeping).
- **Duel**: `duel` is reused by roads.
- **Primitives**: harm, die, wear, transfer.
- **Signs**: raided, fight.

**F-roads (travel)**
- **State**: roads (from the spec, `RD.build`); transit; traces; mind landmarks, on_the_way, found.
- **Primitives**: depart, arrive, transit, traces.
- **Verb**: travel (`when` roads).
- **Today**: travel, travel_choices, travel_morning, road, soaked.
- **Phases**:
  - dawn (arrivals; `arrive`)
  - work.post (morning departures, lighten, arrive_evening)
  - night.pre (departures)
  - night.roads (`RD.night`)
  - night.fuse (the kinds meeting, find and crossing; meeting waves; `settle_meeting`)
- **Prompt**: `road_opening`, `fuse_prompt` words, `lighten_prompt`, "On the way".
- **Record**: road_rec.
- **Kernel needs**:
  - a "heavy, ask again" sub-call in the work loop (a generic "verb asks a follow-up question" hook)
  - `Here(transit=True)`
  - `World.company` reading today's road meetings, which should become a registered "company" provider

**F-herds on roads**
- **Phases**: night.roads (`HD.follow`, `feed_pack`; `_herd_finds`, `_driven_splits`).
- **Fuse kinds**: herd and split.
- **Hooks**: arrival (`HD.arrive_with`) and departure (`HD.lead_ox`).
- **Verb options**: the travel `lead` option.
- These are now spread over roads.py, night.py and run.arrive.

**F-life (in this slice)**
- **Phases**:
  - dawn (`LF.dawn`; the `death` incident)
  - settle (`LF.settle` partners, `children_work`)
  - night (`LF.night`, `care_gifts`)
- **Hooks**: departure (infants carried) and arrival (carried infants arrive); the child-guardian rule for offers.
- **Night narration**: births, care and lost.
- **Today**: partner, try, care, care_by, care_gift.
- **Evening asks**: try and partner.

**F-evening**
- **Switch**: `spec.evening` (true or "plan"); verb `when: evening` gating (meet, come); schema `when`.
- **Phases**:
  - decide.pre: the meeting block splice; plans at the hearth skip the morning call; `needs_morning` reads the last night rec
  - talk.post: `meeting_step`
  - work rules: morning travel first; `used=budget`
  - work.post: `morning_departures`, `arrive_evening`
  - evening: the whole step
- **Today**: travel_morning, skipped_morning, day_seen, memory_done.
- **Person fields**: plan_next, arrived_by, came_from.
- **Verbs allowed at night**: `NIGHT_VERBS`.
- **Kernel features it needs**:
  - an optional step with its own commit
  - a way to replace the morning call by a stored plan
  - a "re-plan" channel in the meeting

**F-fuse (kernel part plus raid)**
- The night.fuse phase and the registry belong in core.
- The raid kind belongs to F-combat. Today it lives in fuse.py.

**F-memory**
- **Phase**: memory, plus the optional evening fold.
- **Kernel needs**: `conv.ends` (from the kernel's Conversations) and the frozen schema reuse.

**F-percept**
- **Phases**: dawn (`PC.dawn`), evening (`PC.evening`, twice), night.post (`PC.close_day`).
- **Other**: the mind's own today; `apply_notes` on every reply.

**F-labour**
- **Phase**: work.post / pre-settle (`LA.close_day`, which now runs between steps).
- **Other**: the budget modifiers (`over_ok`), narration, `today.units`.

**F-layout**
- **Phase**: work.post (`LY.routes`).
- **Hooks**: the arrival and departure way learn and wear; mentions of hidden ways.

**F-sched (incidents and signs)**
- **Phase**: dawn, with incident kinds as a registry: `stray` registered by herds and farm, `fire` by buildings, `death` by life.

**F-cap**
- **Hook**: run start, `J.meta("capacity")`.

---------------------------------------------------------------------------------------------------------------------------------

## 9. COUPLINGS THAT WOULD BE AWKWARD TO SPLIT

1. **Result lines are the inter-feature bus.** `results[n]` strings carry meaning:
   - "You said (" counts units for the budget (run 249, 950)
   - "You told " counts the message cap (274; evening 125)
   - "Refused: travel: you carry" triggers lighten (982)
   - "You offered " is parsed for the oid (313, 596)
   - "Refused" drives the dedupe
   - `PC.SPEECH` prefixes filter the evening's "Your day"
   - exchange.view_tables re-parses "You told "/"You said (" lines from the **runner checkpoint** to build `messages`

   Any rewording breaks budget, lighten and the published views. These should become structured result records.
2. **Prompt splicing by string replace.** run 884-885, 496-503, 1100 insert blocks by replacing "Plan your day. Reply with JSON only." or " Reply with JSON only.". The morning, evening, memory and kept-request texts from prompt.py, evening.py and memory.py are all coupled to that exact tail.
3. **One schema for day and night** (prompt.py:75): every FUSE choice is in the `do` enum so that a fuse call can continue the conversation (a changed schema restarts it). A feature that adds a fuse kind or a verb changes every agent's schema, and so the conversation restart points and the cached-session behaviour. Feature registration must therefore feed one schema built once.
4. **The night is a braid of five features with an order of side effects.** departures (roads, herds, life) → roads night (roads, herds, signs) → fuse plan (raid detection needs `night.sleeping_places`, which writes `today._floor`) → fuse answers (write `today.guards`, `awake`, `fled`, `e.fight.handed`) → `N.night` (`settle_fights` reads those, then sleeping, fire, food with labour `units`, life, decay, farm, offers lapse). `fuse.py` imports `night` and `night` imports `settle`. The raid kind lives in the registry module. Splitting needs explicit phase ordering and the `today` keys declared per feature.
5. **The `today` dict is a shared mutable blackboard with no owner.**
   - 19 keys are pre-seeded by run.py and more than 20 more are created ad hoc by verbs, farm, labour, roads, fuse, night and the evening.
   - `blank_today` is imported by landgen/gates.py.
   - `World.company` (core) reads `today.road.meetings`.
   - `EVN.needs_morning` reads `w.s["log"][-1]` (the night rec).

   A registry of today keys with an owner and a lifetime is needed before anything moves.
6. **`CARRY`, i.e. `locals()`, is the runner's checkpoint.** Any new runner-side variable that must survive a resume has to be added to `CARRY`, and exchange reads `carry.results`. Moving the step code into feature functions breaks the `locals()` capture. The runner state should become an explicit object.
7. **Step names are hard-coded in three places, and they disagree.**
   - run.py has the evening step.
   - `branch.STEPS` has no "evening", and `order()` raises `ValueError` on `dN.evening` (verified).
   - execution.md and round.md list no evening step.

   A registered phase list must feed both the scheduler and branching.
8. **Request keys depend on the step and the per-agent call count.** Moving a call (for example the meeting, now keyed under the last `talk.N`; or the evening memory fold) into another step changes the keys, so an old run cannot be resumed under new code (replay mismatch). Phase registration must keep the key scheme stable.
9. **`LA.close_day` runs between commits** (1058-1059). Its `set` changes are journaled under the previous, already-committed step but are only in the next checkpoint. On a rewind to `dN.evening` or `dN.work`, the `changes` rows for that step include changes its checkpoint lacks.
10. **Direct state writes** (§7) bypass `apply`, so hooks and the `changes` table miss them. These are transit updates, mind landmarks, on_the_way, found and ways, road-end wear, skill, fuse_calls, left and life. A feature package that relies on hooks (credit, overflow) or on the changes table for views would not see them.
11. **Cyclic imports, kept alive with function-level imports.**
    - roads ↔ herds
    - fuse ↔ night ↔ settle
    - agreements ↔ verbs
    - run ↔ api
    - world init → agreements, knowledge, perceive, things, buildings

    `World.__init__` installs feature hooks itself (`AG.install`, `BL.install`). The core imports features. This inverts the dependency the redesign wants.
12. **Fuse registration is an import side effect.** The road kinds exist only if `roads.py` has been imported (run.py does so). A feature loader must import feature modules explicitly and in a fixed order: `gather` sorts by start time but iterates `SOURCES` in insertion order for the tie-break id.
13. **The talk delivery mixes four features in one loop**: speech, knowledge, offers with child guardians, and notes and cards. The "woken" decision (who gets a talk call) depends on all of them. The evening `_requests` likewise reads the today keys of try, partner and joins, and offers.
14. **Agreements reach into many features.** Payment uses `KN.available` (knowledge), `here.takeable` and `party_container` (lodging and claims), and the `plots` prim with `FM.holdings` (farm). Work legs read the action record written by every verb's `here.record`. Offers on the road use `Here(transit=True)`. Settlement needs presence (roads).
15. **The `bot_plan`/`bot_fuse` responders** know verbs, items, roads, offers and fuse kinds. They have to be assembled from feature contributions or stay crude.
16. **exchange depends on the legacy publish_hf.py** (FILES, CARD, SUMMARIES), on `farm` for the parcels view, and on the runner carry's `results`. Its "view tables" are a feature-specific projection that sits in the kernel's export.
17. **Cost and record lines** (1082-1137) name the social and life outcomes directly (the `rec.update` keys and the print). That needs a "record contribution" hook.

---------------------------------------------------------------------------------------------------------------------------------

## 10. BUGS, DRIFT AND ODDITIES FOUND

1. **branch.STEPS lacks "evening"** (branch.py:24). `order("dN.evening")` gives `ValueError: tuple.index(x): x not in tuple` (checked in Python). `_cut` evaluates `later(step)` over every row of steps, checkpoints, events, changes and requests, so **rewind, fork and continue of any `evening:` world** (e.g. specs/fishing/water.yaml, goal_probe/*) should fail once an evening step exists.
2. `MEETING_WAVES` is defined at run.py:610, after `meeting_step` uses it. It works because it is resolved when called.
3. `evening_step` is annotated `-> None` but returns `{}` or `folded`. `meeting_step` and `fuse_calls` return nothing.
4. `TECHNIQUES` is imported in run.py:22 and unused. `fuse.WORDS` is unused. `roads.apply_choice(by_call=...)` is unused.
5. data.py:792 refers to `roads.CHALLENGES`, which does not exist (`challenge()` is an if-chain).
6. `LA.close_day` runs between steps (see §9.9).
7. The `lighten` talk_log entry (run 1025) has no `error` or `thinking` keys, unlike the others.
8. round.md lists no `settle` step in its plain table. execution.md lists no `evening` step (spec drift from the code).
9. `generate.build` mutates its input `base["lines"]` (d["place"]).
