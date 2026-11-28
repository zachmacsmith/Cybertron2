# Each craft's lines by familiarity

**Status:** discussion
**Owner:** bench (the lines); 37.2 (the renderer and TECHNIQUES, where they would go)

## Summary

For all 161 crafts in TECHNIQUES (138 shown as craft lines, 23 ways or unshaped rows), a line saying what doing it does (104 new,
34 existing kept) and four lines of what a person is told at each familiarity: aware, rough, capable, known. Each claim is grounded
in the engine's code (file and function recorded per craft). Data only: nothing is wired into the prompt.

## The proposal

- The lines: `craft_lines/craft_lines.json` (merged from five parts, checked by `check.py`), readable as `craft_lines/craft_lines.md`
  (`render.py`).
- **does**: what doing the craft does, in the interface's voice; for a made thing, what it is for and how it is used ("make a
  harness: with one in hand you can lead an ox as a pack ox, and two let a yoked pair of oxen draw a plough"). Fills D5-2's "every
  technique of theirs with what it does" (L-204; stable's Q-112).
- **aware** (at most 10 words): what it is for, in plain words. Beyond D2-352, which shows aware as the name and who does it.
- **rough**, **capable**, **known** (25, 30, 30 words): know-how that adds level by level: what it is done with and how it commonly
  goes wrong; what makes it go better or worse as the engine computes it; the finer interactions. None repeats a generated number
  (inputs, units, odds, life), and none states the world (yields, seasons, places), per D5-2.
- If adopted, the fields would join each TECHNIQUES row (`does`, and level hints in place of the single `hint`, D2-356), with
  `iface.craft_line` showing each level's line beside the generated recipe.

## Why

Zach, 28 Nov: "Can you go and write all the different level of knowledge lines about all the crafts and techniques". In the
Fallowmere runs no arm made a pack basket in 60 days, though its line never said what it carries (now fixed for three rows); 104 of
the crafts showed only a label, which for a made thing says nothing of what it is for. D5-2: "an act or option not shown does not
practically exist".

## Alternatives considered

- Generate the made things' `does` from ITEMS' fields only (stable's recommendation on Q-112): shorter and self-updating, but it
  cannot say how a thing is used (a trap set in water, a harness in hand) or the know-how of the levels.
- One `hint` per craft, as now: no growth with familiarity, against D2-352's "the recipe's detail grow with familiarity".

## Open questions

- Whether these go into the prompt, and the prompt's size (Q-102): about 140 crafts a world, though a person sees only their own
  and the everyone-knows set.
- Whether aware shows a gist (beyond D2-352).
- Two lines name a season (cut withies, hay), because a cut out of season silently gives nothing: world or interface (D5-2)?
- The suspected faults found while grounding the lines (`craft_lines/suspected_faults.md`): which are bugs (D5-11). Several lines
  describe the engine as it is (manuring keeps the dung, gathering never fails); they change if the faults are fixed.

## Affects

TECHNIQUES rows (data.py and the registered rows of gear.py, process.py, stores.py, wild/methods.py), `iface.craft_line`,
`knowledge.craft_parts`; the prompt's size.

## History

- 28 Nov (bench, W-205): drafted for all 161 rows by five drafters from dumps of each row and its items, each line grounded in the
  handlers; merged and checked (161 of 161, no problems); the suspected faults collated for Zach, sent to no one.

## Sources

`craft_lines/BRIEF.md` (the drafters' brief), `craft_lines/part_1.json` to `part_5.json`, D2-352, D2-356, D5-2, D5-11, L-204,
stable's Q-112 and Q-102.
