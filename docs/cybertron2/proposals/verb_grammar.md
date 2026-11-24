# A grammar of acting: a few universal verbs, the thing as the target, techniques as the how

**Status:** exploration (22 Nov 2026). Nothing decided, nothing built.
**Owner:** 37.2 (this exploration); the verbs and their registry are 37.4's (proposals/verbs.md, verb_modifiers.md). **Related:** the
verb list (OPEN Q-27), the verbs and livelihood archetypes (W-70, D2-243), acts on owned things (acts_on_owned_things.md, Q-80),
knowledge in their own words (Q-81), the crafts evaluation (W-74).

## Summary

The verb design's intent was a small grammar: a few verbs acting on objects, the how coming from technique rows as data (D4-24). It
holds where it was built (five verbs carry 80 to 95% of acts; `make` is data on one handler) and drifted elsewhere: overloaded verbs,
a place where a thing should be the target, social acts added one verb at a time, crafts with a process needing code. Explored here:
**a verb is the shape of an act; a technique is learnt knowledge of how; the agent names the technique and its target, and the verb
only when one technique has more than one shape.**

## What the evidence shows (crafts_evaluation.md, Part 5)

- 18 to 29 of the 38 verbs were used in nine runs; gather, work, take, move and give make 80 to 95% of all acts.
- `gather` covers taking from the land, setting traps and hunting; `work` about 30 kinds of work; agents used `work` for `make` crafts
  (27 refusals in two runs).
- Acts took places, not things: the set-for-lift confusion (about 40% of trap acts), the snares and herds taken from another.
- Social verbs grew one at a time (host, grant, revoke, join, admit, found, meet, come, write, erase), against the rule that a new verb
  needs Zach's yes (Q-27).

## The proposal (exploration)

1. **A verb is a shape:** what it takes (a held thing, a place, inputs, a person), what it costs, how long it lasts, what kind of
   outcome it gives. Examples: **set** (place a held thing where it works over time), **tend** (act on a placed thing: take its catch,
   reset it), **make** (inputs into outputs), **take**, **give**, **go**, **speak**, **change** (a door, a gap, a rule).
2. **A technique is the how:** what is set, what it catches, its rates, its lessons, its knowledge levels (trying_and_learning.md).
   A bespoke "set snare" verb would copy set's shape for every technique; that is why the grammar is wanted.
3. **The agent names the technique and the target;** the engine knows the technique's verb. The verb is named only when one technique
   has more than one shape (setting snares against tending them).
4. **The target is the thing,** by tag or a known name, defaulting to one's own when that is obvious (Q-80).
5. **Techniques may add modifiers,** declared in data, as the hunt's party options are now.
6. **A new verb only when an act has a new shape** the others cannot express; otherwise it is a technique.
7. **Social acts folded into a few shapes:** offer and agree (exchange, membership, partnership), let (host, grant, revoke, admit),
   join and leave, speak (say, tell, meet).
8. **Verbs follow knowledge and stage** (Q-81): a child does not see founding a household.

## Why

Zach, 22 Nov: "wasn't the point of verbs to unify into one system of the types of ways they could interact with the world? Is this
failing or was it a bad design in the first place or other things just not being built well for it ... I don't want every single way
of interacting to have a bespoke command? There should be some sort of composable expressible grammar for interacting with the world,
no?"; and "how is setting a snare technique under set verb different from just a bespoke setting a snare verb? ... if you do have to
say a verb just to say a technique what is the verb actually doing?"

## Open questions

1. The shapes: which eight to ten?
2. Naming the technique alone, the verb only when ambiguous?
3. The social acts folded into offer, let, join and speak?
4. Decided with the verb list (Q-27) and the archetypes rework (W-70), as one build (D2-266)?

## History

- 24 Nov 2026: accepted in part: D5-2 (The prompt's interface shows every act a person can take, each with a descriptio).
- 23 Nov 2026: accepted in part: D2-314 (The eleven act shapes are the verb list: go, gather, set, tend, make, work, buil).
- **22 Nov 2026:** written as exploration by 37.2 from the day's conversation (Zach quoted under Why), under D2-277 (every explored idea
  written down), with the crafts evaluation's counts.

## Sources

docs/review/37_growth/02zzzh_hunt_fish/crafts_evaluation.md; proposals/verbs.md (37.4's), acts_on_owned_things.md; the rendered
system prompt (37 verbs, 22 Nov).
