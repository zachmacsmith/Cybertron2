---
id: docs/cybertron2/proposals/lesson_in_teachers_craft.md
kind: proposal
updated: "2026-11-19"
---
# A lesson is in the teacher's craft

*proposal · retrospective, accepted: D4-123 (19 Nov 2026) · `docs/cybertron2/proposals/lesson_in_teachers_craft.md`*

> A lesson happens when a teacher and a learner set time aside for each other the same day, at one place. If they named different crafts, the lesson is in the teacher's craft, and both are told what was taught and what was asked for. A learn that finds no teacher names the craft it was for. A world's 


**Status:** retrospective, accepted: [[D4-123 A lesson is in the teacher's craft|D4-123]] (19 Nov 2026)

**Owner:** 37.4

## Summary

A lesson happens when a teacher and a learner set time aside for each other the same day, at one place. If they named different crafts, the lesson is in the teacher's craft, and both are told what was taught and what was asked for. A learn that finds no teacher names the craft it was for. A world's physics can set the day this starts (`teach.any_craft_from_day`, default 0). A run that began before it can keep its earlier days as they were.

## The proposal (as built)

- `settle.settle_teaching`: the teach and the learn are paired by teacher, learner and place.
  - The craft named by the teacher is the one taught.
  - On a mismatch, the teacher hears "X wanted to learn A, but you taught B instead, so they learnt B".
  - The learner hears "You wanted to learn A, but Y taught B instead, so you learnt B", then the usual lesson line.
- An unanswered learn: "You meant to learn A from Y, but Y did not set aside time to teach you."
- `PHYSICS["teach"]["any_craft_from_day"]` (decided: 0). Before that day, the crafts named must match, with the old wording, so a resumed run replays its earlier days exactly.
- The runs world's model run ([[W-58 The runs world with a model to each household|W-58]]) starts it at day 14 (`any_craft_from_day: 13` in the run's stored spec). Two interventions follow day 13:
  - Saer is given boiling salt at the level a day's lesson gives (capable), "taught by Lambert".
  - An event at Highpool tells Saer and Lambert that the teaching took.

## Why

Lambert Brook taught Saer "boil salt" on days 9, 11 and 12 of the runs world. Saer asked each time for "salt pan", which is the key of a different technique (sun-dried saltmarsh salt) as well as an alias of the brine-pan fitting. Nothing took, and neither was told why. Saer asked every evening whether the lesson had taken: about 12 units spent for nothing.

Zach (19 Nov): "surely they can be the same skill they feel similar enough? Fix it so it says which skill they taught / wanted to learn exactly. Also, if there was a mismatch they should just end up getting a lesson on whatever the teacher is teaching. Can you insert it so that the person who was being taught now knows as well?"

## Alternatives considered

- **Rename the saltmarsh technique** so "salt pan" no longer names two things. This fixes this case only, and two crafts can still be confused by their wording. Not done; the name clash stays (OPEN).
- **Refuse a mismatched lesson and say why.** The words are clearer, but a day is still lost. Zach chose the lesson in the teacher's craft.

## Open questions

- Should "salt pan" stop being both a fitting alias and a technique key? (OPEN [[L-128 'salt pan' names two things|L-128]])

## Affects

- cybertron2/engine/settle.py; cybertron2/engine/data.py (PHYSICS teach).
- tests/test_cybertron2_lesson_mismatch.py.
- spec/agents/actions.md.
- runs/water_runs_models_r1 (stored spec, interventions 4 and 5).

## History

- **19 Nov 2026:** built at Zach's request on branch `runs-models`; recorded as [[D4-123 A lesson is in the teacher's craft|D4-123]].
- **19 Nov 2026:** wording changed at Zach's word ("something like 'you wanted to learn x but they taught y instead so you learnt y'").

## Sources

- The runs world's model run, days 9 to 13 (Lambert's and Saer's turns).
- Zach in conversation, 19 Nov.
