# Stage 4 of the fishing, hunting and materials wave: signs, people and worlds (report)

23 Nov 2026, 37.2 (build subagent). Thread W-100, under the wave's integrated design (W-85). Branch `w85-s4-people` (from `main` at
bb70d396, after stage 3 merged), not pushed, not merged. Specs: `docs/cybertron2/proposals/w73_design/u8_signs.md`, `u9_people.md`,
`u11_worlds.md`, each read under its "Decisions since" table; basis.md, build_plan.md (stage 4, live run 1), integration.md; stage 1 to 3's
reports; guides/senses.md; steering.md §2 and §4; scenario_design.md; feature_packages.md §9.1 and §10. No model calls, no live runs,
no Hugging Face; bots for interfaces only (D2-298).

## In brief

- **Built, as feature units in new modules (D2-244):** `wild/river.py` (u8: the river's night record, the bands, the four leads,
  the flow, slackening, ice, otters and the fen, the carried catch); `engine/core.py` (u9 §1, §2: the core prompt, the reply, the
  system prompt in u9's order, the fixed lines) and `engine/shapes.py` (u9 §3; D2-314: the eleven shapes over the 40 handlers) behind
  `prompt: core`, with today's prompt and verb list kept as `prompt: old` (D2-331); `engine/learning.py` (u9 §4; D2-307, D2-326) behind
  `learning: record`; the watch act as `guard` widened (D2-320); `engine/livelihoods.py` and `engine/founders.py` (u11 §1 to §4, u9 §5;
  D2-268, D2-311, D2-319); `landgen/gate_check.py` (u11 §5: P1 to P21, M1 to M8, the dry probe); Eelmouth remade
  (`specs/make_eelmouth.py`, `nutrition/eelmouth.yaml`, `nutrition/eelmouth_old.yaml`; D2-316, D2-330, D2-331, D2-334).
- **The gate check:** the remade Eelmouth passes with four warnings (P7 lessons not written, P10 the pan's mending wants copper,
  P11 copper made nowhere, P18 no village in reach: the last three by design, C3); today's runs world is refused for P3 (no livelihood
  rows) and P2 (no keeper lines), as u11 §5.3 said.
- **Tests:** before (bb70d396) 814 passed, 2 skipped; after (the branch head) 835 passed, 2 skipped (21 new in
  `tests/test_cybertron2_stage4_people.py`). One test updated to u8 §5's keeping words (§4).
- **Bots:** `runs_high` with `--bots runs` for 40 days: no errors, replay of 320 steps with no mismatch, 5 alive on day 40. The remade
  Eelmouth with `--bots runs --days 40`: no errors, replay of 304 steps with no mismatch; the village dies out by day 38 (the run ends
  when no one is left). That is the bots' fixed policy on a world with fewer traps and rougher hands, not a reading of the world (D2-298; §7).
- **Renders:** every founder's system prompt and first morning message, both live arms, day 0, in `live1_renders/` (§7).

## 1. What was built, by file

| File | What changed |
|---|---|
| `wild/river.py` (new; u8) | data: `BANDS`, `DAWN`, `DAY`, `CARRIED`, `WATER_CRAFTS`; reads: `band`, `year_basis` (last year's tally, else this year's tally, what is still to start upstream and what is on the way), `flow_today` (`river_now`'s flow: the catchment's rain and the day's weather, as the night reads it), `river_now`, `passing`; the record (`record`, from `_runs_night`); the emitters `dawn_events` (the dawn cue and the dawn rows of the flow and the ice), `day_signs` (the run in bands, the flow, slackening, otters, the weir's overflow, the fen), `carried` (the catch carried home) |
| `engine/wild.py` | `_runs_night` captures what passed before any take and writes the river's record before the runs move on |
| `engine/run.py` | `RV.dawn_events` at dawn; the shapes' normalising of each planned act in a core world; the meeting block anchored on the world's closing line |
| `engine/perceive.py` | `dawn` reads a dawn event's `knows`, `lay` and `only`, and a text once; `practised` adds `fish` (any water craft from a rough idea up, D2-325; a basic one only practised) and `expert:fish`; a founder's seeded lines keep their source, and their places are counted from day 0 (D2-308) |
| `engine/signs.py` | `_wild_river` emits u8's rows (the old "down" and "up" rows give way); `facts` adds the carried catch; the sky's two river rows only where the river keeps no record (u8 §3.1); the smokehouse's rows reworded to what is seen from outside (u8 §5) |
| `engine/core.py` (new; u9 §1, §2) | `CORE` (u9 §1.2's twelve lines and their variants), `GRAMMAR` (the rules block's grammar at the core's budget, 78 words), `reply_text` (u9 §1.3 with the person's own example), `system_prompt` (u9 §2.1's order), `rest_line` (D2-301), the fixed lines (`CLOSING`, `EVENING_WHY`, `EVENING_STANDS`, `MEMORY_APPEND`) |
| `engine/shapes.py` (new; u9 §3) | `SHAPES` (args, grammar line, faces), `normalize` (a craft or an act to a handler; a set technique named alone by what stands; refusals naming one's own crafts), `quiet`, `lines` (What you can do), `crafts_by_shape`, `example` |
| `engine/prompt.py` | `system_prompt` and `schema_for` dispatch on `prompt: core` (`do` and `what` free, `look_up` gone, `on trouble` in the alphabet's order); the closing line by the world; the memory request's append wording in a core world; children's seeded lines shown without their source |
| `engine/view.py` | the closing line by the world; "You rested n units yesterday." in "## You" in a core world |
| `engine/evening.py` | in a core world, "What you set stands ..." and the why line without "tomorrow" |
| `engine/here.py` | `Mind.core` |
| `engine/verbs.py` | `do` and `cost` read a shaped act; `_make`'s odds and materials from `learning.try_row`; `guard` widened (a place or a herd, by night or by day, D2-320), a day's watch costing the units given |
| `engine/learning.py` (new; u9 §4) | `CLASSES`, `CLASS_OF`, `scale`, `share`, `skill_of`, `practice_of`, `try_row`, `tried`, `taught`, `fade_params` |
| `engine/knowledge.py` | `tried` goes to `learning.tried` in a learning world (the hunt keeps its curve); `skill_word` reads the class's range there and never fails below a range |
| `engine/settle.py` | `_teach_day` goes to `learning.taught` in a learning world |
| `engine/labour.py` | fading on the life clock in a learning world |
| `engine/livelihoods.py` (new; u11 §1 to §4) | the fifteen rows, `HOLDINGS`, `fill` (pinned households: experts by D2-270's size rule, the capable share, a keeper raised where none can keep a holding, apprentices by a keyed draw, the second trade's hands, knows and skills by band and class, keepers, gear by D2-330 C5, the cast, neighbours aware, the livelihood line), `livelihood_line` |
| `engine/founders.py` (new; u9 §5) | the templates (BS1 to BS9, PE1, PE2, HH1, HH3, HH5 to HH9, FI1 to FI12, FI15 to FI19, SA1 to SA5, the NB lines, HL), `wanted`, `render`, `cap` (u9 §5.2's drop order and protected lines), `seed_world` |
| `engine/life.py`, `engine/data.py` | a youth eats 0.8 a night (D2-330 C6); `LIFE.youth` |
| `engine/world.py`, `engine/schema.py`, `spec/core/world_schema.md` | people `livelihood`, `crafts_first`; buildings `keeper`; `today.day_watch`; `wild.river`; version 15 |
| `wild/kinds.py` | `SCARE_WORDS["watch"]` |
| `engine/book.py` | the rules block names "the Marshs household", not "the the Marshs household" |
| `landgen/gate_check.py` (new; u11 §5) | `people_checks` (P1 to P3, P5 to P8, P10 to P21), `check` (with `gates.making_gates`, `probe_making` and `gates.probe`), a command line |
| `specs/make_eelmouth.py`, `specs/nutrition/eelmouth.yaml`, `eelmouth_old.yaml`, their `.report.json` | Eelmouth remade and its two live arms (§1.1) |
| `specs/render_eelmouth.py`, `live1_renders/` | the renders of §7 |
| `tests/test_cybertron2_stage4_people.py` (new) | §2 |

### 1.1 Eelmouth remade (u11 §7; D2-330)

From `runs_high.yaml` (seed 5: the same land and people). The Salt House and the spring to the Brooks (C1); a rock parcel, the Scar,
beside the Spinney and Hazel Copse (C2), with each head given a rough idea of quarrying (a default taken: no mason lives here, so the
stone could not otherwise be had; reported in the world's report); no other village in reach (C3); water-only as the runs world already
was (D2-316); the smoke huts wattle huts of one set of racks, a hut room of 2 spaces (D2-284, D2-291). Pinned: the Marshs fishers
(expert: weir and nets), the Shepherds fishers (expert: keeping; fowling postponed, D2-318), the Brooks salters with fishing beside.

| Person | Band | Keeps | Model | Seeded lines (words) | Livelihood line |
|---|---|---|---|---|---|
| Peter (head) | expert, weir and nets | the weir | Opus | 20 (676) | You live by fishing, and you are best at the weir and its nets, and you keep the weir on the Isel. |
| Nichola | capable (raised to keep the smoke hut) | the Marsh Smokehouse | Sonnet | 20 (669) | You live by fishing, and you keep the Marsh Smokehouse. |
| Nigel (youth, 18) | broad, apprenticed to Peter | | Haiku | 10 (350) | You are learning your household's living from Peter, at the weir and its nets. |
| Hamon (head) | expert, keeping | the Shepherd Smokehouse | Opus | 20 (651) | You live by fishing, and you are best at keeping the catch, and you keep the Shepherd Smokehouse. |
| Gunnild | broad | | Haiku | 19 (567) | You live by fishing. |
| Oliver (head) | expert, the pan | the Salt House | Opus | 20 (642) | You live by boiling salt at the spring, and by fishing beside it, and you are best at the pan, and you keep the Salt House. |
| Katherine | broad salter, capable fisher | the Brook Smokehouse | Haiku | 20 (664) | You live by boiling salt at the spring, and by fishing beside it, and you keep the Brook Smokehouse. |
| Petronel (youth, 14) | broad | | Haiku | 8 (274) | You are learning your household's living. |
| Henry, Margery (children) | | | | 2 each, as if passed by a carer | |

Gear (C5): six wicker traps each to Peter, Nichola, Hamon and Katherine (the capable and expert setters), a gill net to Peter, a hand
line to each adult fisher, four copper hooks in each fishing house (nothing gives bone yet). Settings: `prompt: core`, `learning:
record`, `memory.kept` 40 words, a place every 3 days, 30 in all (D2-266, D2-308), `llm.week_stop` 0.99 (D2-334), 40 days. The
comparison arm `eelmouth_old.yaml`: `prompt: old`, `skills.depth: none`, no kept lines (the world's generated memories as today), 14 days.

## 2. Each change, with its test

All in `tests/test_cybertron2_stage4_people.py`.

| Change | Test |
|---|---|
| the core's twelve lines and variants; no horizon, season or food figure but line 2's "fewer in winter" | `test_core_words_render_twelve_lines_with_no_horizon_season_or_food_figure` |
| `prompt: old` keeps today's prompt and verbs; the core replaces it; the closing line; `do` free | `test_the_old_prompt_is_kept_as_a_setting_and_the_core_replaces_it` |
| the reply's example from one's own living; offers in placeholders | `test_reply_examples_are_each_persons_own_craft` |
| the shapes: a craft, a shape with its face, an old verb; a refusal naming one's crafts | `test_the_shapes_resolve_a_craft_or_an_act_to_its_handler` |
| a set technique named alone: set from the hands, then tended | `test_a_set_technique_named_alone_sets_from_the_hands_then_tends` |
| units left are rest, said next morning (D2-301) | `test_units_left_are_rest_said_next_morning_with_no_push` |
| learning x 64 / lifespan; fading on the life clock (D2-307) | `test_learning_scales_with_the_lifespan_and_fades_on_the_life_clock` |
| practice alone reaches known, twice the tries (D2-326) | `test_practice_alone_reaches_known_more_slowly_than_with_teaching` |
| a session by class, never past the teacher's peak | `test_a_lesson_session_lifts_by_class_and_never_past_the_teachers_peak` |
| old worlds keep the old learning | `test_old_worlds_keep_the_old_learning` |
| the watch act (D2-320) | `test_the_watch_act_over_a_place_a_herd_or_a_building_by_day_or_night` |
| the bands | `test_bands_by_the_stations_year` |
| the river's record, its flow the night's | `test_the_river_record_is_written_each_night_and_its_flow_is_the_nights` |
| dawn rows by the rule and by who reads them | `test_dawn_rows_reach_the_houses_by_the_rule_and_only_those_who_read_them` |
| the carried catch: others, never the carrier; 3 kg nothing; fish from the store nothing | `test_the_carried_catch_reaches_the_others_and_never_the_carrier` |
| no sign directs an act | `test_no_sign_directs_an_act` |
| the fill: bands, keepers, gear, cast (D2-270, D2-330) | `test_the_fill_places_bands_keepers_gear_and_the_cast_by_d2_270_and_d2_330` |
| the founders' lines: 20, 40 words, figures from state, the evening line (D2-319), the old arm none | `test_every_founders_lines_fit_twenty_and_forty_words_and_state_their_figures` |
| the cap's order and protected lines | `test_the_cap_drops_in_order_and_keeps_the_protected_lines` |
| the gate passes Eelmouth, refuses the runs world, an all-Haiku cast and an apprentice to no expert | `test_the_gate_check_passes_eelmouth_and_refuses_todays_runs_world` |
| a youth eats 0.8 | `test_a_youth_eats_eight_tenths` |

## 3. The numbers changed

- **A youth's food** 0.8 a night (was 1.0), every world (D2-330 C6).
- **The river's rows' `own`,** set to land where u8 §6 intends through the rule (guides/senses.md item 4). The engine's presence is
  about 1 on a parcel one worked and about 0.125 next door for a row seen "around" (u8 §6 reckoned 0.5 and 0.3), so the around rows
  carry about 2.4 times u8's own: eels running 2.9, thick 3.8, a glut 4.8, salmon in the pool 3.8, the first silver eels 3.6, the river
  up 2.9, dropping 2.4, an otter in day 2.4, the weir's overflow 2.9; the roar 3.3, the night's splashing 2.7, eels on the fen grass
  2.4. As the rule gives them now (Peter worked at the Isel, Hamon at the Fen next door, Gunnild at the Street):

| Row | At the water | Next door | The Street | u8 §6 (water / next door / Street) |
|---|---|---|---|---|
| eels running (sight 2.9, around) | 1.00 | 0.37 | 0 | 0.6 / 0.36 / 0 |
| eels thick (3.8, around) | 1.00 | 0.48 | 0 | 0.8 / 0.48 / 0 |
| a glut (4.8, around) | 1.00 | 0.61 | 0 | 1.0 / 0.6 / 0 |
| herons standing (sight 3.0) | 1.00 | 0.38 | 0.13 | 1.0 / 0.9 / 0.15 |
| the roar (sound 3.3) | 1.00 | 1.00 | 0.25 | 1.0 / 1.0 / 0.25 |
| the night's splashing (sound 2.7, night) | 0.24 | 0.24 | 0.24 | 1.0 / 1.0 / 0.24 |
| eels on the fen grass (sight 2.4) | | 0.31 | 0.06 | / 0.36 / 0.06 |
| the smell of a run (smell 0.8) | 0.40 | 0.24 | 0.04 | 0.4 / 0.24 / 0.04 |
| the river in spate (sight 2.0) | 1.00 | 0.25 | 0.08 | 1.0 / 0.6 / 0.1 |
| the fishers' band reading (sight 0.9, near) | 1.00 | 0 | 0 | 0.9 / 0 / 0 |
| otter tracks (sight 0.6, near) | 1.00 | 0 | 0 | 0.6 / 0 / 0 |
| the expert's eel night (everyone at the place, 0.3) | 0.2 to 0.4 for an expert anywhere at the place (tested) | | | 0.3 |
| smoke rising from a smoke hut (sight 3.6) | | 0.46 (the Street is next door to Eelmouth Field) | | 0.75 / 0.45 / 0.075 |

  On the parcel the plain rows are near certain (higher than u8's 0.6 to 0.9, by the engine's presence there); next door and from the
  Street they land on u8's figures. The night rows from the water are low for one asleep at home, as u8 intends.
- **The rows' thresholds:** bands at 2, 8 and 20% of the station's year (u8 §1; calibrate); the carried catch from 5 kg of fresh fish
  after work on water or fen, "as much as they can carry" from 10 kg.
- **Learning (`learning: record` worlds only):** u9 §4.2's classes (chances aware/rough/capable 0.6/0.8/0.95 simple, 0.35/0.55/0.8
  practised, 0.15/0.35/0.65 skilled; materials 1.3/1.15/1.05, 1.8/1.5/1.2, 2.0/1.8/1.4; marks 1/2/2, 2/3/4, 3/4/4; tau 7, 17, 33;
  ranges 0.8 to 1.3, 0.6 to 1.6, 0.5 to 2.0); practice alone needs twice the mark to known and, in a skilled craft, grows at a quarter
  past half the range (D2-326: `ALONE` 2, `ALONE_BEYOND` 0.25, defaults); a session +2 score, simple and practised to capable at once,
  skilled to rough then capable, skill toward the teacher's peak by 1 - 0.75^s (x1.3 at the peak); fading after 16 days, half of what
  can be lost each 32, divided by s.
- **The fill's defaults:** experts by D2-270; the capable share a third of the rest, rounded; the apprentice draw 0.5 (B11-2); skills
  by band within the class's range (an expert the top 45%, a capable member the middle quarter, the broad band the lowest quarter).
- **The prompt's sizes** (words, day 0): the core system prompt 1,396 to 1,798 (u9 §2.9 estimated 1,000 to 1,470: the universal crafts
  under make and work run long, and every person's people and places are as before); the old system prompt 6,517 to 6,947. The first
  morning message 1,522 to 1,948 in the main arm (the 20 seeded lines are about 650 of it) and 1,066 to 1,279 in the old.

## 4. Tests updated, and why

| File | What and why |
|---|---|
| `test_cybertron2_water5_keep.py` | `test_the_smokehouse_and_the_salt_pan_are_seen_and_smelt`: the smokehouse's rows are u8 §5's words ("smoke rising from ...", "the smell of smoke and meat about ..."), which say what is seen from outside and no longer name what hangs inside |

No other test changed: the new behaviour sits behind `prompt: core` and `learning: record`, which no older world sets, and u8's rows
replaced only rows no test pinned.

## 5. Spec drift found

- **The handlers are 40, not 38:** stages 2 and 3 added `tend` and `rule`. The shapes sit over all 40.
- **`rule` stays an act** (`{"do": "rule", ...}`, free, under change), as stage 3 built it, not u9 §1.3's free reply field.
- **`watch` stays the learning verb** (a day beside someone); u9's attention with units (§4.5, departure 21) is not built. D2-320's
  watch act is `guard` widened.
- **u9 §1.2's line 2 names winter** ("fewer in winter"), though u9 §7's test forbids season words; the line is kept as written.
- **A world without `prompt`** keeps the old prompt (D2-314: old worlds keep the 38); the remade Eelmouth sets `prompt: core`.
- **`river_now`'s record:** `share_run` returns no "turned"; the weir's overflow is its share of what passed less what it took. The
  first year's basis is this year's tally, the quota still to start upstream and the pulses on the way (u8 §1's "the quota and dues at
  the window's start").
- **Presence:** see §3: `own` was moved, not the rule.
- **The sky's river rows** are kept for worlds whose river keeps no record. The "fish rising" and "quiet water" rows (u8 §3.4) and the
  ambient "water running over stones" (data.py) are not reworked.
- **The Shepherds' second living** (fowling) is out with fowling (D2-318); **FI19** names the salter's need as firewood (the world has no
  grain); **FI10** reads D2-302's cost table (`cost.first.wattle`), where u9 assumed another shape.
- **u11's worked Eelmouth** put Gunnild and Katherine at broad and Nichola at capable; the fill reaches the same by raising a keeper to
  capable where no one could keep a holding (a step u11 §2.3 names, here made explicit and reported).
- **C2's rock** needed a hand that can quarry (no row has quarrying in the fisher's or salter's bands); each head has a rough idea of it
  (reported in the world's report).
- **Old line numbers:** u8's `wild.py:3072` (`_runs_night`) is at 3223; `signs.py:2417` (`_wild_river`) at 2441; `signs.py:888-902`
  (PERSON) at 904; `perceive.py:350` (`dawn`) at 365; `prompt.py:490` (`system_prompt`) at 490; `view.py:222` at 222; `evening.py:85-91`
  at 89-95; `memory.py:135` at 135. The rest matched.

## 6. Not done, and why

- **u9 §4's lessons, failure lines, capability points, aptitudes, attention spent in units, children minded at home:** not built
  (the brief named the record, the scale and D2-326's practice and teaching). P7 warns that no craft has lesson rows.
- **u9 §2.6 (goods by familiarity), §2.7 (one's own things with their tags in "## You"), the carry line in kilograms:** not built.
- **u11's generator steps 3, 5 and 7** (unpinned households drawn by `village_mix`, the tree with livelihoods, what spouses carry), and
  the Hollinford maker: not built; `fill` takes pinned households on a written world and reports the unpinned.
- **Founders' templates** for the farmer, herder, hunter, smith, miller, builder, woodsman, basket maker, cord, trader and cottager
  (their rows are written; their lines are not): Eelmouth needs only the fisher's and the salter's. PE3 (elders) not written (no elder).
- **u8's gaps** as u8 lists them (the moon, a flood over the land, gulls, news from upriver, smell's visibility, the remembered good
  and thin years past two). The fowl rows are as built.
- **The old arm's stripping** is in its world file (`skills.depth: none`, no `kept`), not in `prompt: old` itself.
- **Records** (the W-100 row, `records commit --builds`, hygiene): the calling session's.

## 7. Results

**Tests (`python3 -m pytest -q`, six shards):** before (bb70d396) 814 passed, 2 skipped; after (the branch head) 835 passed, 2 skipped.

**Bots:** `python3 -m cybertron2.engine run cybertron2/specs/nutrition/runs_high.yaml --bots runs --days 40 --out <dir>`: 40 days, no
errors, the seeded death on day 1, deaths on days 25 to 32, 5 alive on day 40 (stage 3: days 24 to 26 and 39, 4 alive); its replay checks 320 steps with no mismatch.
`python3 -m cybertron2.engine run cybertron2/specs/nutrition/eelmouth.yaml --bots runs --days 40 --out <dir>`: no errors; deaths from
day 19 (the Shepherds and the Brooks by day 22, the Marshs from day 36), no one left on day 38, where the run ends; its replay checks
304 steps with no mismatch. From its turns: 16 settings of traps from the hands, 33 tends, 10 makes of traps, 45 acts by the households'
rules; the river's rows reached people as designed (the roar on 46 person-mornings, the expert's eel night 10, the night's splashing 13,
eels on the fen grass 6, edge ice 9, the eels running in the shallows 6, salmon 4, the run over 1). The bots' policy has the heads keep
and only those who know the setting and the making set traps; in Eelmouth only four people hold traps (24 against the runs world's 36)
and three know the traps roughly, so the bots catch less. That is the policy on a different world, not evidence about it (D2-298).

**The gate check** (`python3 -m cybertron2.landgen.gate_check <world>`; people checks on every current world):

| World | Refused | Warned |
|---|---|---|
| nutrition/eelmouth, eelmouth_old | none | P7, P10, P11, P18; M1 to M8 none (M4 gone with the Scar, M6 with Peter's net-making, M3 with C5's gear); the probe: only the farm's acts and the fowling net shut |
| nutrition/runs_low | P3 x3 | P7, P18 |
| nutrition/runs_medium | P2 x6, P3 x3 | P7, P18 |
| nutrition/runs_high | P2 x10, P3 x3 | P7, P10, P18 |
| water/runs | P2 x6, P3 x9 | P7, P10, P16 x6, P18 |
| water/river | P2 x4, P3 x6 | P7, P10, P18 |
| water/lake | P3 x3 | P7, P18 |
| fishing/water | P3 x3 | P18 |
| valley_s5 | P2 x2, P3 x4, P21 | P7, P18 |
| hollins_s7 | P3 x5, P21 | P7, P16 x3, P18 |
| hollins2_s8 | P3 x3, P21 | P7, P18 |
| region_c_s27 | P2 x6, P3 x12, P21 | P7, P16 x7, P18 |
| two_valleys_s1 | P2 x4, P3 x5, P21 | P7, P18 |
| wide_s7 | P2 x2, P3 x7, P21 | P7, P16 x6, P18 |
| wenbridge | P1, P2 x2, P3 x5 | P7, P18 |
| combe | P3 | P7, P18 |
| frontier_camps | P3 x4 | P7, P18 |

P3 everywhere is the absence of livelihood rows in worlds made before them; P21 is a world without the beliefs view.

**The renders** (`python3 cybertron2/specs/render_eelmouth.py`): `live1_renders/main_<name>.md` and `old_<name>.md` for the eight
founders who act on day 0, with a size table in `live1_renders/README.md`.

## 8. Live run 1: the commands (on Zach's go, D2-333; each published to Hugging Face when it finishes, D2-332)

From the repository root, with the stage merged (or from this worktree):

- the main arm: `python3 -m cybertron2.engine run cybertron2/specs/nutrition/eelmouth.yaml --out runs/live1_eelmouth` (40 days);
- the comparison arm: `python3 -m cybertron2.engine run cybertron2/specs/nutrition/eelmouth_old.yaml --out runs/live1_eelmouth_old` (14 days);
- the bot null arm: `python3 -m cybertron2.engine run cybertron2/specs/nutrition/eelmouth.yaml --bots runs --out runs/live1_eelmouth_null`.

Each writes its run to the `--out` directory (`run.db`, the journal; `run.json`; `turns.jsonl`, `days.jsonl`, `perception.jsonl`,
`memory.jsonl`, `state.json`). The backend is `LLM_BACKEND` (default `claude_code`); both live arms stop at 99% of the weekly window
(`llm.week_stop` 0.99, D2-334). Publishing: `python3 -m cybertron2.engine publish runs/live1_eelmouth --push` (and the same for the others).
