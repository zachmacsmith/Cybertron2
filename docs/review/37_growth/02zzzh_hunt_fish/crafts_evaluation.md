# Crafts and techniques: what the design meant to be, how it held up, and what follows

22 Nov 2026, 37.2 (subagent). Thread: the crafts and techniques design evaluated (W-74). No code changed.

Zach (22 Nov): "Can you evaluate overall: what was the intent for the generalized design and theoretically extensible design for
the crafts and techniques, how well has it held up, where is it failing, does this point toward any new design choices etc.? ...
how well have things been actually working. The 28 day river run could be especially good to look at."

**Runs read** (all from `zachmacsmith/cybertron2-runs`, journals in full): the river run `water_runs_models_r1` (30 days, d0 to d29:
the full run, re-uploaded 20 Nov; its viewer pages stop at day 6 but the journal does not), `pw1_opus_sonnet_r1` (100 days),
`wild_region_s7` (30), `water_lake_r1` (14), `water_lake_r2` (24), `c3_combe_rich` and `c2_combe` (80 each), `f1_frontier` (39),
`e2_labour` (32). No run asked for was missing. Thinking is kept only for Haiku 4.5, Opus 4.5 and Sonnet 4.5 in the river run;
the others' reasons come from `why`, talk, notes and memories. Scripts and extracts are in the scratchpad (`eval/scripts/`).

**Read with:** the engine audit ([engine_audit.md](engine_audit.md): goods, gear, sets, tool grades, wear and the seams; not
repeated here), why the villagers did not fish ([02zzy](../02zzy_why_they_did_not_fish.md)), the fishing methods compared
([02zzy2](../02zzy2_fishing_methods_compared.md)), carrying in the runs ([02zzv](../02zzv_carrying_in_runs.md)), the river run's
first week ([38.78](../../38_space_engine/78_runs_models_days0_7.md)).

## The short answer

- **The intent** was one mechanism for every craft: a small set of verbs whose objects are technique rows (D4-24); knowledge as
  four levels per person that rise by being told, watching, explaining, teaching and practice, and fade without it (D4-33,
  D2-52, D4-105); legible to agents through cards, options with near misses and refusals that name the shortfall; and a new
  craft as a data row.
- **What holds:** the knowledge store and its paths work and are used (17 lessons in the river run, each raising its learner to capable or known);
  refusals name the shortfall and agents learn from them and write the rule down; `make` really is data-driven; general wild
  methods generated from traits (D2-204) are the one place the "new kind is a row" promise is kept; fading works as decided.
- **What fails:** the deep chains almost never run. Across nine runs and about 5,500 agent-days, nobody milled grain, baked
  bread, built a weir or a smokehouse, or smoked anything; charcoal was made once and copper only by a household seeded as
  smiths. The causes are mostly not the knowledge model: world gates that were never checked (no rock in any river village, a
  water mill that needs 200 grain in one act), recipes shown without their inputs, a 10-option list cut in table order that
  never shows the crafts people actually use, a 73-craft "Everyone knows" line, and a goal that spends the units elsewhere.
- **In the code** the design bent: of 132 technique rows only `make` (31) is truly data on one handler; `gather` and `work` (53)
  run on 33 yield kinds, 25 of them used by a single craft and each a branch in `verbs._technique`; `build` (25) has its real data
  in five other tables; 23 rows are modifiers. A new craft of any depth (the smokehouse, the weir) costs 300 to 1,100 lines of code
  in 5 to 10 files for 25 to 80 lines of data.
- **What follows,** ranked by expected effect: verify every gate in the generator; show each craft's inputs and what it gives where
  agents look; order options by relevance (or drop them, as the river run does); seed knowledge by livelihood (W-70) so the craft
  list is short and specific; make the thing the target of an act (Q-80); redefine `aware` so it can be tried; then move the yield
  kinds into packages as code beside data, which the feature-packages cut needs anyway.

## Part 1: the intent

### What the records set out

| Goal | Where it was set | What it says |
|---|---|---|
| **The world grows by data** | D4-24 (23 Oct); proposals/verbs.md, knowledge.md | "new and richer actions are added as data (techniques, fittings, settings, powers, clauses) on a small set of verbs, and agents come to know them in the world (seeing, being told, taught, reading, trying), not from a complete manual" |
| **Few verbs, many objects** | knowledge.md §1; verbs.md (24 verbs; the list never decided, Q-27) | "cybertron 1 had 145 actions, one per mechanism. Here the verbs are few and general, and the variety is in their objects" |
| **Knowing that vs knowing how** | knowledge.md §3, §4c; D4-33 | four levels, aware, rough idea, capable, known; "Awareness without know-how is what makes specialists worth paying and secrets worth keeping"; seeded knowledge of other lines' crafts is awareness, not skill (D4-33) |
| **Paths up** | knowledge.md §4c, §4e | told or mentioned: aware; 3 sightings: rough; `explain`: rough; `teach` one session: capable (a youth: known); 2 successes a level by practice; trying with a rough idea at x1.7 inputs, 1 in 2 |
| **Skill by practice and fading** | D2-52; D4-103 phase 2; D4-105 | basic work x1.0 to 1.5, a trade x0.5 to 2.0; fades only after half a year unpractised, never below 60% of one's best gain, relearnt three times faster |
| **Legible to agents** | knowledge.md §2, §4c, §4d; D4-95 | "what an agent can do here computed and shown"; "near misses help planning ('you could make a blade with 4 more copper')"; refusals "saying exactly what is short, at no cost"; a look-up of the full card |
| **No blind crafting** | knowledge.md §6 | "an agent can only make what it knows how to make"; "Agents are never asked to guess" |
| **A basic set and trades** | D2-43 (recipes.md §5) | basics everyone knows; ten trades |
| **Modifiers as know-how** | D2-93, D2-112 (verb_modifiers.md) | ways of doing an act (hidden, method, range) are rows, learned like crafts |
| **General methods for the wild** | D2-204 (methods_and_encounters.md) | "bespoke single actions should in general usually instead be using general methods in a specific way"; take tables generated from the kinds' traits; skill in two layers (method, familiarity by kind) |
| **Recipes at scale** | D4-97 (mill_and_oven_scale.md) | ox mill 64 grain in 2 units, water mill 200 in 2, oven 100 loaves in 3 |
| **Packs** | D4-103, D4-104 | switchable bundles of rows; "a pack off is a clean null arm" |
| **Tags** | D4-68 (referent_tags.md) | things one acts on get short tags (H2, T5) the verbs accept |
| **Show by familiarity** | D2-251 (20 Nov, from Q-51); agent_view.md point 3 | "a short sentence for one who has only heard of it, a longer one with what it gives back for one who knows it roughly, the specifics ... for one who knows it well; one pattern for everything" |
| **The view without computed choices** | D4-78 (`view: beliefs`); agent_view.md point 1 | "Drop 'Today you could' and 'Not yet'. A refused act already says why" |
| **Livelihoods first** | D2-243 (20 Nov), W-70; livelihood_archetypes.md | verbs and archetypes reshaped before the feature-packages rework, "keeping this future refactor in mind" |
| **Features as units** | D2-244, L-133; feature_packages.md P3 | "Features are data on the core's primitives. A package adds code only for a new kind of thing; a new kind of change (a yield kind); a process with its own dynamics; the context its signs read" |
| **A web of chains** | economy_web.md (discussion) | "The engine's economy is mostly one step deep: 63 goods, most of them one act from the land and one from being eaten" |

### The design's goals, as its authors set them

1. **General:** one mechanism (a technique row: verb, `at`, inputs, tools, fittings, yield, units) for every craft, from foraging to
   smelting, and for every way of learning it.
2. **Extensible:** a new craft is a data row; a new pack switches a set of rows on and off.
3. **Knowledge as levels that rise and fade,** so specialists, teaching and secrets have value.
4. **Legible:** agents see what they know at the depth they know it, what they can do here, what they nearly can, and a refusal
   that teaches the recipe.

Two of the original promises were changed on the way: "Today you could" was dropped where `view: beliefs` is set (D4-78), and the
aware level, "Cannot attempt it" in §4c, became tryable for some crafts (`untaught: tryable`, 10 rows).

## Part 2: how it has held up in the code

### The technique table today (main, 22 Nov)

| | Rows | Handler | Truly data? |
|---|---|---|---|
| `make` | 31 | one handler, `verbs._make` (verbs.py:760-856) | **yes**: inputs, gives, `at` fittings, units; with special cases inside it for racks (`rack`, `batch`: 4 rows), the smokehouse's tended fire, the water wheel's gap (`mill_rate`), the brine pan's rim mark, an ox at millstones |
| `gather` | 21 | `verbs._technique` (verbs.py:559-757), dispatching on `yield.kind` | partly: `stock`, `fixed`, `pool`, `chance` are general; the wild layer's 7 take methods share `wild_take`, generated from traits (wild/methods.py `build`) |
| `work` | 32 | the same hub | mostly not: 25 of the 33 yield kinds on gather and work rows are used by **one technique each** (sow, weed, reap, herd, care, milk, slaughter, repair, bury, burn, tend the smoke, den work, gather young, pest work, guard the field, shut, ...), each a branch of the hub calling farm.py, wild.py, keeping.py or wear.py |
| `build` | 25 | `_build`, `_monument`, `_weir_part`, `_fitting`, `_add_room`, `_upgrade` (verbs.py:899-1408, about 500 lines) | the rows are shells: the materials live in ROOMS, BLUEPRINTS, FITTINGS (17), MONUMENTS and WATER_WORKS |
| modifiers | 23 | `modifiers.resolve` | data, but kept in the craft table, so they count as crafts for awareness ("hidden: under brush" heard of 35 times in the river run) |
| **All** | **132** | | **94 basic** (71%); packs: none 79, wild 25, farming 17, water 9, two rows in both |

Other bends, beyond what the engine audit found (gear, sets as free containers, two tool grades, wear not reaching the take):
- **Twin rows by pack.** `forage` and `gather wild food`, `hunt` and `hunt the wild` are the same act twice. The old rows live on for
  replay; the mention rule makes people "aware" of them (29 `forage` awareness records in the river run, from people who forage
  daily), and children are seeded with `forage` while adults use the other.
- **Names in code.** Outside data.py, `"weir"` appears 32 times in 9 modules, `"trap in water"` 21 times in 7, `"hearth"` 16 times in
  7, `"salt"` 13 times in 4. A craft that has a process (catching by night, a fire to tend, a gap to set) is not a row: it is a
  row plus a module plus signs plus prompt prose.
- **Recipes with an all-or-nothing minimum.** `water mill` takes 200 grain in one act and `mill` 64, not "up to" (no `batch`):
  D4-97's scale, built as a minimum.
- **The description ladder (D2-251) is not built.** No technique row has a `does` sentence (17 of 17 fittings do); 3 rows have a
  `manual`. The `make` line in the verb list gives each recipe's fitting but never its inputs or what it gives (prompt.py:128
  `_craft_note`); `build` lines give materials and units in full.

### What a new craft costs

| Addition | Commits | Data lines (data.py) | Code lines added | Code files touched |
|---|---|---|---|---|
| The smokehouse and the brine pan (brief 5 §4a, §4b, D2-209) | 5be6fa30, c102502d | 55 | 401 (keeping.py new, 252) | 11: clocks, knowledge, night, perceive, prompt, run, signs, verbs, here, keeping, capacity/graph |
| The weir (brief 5 §3, D2-210 to D2-213) | f8e97336, c2f2ff46 | 45 | 801 | 9: night, prompt, signs, things, verbs, wild, world, knowledge, wild/runs |
| The weir in sections by position and material (W-69) | 099c9d38, 5608de7d | 41 | 330 (wild/gear.py new, 196) | 5: prompt, verbs, wild, wild/gear, bots_livelihood |

So a craft with any process of its own costs 7 to 18 lines of code for every line of data, a quarter of it in shared hub files
(feature_packages.md §11 measured the same share for the wild briefs). The `make` recipes added in the same briefs (salt fish, salt
meat, dry fish, smoke fish) were the cheap part: a row each.

**Verdict on the code.** "A new craft is a data row" holds for one-step recipes at a fitting and for take methods over wild kinds.
It does not hold for anything that acts on the land, a beast, a thing or the night, which is most of what makes a livelihood. The
hub is the seam the feature-packages cut (D2-244) must open: P3 already allows "a new kind of change (a yield kind)" as package
code, which is the honest form of what has been built.

## Part 3: how it has worked in the runs

### Refusals of craft acts (gather, work, make, build, teach, learn, explain)

| Run (days) | Craft acts | Craft refusals | Share | Target | Place or season | Input | Site state | Tool or fitting | Unknown craft | Wrong verb or name |
|---|---|---|---|---|---|---|---|---|---|---|
| river (30) | 2,695 | 370 | 13.7% | 109 | 102 | 81 | 13 | 26 | 17 | 10 |
| pw1 (100) | 4,967 | 327 | 6.6% | 93 | 83 | 101 | 32 | 0 | 13 | 1 |
| wild_region_s7 (30) | 2,933 | 214 | 7.3% | 71 | 31 | 46 | 47 | 6 | 7 | 1 |
| water_lake_r1 (14) | 369 | 36 | 9.8% | 16 | 11 | 6 | 0 | 2 | 1 | 0 |
| water_lake_r2 (24) | 514 | 49 | 9.5% | 13 | 15 | 2 | 8 | 8 | 1 | 0 |
| c3_combe_rich (80) | 1,192 | 91 | 7.6% | 16 | 41 | 9 | 24 | 0 | 0 | 0 |
| c2_combe (80) | 971 | 95 | 9.8% | 11 | 34 | 8 | 38 | 0 | 0 | 1 |
| f1_frontier (39) | 741 | 101 | 13.6% | 20 | 35 | 17 | 19 | 0 | 4 | 0 |
| e2_labour (32) | 486 | 86 | 17.7% | 20 | 20 | 5 | 14 | 1 | 9 | 17 |

Classified from the result lines by text (a refusal the runner repeats is counted once; "other" left out). "Target" is a named
thing that is not there or not so (a sound house to repair, a pest not on the crop, a herd by a wrong name). "Unknown craft" is
rare everywhere: the knowledge gate almost never blocks, because almost everything is basic.

What they did next: of the river run's 57 refused `make` acts, 12 were retried within three days; pw1 36 of 85, wild_region 15 of
36. The rest were dropped.

### Knowledge moving

| | river (30 d) | pw1 (100 d) | wild_s7 (30 d) | lake_r2 (24 d) | c3 (80 d) | c2 (80 d) | f1 (39 d) | e2 (32 d) |
|---|---|---|---|---|---|---|---|---|
| Aware from speech | 226 | 75 | 118 | 18 | 9 | 13 | 11 | 47 |
| Rough from watching / explain | 4 / 2 | 11 / 0 | 1 / 0 | 2 / 1 | 0 | 1 / 1 | 0 | 0 / 3 |
| Lessons (teach and learn met) | 17 | 5 | 0 | 1 | 7 | 2 | 0 | 0 |
| Level rises by practice | 3 | 3 | 6 | 5 | 0 | 1 | 0 | 0 |
| `explain` used (entries) | 9 | 0 | 0 | 1 | 0 | 2 | 4 | 2 |
| `look_up` (replies) | 18 of 4,847 | 2 of 3,478 | 7 of 2,472 | 1 of 1,220 | 6 of 716 | 2 of 594 | 6 of 1,080 | 1 of 1,057 |
| Skill records faded (end vs start) | 93 | 215 | | | | | | |

Counted from the journal's `learn` changes and, for fading, the first and last checkpoints. In the river run the lessons were in
milking (4), boiling salt (3, plus Saer's two "taken after all" by intervention, D4-123), wicker traps (3), nets (2), mining,
smelting, ploughing. Most awareness from speech is noise: of 226 records, 45 are `hunt` (the old row), 35 `hidden: under brush`, 31
`wall`, 29 `forage`, 19 `cheese`.

### The deeper chains

| Chain | river | pw1 | wild_s7 | lake r1, r2 | c2, c3 (80 d) | f1, e2 |
|---|---|---|---|---|---|---|
| Dry meat or fish on the hearth rack | 77 meat (8 people, from day 8), 5 fish (3 people, from day 3) | 472, 17 people, from day 3 | 80, from day 17 | 10, 38 | 4, 0 | 5, 0 |
| Salt (boil salt) | 48 salt, 2 people, from day 4 (after the pan was raised by intervention, day 3) | none in world | none | none | none | none |
| Salting meat | 104, 12 people, from day 14 | | | | | |
| Smokehouse, smoking | 1 attempt (not done: units) | | | 0 (known by all) | | |
| Milling (grind, mill, water mill) | 1 act (wrong verb) | 0 | 0 | 0 | 0 | e2: the water wheel 101 work acts, unfinished at day 32 |
| Bread | 1 refused | 0 | 1 try, 0 made | 0 | 1 try, 0 | 0 |
| Charcoal | 0 | 1, day 56, after a lesson on day 27 | 3 tries, 0 | 0 | 0 | 0 |
| Copper, copper tools | 0 (no rock in any village) | 0 | 13 copper, 11 tools, from day 1, by the seeded smiths | 0 | 0 | 0 |
| A weir | 0 acts (talked of 16 times, all by the Opus 5 Wrights) | | | 0 (known by all) | | |
| Ploughing | 28 acts, the Fields; Drew taught day 21 | 29 | 83 | 5, 17 | 33, 45 | 0 |

### The day's options (pw1 and wild_region_s7; the river run shows none, `view: beliefs`)

| | pw1 | wild_s7 |
|---|---|---|
| Mornings with an options list | 1,637 | 1,026 |
| Lists at the cut of 10 | 1,637 (100%) | 1,026 (100%) |
| Gather, work, make acts named in that morning's list | 66% | 73% |
| Most chosen positions | 8th (998), then 7th and 9th (526 each) | 10th (430), 9th, 8th |
| Listed every morning | fell, firewood, clear, sow | firewood, clear, sow |
| Never listed, though done | milk (83 acts), dry meat (71), snare (136), net (27), care (237) | milk (43), smelt (17), copper tool (16), care (41) |
| Most frequent near miss | "work ditch, but ... is not wet ground" (1,405 mornings), "work terrace, but ... is not hill ground" (1,292) | the same two, 1,021 mornings each |

`knowledge.options` walks TECHNIQUES in table order and stops at 10 (knowledge.py:411), so the first rows of the table (felling,
firewood, clearing, sowing) fill the list and the wild layer's methods, milking and the rack never appear. A quarter to a third of what
agents did (27 to 34%) came from the system text's craft list instead.

### Findings

1. **The river run starved beside the crafts that would have fed it, and the knowledge model was not why.** 25 died (20 of
   hunger), 22 were born; at the end only the Fields held food (W-58). Every craft that could have changed that was known to
   someone: the Fletchers held Middleham Mill, the Brooks were skilled at mining, smelting and copper tools with an anvil at
   Highpool, the Marshs knew quarrying, everyone "knew" the weir and smoke racks. None of it ran:
   - **No rock in any of the three villages** (the checkpoint's parcels: rock only at Stanwood, Hartcliffe, Thornholt and w4, one
     or two days off, all empty). Mining and quarrying need rock and a tool; a crude tool needs half a stone; a hand mill two. The
     Wrights (Opus 5) worked out the chain on day 0 and chased stone for 30 days: Aldric, day 0, "ground to meal and baked to bread
     it is near fifty, out of the same forty ... A hand mill wants two stone and there is no stone in Lowstrand". Matthew walked to
     Highpool for stone, which has none. Nobody went to the rock.
   - **The water mill needs 200 grain in one act.** The most grain any household store held in the run was 178 (Field House); the
     Fletchers, who hold the mill, never had more than 40. Nobody tried it.
   - **The Brooks' pan:** the world gave them the salter's craft and the spring but no pan, raised by intervention on day 3
     (Zach, 17 Nov). Salt then became the one chain that worked (finding 6).
   These are world-design faults of exactly the kind scenario_design.md warns of ("every access gate verified in a dry run"), and
   the generator's prompt advertises the crafts regardless: "Highpool ... its people know ... mining copper ore, quarrying stone".

2. **Recipes are not shown where agents look.** The `make` list names each recipe and its fitting, never its inputs or output;
   agents learn the amounts from refusals ("make salt meat: it needs 1 salt; you have 0 to hand; salt is made by boiling salt from
   brine"; "make fishing rod: it needs 0.1 hide", 9 times in the river run, the rod's hide of 02zzy2). `look_up`, the designed
   place for the full card, is used in 0.1 to 0.8% of replies in every run (18 of 4,847 in the river run, 1.2% of its morning plans; 2 of 3,478 in pw1). The
   strong models compute chains from the food table instead (meal 1.0 against grain 0.7, "bread is thirteen meals to the ten",
   Payn, Opus 5, day 8); the weaker ones do not reach them.

3. **(Older view only.)** Current worlds use `view: beliefs` (review 38.40 §9, Zach 1 Nov; STANDARD in prompt.py since 38.70b), which shows no options list ("No computed choices"); the river run had none. This finding is about pw1 and wild_region_s7, which ran on the earlier view; the list survives in code for worlds without `view: beliefs` and in the bots. **The options list hid the crafts people use and advertised the ones they do not.** Every list in pw1 and wild_region_s7 was at
   the 10-row cut; milking was never listed in 1,637 mornings while agents milked 83 times; "make clappers" was listed 1,011 times.
   The near misses were mostly "work ditch, but Ashford Field is not wet ground" (1,405 of 1,637 mornings). The design's
   "near misses help planning" is right; the list built in table order, with no relevance, is not that design.

4. **"Everyone knows" is too long to be read and too flat to make specialists.** The river run's line lists 73 crafts in 1,971
   characters, weir and smoke racks among them (livelihood_archetypes.md counted 72 on 16 Nov). Every adult in all nine households
   is "By trade: sowing a field broadcast and reaping a crop", the Brooks (salters and smiths at Highpool, which has no fields)
   included. 94 of 132 rows are basic, so the "unknown craft" refusal fires 17 times in 2,695 river acts: the knowledge gate
   that was meant to give specialists their value hardly exists.

5. **The knowledge paths work when people use them, and teaching is the one they use.** 17 lessons in the river run, 13 to
   known and 4 to capable; the learners went on to use what they learned (Drew ploughed after day 21, Matilda boiled salt on day 23). Watching gave 4 rough ideas, `explain` 2, practice 3 level rises. Teaching needs both to name it the same day; Wilmot
   (Opus 5, day 19) asked to learn netting, Aldric did not teach, and the act was refused: "you know of netting birds with nets
   and decoys, but have no idea how it is done". Peter (Fable 5.2) was taught mining (day 11) and smelting (day 16) and never mined
   or smelted: there was no rock.

6. **One specialist chain did work: salt.** Once the pan stood, the Brooks (Fable 5.2) boiled 48 salt, taught it to four of their
   own, and sold it down the river; 11 of the run's 24 trades are salt for grain or meat ("Salt fetches 2 grain or meat each at
   Middleham, so I boil salt today for Peter to carry there", Lambert, day 16), and 12 people salted 104 meat from day 14. This
   is the design working as meant: a craft held by one household, a product others need, a price learned and kept ("Osric Field
   paid 2 grain per salt", Peter's kept line).

7. **The goal and the units crowd the crafts out.** River agents planned 515 units of `try` against 89 reaps and one smoke-racks
   build, which failed for want of a unit (Matthew, Opus 5, day 14: "four units go to Annora before anything, and I push two units
   past my strength to build smoke racks"; result "Not done: build smoke racks: it takes 2 units and you had 1 left"). The weir,
   at 12 timber and 24 units by a crew, was asked for by Aldric on days 6, 8 and 9 and never begun. Investment crafts need spare
   units that a hungry, line-maximising household does not have.

8. **Misreadings carried forward.** Known ones recur: set mistaken for lift (02zzy2; now in the memories or kept lines of 14 river agents, "GATHER
   SETS A LINE, TAKE LIFTS IT", Absolon, day 29); the rod's hide; "By trade: sowing" (02zzy). New ones: two salt crafts with near
   names (`salt pan` on saltmarsh and `boil salt` at a pan): Saer asked to learn "salt pan" three times while Lambert taught boil
   salt, fixed by D4-123; `work` used for `make` and `gather` crafts ("'dry meat' is not a way of working you know", 10 in the
   river run, 17 in e2, where "water mill" and "mill" were named as builds 14 times); "Middleham Water is fished out", written by
   the Fields from day 12 and kept to day 29, passed to the child Hob as "Lessons:", in a river whose fish come in runs.

9. **Skill fading works and mostly erodes seeded skills nobody uses.** pw1's 215 faded records are hearth, wall, medium room and
   quarry (19 to 20 people each), crafts seeded as known and never practised in 100 days; the river run's 93 are select seed, net,
   hoe, wicker traps. Practice raised 37 river skills by more than 0.05, the largest Wilmot's den work, 0.5 to 0.89.

10. **Model strength shows in exploration, not in deeper chains.** In the river run the Opus 5 Wrights used 38 different crafts and
    the Opus 5.5 Fields 32, against 12 to 26 for the others; their craft refusals were higher (14 to 17 per 100 acts) because they
    tried more. Haiku 4.5's were highest (26.8). Fable 5.2's Brooks taught most (20 teach or learn acts). No model got past the
    world's gates.

## Part 4: verdict and design choices

### Graded against the intent

| Goal | Grade | Why |
|---|---|---|
| General (one mechanism) | **partly** | one shape for every row; one handler for `make`; but 25 single-use yield kinds and five side tables for building |
| Extensible (a craft is a row) | **holds for recipes and wild methods, fails for processes** | the smokehouse and the weir cost 400 to 1,100 lines of code each |
| Levels that rise and fade | **holds** | every path built, used and taking; fading as D4-105 |
| Specialists and dependence | **fails** | 71% of crafts basic; one trade line for everyone; archetypes not built (W-70) |
| Legible: crafts known by depth | **partly** | levels shown by name and source; the depth ladder (D2-251, agent_view point 3) not built; inputs never shown for `make` |
| Legible: what can be done here | **fails as built** | the options list in table order at a cut of 10; dropped in `view: beliefs` worlds, where "here one can ..." stands in |
| Legible: near misses | **fails as built** | dominated by the impossible (ditch, terrace) |
| Legible: refusals | **holds** | name the shortfall; agents learn amounts from them and keep the rule |
| Look-up of the card | **unused** | 0.1 to 0.8% of replies |
| Deep chains reachable | **fails** | world gates unchecked; minimum batches; units |

**Faults by kind.**
- **Engine:** the hub of single-use yield kinds; all-or-nothing minimums for mills and ovens; twin rows by pack; modifiers in the
  craft table; awareness by string match on common words; the options list's order and cut.
- **Legibility:** no inputs on `make`; the 73-craft basics line; one trade line for all; near names (salt pan, boil salt); verbs
  for crafts (`work` against `make` against `gather`); set and lift; the card only by look-up.
- **World design:** no rock in three villages whose crafts need it; a spring without a pan; a mill nobody can fill; a goal that
  rewards spending units on `try` over investment; a fishing village whose people are told they are sowers.

### Design choices that follow, ranked by expected effect on behaviour

1. **A gate check in the generator, run on every world.** For each craft a household is told it knows (or that its village knows),
   confirm the cover, the fitting, the inputs at a reachable scale and a tool exist within a day; flag "knows mining, no rock
   within a day", "a mill that needs more grain than any household holds", "a spring and no pan". This is livelihood_archetypes.md
   item 5 extended from resources to whole chains, and the cheapest change here with the largest effect: the river run's missing
   chains were all gate faults.
2. **Recipes where agents look.** Put each known recipe's inputs, output and units on its line in the verb list and the craft list
   (the `build` lines already do it), with the D2-251 ladder for depth: aware, a sentence of what it is for; rough, the main input
   and where; capable or known, the numbers. Then the card and `look_up` become redundant and can go.
3. **Minimums as "up to".** Mills, ovens, salt and smoke batches take what one has up to the batch (the `batch` flag that the
   racks already use), with the scale saving kept by units, not by a floor.
4. **Options by relevance, or none.** Either keep D4-78's way (no options; the place lines' "here one can ...") everywhere, or order
   the list by what one did recently, what is in season and what one's household lives by, drop near misses that cannot become
   possible (a field that is not wet), and show near misses one step back only (the input one lacks and where it comes from).
5. **Livelihood archetypes seeding a household's knowledge (W-70).** Shrink the basics to the ~35 universal acts; seed core,
   common and specialist crafts by archetype; derive the trade line from the archetype ("By trade: salter", "fisher"); tie the
   archetype to the land through the gate check. This brings back the specialist the design was for, and shortens the system text.
6. **The thing as the target of an act (Q-80, acts_on_owned_things.md).** Lifting traps and snares, taking from piles, slaughtering
   and milking name the thing (tag) and default to one's own. In the river run, takes, gives and moves of things not there or not
   in hand are 305 of 979 refusals, more than any craft class, and set-versus-lift is the most kept rule.
7. **Aware redefined, and learning by watching and handling.** Aware: knows what it is for and may try it by guessing (the
   `untaught: tryable` rule for all); rough: knows the main input; watching a craft done beside one, or handling its product, moves
   one up. And awareness by mention restricted to a craft's own name, not its common words (no more "wall", "hunt", "under brush").
8. **Uses of goods as knowledge.** A good one holds knows its uses at the depth one knows them ("salt: keeps meat and fish; the
   Brooks boil it"), so a product carries its craft into another household. The salt trade did this by talk; the engine could hold
   it.
9. **Crafts as data versus code, for the feature-packages cut (D2-244).** Accept P3's form: a recipe is a row; a process (a set, a
   rack, a tended fire, a weir's gap) is a yield kind written as package code with its data, signs and prompt lines beside it.
   Retire the twin rows (forage, hunt) to replay-only, move modifiers out of TECHNIQUES, and give every row a `does` sentence.
   This changes little in behaviour on its own but halves the cost of the next chain.

## Part 5: memory against the rules, and verb and prompt use

### What agents carry against what they are given

| | Words |
|---|---|
| System text (Osric, river run, day 10) | 5,744: people 383, rules 961, places 376, crafts 581, verbs 2,890, reply format 425 |
| The morning message | about 1,400 |
| Their own memory, a stretch | budget 330 to about 600 words by age for a rewrite (Haiku: 150, appended); kept lines up to 80 words (river, pw1) or 25 (wild, lake) |

| Run | Model | Memory rewrites | Words, mean | Share of budget used |
|---|---|---|---|---|
| river | Fable 5.2 | 46 | 498 | 0.99 |
| | Opus 5, Opus 5.5 | 48, 46 | 458, 460 | 0.92, 0.89 |
| | Sonnet 5 | 51 | 465 | 0.95 |
| | Sonnet 4.5, Sonnet 5.5, Opus 4.5 | 52, 45, 40 | 342, 288, 323 | 0.67, 0.58, 0.61 |
| | Haiku 4.5, Haiku 5.5 (append, 150) | 41, 39 | 114, 134 | 0.76, 0.89 |
| pw1 | Opus 5.5, Sonnet 5.5 | 280, 257 | 528, 375 | 0.95, 0.65 |
| wild_s7 | Opus 5.5, Sonnet 5.5, Haiku 5.5 | 91, 44, 185 | 492, 284, 139 | 0.83, 0.47, 0.93 |

Kept lines: river 481 written (36 words mean, 116 dropped), pw1 287 (29), wild_s7 319 (19, cap 25), lake_r2 106 (19).

**What they write** (sentences classified by keyword, approximate): rules, recipes and prices are 16% of memory words in the river
run, 10% in pw1, 11% in wild_s7, 6% in lake_r2; the state of things (stores, holdings, beasts, places) 58 to 78%; people and events
11 to 21%; plans 3 to 5%. Kept lines lean to rules: 155 of 481 in the river run and 125 of 287 in pw1. The rules they keep are
mostly what refusals taught them: "To lift snares use take {item: meat, from: the place}; 'gather snare' only sets a new line.
Learning needs teacher 'teach' and learner 'learn' the same day" (Peter, Fable 5.2, day 6); "After a birth, 'try' is refused for
about two days" (Mabel); "A WORK IS REFUSED OUTRIGHT IF YOU ARE A TENTH SHORT OR A UNIT SHORT" (Lucy, Opus 5, day 26); and measured
yields, "fishing by hand 3 units for 1.3 fish; wild food in South Wood 0.3 meals for FOUR units; bird nets four units for nothing"
(Aldric, day 8).

**Lost or wrong.** A salt price written by 41 agents was dropped and not rewritten 19 times; "teach and learn the same day" 5 times
of 17. The longest-lived wrong belief is "Middleham Water is fished out": the Fields wrote it on day 12 and carried it in every
memory to day 29.

**What passes to children.** In the river run 134 of 487 care acts carried a `pass` line; 21 were about how the world works (Lucy,
day 25, to Thomasin: "fresh meat rots in the hand and dried meat is four times the food and keeps for months - dry or salt every
scrap the same day"), the rest about the line, kin and partnering. pw1: 11 of 237, all identity ("We are the Ashford folk ...");
wild_s7: 3 of 41. Teaching reached youths (Drew, Olive, Stephen, Dionisia, Absolon: milking, nets, wicker traps, boiling salt); the care
lines themselves carried almost no craft.

### Verbs and arguments used

| Run | Verbs used (of 38) | Never used | Top five, of all acts |
|---|---|---|---|
| river | 29 | release, revoke, leave_household, found, attack, fire, part, write, erase | gather 1,279, work 1,272, take 411, move 317, try 248 (80%) |
| pw1 | 21 | accept, host, revoke, join, admit, leave_household, found, set, watch, attack, partner, part, order, meet, come, write, erase | gather 3,441, work 1,298, give 405, move 297, travel 201 (89%) |
| wild_s7 | 18 | 20, among them teach, learn, guard, partner, write | work 1,594, gather 1,210, move 349, make 99, give 98 (95%) |
| lake_r2 | 16 | 22 | work 293, gather 192, move 43, take 30, give 27 (88%) |

Arguments past `what` and `at` are rare: `for` (on 20 to 50% of gather and work acts), `looking for` (64 river, 140 pw1), `range`
(37, 167), hunting `with` (15); build's `structure`, `describe`, `how` a handful; `hidden` once. Reply fields: `fallback` 96 to 99%,
`attend` 86 to 94%, `tell` 50 to 83%, `note` 3 to 38%, `offers` 2 to 9%, `look_up` 0 to 1%, `explain` under 1%.

**Rules broken or not known** (non-craft refusals, river run 609): taking from a place where nothing lies 140; giving or moving
more than in hand 96; notes full at 8, 87; pinning a note that does not exist 37; a door barred or set by one who does not manage
it 23; telling someone not here 22; offer syntax 22; trying too soon after a birth 18 (not in the rules: learnt only by refusal,
then kept); private-message limit 15; trying before both are grown 10.

**Learnt only from refusals:** the least batch for salting (02zzy: "it needs 4 fish; you have 2"), the rack's one batch ("the rack
at its fire in Field House is full", 12 in the river run), salt as an input of salting, the rod's hide, the gap after a birth, set
against lift, teach needing a matched learn, a unit short meaning nothing done.

*Current as of 22 Nov 2026.*
