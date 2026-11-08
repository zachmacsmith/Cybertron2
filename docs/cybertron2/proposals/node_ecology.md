# Proposal: ecology designed from the node outward

**Status:** discussion (8 Nov). Nothing decided, nothing built. **Owner:** 37.2 (the engine side with 37.4).

**Affects:**
- spec/environment/resources.md (wild stocks);
- spec/economy/production.md (losses to wildlife);
- spec/economy/livestock.md (beasts at risk);
- living_populations.md, wildlife.md, wild_plants.md, husbandry.md;
- engine data RESOURCES and TECHNIQUES; the generator's per-node reservoir.

**Model:** [02zp_ecosystem_models/node/](../../review/37_growth/02zp_ecosystem_models/node/). **Analysis:** 02zp part three.

## Summary

Zach, 8 Nov: "maybe we should have designed everything first and foremost for the nodes. The land itself was supposed to be a
general way to make systems interact from outside ... but you seemed to focus everything on that without considering how it
actually fits into the society."

**Why the earlier design missed.** The ecology of 02zp parts one and two was designed and calibrated at regional scale: a 2,500 km²
window, decades, densities per km². A generated village holds about 0.55 km² (fields 0.3, wood 0.1, pasture 0.1), so four villages
touch about 0.1% of that land. In a village's 10 ha wood, real densities give 0.8 red deer, 1.5 roe, 0.4 boar, and 0.002 wolves.

**The proposal: design from the node outward.**
1. The node's parcels carry what people can change in days to a season.
2. The land around each node is a reservoir that refills the parcels and sends visitors as events.
3. The regional web only sets each reservoir's size, swings and visit odds.
4. Every element must pass a relevance test: it moves a household's food or work by about 10% in some year or under some choice.

**The model's first answer:** at village scale the land matters less as food than as **a threat to crops, stores and beasts**, and
as **rights over what may be taken**.

## The scaling principle (an assumption; the year-length question 37.4 has put to Zach)

- **Time:** an engine year of Y days stands for a real year, so one engine day is 365/Y real days, for the land and for people alike.
- **Food:** one engine food is 365/Y real person-days of food (11.4 at Y = 32). Animals and harvests count in food at their real
  content × Y/365: a hare 0.18, a roe 1.1, a red deer 3.9, a cow 12.
- **Work:** returns (food per unit of work) keep their real ratios; a unit is a sixth of an engine day.
- **Against the engine now:**
  - fields come out about right (48 net food a plot-year against about 90 real-scaled);
  - a slaughtered cow (60 meat, 90 food) is about 7× generous;
  - the forage stock is about 2 to 3× generous;
  - the game stock is about 150× generous.

## What the model found (02zp part three)

**Method:**
- villages from five generated worlds (settled lowland and frontier, fen, upland, plain, sand country), with their own parcels and
  the land within 5 km;
- 12 people;
- three kinds of year: normal, a mast year, and the bust year after it with a hard winter;
- five household choices: farmers only, mixed, hard hunters, guarded, and the lord's forest.

**Each element as a share of the village's food need for a year** (median, with the worst case in brackets):

| Element | Farmers | Mixed | Hunters | Guarded | Relevant? |
|---|---|---|---|---|---|
| hazel nuts | +1% | +3% (+8%) | +3% (+8%) | +3% | as a season (about 11% of autumn need) |
| fruit, fungi, roots | under 1% | 2% | 2% | 2% | no (health, not food) |
| hares | 0 | +1% | +2% | +1% | no |
| deer and boar hunted | 0 | +1% | +3% (+8%) | +1% | as a windfall and a right, not as food |
| fish and eels | 0 | under 1% (+2%) | +3% | +2% | where there is water; the eel run in autumn |
| **boar in the crops** | **−19% (−52%)** | −19% | −19% | **−4% (−10%)** | **yes** |
| deer in the crops | −5% (−8%) | −5% | −5% | −3% | yes, with the others |
| pigeons and birds | −6% | −6% | −6% | −4% | yes, with the others |
| rats in the stores | −5% | −5% | −5% | −2% | yes, with the others |
| wolves at the beasts | −0.1% | | | 0 | not as food; as danger |

**By world** (mixed households, normal year; losses after a mast year in brackets):

| World | Wild food | Losses |
|---|---|---|
| frontier | 11% | 37% (69%) |
| fen | 9% | 38% (71%) |
| upland | 10% | 24% (37%) |
| plain | 9% | 29% (49%) |
| sand country | 7% | 16% (17%) |

**What it means:**
- **Guarding** (night watch in the ripening weeks, children scaring birds, cats, folding beasts) costs about 4% of the village's work
  and cuts losses about four-fold.
- **The damage figures are first values and probably high.** Real boar damage is usually 1–10% of crops near woods, and 20–50% only
  locally in bad years. Even at a third of these figures, losses pass the test and wild food does not.

## The proposal

**1. Parcel stocks people can change** (on the year clock, with real yields and seasons; the clock as above):
- nuts and mast in autumn (they keep), fruit in late summer, greens in spring;
- hares (and rabbits as a warren pack);
- fish, and eels with their autumn run;
- fowl on wet parcels in winter;
- coppice and hay (built).

All as stocks with seasons (the `periodic` rule, D4-104) and real yields. Together they give about a tenth of a village's food, most
of it in autumn.

**2. A reservoir per node,** written by the generator. It is the land within about 5 km, by ecosystem: wood, heath, wetland, water.
It sets three things:
- **how fast** the node's parcels refill: a copse joined to big woods refills in a season, an isolated one does not;
- **the odds of visitors:**
  - a red deer group or roe in the wood;
  - a boar sounder in the crops, worst in the bust year after a mast year, and near big woods;
  - deer and pigeons in young crops;
  - wolves at the fold in a hard winter near a large wood;
  - the eel run and winter flocks;
- **what eras and history change slowly:** wolves gone a generation ago, a wood cleared.

**3. Visitors as events on parcels,** with signs: tracks and rooting before a raid; a sounder seen at the wood's edge; howling. Each
has a loss if not met.

**4. People's levers,** each a technique or a work:
- **watch a field by night,** at a unit cost;
- **scare birds** (children's work, wildlife.md §11);
- **fence or hedge** (built fences, D4-114);
- **keep dogs,** keep cats, raise stores on staddles;
- **fold the beasts;**
- **hunt or trap the raiders,** where rights allow;
- **keep** a warren, a dovecote or a fishpond.

**5. Rights:** who may take deer and boar (D2-194).
- **The forest law's conflict is the strongest social lever the ecology gives:** the lord's deer and boar eat the villagers' crops,
  and the villagers may not kill them. It was historically the sharpest grievance about wildlife.

**6. The regional web stays offline.** It sets each reservoir's size, its swings by year and era, and its visit odds. Long cheap runs
can use it directly.

**7. Relevance test before building anything:** each element must move some household's food or work by about 10%.

## Why

- **It fits the society:** the elements that pass the test are the ones people must act on together.
  - Watching fields is collective action: who sits up, who pays.
  - Fencing and hedging is shared work.
  - Stores need guarding.
  - The lord's game against the villagers' crops is a dispute over rights.
- **Wild food stays a supplement,** as in reality. That protects scenario_design §1 (an open forest makes everyone self-sufficient
  and the society inert), and its autumn timing gives storage its value.
- **Variation by year** (mast, bust, hard winter) doubles losses in bad years. That gives reasons for storing, lending and insurance
  between villages, and since weather is shared nearby (D4-109), it tests whether they can insure each other.

## Alternatives considered

- **The regional web live** (02zp part two): rejected for the live engine. The society cannot affect it, and its timescales exceed a
  run.
- **Wild food as a main food:** rejected. Real yields at village scale are about 10%, and anything more makes agents self-sufficient.
- **No ecology beyond stocks:** loses the threats, which are the relevant part.

## Open questions (for Zach)

1. Design the ecology from the node outward, as above, with the regional web offline?
2. The scaling principle: one engine food is 365/Y real person-days, with animals and harvests at real content × Y/365. This is part
   of the year-length question with 37.4.
3. Losses to wildlife (boar, deer, birds, rats, wolves) as the first ecology to build, with watch, scaring, fencing, cats, dogs and
   folding as the levers?
4. Forest rights: should a world be able to make deer and boar the lord's, so that crop damage becomes a dispute?
5. Recalibrate wild food to real yields (about a tenth of need, mostly in autumn) and game to real counts?

## History

- 8 Nov: proposed after Zach's point that the ecology was designed for the land, not for the nodes. First model at village scale (02zp
  part three).
- 8 Nov: the kinds themselves (layered rules, signs, lore, lags mostly inside a year) are designed in
  [wild_systems.md](wild_systems.md), which builds on this proposal's scale, coarse layer and groups.

## Sources

- 02zp parts one to three; generated worlds (the generator on `climate-calibration`, 5ef36fe);
- engine data (PHYSICS farming, TECHNIQUES, HERDS);
- wildlife.md (D2-192 to D2-196);
- forest law (Rackham; Young, *The Royal Forests of Medieval England*);
- crop damage by wild boar in Europe (approximate).
