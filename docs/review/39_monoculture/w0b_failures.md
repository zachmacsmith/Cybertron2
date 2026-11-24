# World 0b: where the failures came from (24 Nov 2026, session bench, W-202)

Zach (24 Nov): "dig into the runs: their behavior and plans … Were they failing to try get food, not trying new things, not
thinking of appropriate actions at all, messing up the commands / getting a lot of rejections or getting confused or what?"

Data: the five arms as stopped (Sonnet 5.5 18 days, Haiku 5.5 23, Haiku 4.5 6, Sonnet 4.5 5, Sonnet 5 2), from each run's
turns.jsonl, days.jsonl and run.db (changes, events). Scripts in the session's scratchpad (metrics.py). All on the interface audited
in prompt_audit.md, before D5-2.

## The figures

| | Sonnet 5.5 | Haiku 5.5 | Haiku 4.5 | Sonnet 4.5 | Sonnet 5 |
|---|---|---|---|---|---|
| days, alive of 21 | 18, 17 | 23, 10 | 6, 17 | 5, 21 | 2, 21 |
| acts | 1,930 | 1,237 | 293 | 432 | 150 |
| refusals (acts and reply fields) | 317 (16%) | 528 (43%) | 286 | 136 (31%) | 46 (31%) |
| acts on food | 37% | 43% | 39% | 42% | 28% |
| distinct acts used | 48 | 66 | 50 | 42 | 41 |
| food made (meals) against person-nights | 459 / 397 | 260 / 446 | 65 / 126 | 73 / 109 | 13 / 43 |
| food lost to spoiling and vermin (meals) | 119 | 136 | 54 | 35 | 31 |
| food floors the people set ("keep at least") | none | 9 | 1 (96 grain as seed, 32 held) | 1 (30 seed grain) | none |
| arrivals at the other village | 9 | 0 | 0 | 0 | 0 |
| offers / agreements | 27 made (155 lots) / 0 | 22 / 1 | 0 / 0 | 0 / 0 | 6 / 0 |

## Four sources, in order of weight

### 1. The world gives little food, and less in winter (all arms)
- Most food labour went to foraging and hand fishing. Foraging yields greens, watercress and mushrooms at about 0.04 to 0.1 of a
  meal each; the Brook was "fished out for now" (Sonnet 5.5: 42 refusals); few had a line or rod ("you have no line to fish with").
- The run starts in late summer: autumn by day 4, winter by about day 13; the water iced over ("the Brook is iced") and closed
  fishing.
- Spoiling and vermin took a fifth to a half of what was made.
- Hunger cuts a person's units (to 1), so a short week becomes a spiral.
- Only Sonnet 5.5 made more food than its people's nights; it still went hungry at Highpool, where the food was not.

### 2. The models' own choices (Haiku most)
- **Floors on their own food, kept while starving.** Haiku 5.5 set nine ("keep 20 smoked fish for the hungry time"; "keep the grain
  at 30"); Haiku 4.5 kept 96 grain as seed against 32 held and the farming household died on day 2. Sonnet 4.5 set one, saw it
  ("my seed rule at 96 grain blocks eating our 31.8 grain. Must fix this immediately") and changed it. Sonnet 5.5 set none.
- **Labour spent elsewhere while starving.** Haiku 5.5: 110 acts twisting cord, 50 repairing (often a "sound" building), 117
  tries to light a fire with no fuel in hand (the same refusal 117 times). Haiku 4.5: guarding fields and setting snares for rats
  on the day the household starved.
- **The trade the world was built on did not happen.** Sonnet 5.5's salt-holders posted 27 offers of salt for grain, but at
  Highpool, where only other fishers saw them; the grain was at Middleham. One went to Middleham hungry on day 14. No agreement in
  18 days. Haiku 5.5 never travelled between the villages at all.
- **Little exploring**: no arm went to Lowstrand or any unexplored place.
- Variety is not the problem: each arm used 41 to 66 different acts.

### 3. The interface (all arms; Haiku 4.5 and 5.5 most)
- **Hidden acts and options** (prompt_audit.md): no watching, meetings, partnering, far hunting or hunting parties anywhere; few
  tries for a child.
- **Names the prompt does not match**: storing foraged food as "wild food" when the hands hold mushrooms, greens or watercress
  ("there is no wild food in your hands": 26 to 64 a run); "sleep" with no building (52 in Haiku 4.5: "no building called None");
  "bury", which no act is called (29 in Haiku 5.5); "say" put among the acts (20 in Sonnet 4.5); "racks called 'me'" or "'my
  hands'" for moving goods; a lesson without its fields ("say the lesson").
- **Limits met over and over**: three private messages a day (51 to 63 refusals in the Haiku arms), eight notes.

### 4. Plain mistakes and confusion
- A Sonnet 5.5 founder slaughtered the Fletchers' calf, not his own dead bull, and owned up in the evening.
- Haiku 5.5 repeated refused acts many times; the engine notes "(tried once, not again)" and they tried again.

## By model
- **Sonnet 5.5**: few refusals, no food floors, the only arm that travelled, traded and tried for children. Its failures are the
  world's (low food, winter, fishing out) and one of planning (offers where the buyers were not).
- **Haiku 5.5**: many refusals; nine food floors kept while dying; labour on cord and repairs; never left its village. Half dead by
  day 23.
- **Haiku 4.5**: the interface (sleep, tell, notes) and one seed floor that killed a household by day 2.
- **Sonnet 4.5, Sonnet 5**: too short to read (5 and 2 days); Sonnet 4.5 caught and fixed its own floor.

## What this means for the next runs
1. The interface (W-109, D5-2, D2-350): the hidden acts and options, and the names that do not match (wild food, sleep, bury, say).
2. The world: start in spring, not late summer (World 0b starts at summer day 4, winter by day 13); food that keeps; a fishery that
   does not fish out in a week. The design said "the first winter is survivable with care, not without it"; this one was not
   survivable with the care these models gave it, and barely with Sonnet 5.5's.
3. The trade: whether offers are seen only where posted is the engine's rule (and the prompt says so); the farmers never came to
   Highpool. A market or a carrier is a design question, not a fix.
