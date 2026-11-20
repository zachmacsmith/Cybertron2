# Why the villagers of the runs world did not fish

20 Nov 2026, 37.2 (subagent)

This note reads the three live runs of the runs-only nutrition world (`cybertron2/specs/nutrition/runs_*.yaml`; W-69, D2-256),
the agents' own replies, talk, notes and memories, and the prompts they were shown. Thinking was withheld in every turn (no
`thinking` text in turns.jsonl or run.db), so the agents' reasons come from their `why`, their talk, their notes and their
memories. The low and medium runs are finished. The high run was read at day 28 of turns.jsonl (its log is at day 38, 10 alive).
The bots are `cybertron2/engine/bots_livelihood.py`, with results in 02zzw_water_fixes.md §6 and §7.

## The short answer

The LLM villagers were not shown the year a fisher knows. They began in late summer at an empty river. Every early try at it
said "no fish". By the time the eels came down (nights 6 to 17), most of them had written the river off as "fished out". The
first run nights fell in floods, which smashed the few traps they had out. Each trap is one small set that catches one or two
eels a night and needs its own lift by tag. Nothing they were shown suggested that many traps were needed. Snares, which give
visible hares, and the fallback's endless gathering filled their days instead. In the high arm the weir did its job: it
collects the catch in one place and a single lift takes all of it.

## The numbers

Counted from results lines and from days.jsonl's `wild.runs` (heads caught, robbed and wrecked). Food values are the prompt's
table (fish 0.46 at a lit fire, meat 0.6, the wild plants by kind), so these are approximate.

| | low | medium | high (to day 28) |
|---|---|---|---|
| Traps set (acts) | 23 | 35 | 34 |
| Most traps in the water on one night | 4 | 8 (day 6) | 11 (day 6) |
| Eels caught in traps (heads) | 56 | 69 | 134 |
| Traps robbed by otters / wrecked | 19 / 6 | 15 / 20 | 45 / 25 |
| Weir catch (heads) | none | none | 477 eels, 77 salmon, 10 lamprey |
| Food lifted from own traps / weir (results) | 8.9 / none | 9.8 / none | 14.8 / 233 |
| Food from snares (results) | 41.8 | 35.6 | 28.1 |
| Gather wild food acts (of which fallback) | 512 (326) | 557 (361) | 532 (386) |
| Firewood acts (of which fallback) | 149 (144) | 323 (317) | 472 (432) |
| Food from gathering | 71.2 | 97.1 | 63.5 |
| Deaths | 10 of 12 by day 24; last day 54 | 9 by day 24; last day 55 | 3 by day 18; 10 alive at day 38 |

- **The bots** (`traps=8, keeper_traps=3`) keep about 8 traps a fisher in the water through the windows, and caught 1,217 eels in
  low and 1,268 in medium (02zzw §7), against 56 and 69 here.
- **Food a unit.**
  - The bots' fishing gave 0.52 food a unit of work in low (02zzw §6).
  - Here: gathering about 0.14 food an act, snares about 0.33 (sets and lifts), the LLMs' own traps about 0.2 (sets and lifts,
    with the wrecks and otters).
  - Gathering gave the least for the work, but it was where most of their units went.
- **The fallback.** About two thirds of the gathering, and nearly all the firewood, was the fallback filling units left over,
  not a choice made in the plan. The plan-act counts in the brief (193 gathers against 15 traps in low) understate the
  imbalance in what was done: 512 gathers against 23 trap sets.
- **High.** The high arm's weir caught about as much as the bots' weir over the same nights. The gap in high is in its traps
  only.

## 1. What the prompt shows them

**The river.** In every arm, every day, the Isel is shown as:

> - the Isel (water): a broad slow river. Next to Eelmouth Fen.

- Every other parcel lists what one can do there ("here one can clear, clear for building, cut, fence, firewood, reap, sow...").
  The water lists nothing.
- Its height is never shown: only the day's weather word ("rain all day", "heavy rain"). The bots read `river_tonight`, the flow
  from the catchment's rain (the code says this read is wider than the signs).
- In high the weir is a line of its own: "a fish weir (stakes and wattle across the river, wicker traps in its gap); its gap
  shut; 3 sections (timber sound, ...); worked by Nichola, Peter".

**The runs and the year.** Nothing in the system prompt or the opening memory says that eels run down in autumn, salmon go up
after spates, or lampreys come in spring.
- "What you remember" holds the founders, "Hard winters you remember ...: last winter", and a debt or a quarrel over grain or a
  pig.
- The calendar line ("Autumn, day 3 of the season (5 left)") never connects the season to the runs.
- The bots are given exactly this ("it knows the year (the run windows, as a fisher knows the seasons)", `run_season`), and they
  set traps the day before a window opens.

**The run's sign** (`kinds.RUN_SIGNS`, emitted by `signs._wild_river`) is good text, grounded in the run at the water:

> the eels are running at the Isel tonight: the traps and the weirs on the river will fill
> the water at the Isel alive with eels in the dark, all going downstream
> salmon going up through the Isel, leaping at the shallows

The problem is where and when it can be seen:
- It is a sight sign on the river parcel, three steps from the Street (the Street, Eelmouth Field, Eelmouth Fen, the Isel), so
  only someone who went to the water that day sees it.
- It reaches them in the evening ("What you saw today"), when the day's units are spent, so the earliest traps it can bring are
  the next day's.
- The bot's `run_here` reads the run at dawn and sets that day.
- In low, no one was at the Isel on days 6 and 7, the first run nights. All three heads were in the Spinney (a deer drive, a stalk)
  and the rest gathered there or cleared. The first
  to see the run were Peter and Henry (salmon, day 8) and Petronel (eels, day 9).
- In medium and high it was first seen on day 6, by those who had already set traps (Oliver; Hamon, Nichola, Oliver).
- No sign gives the run's timing: no sign of a cue coming (the river rising brown after rain), and no village-wide sound or smell
  of a run (gulls, herons, otters busy).

**The trap** is one clause in the gather verb:

> trap in water (set wicker traps in the water at dusk; they fish by night for some nights, best when things run: come back to
> your traps and take what is in them, or it rots there or another finds it)

What is missing:
- That one act sets one trap. "You set traps in the water" reads as a whole line of gear, and the agents speak of "my traps" and
  "both sets of traps".
- What a trap holds (10 kg, `WATER_WORKS.trap.hold`) and what it takes on a run night (one to six eels, 0.5 to 3.4 kg).
- That more traps take more of a run.
- That a spate smashes about half of the traps in the water and a flood most (`wreck` 0.5 and 0.85).
- That the lift is a `take` from the trap's tag, one unit for each trap.
- The low arm's adults have only "a rough idea of: setting wicker traps in the water overnight ... You could try these, at a
  cost in materials and a risk of failing". No material cost showed up in any trap set's result, and no failure line did either.
- In low the youths Nigel and Petronel know the craft (novice) while the adults do not. No one asked them to teach it
  ("taught 0" all run).

**Keeping** is described fully for smoking ("a batch at a time on the racks for 3 nights of fire, smoked to half the weight
and keeping for months; tend the smoke once each day, or the fire dies that night"). Salting is a bare "salt fish", with no
inputs or rate given. The agents learned salting's least batch from refusals ("make salt fish: it needs 4 fish; you have 2 to
hand", 15 times in high).

**Misleading text in the prompt itself:**
- **The trade line.** Every adult is "By trade: sowing a field broadcast and reaping a crop", in a world with no fields and no
  seed. The village knows "dibbling seed". The seeded memories are of grain lent and a pig gone missing. The agents act on this
  (§2b).
- **The fallback example** in the reply schema is "(say, gather firewood)". Firewood fallbacks ran 144 to 432 times while the
  stores held 60 to 135 firewood.

## 2. What they said

**a. The empty river in summer taught them it was empty.**
- The run starts on day 5, and the world stocks no resident fish (README).
- Fishing by hand before that was refused with `there is no fish at the Isel`, and traps set on days 0 to 4 took one eel or
  nothing.
- Quotes:
  - Gunnild (Haiku, low, day 1): "No fish in the Isel today, but I brought back a good load of greens and watercress from the
    fen." The good load was about 2 meals for 7 units.
  - Hamon (Opus, high, day 1; a master smoker and salter, a skilled trapper): "Gunnild, the traps held nothing, so the Isel is
    fished out."
  - Hamon (Opus, high, day 2): "The Isel is fished out, so I'll set snares and hunt the woods around for meat we can dry for
    winter." His pinned plan carried "Isel fished out" on days 3 and 4.
  - Gunnild (Haiku, high, memory of days 5 and 6): "The Isel traps caught nothing, so the river is fished out."
  - Hamon (Opus, high, day 0): "the fowl and fish there are hunted thin". This echoes a sign of the same day, "the salmons break
    and run long before you are near: hunted too often here" (`_wild_wary`, from the first hunt and nets at the Isel; see §5).
- The refusal also fires during the runs, because fishing by hand takes only resident fish:
  - Peter (Opus, low, day 9), who had seen the salmon running the evening before, was refused "there is no fish at the Isel".
  - Henry and Denise (Haiku) kept trying by hand through the run. Denise (Haiku, low, day 15): "Father, where are the fish
    running? If there are none, Henry and I will set snares".

**b. They thought of themselves as farmers.**
- Oliver (Opus, low, day 1, note): "There were no fish at the Isel by hand (day 5). ... Seed: ask Shepherds/Marshs for grain or
  beans, paying in coin (I have 2). ... Then clear and sow Eelmouth Field".
- Hamon (Opus, low, day 1) posted offers of coin for rye and grain that stayed open all run.
- Petronel (Haiku, medium, day 4): "I'll put my remaining units into clearing Eelmouth Field with him, since about 63 units of
  clearing are still needed there before sowing."
- Katherine (Sonnet, low, days 5 and 6) spent her days clearing "so we can sow once seed is found".

**c. The run came on flood nights, and the smashed traps read as "give up".**
- The first autumn's run nights were floods or a spate on days 6 to 10 (days.jsonl `flow`). The bots set their traps whatever
  the river, and 40 to 46% of their trap catch came on those nights (02zzw §4).
- The agents read "your wicker traps at the Isel smashed against the bank in the spate: they will catch no more" as a reason to
  stop:
  - Peter (Opus, high, day 8): "The traps on the Isel were smashed in the spate, so don't bother with them. I'll see to the
    weir."
  - Hamon (Opus, medium, day 7): "I'm joining Oliver's deer drive today, because the spate is smashing traps."
  - Denise (Haiku, medium, memory day 15): "Eels at the Isel are unreliable; otter at the traps."

**d. They did think the run worth having when they saw it, but at the scale of one or two traps.**
- Hamon (Opus, high, day 6, note): "Eels run downstream at the Isel in autumn, on dark wet nights (seen autumn day 2). Traps
  and weirs fill then. ... Smoke the eels (master) or salt them to keep."
- Peter (Opus, low, memory day 13): "Late autumn eels run at the Isel: wicker traps there gave six eels a night."
- Peter (Opus, low, day 17): "empty all three fresh lines" with Henry.
- Katherine (Sonnet, medium, day 9) told the head that more were not needed: "My traps are set at the Isel and the eels are
  running tonight. Tomorrow I'll empty them first, so you don't need to set more there."
- Oliver (Opus, high, memory day 4): "Traps at the Isel catch little."
- No agent in any arm reasoned about how many traps to set, or tried a number. The most in the water on any night was 4 (low),
  8 (medium) and 11 (high), against the bots' 8 a fisher.

**e. Lifting was hard to get right.**
- `take` "from the Isel" found nothing lying there: refused 4, 10 and 7 times.
- In high it emptied the Marsh weir instead, which counts as theft. Hamon (Opus, high, day 7): "my own traps were smashed in
  the spate, and those eels came from the Marsh weir's traps. That's theirs by right." His memory on day 10: "If my own wicker
  traps are smashed, 'take fish' at the Isel empties the Marsh weir's traps instead: theft." He took 51 fish from the weir this
  way on days 7 and 8, then spent days settling the "Weir debt".
- Oliver (Opus, high, day 6): "Does anyone know which trap tag is ours? T17 was empty, so it's not ours."
- Oliver (Opus, high, memory day 4): "To empty wicker traps: take fish from the trap tag (e.g. T1), not from the place."
- In low, Oliver lifted Peter's traps, and Peter's household then raced him to them at first light.

**f. Snares and the land gave visible, countable returns.**
- Morning lines such as "three brown hares hang in your snares at Eelmouth Common" came daily from day 3. A hare is about 1.7 to
  2.9 meat. Oliver (Opus, medium, day 11): "snares are the one thing that has fed us".
- Gathering results look large in number and are small in food ("0.32 berries, 2.04 greens, 1.28 mushrooms"). The agents
  rarely did the arithmetic: Gunnild's "good load" above; Nichola (Sonnet, low) foraged the Fen alone from day 24 to her death
  on day 54.
- A mast-year sign ("acorns thick in the Spinney; leach them at the hearth into acorn meal") drew whole days of acorn gathering
  ("Acorns come in too slowly to be worth the day", Hamon, Opus, low, day 8).

**g. Winter keeping.** They did plan for it.
- In medium, most of the smokehouse work went on hares, not fish. Haiku youths tended the smoke daily, so medium smoked hare
  meat while its traps lay smashed.
- In high, Peter (Opus) and Nichola (Sonnet) salted the weir's catch: 48 salt-fish acts, 9 boils.
- Low has no keeping but drying at the hearth ("Dry fish takes 3 units at the hearth: plan it first", Peter, low).

## 3. Models

- **Opus heads** did the fishing that was done:
  - Peter (low) set 16 of the arm's 23 traps.
  - Hamon, Oliver and Peter set and lifted most traps in medium and high.
  - Opus also wrote the run down as a lasting lesson (Hamon's "Eels" note, Peter's memory).
  - But Opus also reached the wrong lasting conclusion fastest ("fished out", "don't bother", "catch little"), and spent units on
    house politics: snare theft, the weir debt, keeping units back to try for a child.
- **Sonnet** varied with the arm:
  - In low (only a rough idea of the craft) the two Sonnets set no traps at all and gathered 280 times.
  - In medium and high, Katherine (Sonnet) was the most steady trapper (11 and 10 sets), and Nichola (Sonnet) salted in high.
- **Haiku** are mostly the children and youths (4 units). They followed their heads' orders ("Peter asked me to..."), tended the
  smoke, repeated fishing by hand after "no fish" refusals, and filled the most fallback units with gathering and firewood.
  Haiku trapped only when told to.
- The difference between models is smaller than the difference the prompt makes. Every model drew the same conclusions from
  the same lines.

## 4. The feedback after setting and lifting

- **Set:** "You set traps in the water at the Isel; they will catch by night for about 8 nights, for whoever comes to them." It
  gives no count, no capacity and no cost. "For whoever comes to them" invites the race to lift, but says nothing about how
  much to set.
- **Morning:** "four eels in your wicker traps at the Isel", "an eel in your wicker traps at the Isel". This is legible, and the
  agents acted on it.
- **Lift:** "You took 0.5 fish from your wicker traps at the Isel" (1.1, 1.7, 2.3, 3.4). The morning counts eels and the result
  weighs "fish" in kg, with no meals. Half a fish sounds like nothing: Oliver (Opus, high, day 3) reported "half an eel".
- **Losses:**
  - "your wicker traps at the Isel smashed against the bank in the spate: they will catch no more"; others see "broken wicker in
    the reeds below the Isel".
  - "an otter has been at the traps at the Isel in the night: it will be back while there are fish in them"; "torn at the neck,
    scales and a fish head on the withies: something has had what was in them".
  - None says how much was lost, or that a trap lifted that morning lost nothing. A spate or otter line comes after most lifts.
    The lesson the agents took was that traps are unreliable, not that the catch must be lifted at dawn and the traps set again.
- **Signs that never fired:**
  - "the traps at {place} crammed full" (0 times), because no trap filled.
  - The year's "the eel run was thin this year" appeared in medium (4) and high (1), late, after most were dead.

## 5. What blocked or misled, in the engine and the world

- **`there is no fish at the Isel`** (refused 28, 20 and 30 times in the three arms) is true of resident fish, but it fires
  during the runs and reads as a fact about the river. It is the single most damaging line (§2a).
- **The wariness sign at the Isel on day 0** ("the salmons break and run long before you are near: hunted too often here").
  - It fired after the first hunt or net there, before any salmon could have been hunted, and in high Hamon took "hunted thin"
    from it.
  - "Hunt the wild" at the Isel later met salmon many times in a row, each line "came on a salmon, but it got away", which drew
    more hunts.
  - I did not trace why the wariness was set on day 0, or whether any method could take a salmon in this way. Worth a check.
- **`take` by place on the water** resolves to the weir's traps, which is theft (§2e). Taking from one's own traps needs each tag.
- **No other refusals blocked fishing.** No craft was unknown in medium and high, every trap set succeeded, and nothing said
  "you need" for traps. The rod needs hide ("No rod: it needs hide and we have none", Katherine, Sonnet, high, day 3). The salt
  batch's least shows only as refusals.
- **The world.**
  - The first run's peak fell on flood nights (Q-77). That wrecked most of the early traps in every arm.
  - The 8-day summer before the run, with the larder of 8 days, gave the agents four empty days at the river first.

## What I could not tell

- **The agents' thinking:** it was withheld in every turn.
- **Whether "rough idea" lowered the low arm's catches**, or whether any trap set failed. No failure line appeared.
- **Whether those away from the river could have glimpsed the run's sign.** I did not trace the noticing chance for the run's
  sign at the Street.
- **Why the wariness sign fired on day 0** (§5).
- **The high arm after day 28.** The run is still going.
- **The figure of 18.5 food in the brief.** My 8.9 is lifts from own traps only. The 56 eels caught (about 32 kg, about 15 food)
  include what the otters took.

## What would most likely change behaviour, ranked

1. **Give the fishers the year, as memory, and fix the "no fish" refusal.** This is the bots' own premise.
   - Those who know the trap or weir craft remember the runs from the world's `RUNS` windows: "In autumn the eels come down the
     Isel on dark wet nights, for about ten days; the salmon go up after a spate; the lampreys in spring. Between the runs the
     river holds little."
   - It is a standing fact, so it belongs in "What you remember" or the craft's description, not in a sign (senses guide §3).
     It is grounded in `kinds.RUNS` and the world's calendar. It fits "lore as tested belief" (L-117).
   - The refusal should say what the state holds: "no fish lie in the Isel to take by hand now; the river's fish come in the
     runs, to traps and weirs".
   - This answers §2a, the largest cause.
2. **Let the run's sign reach the village in the morning, as a bundle.**
   - At dawn, for those at the water and those passing: the run in the water.
   - Fainter, across the place: herons and gulls gathering at the river, an otter busy on the bank, eels on the wet grass of the
     Fen.
   - The day before, for the practised: the cue, "the Isel rising brown after the rain: an eel night coming". This is grounded in
     `RUNS.eel.cue` (`rain_after_dry`). It waits on the river's level (D2-215) for the level itself.
   - This is a change worth acting on today (senses guide §2, §4). It matches the bot's dawn read. In low it would have reached
     the village on day 6, while the heads were in the Spinney.
3. **Make the craft's description and the results say the scale.**
   - The verb: one act sets one trap; it holds about 10 kg; a run night fills it with a few eels; set as many as you can lift;
     each lift is a unit, by its tag.
   - The set result: "You set a wicker trap (your 3rd at the Isel)".
   - The lift result: "You took 4 eels (2.3 kg, about 1 meal)".
   - The loss lines: what the loss cost ("the spate took the trap and the 3 eels in it"; "the otter had 2 eels").
   - All of this is in the state. Without it, no agent ever reasoned about how many traps to set (§2d).
4. **Make lifting one's own traps one act a place, and never let a place-take reach the weir.**
   - The weir, where the catch is collected and lifted in one act, is where the LLMs fished as well as the bots. The traps,
     lifted one by one by tag, are where they failed.
   - Whether a lift should cover all of a person's traps at a parcel is a design question for Zach: it changes the gear's
     work cost, which 02zzw §5 calibrated.
   - A place-take on the water taking from one's own traps first is a fix to the verb.
5. **Take farming out of the runs-only world's people** (`make_nutrition_runs.py`).
   - No "By trade: sowing a field broadcast and reaping a crop", no "dibbling seed", no grain-and-pig memories.
   - Their trade should be the arm's fishing craft. Units went on clearing for sowing and on seed offers (§2b).
6. **Make the fallback example neutral, or name the arm's work.** "(say, gather firewood)" in the reply schema is copied
   literally, and the fallback ran two thirds of all gathering and nearly all firewood. A fisher's fallback could as well be
   "set another trap in water", which is what Peter's fallback did on day 10 in low.
7. **Check the wariness sign and the salmon at the Isel** (§5). A sign of game "hunted too often" before any hunt is not grounded
   in a change. A hunt that meets salmon again and again without any way to take them is a lure.
8. **The world's first run on flood nights** (Q-77). It costs the bots too, but it hits the LLMs harder, because they read the
   wreck as a lesson. Once the loss lines in item 3 are in place, the world can stay as it is.

Sources:
- the runs: scratchpad `live/runs_{low,medium,high}/` (turns.jsonl, days.jsonl, memory.jsonl, run.json's `systems`);
- `cybertron2/wild/kinds.py` (`RUNS`, `RUN_SIGNS`);
- `cybertron2/engine/signs.py` (`_wild_river`, `_wild_wary`);
- `cybertron2/engine/data.py` (`WATER_WORKS`);
- `cybertron2/engine/bots_livelihood.py`;
- 02zzw_water_fixes.md §4 to §7;
- docs/cybertron2/guides/senses.md;
- OPEN Q-76, Q-77, L-117.
