# Standing rules: how a household eats, and what it keeps back

**Status:** discussion (13 Nov 2026).

**Owner:** 37.4.

**Builds on:** D4-16 ("reflexes, fallbacks and policies come later"), D4-76 (the fallback each person sets), D4-65 and D4-66 (the
evening at the hearth).

## Summary

Each household has standing rules for the night's acts that now run on the engine's fixed policy, eating first. A person may have
their own as well. The rules hold until changed. Each evening shows them with what they did last night, and the evening is where
they are changed.

## The proposal

1. **A household default.** Every household starts with the engine's current policy written out as its rules:
   - eat from hands first, then the house's store, then other stores one may take from;
   - no-fire food first, then the most perishable;
   - eat raw when there is no fire;
   - full rations;
   - guests fed by the host.
2. **What the rules can say** (eating first; the rest later):
   - what is **kept back** and not eaten at night (seed grain, road food, a store for the winter), with an optional limit such as
     "unless someone is starving";
   - the **order** of eating ("meat, then grain");
   - whether to **eat raw** when there is no fire;
   - **rations** (full, or half when the store is under N days);
   - **who eats first** (children, a woman with child, those who worked);
   - **guests:** whether they are fed, with what, and how much (one's own people, strangers).
3. **A person's own defaults.** They govern what the person carries, and their own choices within the household's rules.
   - A person's rule may narrow the household's ("I won't eat the seed even if it runs out"), but not widen it.
   - To go against a household rule, a person acts by hand: they take from what is kept back. Others can notice the act, as with
     taking. A rule governs the habit and stops no one (the physical-possibility principle).
4. **Who sets them.** The head sets the household's rules, and members propose them at the evening. Anyone sets their own.
5. **Shown and changed at the evening.** The evening call shows the rules in force and what they did last night. For example: "By your
   rule the seed barley (40) was kept back; Joan and Herbert went hungry". A rule is changed by an act at the evening, which costs no
   units.
6. **Away from home.**
   - Setting off, or arriving at a camp, a person gets a road default: eat what they carry, perishables first, and keep back any road
     food named as such.
   - At a camp, the store follows the rules of the camp's household.
   - The road default is shown clearly at the evening where they arrive, so they can change it. Nights spent on the road have no
     evening call, so the default is also shown in the message where they set off.
7. **Later, the same mechanism for:**
   - the fire (keep it lit; firewood before timber, never charcoal);
   - the door (barred at night);
   - herds (where they graze, in at dusk, beasts never slaughtered).
   - Not for trade, trips, loans or taking people in: those are decisions whose trade-offs change, and they are what a run measures.

## Why

- **Zach (13 Nov):**
  - "Should each household have a standing rule about how food is distributed? ... the household could declare that when hungry,
    they eat from X etc. And this stays until changed";
  - "each household should have a default, but maybe an agent can have their own defaults as well. And yes, evening is when it is
    shown or changed. The standing rules can also decide if they give food to guests, what food, etc.";
  - "when they set off to travel or go to a new camp etc. they might get a default, but clearly shown to them in the evening if they
    want to change it".
- **The first peoples run (38.70):**
  - Ashford meant to keep its seed ("The Granary's 47 grain is our seed", Denis, day 27). It drew about 119 grain out of the granary
    by hand in 12 days to feed the house, lend to the Hales and pay for road food, then blamed rats.
  - Nothing let a household mark grain as seed. Seed and food are one good, and the night eats from any store one may take from.
- **Institutional memory.** A rule outlives a person's failing memory and passes to a youth at coming of age, which the aim and the
  memories of the dead did not (38.70b §8).

## Alternatives considered

- **Eating decided each evening, with no standing rule.** Rejected: every night needs a default anyway (people on the road, those
  not called, worlds without an evening, replies that forget). A nightly choice also adds noise to a routine act, and these models
  already drop routine things.
- **A separate "seed grain" good.** Narrower: it covers seed but not road food, rations or guests. It could be added inside this
  (keeping back seed as its own good).
- **The engine keeps seed back automatically.** Rejected: it would decide for them the very thing the benchmark tests.

## Open questions

1. Whether a member may change a household rule at all, or only the head; whether a rule may be set by agreement.
2. How the "unless starving" limit reads: a person starving, or anyone in the household.
3. Whether a person going against a kept-back rule is seen as taking (noticed, a mark against them) or only as a breach of custom.
4. The wording of the rules block at the evening, and its length in the prompt.
5. Whether rules carry into a household founded by a member (as customs do).

## Affects

- night.py (`_eat`, the order of stores and goods), evening.py (the rules block and the act), world.py (household and person
  rules), perceive.py (noticing a kept-back store taken from)
- spec/life (eating), spec/information (the evening)

## History

- **13 Nov 2026:** written from the conversation after the first peoples run (38.70), where Ashford ate its seed. Zach's shape:
  - a household default;
  - a person's own defaults;
  - guests covered;
  - shown and changed at the evening;
  - a road default on setting off.
  Mine:
  - a person's rules narrow the household's but do not widen them, and going against one is an act by hand;
  - eating built first.

## Sources

- docs/review/38_space_engine/70_peoples_run1.md and 70_peoples_run1_qualitative.md
- proposals/fallback.md (D4-76)
- DECISIONS D4-16, D4-65, D4-66

*Current as of 13 Nov 2026.*
