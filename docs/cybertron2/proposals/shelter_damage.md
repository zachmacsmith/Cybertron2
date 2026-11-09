# Damage to shelter in levels, by structure and weather; camps as shelter that grows

**Status:** discussion (9 Nov). Nothing decided or built.
**Owner:** 37.2 (author; the rules would go in spec/economy/buildings.md and lodging.md, 37.2's). The night's breaks, buildings in
the engine and signs are 37.4's (proposals/building_risks.md, deferred, OPEN L-48; camps built out, L-47), so this goes to them.
**Affects:** spec/economy/buildings.md (D2-168's wear), lodging.md (camps, D2-68); the engine's night breaks (`night.py`,
`data.PHYSICS["breaks"]`), building condition (`world.CONDITION`), the wild layer's gaps (`wild.GAPS`, brief 2), signs.

## Summary

A building has one of five levels of condition instead of three (sound, damaged, ruined): **sound, worn, gappy, holed,
failing**. Each level costs warmth, lets damp into the store, and opens gaps only animals of that size or smaller pass, so a shut
wattle house that is merely worn still keeps the fox out, and only a holed one lets it in. Damage comes one level a night at most:
**minor wear** (to worn and gappy) often, from frost, wet and use; **serious damage** (to holed and failing) only from a cause: a
strong wind, a gale or a storm passing over, heavy snow on the roof, a flood on low ground, fire, a raid, or a building left worn
and unmended. **Wind and storms raise both, and serious damage most.** Wattle wears often and is mended cheaply; timber less;
stone hardly at all: that is why better houses are worth building. A **camp** is a lean-to round a fire: it keeps the rain and
wind off a little and keeps no animal out; its defence is its fire, a watcher, a dog and where its food is kept, and it can be
**built out** (more lean-tos, a windbreak, a thorn ring, a raised rack for food, tents pitched in it) toward a hut.

## The proposal

### 1. Levels of condition

| Level | What it is | Warmth (hearth or ring) | The store | Gaps when shut (wild.GAPS) | Sign |
|---|---|---|---|---|---|
| 4 sound | as built | full | as now | its structure's own (wattle and timber small, stone tiny) | |
| 3 worn | cracked daub, a draughty door, thin patches of thatch | -10% | as now | as sound | "a draught at the hearth; the daub cracked by the door" |
| 2 gappy | holes in the daub, thatch thin, a loose door | -20% | damp: spoils 1.5 times as fast | one size larger: small kinds through wattle and timber (rats, mice, the stoat), tiny through stone | "light through the wall by the bins" |
| 1 holed | a wall breached, the thatch open, the door broken | -40% | wet: spoils 3 times as fast, rain in | large: the fox and a dog | "rain coming in on the beds; a hole in the wall a fox could use" |
| 0 failing | roof or wall down | as outdoors | as outdoors | anything | "the roof half fallen in" |

Below failing it is ruined (as now: no shelter, its goods lie in the ruin). The present `condition` 2, 1, 0 maps to sound, holed and
ruined; worlds without the new levels behave as now.

### 2. How damage comes

Each night a building may drop **one** level. Two chances, both by structure, multiplied by the night's weather (the climate's
values at its node, D4-109, D4-111) and by its size (the square root of its floor in spaces over a cottage's: more roof and wall to
fail; calibrate):

| A night's chance of | wattle | timber | stone | camp |
|---|---|---|---|---|
| minor wear (sound to worn, worn to gappy), calm | 0.03 | 0.015 | 0.003 | 0.08 |
| serious damage (gappy to holed, holed to failing; or worn to holed in a storm), calm | 0.002 | 0.001 | 0.0002 | 0.02 |

| Weather that night | minor wear | serious damage |
|---|---|---|
| a frost | x2 | x1 |
| heavy rain | x1.5 | x1.5 |
| a strong wind | x3 | x5 |
| a gale, or a storm passing over (D4-110) | x6 | x20 |
| heavy snow lying on a roof (not stone) | x2 | x8 |
| a flood on low ground (height 0) | x1 | x20 (wattle and timber) |
| left unmended at worn or gappy for a season | x1 | x3 |

So a calm night barely touches a wattle house beyond a crack; a frosty week wears it to gappy; a gale can hole it in a night, and
a stone house rides out all but the worst. Fire, a raid's breaking in (conflict/raids.md) and a beast breaking out are already their
own causes and set the level they reach. All numbers `calibrate`: the test is that a wattle village through an ordinary winter
needs mending every week or two (cheap), and a gale shows which houses were worth building better.

### 3. Mending

Mending raises a building one level for each repair, at a cost by structure and size (D2-168's rule kept: materials and work in
proportion to floor): wattle, earth or daub and a unit (cheap, often); timber, timber and a unit; stone, stone and a unit, and a
mason's skill above holed. A gappy house mended before winter is the lesson; a holed house in a hard winter is the cost.

### 4. Camps

A camp (D2-68: a lean-to and a fire ring, 3 timber, sleeps 4, lasts about 10 nights) is the weakest shelter:

- **Shelter:** as now (the night's food and the cold as in lodging.md). Its life of about 10 nights stays; under §2 it wears fast
  and a gale is likely to flatten it (serious x20 on 0.02: a 40% chance a gale night).
- **Animals:** a camp's gaps are large from the start (as built on `ecology-raiders`): walls keep nothing out. Its defences are
  the **fire** (lit, it scares what fire scares, D2-198), **a watcher** (the night watch, D2-21), **a dog**, and **where the food
  is**: food in the camp's store is open to the fox, rats, a dog, a boar or a bear (brief 2's raid targets and brief 3's
  scavenging read it); food **hung from a tree** (a new way to keep goods at a camp: a rack or a bag on a branch, 1 unit) is out of
  reach of the ground's raiders, not of martens and birds; meat and a carcass at the camp draw scavengers by brief 3's rule.
- **People:** animals come for food, not for people; a sleeper is put at risk only where the danger rule already applies (a bear at
  its cache, a wounded boar, a rabid beast later), raised by food lying at the camp, no fire and no watch (calibrate, rare).
- **Built out** (L-47's camps, as fittings of the camp, each a build): more lean-tos (each 2 timber, sleeps 4 more, one fire still
  warms up to its fire's share); a **windbreak** (hurdles or brush, 1 timber and a unit: the cold's fall halved, wind wear halved);
  a **thorn ring** (brush cut round it, 2 units: keeps out the fox, a dog and a wolf on a night it is whole, wears like a fence); a
  **raised rack** for food (a pole frame, 1 timber: as hanging food); **tents pitched** in it (a tent carried and set at the camp
  sleeps its 2 as a tent does, under the camp's fire). A camp kept and built out for a season can be rebuilt as a wattle hut, which
  is how a camp turns into a place to live (the forays proposal, later).

## Why

- Zach (9 Nov): "what if we add more graduations of damage, especially as houses get larger and there are more types"; "I do
  imagine that wattle houses would get common damage pretty often which is why better houses are better"; "the storms or gales etc
  should significantly increase chances of serious damage and minor wear"; camps "shouldn't really keep anything out, should be easy
  for animals to break through".
- Brief 2's gate (02zx, OPEN Q-37 a): with two levels, a damaged house always had a fox-sized hole, and D2-168's break rate (0.12 a
  frosty night on wattle) damaged most houses in a week, so shutting up protected only until the first frost.

## Alternatives considered

- **Rarer breaks only:** fixes the fox but loses the point that wattle needs constant mending.
- **Damage per room or wall:** truer for large buildings, but a lot of state for a small gain; size as a multiplier is enough now.

## Open questions

1. The base rates and weather multipliers (calibrate against an ordinary winter and a gale, as §2 says).
2. Whether minor wear also lowers a house's beds' comfort or only its warmth and store.
3. Whether a camp's food hung from a tree is a fitting of the camp or a way of putting goods anywhere (a general "hang" at a place).

## History
- 9 Nov 2026: written by 37.2 at Zach's request, answering OPEN Q-37 (a), with camps (L-47) and animals at camps.

## Sources
proposals/building_risks.md, camps in spec/economy/lodging.md (D2-68, D4-49, D4-84, D4-92), buildings.md (D2-168); docs/review/37_growth/02zx
(brief 2's gate); branch `ecology-raiders` (`wild.GAPS`, `night.py` breaks); D2-21, D2-198, D4-109 to D4-111.
