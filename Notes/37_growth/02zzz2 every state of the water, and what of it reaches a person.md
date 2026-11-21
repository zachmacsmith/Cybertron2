---
id: docs/review/37_growth/02zzz2_river_signs_audit.md
kind: note
updated: "2026-11-21"
---
# 02zzz2: every state of the water, and what of it reaches a person

*note · `docs/review/37_growth/02zzz2_river_signs_audit.md`*


21 Nov 2026, 37.2 (subagent). Thread: signs of the river ([[W-72 Signs of the river|W-72]]), under the nutrition worlds ([[W-69 Nutrition worlds|W-69]]). The proposal that follows from
it: [proposals/river_signs.md](../../cybertron2/proposals/river_signs.md).

Zach (21 Nov): "Fishing is currently terribly low right now. I think (a) we need to add a richer tapestry to potential signs. If
they are in the rivers or near and in [the fen] etc their interactions should realistically reflect the numbers and state on an
independent axis from their actions ... definitely shouldn't say the river is empty if it is not. I do also think fishing people
should be seeded with the longer term memories that the runs come and should be prepared for with weirs etc. How much info are
farmers already seeded with, and so fishing seems fair too? Actually check and compare. ... Dig into all the different types of
state of the river and how much is currently reflected in signs."

**Read with:** [02zzy](02zzy_why_they_did_not_fish.md) (why the runs world's villagers did not fish) and
[02zzy2](02zzy2_fishing_methods_compared.md) (the methods compared: hand fishing's engine gap, the lift that sets new traps, nets
that meet salmon and take none, the weir nobody builds). This note does not repeat their findings; it goes state by state.

**Sources:** the code on main as of 21 Nov (file:line below); the three live runs of the runs world (scratchpad
`live/runs_{low,medium,high}/`: `turns.jsonl` fields `prompt` and `results`, `days.jsonl`, `perception.jsonl`); a system prompt
and opening built from `specs/water/river.yaml` (a farming and fishing world) and `specs/nutrition/runs_high.yaml` with
`prompt.system_prompt` and `prompt.turn_prompt` (scratchpad `riversigns/`). "Agent-days" below counts (agent, day) pairs whose
morning prompt carried the line.

## The short answer

- The engine holds a rich river: a flow class every night, the runs as pulses moving down and up the river by the day, each
  year's tally, resident stocks, otters, a heronry, ice by nights of frost, weirs in sections, traps with their catch by kind and
  night, the wreck, the otter's take, the dam's held fish.
- Very little of it reaches a person, and what does reaches them late and in one place. A run is shown as two sight lines at the
  river parcel only, read in the evening and seen the next morning; one of the two needs one to be at the water in the dark, and
  the other needs the trap craft at the level "known". The river's flow is shown only through the day's local weather word
  (twice to four times a run against 17 spate or flood nights). Nothing at all is shown of a run coming, a run slackening, otters
  about, the river falling, fish going past a full trap or weir, or how much a loss cost.
- Several texts mislead. The worst is the hand-fishing refusal "there is no fish at the Isel" (02zzy, 02zzy2). Others: "nothing
  caught in your traps" with no word of the water; a trap whose eight nights ran out described as "fouled and broken"; a weir
  holding a hundred eels counted as "a dozen or more"; "the river frozen from bank to bank" while the traps and the weir fish on;
  "the water is quiet: few fish rising" on a run night where the resident stock is low.
- **Farmers are seeded with far more than fishers.** A farmer gets a trade line that names his work, a family-lore line of the
  sowing times read from the engine's own growth (kept for good), the field's crop in the layout every day, about 40 crop signs
  over its life including a judged ripening date, and phenology markers that time the sowing. A fisher gets the craft's name and
  level, a one-clause note, and "you know something of the eel"; no word of when the runs come, how big they are, or what a trap
  or a weir takes. In the runs world every adult is told "By trade: sowing a field broadcast and reaping a crop". And the farmers'
  lore line is itself cut off at 25 words, mid-sentence (§3).

## 1. Every state of the water, and what reaches a person

### 1a. The table

"Reaches a person now" names each sign or text, where and when it is seen, who reads it and by which sense. "At the water" means
the river parcel (the Isel), which in the runs world is three steps from the Street (the Street, Eelmouth Field, Eelmouth Fen, the
Isel). Signs are read by the one noticing rule ([[D4-75 Every perceived line about the world comes from the one noticing rule|D4-75]]) in the evening (`perceive.evening`) and shown the next morning, unless
marked as a dawn event or a result.

| State | Where it lives | How fast it changes | What reaches a person now |
|---|---|---|---|
| **The river's flow class** (low, normal, high, spate, flood) | Not stored as a value. Worked out each night by `runs.flow` (wild/runs.py:282) from the catchment's rain (today's and half of yesterday's over the mean, summed over every node upstream), with the last four days of rain by node kept in `wild.state.runs.rain` (runs.py:325). Bounds in `WATER_WORKS.weir.wear.flow_at` (data.py:383). It drives weir wear (wild.py:2991) and trap wrecks (wild.py:3152 to 3168) | Daily; the catchment's rain, not the village's | Only through the day's local weather word: "{water} is up and running brown" (signs.py:576, on "heavy rain", `p` 0.3, open to all at the node) and "{water} is still high from yesterday's rain" (signs.py:578, `p` 0.2). In the runs world 17 of 54 nights were spate or flood (OPEN [[Q-77 Whether to tune how often the river reads spate or flood now|Q-77]]); these two lines showed 3, 4 and 2 times in the three arms. A spate on "a clear day" (high, day 36) shows nothing. The wreck lines (below) are the only other trace. The bots read the flow directly (`bots_livelihood.river_tonight`; its docstring: "Where its read is wider than the engine's signs, it says so") |
| **Ice and thaw** | `wild.frozen_run` (wild.py:1207): nights in a row with a low under −3 and a day under 3; small waters freeze after 1, a big river after 3, a lake after 5 (`kinds.OPEN_WATER`, kinds.py:399); a great freeze at 4 (`REGIMES`, kinds.py:534) | Daily | Wildfowl only: "duck and geese packed thick on the open water at {place}, the marsh about it frozen hard" and "the water at {place} frozen over, and the fowl gone from it" (kinds.py:357 to 361, at the water, the day it begins); "the river frozen from bank to bank; birds lying dead on the ice" (kinds.py:535, the great freeze); "duck and geese back on the water at {place} with the thaw" (signs.py:2379 `_wild_thaw`); "ice piled against {weir}, the stakes leaning" (signs.py:533). Ice does not stop a trap, the weir or a run in the engine; the killing-frost sky line deliberately names no ice for that reason (signs.py, the comment after the −6 row). No sign says what ice does to fishing |
| **Season and temperature** | The calendar; the weather values | Daily | The calendar line ("Autumn, day 3 of the season (5 left)") and the sky rows. Nothing ties a season to the runs |
| **The runs: a run passing the village tonight** | `wild.state.runs.pulses`: {kind, stretch, day, heads, direction, held} (runs.py:228, 316 to 432). Pulses for a day are written the night before, so at dawn the run that will pass the village that day and night is already in state (the bots' `run_here` reads it at dawn) | Daily; a pulse moves about 10 km a day (`RUN.km_a_day`), so a run passes a low station over many nights (Eelmouth: eels from about day 6 to 17) | `RUN_SIGNS` (kinds.py:888), emitted by `signs._wild_river` (signs.py:2417 to 2446) at the village's first river parcel, sight, when 3 heads or more pass: "the water at {place} alive with {kind} in the dark, all going downstream" (all; `cond: night`, so only for one at the water in the dark); "the {kind} are running at {place} tonight: the traps and the weirs on the river will fill" (`knows`: trap in water); "{kind} going up through {place}, leaping at the shallows" (all); "the {kind} are running up the river at {place}: a run night" (knows). Live: the eel run's `all` line reached 1, 0 and 1 agent-days in the three arms; the `knows` line 15, 38 and 78 (first on days 10, 7, 7); the salmon's `all` line 11, 5 and 27. **The `knows` key needs the trap craft at the level "known"** (`perceive.practised`, perceive.py:289): in low the adults had only a rough idea, so the eel run was readable to them only in the dark at the water, and the 15 low agent-days are mostly the two youths who knew the craft and Peter after many sets |
| **The runs: the run coming, the window opening** | `RUNS` windows (kinds.py:872: eels autumn days 0 to 7, salmon autumn and winter days 0 to 3, lampreys spring), the year's quota and dues still to run (`runs.quota`, `runs.due`), pulses upstream; with `runs_set_nights` ([[D2-231 The runs world's runs on set nights|D2-231]]) the set nights of each window (`runs._calendar_cue`) | Seasonal | `WEATHER_LEADS` eel row (kinds.py:410): "the first heavy rain after the dry weeks: the river rising and dark" (all) and "an eel night: dark, wet and the water rising after the dry weeks; set the traps tonight" (expert). It reads `rain_after_dry` even where the runs come on set nights, and it is placed at the village's first wood or scrub parcel, not at the water. Live: 2 agent-days, in high. Nothing else: no sign or memory that a run is due |
| **The runs: slackening and the year's run** | Pulses by night; `runs.tally` by kind, stretch and year (two years kept) | Daily; yearly | "the {kind} run was thin this year at {place}: about {share} of last year's" and "a good {kind} run this year" (kinds.py:895 to 896, knows, the day after the window). Live: once or twice, on days 51 to 63. No sign of a run thinning night by night |
| **Fish held below a shut dam** | A pulse with `held` (runs.py:424) | Nightly in an up-run | "{kind} leaping at the dam by {place} and falling back" (all, own 1.2) and "crowding in the pool below the dam: net them, or draw the hatches" (knows) (kinds.py:897). Not in the runs world (no mill) |
| **Resident fish** | A parcel's `res.fish` {S, K}, one record a water body (engine/waters.py, [[D2-229 One fish stock per water body|D2-229]]); `resident_fish: false` stocks none (wild/switches.py:78). None in the runs world | Daily, slow | `WILD` rows (signs.py:686 to 691): "the water at {nm} is quiet: few fish rising" (S under 0.35 K, eye), "the fish at {nm} have been fished hard" (knack angle), "fish rising all along {nm}" (over 0.75 K, `p` 0.06, the only row for plenty). The refusals "there is no fish at {nm}" (knowledge.py:207) and "the fish at {nm} are fished out for now" (knowledge.py:223) |
| **Otters** | `wild.state.pop.otter` by area (kinds.py:66); the rob in `wild._robbers` (wild.py:3185): a chance 1 − e^(−0.1 × otters about) a night for each unwatched trap holding fish, 30% of its heads, at most 4 (`ROB_SETS`, kinds.py:883); `robbed_by` on the trap | Nightly | Only after a robbery: "an otter's spraint on the stones by {place}, and fish scales" (all), "an otter has been at the traps at {place} in the night: it will be back while there are fish in them" (knows) (kinds.py:901 to 903, that day and the next); the setter's look "your wicker traps at {where} torn at the neck, scales and a fish head on the withies: something has had what was in them" (things.py:365), only when nothing is left in the trap. No sign of otters about before they rob; no word of how many fish went |
| **Herons** | A heronry site (kinds.py:476: at a wood beside water; eats from the water's resident fish) | Seasonal | At the heronry's parcel only: "the herons are back at the tall trees in {place}", "the heronry in {place} stands empty this spring", "grey herons standing in the shallows, a heronry near: a lord's feast in spring" (kinds.py:491 to 495). No heron at a run |
| **Eels in the land** | `pop.eel` by area (resident in the pools and dykes where resident fish are on; the source of the silver-eel run either way) | Slow | An expert hunter's notice: "eels in the mud of the pools and the dykes, about {n}: they run on the dark wet nights of autumn" (kinds.py:592) |
| **Wildfowl on the water** | `pop.wildfowl`; pushed by frost (`OPEN_WATER`) | Daily | The open-water rows above; a hunter's notice "duck and geese on the open water" (kinds.py:590) |
| **The weir** | A building with `monument: weir`, `sections` [{m, foot, level}], `gap`, `crew` (wild.py:2931 to 2952); its traps a set thing with `weir` (wild.py:3038); its hold in kg (`GR.hold`: 100 kg the first section, 70 each added); its take a share of each run passing (30% the first section; `WATER_WORKS`, data.py:376); wear in `broke` | Nightly | The layout every day: "the weir: a fish weir (stakes and wattle across the river, wicker traps in its gap); its gap shut; 3 sections (timber sound, timber sound, timber sound); worked by Nichola, Peter". Wear: "stakes torn out of {weir}, a stretch of wattle gone: the river runs through the hole" (signs.py:531; 122 agent-days in high, mostly carried in the layout's "you saw N days ago"); the gap set (kinds.py:897). Full: "the traps at {pname} crammed full: whatever comes down now goes past" (signs.py:2501), **only to the crew, only at the parcel**, never seen live. The look counts heads by words up to twelve, then "a dozen or more" (things.py:348, `catch_words`): a weir holding 180 eels and 12 salmon reads "a dozen or more eels and a dozen or more salmon". The lift: "You took 55 fish from your weir's traps at the Isel" (kg of fish; no kinds, no meals) |
| **A set trap in water** | A set thing: `set` {method, life 8 nights, set_day, line 1, holds 20 heads, sprung, wrecked}, `goods` (fish in kg), `catch` [{kind, day, n}], `robbed_by`, `robbed` (methods.py:87; wild.py:909, 921) | Nightly | The set result: "You set traps in the water at {place}; they will catch by night for about 8 nights, for whoever comes to them" (wild.py:918). The setter's look (things.py:353 to 376): "four eels in your wicker traps at the Isel"; "nothing caught in your wicker traps at the Isel" (21, 31 and 51 agent-days); spent: "... are fouled and broken, with nothing in them: they will catch no more". A stranger's: "wicker traps set in the water at the Isel, with something in them", "..., fouled and broken" (signs.py:1310 to 1315). The lift (verbs.py:1608 `_lift`, or a take): "You took 2.3 fish from your wicker traps at the Isel" |
| **A trap wrecked** | `set.wrecked` = the flow class; the catch destroyed with "swept away in the spate" (wild.py:3165); a spate 0.5, a flood 0.85 (data.py:386; [[D2-218 Set traps in high water|D2-218]]) | Nightly | The setter: "your wicker traps at {pname} smashed against the bank in the spate" (signs.py:2508) and the look "... smashed against the bank in the spate: they will catch no more" (things.py:371); others: "broken wicker in the reeds below {pname}" (signs.py:2511). Said "spate" for a flood too. No word of what was in it, or that the traps in other parcels or the fen stood |
| **The race and the mill** | A water wheel's gap; a trap in its race takes half of an eel run down (`WATER_WORKS.mill.race`); a shut dam holds half of a run up (`stop`) | Nightly | The gap set, held fish (above). Not in the runs world |
| **The fen** | Cover `fen` (reed and sedge over standing water, low by the water); part of the area's small waters (freezes after one hard night); traps may be set there (`trap in water` at water or fen, methods.py:72). **A trap in the fen meets the run passing the village at the same density as one in the river** (`_set_night` draws by the area, wild.py:965) **and is never wrecked** (the wreck loop takes river parcels only, wild.py:3160) | Daily | The ambient "reeds hissing in the wind on {name}" (data.py:174), the brine spring's line, the fowl rows. Nothing of the water in the fen, eels in its dykes, or its standing safe in a spate |
| **Floodplain and flooded parcels** | Not in state: floods over the land are environment systems phase 1, unbuilt ([[W-49 Environment systems|W-49]]). A beaver dam floods a meadow (sites) | — | The dam's "the low meadow at {place} under water again behind a dam of sticks" (kinds.py:503). Nothing else can be said of a flood over the land |
| **Brine springs and salt pans** | `res.brine` on the parcel; a brine pan fitting (wear after 60 uses); salt pans by season (data.py:607) | Standing; the pan by use | "a spring welling up at {nm}, a white rim of salt dried on the stones round it" (signs.py:737, own 0.15): a standing fact read as a sign, shown again and again (19 agent-days "(yesterday)" in the runs world), and already in the place's own text |
| **The water's own text** | Parcel `text` by river class (landgen/write.py:166): "a broad slow river", "the river, running between banks", "a brook, quick and shallow" | Never | The layout: "the Isel (water): a broad slow river. Next to Eelmouth Fen." Unlike every other parcel, no "here one can ..." (prompt.py `_place_lines` lists only techniques whose `draws` the parcel holds). The ambient "water running over stones in {name}" (data.py:167) for every river, broad and slow or in flood |

### 1b. Where, when and to whom: what the rule gives

From `NOTICING` (data.py:1010) and `things.presence` (things.py:457), for an ordinary eye in clear daylight:

- **A sight sign at the water** is read at its own × 0.5 by one who worked there, × 0.3 crossing it or next door (own 0.5 or more),
  and × 0.05 from anywhere else at the node (own 0.8 or more). From the Street, the run's `knows` line (own 0.8) comes to 0.04 a
  person: in practice only those who went to the water saw a run.
- **Sound and smell carry by steps** (`carry`: sound 0.5, 0.45, 0.2, 0.1, 0.05; smell 0.5, 0.3, 0.12, 0.05, 0). The river has no
  sound or smell sign of a run, a spate or anything else, so nothing carries to the houses.
- **When.** Signs are rolled in the evening and shown next morning, so a run first seen at the water on a run night is acted on
  the day after. Only dawn events (`perceive.dawn`, perceive.py:350) reach a person in the morning they happen; the river writes
  none.
- **How many.** At most 5 lines are noticed an evening (`NOTICE_MAX`, perceive.py:20), so a run line competes with the day's
  other news.

## 2. What misleads

| Text | Where | Fires when | Why it misleads |
|---|---|---|---|
| "there is no fish at the Isel" | knowledge.py:207 (`ready`: the technique's `draws` resource missing from the parcel) | Any hand fishing or angling where the parcel holds no resident `fish`: every time in the runs world, run nights included; the run take (wild.py:3242) is never reached (verbs.py:587 refuses before 611). 40 such result lines across the three arms | Reads as a fact about the river while eels and salmon pass it (02zzy §2a: "the Isel is fished out"; 02zzy2 §1) |
| "the fish at {nm} are fished out for now" | knowledge.py:223 | Hand fishing or angling where the resident stock is at its refuge, a run night included (the run take again never reached) | The same, in worlds with resident fish |
| "the water at {nm} is quiet: few fish rising" | signs.py:686 | The resident stock under 0.35 K, whether or not a run passes | Says the water is quiet on a night it is full of running eels |
| "nothing caught in your wicker traps at {where}" | things.py:375 | Any look at a trap holding nothing | No word of whether any run passed; a trap set between runs and one set in a run that took nothing read the same. 21, 31 and 51 agent-days |
| "... are fouled and broken, with nothing in them: they will catch no more"; "wicker traps set in the water at {at}, fouled and broken" | things.py:373; signs.py:1315 | A trap whose eight nights are done (`sprung` by its life, wild.py:942) | Reads as damage. Nothing broke: its nights ran out. Shown about 23, 36 and 40 times in the perception log |
| "your wicker traps at {pname} smashed against the bank in the spate" | signs.py:2508; things.py:371 | A spate or a flood | Says spate for a flood; says nothing of what was lost with it or that the next night may be fit to set again. The agents read it as "don't bother" (02zzy §2c) |
| "... torn at the neck, scales and a fish head on the withies: something has had what was in them" | things.py:365 | An otter robbed it and nothing is left | Hides the amount; when the otter took some and left some, the look shows only what is left, so the loss is not seen at all |
| "a dozen or more eels" | things.py:348 (`NUM` stops at twelve) | Any catch of 13 or more of a kind | A weir's night of a hundred or more reads as a dozen: the scale of the weir, the one method that works, is hidden at the look |
| "You took 0.5 fish from your wicker traps" | verbs.py `_take` | Every lift | The look counts eels; the result weighs fish in kg, no meals. "Half an eel" (02zzy §4) |
| "the river frozen from bank to bank; birds lying dead on the ice" | kinds.py:535 | A great freeze (4 hard nights) | The traps, the weir and the runs carry on as if open; the sign says the river is shut |
| "the water at {place} frozen over, and the fowl gone from it" | kinds.py:360 | All the area's waters frozen | The same, at the village's water |
| "an eel night: dark, wet and the water rising after the dry weeks; set the traps tonight" | kinds.py:410 to 413 | `rain_after_dry` in autumn | Under `runs_set_nights` ([[D2-231 The runs world's runs on set nights|D2-231]]) the eels do not run on that cue: it can call a night an eel night with no run, and never calls the set nights. Placed at a wood, not the water |
| "the salmons break and run long before you are near: hunted too often here" | signs.py:2375 | Wariness from hunts and nets at the Isel, from day 0 | "Salmons" (`_kinds_word`); salmon cannot be hunted there, and Hamon (Opus, high) read it as "hunted thin" (02zzy §5) |
| "you know the eel ... of these parts well: their ways, their signs, where they lie" | methods.py:250 (`familiar_line`) | Familiarity 0.6 or more | Claims a knowledge the prompt never gives: no ways, no times. In the runs world the line reads "you know something of the ... eel, ... otter" |
| "By trade: sowing a field broadcast and reaping a crop" | generate.py:378 (the line's first two crafts, basic or not); prompt.py:497 | Every adult in the runs world | A world with no fields and no seed (02zzy §2b) |
| "water running over stones in {name}" | data.py:167 | Any water parcel, any flow | A broad slow river, in flood or low, sounds the same; a standing ambient, not a change |
| "You hunted the Isel and came on nothing" (nets) | 02zzy2 §3 | Netting at the water | Covered there |

**Results that hide what happened** (beyond those above):
- **The share of a run taken.** No result or sign says what passed the village, what one's gear took of it, or what went past a
  full trap or weir. The weir's room is checked every night (`gear_at` room, wild.py:3100) but what it turned away is not kept.
- **What a spate took.** The catch destroyed is in the journal ("swept away in the spate"), never in a line to the setter.
- **What an otter took.** `robbed_by.n` holds it (wild.py:3226); no line says it.
- **That a set trap takes a few eels, and how many more traps would take.** No line ever compares one's catch with what the water
  held, so nobody reasoned about how many traps to set (02zzy §2d).

## 3. Seeded knowledge: farmers against fishers

Built from `specs/water/river.yaml` (Adam, head of the Hobbs at Millham, a farmer who also knows the trap as a novice) and
`specs/nutrition/runs_high.yaml` (Hamon, head of the Shepherds at Eelmouth, a master weir builder and skilled trapper).

| | A farmer (Adam, river world) | A fisher (Hamon, runs world, high arm) |
|---|---|---|
| **Trade line** (generate.py:378, prompt.py:497) | "By trade: sowing a field broadcast and reaping a crop." True | "By trade: sowing a field broadcast and reaping a crop." False: no field, no seed |
| **Crafts** (knowledge.py:389) | "Long practice has made you better than most at: breaking the soil with a hoe (skilled); reaping a crop (skilled); sowing a field broadcast (skilled); weeding a growing crop (skilled)." Ploughing, seed selection, milking "known (skilled)" | "Long practice ...: salting fish to keep (master); hanging fish to smoke (master); tending a smokehouse fire (master); building a fish weir (master)." "You know: ... netting birds (skilled); ... setting wicker traps in the water overnight (skilled)" |
| **What the craft does** (prompt.py `_craft_note`) | Sowing, reaping and the rest are basic, by label; the field's work list is on every field in the layout ("here one can ... reap, sow, ...") | The trap: one clause in the gather line ("set wicker traps in the water at dusk; they fish by night for some nights, best when things run: come back to your traps and take what is in them, or it rots there or another finds it", methods.py:106). The weir: "weir (12 timber, 24 units of work, a monument: no room, 3 lines)" under build; nothing says what it takes. Hand fishing and angling: no description. The water lists nothing one can do there |
| **Lore, kept for good** (lore.py; data.py:154 `LORE = {"sowing": {"to": "farmers"}}`; given to field holders only, lore.py:72) | "Barley does best sown in spring, and well early in summer or late in winter; rye does best sown late in autumn, and well in" — the line as shown: **cut at 25 words** by `memory.seed_line` (memory.py:135, 158). The full text (lore.text) goes on: "... summer or early in autumn; beans do best sown early in summer, and well in spring; rye wants a winter; sown at other times, crops come up poor or not at all." Every farming world's farmers have lost the beans and the winter rule | None. No line about the runs, their seasons, their size, the weir's take or keeping |
| **What you remember** (generate.py:290 to 331) | Founders; "Hard winters you remember, when the frost came early and the stores ran out: last winter."; kin; a feud over a field; a debt of grain | The same generic lines; the debts are in grain and timber |
| **The year's own state, shown daily** | The field's crop in the layout ("much fields (barley)"; "barley on 4 (Reeds 3, Webbs 1)") | The river's one fixed line: "the Isel (water): a broad slow river" |
| **Signs that time the work** | `CROP` (signs.py:32 to 117), about 40 rows over a crop's life: "just through, a green haze on the soil", "in flower", "the ears filling", "you judge the barley in X will be fit to reap in about 5 days" (a timing, by the reaper's knack), "the ears rub out hard in the hand: the barley is ready", "cannot stand much longer: it must be cut tomorrow or lost". The phenology markers (kinds.py:730): "the blackthorn's in flower: time to sow the {crop}", "the cuckoo's calling: time to sow the {crop}", "the first frost: get in what is left in the fields". Sky leads for the sower ("rain tomorrow, likely") | `RUN_SIGNS`: about 14 rows over the whole river, only on the night itself, at the water, two needing the craft at "known" (§1a). One weather lead for the eel night (misplaced, §2). No marker for a run |
| **Familiarity with kinds** (methods.py:250) | — | "you know something of the brown hare, eel, fox, otter, red deer, roe deer, stoat, wild boar and woodpigeon": a list, with nothing behind it |

**Plainly:** a farmer is told what he is, when to sow each crop (by the engine's own growth), sees his crop every day and is told
when it will be ready. A fisher is told he is a farmer, is never told when the fish come or how many, sees a river that never
changes in the layout, and learns of a run only if he happens to be at the water that day and knows the craft well. Farmers' lore
itself is broken (cut at 25 words), so the comparison is with what farmers were meant to get, and the fix to the cap helps both.

## 4. Gaps by state

| State | No sign at all | One thin sign | Seen too late or too locally |
|---|---|---|---|
| The flow | Rising, bank-full, spate, flood, falling and clearing on any day not "heavy rain"; the catchment's rain from upriver | "up and running brown" on local heavy rain, `p` 0.3 | Read in the evening; the wreck lines the morning after the traps are gone |
| Ice | What ice does to fishing (nothing, in the engine); ice along the edges | The fowl's frozen-over line, the great freeze | At the water only |
| The run coming | The window opening, the run due, the first eels at the village, a set night ([[D2-231 The runs world's runs on set nights|D2-231]]) | The misplaced eel-night lead | — |
| The run passing | Sound, smell, birds and otters at a run; the run in the fen; the run by day for those without the craft; the run's density (a trickle or a glut) | The two sight lines | At the water only, evening only, the `knows` line only at "known", the `all` eel line only in the dark |
| The run slackening, ending | Night by night | The year's thin or good line, the day after the window, for the practised | Too late to act on |
| Resident fish | — | "fish rising all along" (`p` 0.06) | — |
| Otters | Otters about before they rob; how much they took | Spraint and scales after | At the parcel, that day and the next |
| Herons and other fish-eaters | Herons at a run | The heronry's season lines | At the heronry only |
| The weir | What it turned away; what it took of the run (a share); its catch's size at the look | "crammed full" to the crew | At the parcel, crew only |
| Set traps | That a trap's nights are done (as opposed to broken); what passed it; the catch's weight in meals; one's other traps | — | — |
| The fen | Eels in its dykes in a run; its traps standing in a spate | — | — |
| Floodplain | Floods over the land (not in state) | — | — |
| Brine | — | The spring line (a standing fact shown as a sign) | — |
| The year as a fisher knows it | Everything (no lore, no memory, no marker) | — | — |

## What I could not settle

- **Whether a trap in the fen should meet the river's run.** The code does (§1a, the fen); it may be intended (eels go through
  fen dykes) or a side effect of drawing a set's run by the area. It decides whether a sign may say the fen's dykes are the safe
  place in a spate. A question for Zach in the proposal.
- **Heads passing the village each night.** Not kept in `days.jsonl` by village (only the river's starts), so I did not tabulate
  what each run night held against what was taken. The proposal's river record would keep it.
- **The low arm's `knows` readers.** Peter (Opus) read the eel run's `knows` line 3 times; I take it his trap craft rose to "known"
  by practice (16 sets), but did not trace his level by day.

*Current as of 21 Nov 2026.*
