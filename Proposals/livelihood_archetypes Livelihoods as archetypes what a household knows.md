---
id: docs/cybertron2/proposals/livelihood_archetypes.md
kind: proposal
state: "discussion (16 Nov 2026). Scoping only; nothing built (Zach: \"don't do this yet "
updated: "2026-11-16"
tags: [proposal, closed]
---
# Livelihoods as archetypes: what a household knows, seeded by how it lives

- **state**: discussion (16 Nov 2026). Scoping only; nothing built (Zach: "don't do this yet 
- **summary**: "Everyone knows" has grown into a catch-all: 72 crafts on every adult's standing instructions, most of them added by each brief so that nobody would lack them. The proposal is: - shrink it to the acts any adult of the time could do; - give each household a **livelihood archetype** (arable farmer, fi

## Text
# Livelihoods as archetypes: what a household knows, seeded by how it lives

**Status:** discussion (16 Nov 2026). Scoping only; nothing built (Zach: "don't do this yet but scope out").

**Owner:** 37.4.

**Touches:** the people generator (`engine/generate.py`, `landgen/write.py` TRADES), TECHNIQUES' `basic` flag (`engine/data.py`),
teaching and awareness ([[D2-153 The lifespan is a world setting that scales every part of a lif|D2-153]], `aware_of`), every world builder.

## Summary

"Everyone knows" has grown into a catch-all: 72 crafts on every adult's standing instructions, most of them added by each brief so
that nobody would lack them. The proposal is:
- shrink it to the acts any adult of the time could do;
- give each household a **livelihood archetype** (arable farmer, fisher, hunter-trapper, herder, miller and baker, salter, and so on),
  chosen by the generator from the place and the world's settings;
- each archetype has core crafts, common crafts and rare specialisms, drawn with a controllable spread.

Specialisms then sit in a few households and spread by teaching, marriage and watching, as the engine already allows.

## What is there now (measured 16 Nov, branch `ecology-water`)

- **The count:** TECHNIQUES has 131 rows; 93 are `basic`. Some of those are modifiers, not crafts (a range, a method, "how: fine").
  The standing-instructions line "Everyone knows" lists **72 crafts**, about 1,950 characters (about 490 tokens), on every adult's
  system prompt.
- **The growth:** the `basic` flag was on 55 rows on 2 Nov, 64 on 8 Nov, 79 on 9 Nov and 88 on 16 Nov. Each brief made its new crafts
  basic (the wild layer, brief 4's drying and salting, brief 5's weir and smokehouse) so that no world would forget them.
- **Seeded crafts:** the generator gives each household a line with a few crafts: the farming set (sow, reap, hoe, weed, milk, select
  seed) and trades chosen by the place (`landgen/write.py` TRADES: smith, mason, carpenter, trapper, miller). Others' crafts are
  `aware_of` ("you have seen the Hunts at it all your life"). There is no fisher, salter, smoker or weir-wright trade.
- **What it costs:**
  - **Attention.** In the lake run ([[W-50 The lake world's live run Meresby, 14 people, 14 days ($11.05)|W-50]]) everyone "knew" how to build a fish weir and a smokehouse, and nobody did. Both are one
    line each among 72.
  - **Equality.** Everyone is equally able at almost everything, so nobody is the village's fisher or salter, and there is less to
    trade, teach or depend on.
  - **Forgetting.** The flag protects against a builder forgetting to seed a craft, but it does so by giving everything to everyone.

## The 72, grouped by livelihood

| Group | In "Everyone knows" now | Proposed |
|---|---|---|
| **Universal** (any adult) | felling timber, gathering firewood, cutting young growth, gathering wild food, caring for a child, herding, fencing, gates (open, shut), gathering dung, repairing a building, clearing ground for building, a small room, beds, a camp, a fire ring, making a pack, a bedroll, a tent, a crude tool, a crude weapon, burying the dead, burning a carcass, a cairn, fishing by hand, drying meat over a fire, boiling acorns, slaughtering a beast, tallow lights, clappers, a horn, working the pests off a crop, guarding a field, shutting the hens and the store | keep basic (about 35) |
| **Arable farming** | clearing new ground, sowing broadcast, hoeing, weeding, manuring, reaping, burning the stubble, cutting hay, drying hay, bins, a granary floor, stalls, a woodshed | archetype **arable farmer** (core); most lowland villages |
| **Milling and baking** | grinding at a hand mill, a hand mill, milling at ox-turned millstones, milling at a water mill, dressing millstones, clearing the leat, relining an oven, baking at a hearth, baking in a stone oven | **miller** (a household by a mill site), **baker** (common in farming villages); a hearth loaf stays universal |
| **Fishing and water** | fishing with a rod, making a rod, smoke racks, smoking fish and meat, tending the smoke, salting fish, a fish weir | **fisher**, from understanding nets to building a full weir. Core: rod, wicker traps, salting fish. Common: nets, smoking. Specialist: building a weir, its sections and footing. |
| **Salt** | the saltmarsh pans, mending a brine pan, salting meat | **salter** (coast or spring); salting meat stays common to farmers and herders |
| **Hunting and trapping** | hunting the wild, setting snares | **hunter-trapper** (wood and frontier). Core: snares, the hunt. Specialist: stalking, drives, den work (non-basic now). |
| **Building** | an owl hole, a carved post | **carpenter** (rooms, halls, mills), **mason** (quarry, walls, footings) as now |

## The proposal

1. **A core of universal acts**, about 35 crafts, stays basic.
2. **Archetypes as data:** each archetype lists:
   - its crafts in three tiers: **core** (everyone in the household), **common** (most of its adults), **specialist** (one in a
     household, or one household in a district);
   - a skill range per tier;
   - where it fits: a river, the coast, a spring, fields by soil, wood, game, a mill site.
3. **The generator picks archetypes for each household** from the place and a world setting. For example, `livelihoods: {fisher:
   0.3, arable: 1.0}` gives the share of households near water that fish, with a spread: the draw of tiers and skill across people,
   seeded and controllable. A village by a river then has a fisher household or two. One of their adults may build weirs, the rest
   know nets and traps, and their neighbours have seen it done (`aware_of`).
4. **Spread is as built:**
   - teaching ([[D2-153 The lifespan is a world setting that scales every part of a lif|D2-153]], the hunt's over days in 4c);
   - marriage carrying a household's crafts;
   - watching (awareness, and trying an unknown craft at a novice's level, as now).
5. **A check in the generator's report:** every resource or work the world holds has someone within reach who knows how to use it.
   For example, a weir-worthy river with no fisher nearby is flagged. This is the guard against forgetting, in place of the `basic`
   flag (38.71, feature 8).
6. **Old worlds unchanged:** the archetypes are a world setting; worlds without it keep today's basics, so replays stay exact.

## Why

- **Zach (16 Nov):**
  - "what is everything in the 'everyone knows' has everything just ended up there? Could we instead group them by common types of
    work, and only give people the things that seem relevant with some (controllable) fluctuations";
  - "If a village is near a river and fishes, they get some range of fishing knowledge, from understanding basic nets to knowing how
    to build a full weir";
  - "something like archetypes would work well as defaults from common livelihoods when generating otherwise you might likely forget
    to give the relevant knowledge when making future runs".
- **The lake run ([[W-50 The lake world's live run Meresby, 14 people, 14 days ($11.05)|W-50]]):** the weir and the smokehouse were known by all and used by none.

## Alternatives considered

- **Keep everything basic and make the line shorter by grouping** (for example, "the work of the water: fishing, traps, smoking, the
  weir"). It saves attention, but everyone stays equally able: no specialists and no dependence.
- **Seed specialisms by hand in each world builder.** That is today's risk: a builder forgets, as the peoples worlds and the water
  worlds both did with other settings (38.70, 38.71).

## Open questions

1. The exact universal core: in particular slaughtering, drying meat, a hearth loaf, fishing by hand.
2. Whether a craft one does not know can still be tried at a novice's level (it can now), or only one one is aware of.
3. The archetypes' list and tiers. Proposed first: arable farmer, herder (dairy, hay, harness), miller, baker, fisher, salter,
   hunter-trapper, carpenter, mason, smith.
4. ~~Whether households carry two archetypes~~ Answered (Zach, 16 Nov): yes, a household can carry two livelihoods (a farmer who fishes); how often is to calibrate.
5. How children learn their household's crafts by growing up in it (now: from the line at coming of age).

6. Individuals with their own specialisms (Zach, 16 Nov): "certain individuals might know specific skills, e.g. especially if they came from another household": one who married in or was taken in brings the crafts of the household they grew up in, and a few individuals carry a specialism of their own.

## Affects

- engine/generate.py (lines' crafts), landgen/write.py (TRADES), engine/data.py (`basic`), the world builders (make_peoples,
  make_water_worlds, make_wild_region), the generator's report.

## History

- **16 Nov 2026:** scoped at Zach's request after the lake run.
  - Counted the basics and their growth (55 on 2 Nov to 93 now; 72 crafts on the line).
  - Grouped them by livelihood, and proposed archetypes with tiers, a spread, and a check in the generator's report.
  - Nothing built.
- **16 Nov 2026 (later):** Zach's answers: households can carry two livelihoods; individuals may know specific skills, especially those from another household. Open question 4 answered, a sixth added.

## Sources

- The lake run, runs/water_lake_r1 ([[W-50 The lake world's live run Meresby, 14 people, 14 days ($11.05)|W-50]]); engine/data.py, engine/generate.py, landgen/write.py.
- 38.71 (features 4 and 8).
- [[D2-153 The lifespan is a world setting that scales every part of a lif|D2-153]].

*Current as of 16 Nov 2026.*

