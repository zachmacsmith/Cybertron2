# The building clock: making durable things at their real share of a year, and what has to come with it

**Status:** accepted in principle: D2-276 (22 Nov 2026); D2-275 (a unit is 2 hours). Staging, factor and companions open.
**Owner:** 37.2; buildings, rooms and the cost code are 37.4's, named on any merge. **Thread:** fishing, hunting and their materials
(W-73); the timber economy (W-76) takes builders and felling further.

## Summary

What ends a thing's life decides the clock it is made on. Things used up in one go or a handful of uses cost real hours; capital
(buildings, works, gear, tools) costs real hours times about 1/7, its life on the same factor; materials stay real. Today the engine's
prices are uneven: gear costs about three times its real share of a year, light works a twentieth to a fiftieth of real hours. The
rule makes works dearer and gear cheaper; to keep villages building, it comes in stages with builders as a trade, cheaper ways to
protect crops than fencing whole fields, and clearing a plot at a time.

## Where the factor comes from

A unit of work is 2 hours (D2-275); people work 7, 6 and 5 units a day by season with no rest days, about 192 units (384 hours) a
world year. A real working year is about 2,700 hours (about 300 days of about 9 hours; historians' estimates of a medieval peasant's
year run from about 1,600 to 3,000). A real share of a year is therefore about 384 / 2,700, about **1/7**; the honest range is about
1/4 to 1/7. (1/11 is the calendar, right for durations, not for work.) The factor is worked out from each world's own numbers and is
one named lever (D2-259). Engine days are long (12 to 14 hours at 2 hours a unit, every day); whether some days should be rest days is
left open below.

## What moves (building_clock.md)

| What | Now (units) | Under the rule |
|---|---|---|
| wood fence round a 2 ha field (its yearly mend) | 10 (2.5) | about 47 to 70 (12) |
| small timber room | 6 | 20 to 32 |
| stone cellar | 6 | 16 to 28 |
| medium timber room | 15 | 32 to 59 |
| small wattle room | 6 | 12 to 24 (and made of withies, posts, daub and thatch: below) |
| dry-stone wall | 20 | 37 to 75 |
| scrub clearing (a unit of size) | 10 | 16 to 40 |
| a weir section | 16 | 1 to 3 (7 to 22 if sized to a large river's take) |
| a net | about 30 | 2 to 3, plus its 1 kg of cord (8 units from flax, 25 wild) |
| oven, smoke racks, hearth | 12, 2, 3 | 2 to 3, about 1, about 1 |
| traps, hurdles, creels, baskets, chests, barrels, tools, weapons | various | a 1-unit floor, or batches |
| stone rooms, halls, millstones, water wheel, vault | | little change |

**Is a house still worth it?** Sleeping out costs 0.5 more food a night (1 on a cold night), a camp 0.2 to 0.5, a tent 0.2 to 0.4;
a household of four with no house eats about 2 food more a night, about 60 a world year, against a small timber room's 20 to 32 units
(about 30 to 70 food of work forgone): paid back in half a year to a year. A house stays worth it, no longer trivial.

**Will they build?** About two thirds of all gathering in the runs was the fallback filling leftover units, so there is labour to
redirect; but investment is crowded out by the day's needs (the river run's weir asked for three times and never begun; smoke racks
not built for want of one unit). Hence the stages and companions.

## The stages

1. **New gear written on the rule from the start** (it is not yet in the data): nets about 3 units plus cord, a line of 6 traps about
   2, hurdles about 7 a unit (hunt_fish_materials.md).
2. **The companions, before any work is raised:**
   - **Builders as a trade:** a builder's skill cuts the units a building takes (to about half at master) and sets its soundness: a
     building's craftsmanship sets how slowly it wears and how seldom it breaks, beside its structure and finish tier (plain, fine,
     rich, grand). The timber economy (W-76) carries the trade further.
   - **Cheaper ways to protect crops than fencing a whole field:** medieval fields were mostly open; beasts were kept off by herding
     (children or a shepherd: the household's order to herd exists), small hurdle folds moved about, dead hedges of cut thorn (cheap,
     rough), ditches and banks, living hedges grown over years. A fence priced by its length, so a small close costs less than a field.
   - **Clearing a plot at a time** (L-153): today a parcel becomes a field only when all its clearing is done; real assarting was
     piecemeal, each cleared plot sown while the next is cleared.
3. **Works raised in stages** (D2-281): from today's (about 1/40 of real hours) to about 1/15, read with bots and a short live run: does building still happen; then to the target of about 1/7. (A smaller factor is cheaper: at 1/7 a cottage of about 500 real hours costs about 36 units, at 1/4 about 63.)
4. Timber and stone in kilograms (D2-264) and carrying (W-71) **before** works are repriced: a timber is about 240 kg, so a small
   room's 8 timber is about 65 loads on foot, which could dwarf the building work itself.
5. The weir sized to its take, then repriced; tool and plough lives (crude tool 20 to 70 uses, copper tool 70 to 200, plough 11 to 27
   plots; handcart and pack given lives); terracing; tests re-pinned; building read in a farm world against its null arm.

## Wattle, straw and clay

Wattle is woven rods (withies or hazel) daubed with mud or clay, dung and straw, on posts, with a thatched roof. The engine costs a
wattle room in timber (8, the same as a timber room) because withies did not exist. Proposed (storage.md): wattle 3 timber, 30
withies, straw, 6 units at today's scale; timber framing 14 timber, 2 stone, 10 withies, straw, a carpenter. **Straw** comes only from
reaping grain and rye (4.7 straw a plot reaped); 400 straw is about 85 plots, so straw's unit must be put in kilograms (D2-264) and a
thatch's need checked against a real roof (tonnes of long straw for a cottage, to source); **reeds** from a reed bed are the stronger,
longer-lasting thatch (benched with the fen, L-125). **Clay** does not exist as a good; the land knows clay soils and vales. Until
pottery, daub is mud and straw dug on the spot (work, no good); clay joins with pottery (crocks, ovens, daub, later bricks).

## Issues to handle in the build

- `verbs.cost` truncates a recipe's units to a whole number, so under one unit is free: a 1-unit floor and batch recipes.
- Builders get several times the practice per house; a novice's skill makes a hall a world year's work.
- Households form about 20 times as often per world year as real, so a growing village spends 2 to 4% of its labour on cottages.
- Code: a `capital` clock and one conversion in `engine/clocks.py`, data rows holding real hours, departures named per row.

## Open questions

1. The factor: decided, a target of about 1/7, staged (D2-281).
2. Rest days: flagged with health, fatigue and illness (L-157).
3. The stages: decided (D2-281).
4. Builders' craftsmanship setting a building's wear and breaks, with the finish tiers?
5. Which cheaper crop protections first: herding by children, dead hedges, folds, fences by length?
6. Wattle of withies, posts, daub and thatch, and straw's unit and thatch's need in kilograms?

## History

- **22 Nov 2026:** written by 37.2 after Zach decided the unit (D2-275: "Let's do 2 hours") and the redesign (D2-276: "Let's try this
  redesign tbh. I think being more expensive makes sense"), from building_clock.md (the audit), storage.md (room costs), and the day's
  conversation: Zach's questions on 12-hour days, the fence at 47 units, a house's payback, builders as a trade ("push builders as a
  trade that are much faster at building, can build sturdier or better houses if more skilled (should buildings have craftsmanship at
  all that affects how much they break down or no?)"), wattle's materials, straw, clay, and clearing a plot at a time.
- **22 Nov 2026:** the staging corrected: an earlier note said "part way, to about 1/4", which is the dearer end; staged instead through about 1/15 to the target of about 1/7 (D2-281); rest days flagged (L-157).

## Sources

docs/review/37_growth/02zzzh_hunt_fish/building_clock.md, storage.md, withies_wood_materials.md; `cybertron2/engine/data.py`
(camping, heat, CLEARING, fences, rooms), `buildings.room_cost`, `verbs.cost`, `farm.py` (straw from reaping).
