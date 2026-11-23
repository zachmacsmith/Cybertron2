---
id: docs/cybertron2/proposals/trying_and_learning.md
kind: proposal
updated: "2026-11-23"
---
# Trying and learning: crafts by difficulty, failures that teach, awareness that is easy to come by

*proposal · discussion (22 Nov 2026). Nothing decided, nothing built. · `docs/cybertron2/proposals/trying_and_learning.md`*

> Every craft gets a **difficulty class** (simple, practised, skilled) that sets how forgiving a first try is, how fast practice raises one, and whether teaching is needed to master it. Every **attempt teaches**: a failure reports a true cause or the next lesson the person has not had, and the engine 


**Status:** discussion (22 Nov 2026). Nothing decided, nothing built.
**Owner:** 37.2 (the crafts' data: classes, failure lessons, sentences); the knowledge core (`engine/knowledge.py`, `verbs.py`,
`perceive.py`, memory) is 37.4's, named on any merge. **Related:** knowledge in their own words ([[Q-81 Knowledge in their own words|Q-81]]), the crafts evaluation ([[W-74 The crafts and techniques design evaluated|W-74]]),
recipes shown ([[D2-263 A craft a person knows at capable or known shows, where they look|D2-263]]), the livelihood archetypes ([[W-70 Verbs and livelihood archetypes, before the engine rework|W-70]]).

## Summary

Every craft gets a **difficulty class** (simple, practised, skilled) that sets how forgiving a first try is, how fast practice raises
one, and whether teaching is needed to master it. Every **attempt teaches**: a failure reports a true cause or the next lesson the
person has not had, and the engine records what they now know of the craft, so the craft's line in their prompt fills in. **Awareness
is easy**: attending to a thing or to someone at work makes one aware of the crafts that make or use it. **Mastery is demanding**:
skilled crafts stop at capable without a teacher. Practice runs on the **life clock**, scaled with the lifespan.

## What is there now

- One try rule for every craft (TRY, `engine/data.py`): a rough idea uses 1.7 times the materials and works half the time; capable
  1.3 times and three times in four; known always. A failed make loses all its inputs.
- Three skill curves only: basic (1.0 to 1.5), trade (0.5 to 2.0), the hunt (1 to 8); tau 50 units.
- A level rises on about two successes, a failure counting half; aware cannot try at all.
- A refusal names what is short ("it needs 0.1 hide", [[D4-95 What a refusal says|D4-95]]), but nothing of the craft is recorded in the person's knowledge: 14
  agents in the river run spent kept lines on "GATHER SETS A LINE, TAKE LIFTS IT" (crafts_evaluation).
- Awareness only from hearing a craft named or from seeding; looking at a thing teaches nothing; watching (4 units) gives a rough idea.

## The proposal

### 1. Three difficulty classes (learning_times.md)

| Class | Crafts (from 18 looked up) | Real anchor |
|---|---|---|
| **simple** | setting snares, twisting cord, line fishing, salting, butchering and skinning, the quern | anyone trying usually manages crudely; Meriam fishing returns show no age effect (Bird and Bliege Bird 2002) |
| **practised** | wicker traps and baskets, netting, hurdles and weirs, smoking, spinning flax, oven bread, charcoal (near skilled), a hunting bow, ploughing | first tries often fail with waste; a beginner makes half a hurdle a day against an old hand's 2.5 to 3; charcoal 1:6 common, 1:4 good practice (FAO 41) |
| **skilled** | smithing, copper smelting and casting, tanning (and a war bow) | apprenticeships of 7 to 10 years (Statute of Artificers 1563; the Bridgwater tanner's indenture of 1424, 10 years) |

The class is a field on each craft row; a craft may override any parameter. Each row also says what skill acts on: yield, waste or
quality.

### 2. The parameters (estimates, to calibrate)

| | simple | practised | skilled |
|---|---|---|---|
| chance a try works, at aware / rough / capable / known | 0.6 / 0.8 / 0.95 / 1 | 0.35 / 0.55 / 0.8 / 1 | 0.15 / 0.35 / 0.65 / 1 |
| materials used, at aware / rough / capable | 1.3 / 1.15 / 1.05 | 1.8 / 1.5 / 1.2 | 2.0 / 1.8 / 1.4 |
| score to rise: aware→rough / rough→capable / capable→known | 1 / 2 / 2 | 2 / 3 / 4 | 3 / 4 / a lesson needed |
| tries from aware to capable (about) | 3 | 6 | 9 |
| practice tau (units, at lifespan 96, scaled) | 10 | 25 | 50 |
| skill range | 0.8 to 1.3 | 0.6 to 1.6 | 0.5 to 2.0, the top half only with a teacher or working beside a master |

A failure counts 1 toward rising at aware and a half above. An optional **crude result** for simple and practised crafts: it works,
but less or worse (a trap that holds less, a net with holes).

**The life clock:** a 7-year apprenticeship is 15,000 to 20,000 hours, more than an engine life holds (about 580 units at lifespan
96), so learning is matched by **share of a life**, not by hours: one life-year is about 10 units of work, 3 to 5 at one's main
craft; seven years' apprenticeship is about 25 to 35 units at the craft. Practice is set at lifespan 96 and scaled with the lifespan,
as the hunt's practice already is (`practice_x`).

### 3. Every attempt teaches

Each craft has an **ordered list of lessons** (an input, a step, a place, a season, the tool), each with a line. A failed attempt:
1. reports a cause the state really holds, if one does (wrong season, wet wood, a missing input, the wrong place): "the rods split:
   withies cut in summer are too brittle; cut them in winter";
2. otherwise gives the **next lesson the person has not yet had**: "the weave came apart at the throat: it wants the rods soaked
   supple"; so failing in a new way teaches more, and the same failure again teaches nothing new;
3. once every lesson is had, says the shortfall is skill ("you know how it goes; your hands are not yet sure of it").
No line claims a cause the state does not hold (the senses guide). What is learnt is kept in the person's knowledge of the craft
(`Mind.know[craft].lessons`), and the craft's line in their prompt shows it: "a wicker trap (a rough idea): withies, soaked; you have
not yet got the throat right". The person may still write it in their own memory; the engine keeps it regardless, since it is
knowledge of the hands, not a note.

### 4. Awareness is easy to come by

- **Attending to a thing** (a trap, a net, a smokehouse, a sack of flour): aware of what it is for and of the crafts that make it
  or use it; for a simple craft, a rough idea at once.
- **Attending to someone at work** for a day (free): aware of the craft; one lesson of it.
- **Working beside them** (today's `watch`, the costly form of attention): a rough idea and two or three lessons.
- **Attention can be spent on** (exploration, Zach 22 Nov: "Spend more actions of attention? Maybe that would be a better mechanic,
  for noticing nicher things, being more likely to consider/discover relevant techniques etc or pick things up from what others have
  done"): one free attention a day as now, and units spent on more ("observe {thing or person}, 2 units"): rarer things noticed,
  a craft's lessons picked up from watching someone work (with or without their consent; `watch` folds into this), a technique
  discovered from a finished thing, the signs read more fully. Teaching stays its own act: a willing teacher passes more, faster.
- **Hearing a craft named:** aware (as now), but only by the craft's own name, not common words (crafts_evaluation found awareness
  matched on common words).
- **Aware may try** any craft, at aware's odds and waste: guessing the inputs from what one holds, wrong inputs wasted. Whether every
  craft or only some may be tried untaught is open (below).

### 5. Mastery is demanding, teaching is the way up

For skilled crafts practice alone stops at capable and halfway up the skill curve; a lesson from one who knows it (lessons exist,
[[D4-123 A lesson is in the teacher's craft|D4-123]]) or working beside a master takes one further. Teaching was the one path agents used in the river run (17 lessons against 4
rough ideas from watching), so this puts weight where behaviour already is, and makes specialists and the dependence on them real.

### 6. Teaching from the teacher's peak (exploration)

A lesson moves the learner part of the way toward the **teacher's lifetime peak skill** (the engine keeps `peak`, used today for
relearning), not their present skill, so an elder past their best still teaches what they knew; a teacher at or near their peak
teaches faster, their hands showing what their words describe (Zach, 22 Nov: "make teaching depend on their peak skill value
rather than current one ... bridge the current learner and the teacher's lifetime peak, maybe with some benefit if they are
currently at their peak"). The knowledge lines are the agent's own and cannot be read by the engine for this. Today teaching is the
same for every craft: one session with one who knows it makes the learner capable.

### 7. Each craft its own skill profile (exploration)

Zach, 22 Nov: "different techniques could have completely different skill profiles, have much more depth where you could get
better and better, or be very shallow, or quick learning to one level then get much better later ... Should it be discrete or
continuous? Or continuous skill with discrete capability points unlocked along the way?" Proposed:
- **Skill is continuous,** a number per craft that practice raises along that craft's own curve; it governs how well: yield, waste,
  quality, how often a try works.
- **Each craft's curve from a few shapes:** shallow and quick (snares level off early), steady (netting), slow and deep (smithing,
  improving for years), stepped (quick to a basic level, then a long climb); each a start, a level-off point, a rate and a ceiling.
  The difficulty classes (§1) are default shapes a craft may override.
- **Capability points are discrete,** unlocked at thresholds on the curve; they change what one can do, not how well: a timber weir
  section, reading a run a day early, a fine net, teaching the skilled half. A craft's ladder is its list of capability points, one
  or two for some, many for others.

### 8. Transfer through underlying skills (exploration)

Zach, 22 Nov: "should we have techniques also sit on some multidimensional axis of the underlying types of skill needed so there can
be some automatic transfer ... learn faster or have better baseline skill ... Could maybe go with genetic baselines passed on with
some mix from birth tho idk if that would be too much?" Proposed, kept small:
- **Six to eight underlying skills:** working with the hands (weaving, knotting, fine work); fire and heat (smoking, charcoal,
  smelting, baking); reading animals (hunting, fowling, herding); reading water (fishing, the runs); plants and soil; building and
  structure; strength and endurance; dealing with people (trade, teaching).
- **Each craft has a small profile across them** (a net mostly hands; smoking mostly fire, some water).
- **Practice feeds the craft first and its dimensions a little;** a new craft's starting skill and learning speed draw on related
  dimensions: a basket maker takes to netting, a hunter to fowling, a charcoal burner to smoking. A head start of up to about a
  third (calibrate).
- **Inherited aptitude** (a baseline per dimension from a mix of the parents and chance) is an experiment knob, off by default: it
  adds variance that makes runs harder to read, craft ability is mostly learnt, and transfer through practice already gives families
  their trades through who teaches whom.
- A real rebuild: every craft row needs a curve shape, capability points and a profile; best done with the archetypes rework ([[W-70 Verbs and livelihood archetypes, before the engine rework|W-70]]).

### 9. Each craft's row carries

class (or curve shape), capability points, a profile across the underlying skills; what skill acts on; its lessons with their lines (2 to 3 drafted per craft in learning_times.md); a "what it does" sentence
([[D2-251 Every technique, fitting and thing to build says what it does and why…|D2-251]]'s ladder); its inputs and batch ([[D2-263 A craft a person knows at capable or known shows, where they look|D2-263]], [[D2-247 A process of bulk goods has a most it takes at once, not a least|D2-247]]). About 130 rows, best written with the archetypes rework ([[W-70 Verbs and livelihood archetypes, before the engine rework|W-70]]), which
touches every row.

## Why

Zach, 22 Nov: "I think we should make attempting something a more generalized system, so failures always have to be more informative
and give in-engine knowledge as well as instruction. And maybe be more informative the more times they fail etc. if they fail in
different ways. Because I think learning etc. should be relatively forgiving for learning the minimal / awareness of new things, e.g
maybe even just attending to an item could make them aware of a craft or option to do with it, but some should be basic while others
require more mastery. I imagine the familiarity multipliers probably shouldn't be the same for everything but depend on the
difficulty of a craft? Some if anyone tries they can probably do, while others require deep practice or teaching?"

The crafts evaluation ([[W-74 The crafts and techniques design evaluated|W-74]]) found deep chains never run, specialists barely exist (94 of 132 crafts basic), and agents learn recipes
only from refusals they must write down themselves.

## Alternatives considered

- **Keep one try rule and the three curves:** simple, but a salter and a smith learn alike, and no craft needs a teacher.
- **A difficulty number per craft:** finer but harder to calibrate and read; classes with per-craft overrides keep both.
- **Reveal the whole recipe on the first failure:** forgiving, but removes learning by trying; the ordered lessons reveal one piece at
  a time.

## Open questions

1. May aware try every craft (proposed, at a cost), or only those marked tryable untaught?
2. Does the class set the skill range, or each craft?
3. The crude result for simple and practised crafts: wanted?
4. Lessons kept in `Mind.know` by the engine (proposed), beside what the agent writes?
5. Attention as the one way of learning by looking, with watch its costly form (also [[Q-81 Knowledge in their own words|Q-81]], question 3)?
6. The life clock: decided ([[D2-267 Practice and learning are set at a 64-day lifespan and scaled with a…|D2-267]]): practice set at a 64-day lifespan and scaled.
7. Attention spent in units (§4), with `watch` folded in?
8. Teaching toward the teacher's peak (§6), faster at their peak?
9. Continuous skill with discrete capability points, per-craft curve shapes (§7)?
10. Transfer through six to eight underlying skills (§8); inherited aptitude as an off-by-default knob?

## Affects

`cybertron2/engine/data.py` (TRY, SKILL, the craft rows' class, lessons and sentences), `knowledge.py` (levels, rising, cards,
crafts_lines), `verbs.py` (make, the try's outcome and lines), `perceive.py` (attention), `prompt.py` (the craft line showing lessons),
the world makers (seeded levels).

## History

- 23 Nov 2026: accepted in part: [[D2-326 Practice alone can bring a person to known in any craft|D2-326]] (Practice alone can bring a person to known in any craft (so new crafts can emerg).
- 23 Nov 2026: accepted in part: [[D2-307 Learning is scaled with the lifespan in every part|D2-307]] (Learning is scaled with the lifespan in every part (each increment times 64 / li).
- **22 Nov 2026:** §4 (attention spent in units), §6 (teaching from peak), §7 (skill profiles and capability points), §8 (transfer through underlying skills; inherited aptitude) added as exploration, from the day's conversation (Zach quoted in each), under the rule that every explored idea is written down ([[D2-277 Every idea explored in conversation is written down before moving on|D2-277]]).

- **22 Nov 2026:** drafted by 37.2 at Zach's request (quoted under Why; "you can continue the learning times agent"), from
  docs/review/37_growth/02zzzh_hunt_fish/learning_times.md (18 crafts, the classes, the parameters, the life clock, failure lines;
  sources mostly from search summaries, page fetches blocked) and the crafts evaluation.

## Sources

docs/review/37_growth/02zzzh_hunt_fish/learning_times.md and crafts_evaluation.md; `cybertron2/engine/data.py` (TRY, SKILL),
`knowledge.py`; proposals/knowledge_in_their_own_words.md, hunt_fish_materials.md.
