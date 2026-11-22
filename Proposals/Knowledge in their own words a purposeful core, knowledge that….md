---
id: docs/cybertron2/proposals/knowledge_in_their_own_words.md
kind: proposal
updated: "2026-11-22"
---
# Knowledge in their own words: a purposeful core, knowledge that differs by person, memory that grows, and passing it on

*proposal · discussion (22 Nov 2026). Nothing decided, nothing built. · `docs/cybertron2/proposals/knowledge_in_their_own_words.md`*

> Today every agent's system prompt tells them about 4,400 words of how the world works (rules, crafts, 37 verbs), mostly the mechanics built first, while they hold about 600 to 1,000 words of their own. Proposed: a **short, purposeful core** told to all (only what cannot be learnt by living); **knowl


**Status:** discussion (22 Nov 2026). Nothing decided, nothing built.
**Owner:** 37.2 (the content: lore, seeded knowledge, the worlds); the prompt, memory and knowledge core are 37.4's, named on any
merge. **Related:** the verbs and livelihood archetypes ([[W-70 Verbs and livelihood archetypes, before the engine rework|W-70]], [[D2-243 The verbs and the livelihood archetypes are reshaped first, as their…|D2-243]]), the verb list ([[Q-27 Keep the 38 built verbs, or fold them back to about 22 to 24|Q-27]]), how much seeded memory each livelihood
starts with ([[L-141 How much seeded memory each livelihood starts with|L-141]]), the crafts evaluation ([[W-74 The crafts and techniques design evaluated|W-74]]), the fishing and hunting network ([[W-73 Fishing, hunting and their materials developed together|W-73]]).

## Summary

Today every agent's system prompt tells them about 4,400 words of how the world works (rules, crafts, 37 verbs), mostly the
mechanics built first, while they hold about 600 to 1,000 words of their own. Proposed: a **short, purposeful core** told to all
(only what cannot be learnt by living); **knowledge that differs by person** (crafts, recipes, verbs, lore, seeded by household and
livelihood, learnt, taught, forgotten); **a long-term memory that grows** a place each stretch, in their own words; **attention as
the way of learning by observation**; and **passing it on to children as a real challenge**, measured.

## What is there now (21-22 Nov, read from the code and rendered for one agent)

| Part | Size | Same for everyone? |
|---|---|---|
| System prompt: who you are, your people | about 180 words | no |
| System prompt: "How life works here" (the day, units, eating, a table of every food's value, fuel, work's food cost, fittings' wear, fading, buildings, ownership, learning, noticing) | about 960 words | yes |
| System prompt: crafts by level, then 37 verbs with arguments and notes (the gather line lists every method; make lists recipes by name only; build gives every building's costs) | about 3,400 words | mostly |
| Reply format | about 430 words | yes |
| **Their own memory**, rewritten each 3-day stretch ([[D4-61 An agent rewrites its one memory each stretch, within a length that…|D4-61]]) | 150 to 800 tokens by age (about 360 to 570 words for an adult); Haiku append mode: 150 words a stretch, the last six shown | own |
| **Kept for good** ([[D4-64 Lines kept for good, passed on through care, replacing customs|D4-64]]), word for word | 25 words a line; 4 places in childhood, 1 at coming of age, about 5 over adult life (about 10 lines, 250 words) | own |
| **Notes** | 8 of 150 words; titles shown, 2 opened a day, 1 pinned | own |

What the prompt does not say at all: the seasons and what they bring (runs, fowl, game), spoilage and keeping, how much one can
carry, set gear and lifting it, what goods are for. Those reach agents only by signs and refusals, or not at all. **The prompt
records the order things were built in, not a choice.**

**Passing on to children** exists: caring for a child takes a `pass` sentence that becomes the child's kept line ([[D4-64 Lines kept for good, passed on through care, replacing customs|D4-64]],
`life.care_gifts`). In three past runs: peoples world (pw1, 100 days) 24 entries in 417 care acts, about half a dozen distinct
sentences; wild region 7 entries, one sentence; the second lake run none in 7. Every sentence passed is identity and values ("We are
the Ashford folk: keep the kin together, the field sown and the store full"; "Keep the store full through winter, and our blood must
outlast every hard frost"); **none is how the world works**, which agents have no reason to pass when the prompt tells everyone. The 30-day river run passes more (crafts_evaluation, Part 5): 134 of 487 care acts passed a line, 21 of them about how the world works, one a false belief ("Middleham Water is fished out", kept from day 12 to 29 and passed to the child Hob). Memories fill 0.6 to 1.0 of their budgets; rules, recipes and prices are 6 to 16% of memory words but about a third of kept lines (155 of 481), mostly lessons from refusals.

**Learning by observation** is two mechanisms: `attend` (free; one thing seen in detail next morning; gives sight, not craft) and
`watch` (4 units beside someone; a rough idea of their craft). The **look-up** of a craft's card is used in 0.1 to 0.3% of replies.

## The proposal

### 1. The core: short and purposeful

Told to everyone, about 300 to 500 words, each line there because it cannot be discovered by living or because its absence would
make a run measure confusion rather than society:
- the shape of a day (morning plan, work, evening), units of work and that unused units are wasted;
- that everyone eats each night, hunger and starving, and death;
- how to reply (the format), how to speak and to whom;
- that one can learn, teach, remember, keep and forget; that what one knows is one's own and differs from others';
- that others hold things, and taking what is another's is a choice others may see.
Each line of the core carries a reason in the design (why it is told rather than learnt). Everything else moves to the knowledge
layer or is learnt.

### 2. Knowledge that differs by person

- **Crafts and recipes as items of knowledge**, at the levels that exist (aware, rough, capable, known; [[D4-24 The world grows by data, and agents explore and learn it|D4-24]], [[D4-33 Seeded knowledge of other lines' crafts is awareness, not skill|D4-33]]), redefined so
  that *aware* is knowing what a thing is for (and one may try by guessing), *rough* the main input, *capable* and *known* the full
  recipe with less waste (proposals/hunt_fish_materials.md legibility; [[W-74 The crafts and techniques design evaluated|W-74]]). Known recipes show their inputs where agents look
  (the craft list, the day's options), not in a look-up they do not use.
- **Verbs follow knowledge and stage:** a child does not see writing on monuments or founding a household; a verb appears when one
  can do it.
- **Lore,** such as when the eels run, which foods keep, when to sow rye, what a hard winter needs: seeded as starting memories in
  the person's own voice, by household and livelihood ([[L-141 How much seeded memory each livelihood starts with|L-141]], [[W-70 Verbs and livelihood archetypes, before the engine rework|W-70]]), each line read from the engine's own state (the run windows,
  the crop calendar, the stocks) so that it is never false at the start.
- **Uses of goods** known by familiarity: one's own livelihood's goods and their uses; others' only by name.

### 3. A long-term memory that grows

One kept place opens **each stretch** (3 days), instead of about five over a life, and a kept line may run to about 40 words: over
a 64-day life about 20 lines, roughly 800 words, all in their own words, beside the rewritten memory. A person may also rewrite a
kept line (to correct it) at the cost of the place it held. The places opened by care in childhood stay as they are.

### 4. Attention is how one learns by looking

- Attending to someone at their work for a day (free): one learns the craft exists, what it is for and what goes into it (to aware,
  towards rough).
- Attending to a finished thing (a trap, a net, a smokehouse): what it is made of.
- Working beside them (today's `watch`, a way of attending that costs units): a rough idea.
One mechanism, its depth set by the time given; `watch` becomes a form of attention.

### 5. Passing it on, as the challenge

- A carer's `pass`, lessons in a teacher's craft ([[D4-123 A lesson is in the teacher's craft|D4-123]]), `explain`, `teach` and attention are the channels. With world knowledge
  no longer told to all, what is passed decides what the next generation knows.
- The core says plainly that what one knows dies with one unless it is passed on; nothing tells them what to pass.
- Measured in every run: what is passed (identity, values, practical knowledge, places, warnings), how much of a parent's craft and
  lore reaches a child, what is lost or garbled across a generation.

### 6. The founders' starting knowledge, and passing it on as the challenge

**Who it is for:** the founders, the people alive when a world starts, and no one else. Children are born knowing none of it; they
have it only if someone passes it on, and how well that happens is part of the challenge (§5). (The mechanism exists: a world's
`customs` are lines kept for good, seeded to those alive at the start, `perceive.seed_knowledge`, [[D4-64 Lines kept for good, passed on through care, replacing customs|D4-64]].)

**What it is:** a **common set of knowledge** we decide is good to seed, so the founders start with a working understanding of how to
live in and act on the world, in their own voice: how the year goes and what each season brings; which foods keep and how; what
their household's crafts need and where those things are found; how knowledge is got (watching, trying, being taught) and lost (it
dies with you unless taught). Each line is read from the engine's own state where it states a fact (the run windows, the crop
calendar, the stocks), so it is true at the start; its length is set by the kept places (§3).

**Common sets by practice:** beside the base everyone shares, each practice has its own common set, and a founder starts with the
set of what they practise (their livelihood archetype, [[W-70 Verbs and livelihood archetypes, before the engine rework|W-70]]; how much each starts with, [[L-141 How much seeded memory each livelihood starts with|L-141]]). Examples:
- **fishers:** when the runs come and how long they last; which gear takes what (traps and the weir in a run, hands only in the
  shallows); how to keep a glut (smoke, salt) and what it needs; where withies and cord come from;
- **farmers:** the crops' calendar (when to sow wheat and rye, beans), what the soil needs, the harvest and its keeping;
- **hunters:** where game lies by season, which methods suit which beasts, how far to go and what can be carried back, dressing a
  kill;
- **herders, salters, smiths and others** likewise, each with what its practice knows best, including which of its techniques
  work best and when.
So a fisher knows fishing well and farming only as a neighbour sees it, and the reverse: knowledge differs by practice from the
first day, which is what makes asking, teaching and trading worth it. The sets are written once per practice and checked against
the engine (§2), and the archetypes decide which practices a world's households have.

**What may vary, as a parameter of a world:** the common set is the default; a world may vary parts of it as a culture, for
example a people that holds "what we know dies with us unless we teach it to our children" against one that does not, or one that
keeps its crafts within the household against one that shares them. Run side by side on the same land, these show what each does
to knowledge across generations. They keep to the scenario rule that goals are in-world aims, never scoring proxies
(`docs/scenario_design.md`): beliefs a people holds, not instructions to score. (Brief 5's worlds took "no seeded customs", [[Q-51 Brief 5 (river and water)|Q-51]];
that was a choice for those worlds, not a rule against it.)

## Why

Zach, 22 Nov ("we should also think of core sets of standard starting memories: e.g that you must pass on knowledge about the world
to your children or they will forget, or to remember and explore the mechanisms of the world etc. These themselves can be
experimental parameters to vary as different cultures"): "we should reconsider how much of this should be in everyone's system prompts compared to maybe a richer layer of
knowledge and recipes / crafts that learnt but more specialised and heterogeneous so not everyone knows ... the shared system prompt
should be as minimal as possible, with verbs and techniques varying based on what they know, but likely growing a larger portion of
space for them to keep their own knowledge of how the world works ... their memories should grow over time in their own words, from
experimentation and discovery etc, and then starting knowledge is just seeded starting memories that can be taught as lessons to new
children and passed on"; "basic stuff like eating food etc. maybe starting core, but this should be very purposeful. But then also
part of the challenge is passing on the information to children."

The live runs showed the cost of the present shape: agents told 37 verbs did not know the eels run in autumn (02zzy); the farmers'
lore line is cut at the 25-word cap; nothing practical has ever been passed to a child.

## Alternatives considered

- **Keep telling everything:** cheap and safe for calibration; leaves knowledge, specialisation and teaching with no work to do.
- **Tell nothing beyond the reply format:** the early days spent rediscovering physics; runs measure confusion.
- **A larger rewritten memory only:** weak models rewrite badly (the reason for Haiku's append mode, [[D4-61 An agent rewrites its one memory each stretch, within a length that…|D4-61]]); kept lines, word for
  word, hold knowledge better.

## Risks, and how they are measured

1. **Self-written knowledge is lossy and can be wrong** (the "fished out" belief spread from three bad nights, 02zzy). Realistic,
   but a starving village may then be the world or what they believe of it. **Every experiment on this has a paired arm with the
   knowledge told** (the null arm, scenario_design), and the evaluation reads written memories for errors.
2. **Weak models.** Haiku's memory is already handled apart; kept lines word for word should suit them better than rewriting.
3. **Cost moves:** a shorter system prompt saves tokens; larger memories and knowledge cards add them per person. Measured per run.
4. **Seeded knowledge must be true:** read from the engine's own state, never written by hand.

## Open questions

1. The core's lines: which, and the reason for each (a draft list to review)?
2. A kept place each stretch, and lines of about 40 words?
3. Attention as the one mechanism of observation, with `watch` as its costly form?
4. Verbs shown by knowledge and stage?
5. A told-knowledge arm beside every learnt-knowledge experiment?
6. Built with the verbs and archetypes rework ([[W-70 Verbs and livelihood archetypes, before the engine rework|W-70]]) and the verb list ([[Q-27 Keep the 38 built verbs, or fold them back to about 22 to 24|Q-27]]), or before it?
7. The founders' common starting knowledge: which lines, and which cultural variants (if any) to run first?

## Affects

`cybertron2/engine/prompt.py` (system_prompt, crafts_lines, the verbs' lines, REPLY_LINES), `memory.py` (KEPT, budget), `knowledge.py`
(levels, cards), `perceive.py` (attention), `life.py` (care_gifts), `verbs.py` (watch), the generator's people and lore, the world
makers.

## History

- 22 Nov 2026: accepted in part: [[D2-268 The founders' starting knowledge|D2-268]] (The founders' starting knowledge (founders_knowledge.md): seeded lines are ordin).
- 22 Nov 2026: accepted in part: [[D2-266 Knowledge in their own words|D2-266]] (Knowledge in their own words (proposals/knowledge_in_their_own_words.md), as ans).
- **22 Nov 2026:** §6 added: standard starting memories as culture, an experimental parameter (Zach, quoted under Why).
- **22 Nov 2026:** §6: common sets by practice added (Zach: "there will be different common sets eg different practitioners will start with more knowledge about their practice eg fishers know how to fish and stuff about which techniques are best etc compared to farmers or hunters. This connects with the archetypes sorta work").
- **22 Nov 2026:** §6 corrected after Zach: "I didn't mean all children were seeded with it on birth, just I meant for us deciding a common set of knowledge that is good to seed the founders so that they have a good understanding of how to interact with the world, with that they still need to pass it on, but how well they pass it on is itself part of the challenge." Now: a common set seeded to the founders only; children have it only if passed on; cultural variants are a parameter beside the default.
- **22 Nov 2026:** the crafts evaluation's memory measures added (02zzzh_hunt_fish/crafts_evaluation.md, Part 5).
- **22 Nov 2026:** drafted by 37.2 at Zach's request (quoted under Why; and "Yes" to writing it), with the system prompt rendered for
  one agent in the runs world (high arm), the memory limits read from `memory.py` and `data.py`, and the `pass` sentences counted in
  three published runs (pw1_opus_sonnet_r1, wild_region_s7, water_lake_r2).

## Sources

`cybertron2/engine/prompt.py`, `memory.py` (DEFAULTS, KEPT), `converse.py` (the 3-day stretch), `data.py` (notes), `life.py`
(care_gifts), `knowledge.py`; the dataset `zachmacsmith/cybertron2-runs` (responses.parquet of three runs); 02zzy, 02zzy2, 02zzz;
proposals/hunt_fish_materials.md, acts_on_owned_things.md, livelihood_archetypes.md.
