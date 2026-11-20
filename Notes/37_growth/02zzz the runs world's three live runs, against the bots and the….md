---
id: docs/review/37_growth/02zzz_live_runs_world.md
kind: note
updated: "2026-11-20"
---
# 02zzz: the runs world's three live runs, against the bots and the targets

*note · `docs/review/37_growth/02zzz_live_runs_world.md`*


20 Nov 2026, 37.2. Thread: the nutrition worlds ([[W-69 Nutrition worlds|W-69]]). Zach (20 Nov): "please do the bot run then just the 3 live water calibration
runs to see if the surpluses etc line up ish".

**What was run.** The runs-only world (`cybertron2/specs/nutrition/runs_{low,medium,high}.yaml`, maker
`make_nutrition_runs.py`, seed 5) on main `98b2f7f7`: the food values on one basis ([[D2-258 The food values are put on one physical basis|D2-258]] to [[D2-262 The runs at a real river's size|D2-262]]), the water fixes (weir
sections by position and material, traps and the weir sharing a run, wear in [[D2-210 The weir in sections, capped, with upkeep by the river|D2-210]]'s band, smokehouses apart; 02zzw). 12 people
in three households, Opus at each household head, Sonnet in the middle, Haiku the rest; 64 days from late summer (two autumn runs,
two winters); `LLM_BACKEND=claude_code`. Cost: low $14.50, medium $14.78, high $33.48 ($62.76). The runs are in the session
scratchpad (`live/runs_*`), not yet published (no Hugging Face token in this session). Why the agents fished so little:
[02zzy](02zzy_why_they_did_not_fish.md).

## The numbers

Food is the engine's food (1 = 2,500 kcal); fish caught in food at 0.46 a kg. Bots: `--bots runs` on the same arms (02zzw §7).
"Fed per fisher": food caught per unit of fishing work × 7 units ÷ 1.1 food a day. Targets (proposals/subsistence_worlds.md):
survivable at medium, a bounded surplus at high, 6 to 15 people fed per fishing worker.

| | low: live / bots | medium: live / bots | high: live / bots |
|---|---|---|---|
| Fish caught (food) | traps 18.5 / 341 | traps 23.2 / 364 | traps 52 + weir 465 / traps 342 + weir 841 + nets 14 |
| Kept (kg): smoked / dried / salted | 0 / 0 / 0 / 0 / 50 / 0 | 1 / 1 / 0 / 102 / 18 / 0 | 97 / 0 / 448 / 278 / 49 / 120 |
| Fresh eaten / spoilt (kg) | 21 / 0 / 297 / 11 | 20 / 0 / 174 / 2 | 285 / 54 / 452 / 969 |
| Lost: swept / otters (kg) / fire (food) | 9 / 11 / 0 / 240 / 92 / 0 | 19 / 9 / 0 / 292 / 81 / 0 | 45 / 39 / 34 / 257 / 95 / 16 |
| Store at the first winter (day 13) | 30 (12 alive) / 101 (11) | 19 (12) / 97 (11) | 201 (12) / 310 (11) |
| Store at the second winter (day 45) | everyone dead / everyone dead | 5 (2 alive) / everyone dead | 175 (9) / 292 (5) |
| First missed meal | day 14 / 24 | day 12 / 26 | day 12 / 30 |
| Deaths (of 12, with an infant) | 13, by day 23 but one (day 53) / all by 36 | 12, 9 by day 23, the last day 54 / all by 36 | 3, all on day 17; 9 alive at 64 / 7; 5 alive at 64 |
| Food a unit of fishing work | 0.18 / 0.52 | 0.11 / 0.50 | 0.59 / 1.43 |
| Fed per fisher (caught) | 0.7 / 3.3 | 0.5 / 3.2 | 2.7 / 9.1 |
| Store at the end | 10 / 0 | 1 / 0 | 26 / 108 |

## What it says

1. **The high arm lines up, roughly, in survival but not in surplus.** The live village came through both winters with 9 of 12
   alive and the second winter's store at 175 food (about 18 days for 9). Its weir took 465 food against the bots' 841. It salted
   448 kg (the bots 120) and smoked 97. But on 0.59 food a unit of fishing work it fed 2.7 people per fisher, under the target's 6;
   the bots, at 9.1, are inside it. It ended with 26 food: a thin margin, not a surplus.
2. **High's three deaths were distribution, not production.** On days 15 to 17 the village held about 200 food, nearly all in the
   weir household's store (the Marshs). The Brooks begged for fish for two days ("Hamon, my household is starving ... Could you
   spare 4 fish?" Oliver, day 17), were refused or sent elsewhere, and three starved the same night; the next morning Peter gave
   salt fish to the two left. The bots lost people in the spring gap the same way (they do not share between households).
3. **Low and medium did not fish, so they say nothing about the world's balance.** They caught 18 and 23 food of fish against the
   bots' 341 and 364, set at most 4 and 8 traps on any night (the bots about 8 a fisher), and starved in the first winter, faster
   than the bots. 02zzy gives the causes: nothing tells them the eels run in autumn, the fishing-by-hand refusal reads as "the river
   is empty", the run's sign is seen only at the river and only in the evening, smashed traps read as "give up", and nothing tells
   them a trap is a small catch so many are needed. All three models drew the same conclusions from the same lines.
4. **The bots say medium is not survivable even played well,** and low is not meant to be. Medium's bots keep 120 kg against about
   300 food needed between the runs (OPEN [[Q-76 Whether the runs world's medium arm needs more keeping capital|Q-76]]).
5. **Salting binds the bots, not the high arm's people.** The people salted 448 kg (at 4 kg a unit of work, about 112 units) and
   spoilt 54; the bots salted 120 and spoilt 969. At salting's real rate (02zzx: about 20 kg an hour proposed, OPEN [[Q-73 Whether salting fish and meat stays at 4 kg a unit of work|Q-73]]) the
   bots' high arm would keep most of its glut.

## Reading against the targets

- **Survivable at medium:** no, for both the people and the bots. For the bots it is keeping capital ([[Q-76 Whether the runs world's medium arm needs more keeping capital|Q-76]]); for the people it is
  first whether they fish at all.
- **A bounded surplus at high:** the bots, yes (9.1 fed a fisher, 108 food at the end); the people survive but with no surplus.
- **The live runs are not yet a test of the balance** for low and medium: what they measure is the prompt's legibility of a
  fishing livelihood. The high arm is the one comparison that holds, and it is within a factor of two to three of the bots.

## What to do next (for Zach)

1. The legibility fixes of 02zzy, ranked there: a memory of the runs for those who know the crafts; a dawn sign of the run that
   reaches the village; the scale of a trap in its craft and results; a lift per place; farming switched off in this world with
   `packs_off: [farming]` and the farming trade removed; the reply schema's fallback example neutral. Then the same three runs
   again.
2. Salting's rate ([[Q-73 Whether salting fish and meat stays at 4 kg a unit of work|Q-73]]) and medium's keeping ([[Q-76 Whether the runs world's medium arm needs more keeping capital|Q-76]]), then the bots again.
3. Sharing between households in hunger is the agents' own; the world could make a household's starving more visible to its
   neighbours (a sign, grounded in state) before anything else.
