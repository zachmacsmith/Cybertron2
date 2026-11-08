# Proposal: what is physically possible is possible; the consequences are social

**Status:** part 1 retrospective, accepted: D4-114 (8 Nov; built). Part 2 (the audit of claims) discussion. **Owner:** 37.4.
**Affects:** engine/farm.py, herds.py, verbs.py, lore.py, data FENCES; spec/world/holding.md, spec/core/processes.md;
economy/livestock.md (37.2's: OPEN Q-30).

## Summary

D4-23 already says the engine enforces only possession: claims are records, and using land against one is seen, never refused.
The Brookend run (p1) found places where the engine broke that, and others where its rules wasted the people's work:

1. **The ox the stones would not take.** The Crofts lent the Millers an ox, then gave it to them outright for days; the stones
   still refused it ("the ox on the Green is still yours, not one we may use"), because working beasts needed the `access` right.
   Hugh paid back the bread it had bought. Built: any beast at the place can be worked, whoever holds it; another's is seen.
2. **Fences on a season clock.** 137 acts (11% of all) went into three fences, none standing at the end: a wood fence lost a
   level a season (8 days) unless a quarter of its build went into mending each season, a fallen one was rebuilt from nothing,
   and one finished the day before a season turned lost a level at once. Built: by the year, safe in its first year, half kept.
3. **The lore named one window.** "Sow barley in spring" kept everyone from resowing after the summer harvest, though barley sown
   early in summer gives 0.85 of a full crop; nobody sowed in 32 days. Built: each crop's best and good halves of the seasons.

## Why (Zach, 8 Nov)

- "fix the ox lending, fences, lore and Green, then rerun"
- "I feel like the general default should be that anyone can use a thing if they physically could. Claims shouldn't be stopping
  people. Instead, it should be that socially it doesn't make sense. Claims should often not be enforced ... if it is physically
  possible it should be possible. The consequences are then social."
- On the fences: "137 fencing actions seems kind of insane?"

## The proposal (part 1, as built)

- farm.usable_herds: every herd here with the beasts needed, one's own or nobody's first; farm.beasts_note: an event naming
  whose beasts were worked, concerning their holders, and the words on the result (millstones, plough). A pack ox: any ox here
  (one's own first), seen if another's.
- FENCES wood: `mend` 0.25 a year (clocks: year), `kept` 0.5; herds._fences: the level falls at the year's turn, not in the
  fence's first year; farm._fence: a fallen fence restarts from half its build.
- lore.sowing_times: by halves of the seasons, best (within 5%) and well (3/4 of a full crop): "Barley does best sown in spring,
  and well early in summer or late in winter; rye does best sown late in autumn, and well in summer or early in autumn; beans do
  best sown early in summer, and well in spring; rye wants a winter; sown at other times, crops come up poor or not at all."
- Brookend (specs/make_plenty.py): the Green at size 4 (room to build), 48 days, children on.

## Part 2: the audit of claims (discussion)

To come: every place the engine still refuses an act for want of a right, and what each should become under the principle.

## Alternatives considered

- **Lending as a grant the engine checks** (a use right passed with the ox): keeps the engine enforcing claims, against D4-23.
- **Fences: lower the mending share but keep the season clock:** the clock is the fault; with 8-day seasons any per-season rate
  is out of scale.
- **Lore: list all seasons with their yields:** too long for a kept line; the two grades carry what a family would pass on.

## Open questions

1. Other rates on a season or event clock that the short year puts out of scale (an audit with the year-length question).
2. Part 2 above.

## History

- 8 Nov: part 1 built at Zach's request after the p1 Brookend run (D4-114).

## Sources

runs/p1_brookend; spec/world/holding.md (D4-23); D2-130; D4-105.
