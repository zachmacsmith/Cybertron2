# Proposal: crops grow by the season; "can" apart from "works"; what a crop shows

**Status:** accepted: D4-106 (8 Nov; built). **Owner:** 37.4. **Affects:** engine/farm.py (sowing, the night, reaping, hoeing and ploughing),
signs.py (CROP, FIELD), data.py (CROPS, ITEMS, TECHNIQUES hay and salt pan), lore.py, capacity/rotation.py;
spec/core/processes.md, spec/environment (crops), information/signs.md.

## Summary

Zach, 8 Nov: "Surely they should be able to sow whenever they want just the farming performance varies? The 'can' should be
decoupled from the 'works'." And: "for seeds that grow badly, it should be clear from signs ... crops should DEFINITELY give signs."

The proposal has four parts:
1. **The engine refuses an act only when it is physically impossible or one has no idea how to do it.** Everything else is done,
   costs its units, and works well or badly by its conditions.
2. **Crops grow by the season.** Each crop has a growth rate in each season. A crop ripens when its growth adds up. What it gives
   depends on how good its growing was. A tender crop loses a share of itself to each cold night. Seed in ground too cold to sprout
   lies there and is slowly lost. The sowing windows of D4-105 stop being rules: they come out of the growth, and families know them
   as lore.
3. **A crop can be removed:** reaped green (a green crop: little food, good fodder) or turned under with a hoe or plough.
4. **A crop shows what is happening to it,** by bundles of signs through the noticing rule. Very bad states are plain to anyone
   working it or passing it; subtle ones need a close look or a farmer's eye.

## 1. Can against works, across the engine

| Refused (stays) | Why |
|---|---|
| no seed, no tool where one is needed, no oxen to plough | one cannot |
| the plot already holds another crop | there is no room |
| sowing thicker than the ground takes | there is no room |
| no soil: water, rock, built ground | there is nothing to sow into |
| a craft one has no idea of (aware); with a rough idea one may try (D2-93) | one cannot |
| nothing there: reaping a field with nothing in it, or a crop that has failed | a fact |

| Done, and works by conditions (was refused) | Now |
|---|---|
| sowing out of its season (D4-103 refused it; D4-105 made it silently give nothing) | grows by the season (part 2) |
| reaping before ripe | a green crop (part 3) |
| weeding a clean crop, or one past weeding | done, gains nothing; the result says so |
| cutting hay out of summer | a yield by season: spring 0.5, summer 1.0, autumn 0.3, winter 0 |
| a salt pan out of summer | spring 0.4, summer 1.0, autumn 0.2, winter 0 |
| sowing turf that has not been cleared (meadow, pasture, heath, scrub) | see part 2: possible and very poor; clearing stays the way to make a field |

Zach, on question 1 of 8 Nov: "yes. But if things are very bad, they should give clear signs, unless we purposefully want it to be
hard to figure out." So a world may lower a bundle's plainness to make a thing hard to read: that is a scenario setting, never the
default.

## 2. Growth by the season

**Data.** Each CROPS row gains:
- `growth`: a rate in each season;
- `hardy`: as now;
- for winter grain, `needs_winter`.

First values (calibrate):

| Crop | Spring | Summer | Autumn | Winter | Also |
|---|---|---|---|---|---|
| barley (grain) | 1.0 | 1.0 | 0.5 | 0 | tender |
| beans (legumes) | 0.8 | 1.0 | 0.4 | 0 | tender |
| rye (winter grain) | 1.0 | 1.0 | 0.6 | 0.1 | hardy; needs a winter, else it gives 0.4 |

**The night step** (farm.night, one pure function `grow_night(c, season, cold)` that the capacity model also calls):
1. **Seed lying:**
   - While the rate is 0, or the night is cold, sown seed has not come up.
   - It loses `lie_loss` (calibrate: 0.04) of itself a night, to birds and rot.
   - It comes up on the first night the rate is above 0, with what is left.
2. **Growing:** `progress += rate[season] / grow_days(crop)`. The crop ripens at 1. Its quality is the mean rate over the nights it
   grew.
3. **The cold:**
   - A tender crop loses `frost_loss` (0.15) of its standing area each winter or cold night.
   - So a late barley thins over a few nights rather than dying at once; most of it is gone within about a week.
   - A hardy crop does not lose area.
4. **Ripe:** what it gives = base (seed, broken soil, soil, ground, skill, crop factor: as now) × quality × weeding × area left. For
   winter grain that met no winter, also × 0.4.

**What comes out of it** (32-day year: barley 8 days to grow, beans 5, rye 11):
- **Barley.**
  - Sown in spring: ripe in summer, quality 1.0.
  - Sown at the end of summer: it grows into autumn, ripens late and smaller (about 0.7).
  - Sown in autumn: it does not finish before the winter, and the cold takes it.
  - Sown in winter: the seed lies until spring and about half is lost.
- **Rye.**
  - Sown in autumn: it grows slowly, stands through the winter and ripens in spring, at quality about 0.7 and with its winter.
  - Sown in spring: it ripens quickly but with no winter, so it gives 0.4.
- **Beans:** their best is summer. They can still be grown twice a year in a short year.

So the windows are an optimum, not a gate. The sowing lore (D4-105) stays and is worded as what works best: "Sow barley in spring,
rye in autumn, beans in spring or summer; late barley comes up poor and the winter takes it; rye wants a winter."

**Sowing turf without clearing** (Zach's question 3: "what would make sense here?"):
- **What happens in reality:** broadcast seed on standing grass mostly feeds the birds, and what sprouts is smothered by the sward.
  Clearing (breaking the turf and its roots) is what makes a field.
- **Recommendation:** allow it on open ground with turf, at 0.1 of a field's yield. The ground stays meadow and its grazing is
  untouched. Refuse it only where there is no soil.
- **Why:** it keeps the rule of part 1, and it makes the value of clearing something one can learn by trying.
- **Cost:** a crop record on a non-field parcel. The field's holdings and shares (D2-172) do not apply there: the sower's claim, as
  on any parcel.
- **If this proves fiddly, the fallback** is to keep clearing as the only way to sow and say so in the refusal ("the turf has to be
  cleared before seed will take in it"). Under the line Zach drew, that is honest: knowing that is part of what everyone knows.

## 3. Removing a crop

| Act | What it does | Leaves |
|---|---|---|
| **Reap green** (reap before ripe) | Each plot cut gives `green crop`. Weight: the plot's ripe harvest × (0.3 + 0.7 × progress). Food 0.15 a unit (green ears roasted), fodder 0.8, spoils 0.2 a night (it heats if kept wet). The plot is free | the ground for resowing |
| **Turn it under** (hoe or plough over a standing crop) | destroys it; the soil gains a little (0.02 × its progress: green manure); the plot is broken and free | broken ground, ready for seed |
| **Ripe, reaped** | as now | stubble |

- **Green crop** is a new good (ITEMS). It names its kind when held ("green barley") through the item's tag (D4-68), so a store
  shows what it is. Beasts eat it from the holders' stores as they eat hay (farm.py's fodder).
- **Resowing a plot with seed lying in it** adds to the same crop, up to the ground's capacity, as sowing does now. A different crop
  needs the plot turned under first. The refusal says so: "there is barley sown in it; turn it under first to sow beans".
- **Will they sow twice by mistake?** Today: a plot of the same crop not yet ripe takes more seed up to its capacity, and a different
  crop is refused. With seed lying visibly (the signs below), a second sowing of the same seed is a choice to top it up, not a
  hidden waste.
- **D4-105's build is the worst of both.** A crop sown out of its window occupies the plot until its ripe day and blocks a resowing
  ("already has barley in it"). Part 3 removes that trap.

## 4. What a crop shows: every state and its signs

How people sense them: the noticing rule (D4-53, D4-75), never a chance on the row. A row gives its plainness (`own`), its sense,
its conditions, its scope and, where it is a farmer's judgement, a knack. The chance then comes from presence:
- working it: on the parcel, attending to one's work;
- passing it: on the day's route (layout.passed, D4-62);
- attending to it: the morning's close look;
- next door: a glimpse.

Plainness by severity (Zach: very bad states plain):
- **plain** (own about 1.0): near certain for anyone working it, likely passing, a glimpse from next door;
- **clear** (0.6 to 0.8): likely working it, sometimes passing;
- **subtle** (0.3 to 0.5, often a knack): working it or attending, mostly for those with the eye or the lore.

The doer of an act gets a touch line (the result line's own words, kind 1 of the guide). Others get sight and sound (kind 2).
Traces last a day or two (kind 3). Snow, frost and rain are conditions (kind 4).

| State | Sign (sense, plainness, scope) | Now |
|---|---|---|
| **Sowing today** | others: "X broadcasting seed across Y, the rooks following" (sight, clear); doer: none (the result says it) | new |
| **Seed lying, ground too cold** | sowing it, the doer: "the soil is cold and hard under your feet: nothing will sprout in this yet" (touch, plain, doer); anyone after 2 nights: "nothing has come up yet in Y, though it was sown N days ago" (sight, clear); "pigeons working the sown ground in Y" (sight, clear, when the loss is high) | new |
| **Coming up thin** (seed lost lying, or poor seed) | "only a scattering of barley has come up in Y, bare soil between" (sight, plain) | new |
| **Just through** | "a green haze on the soil" (exists: kept, own 0.5) | exists |
| **Growing well** | "up in green rows" (exists); "thick and even" (exists, knack sow) | exists |
| **Growing slowly** (a poor season: rate under 0.7) | "the barley in Y is short and pale for its age: it is slow to come on" (sight, clear; knack sow: plain) | new |
| **Late: will not finish before the winter** | exists ("will not ripen before the frosts come"): widened to any crop whose progress cannot reach 1 at its rates before the winter; plain for the knack, clear otherwise | widened |
| **Frost-hit** (a tender crop on a cold night) | next day: "the frost has blackened the tips of the barley in Y" (sight, plain, a trace of 2 days); as losses add: "half the barley in Y lies dead after the frosts" (sight, plain) | new (the full kill is an event today) |
| **Killed** | the frost event (exists); after: "the barley in Y is dead and black, nothing left standing" (sight, plain, lingering until turned under) | widened |
| **Rye without its winter** (`needs_winter`, progress over 0.5) | "the rye in Y has run up thin and is setting few ears" (sight, clear; knack sow: plain) | new |
| **Weeds** | thistle and dock (exists); clean (exists) | exists |
| **Flowering, heading** | beans in flower (exists); "ears filling" (exists) | exists |
| **Blight** | withering, spotted (exists); sour smell (exists) | exists |
| **Same crop twice** | exists | exists |
| **Ripe** | ready for the sickle (exists); birds at it (exists); "rub out hard in the hand" (exists, touch, knack); rain on it (exists); must be cut (exists) | exists |
| **Ripe but poor** (quality or area low) | touching it: "the ears in Y are light and thin: there will be little in them" (touch, clear, knack reap); seeing it: "the barley in Y stands sparse and short-eared" (sight, clear) | new |
| **Reaping a poor crop** | the doer: "the ears are light in your hand and thin in the grain" (touch, plain, doer; the result gives the quantity) | new |
| **Reaping green** | the doer: "the ears are soft and milky: it was not ready" (touch, plain, doer); others: "X cutting the barley green in Y" (sight, clear); a trace: "green swathes laid in Y, cut before their time" | new |
| **Holding green crop** | the store and hands show it by its name ("green barley"); spoiling: "the green barley in Z is heating and going sour" (smell, clear, when wet or more than 1 night old in a pile) | new |
| **Turned under** | others: "X turning the barley under in Y" (sight, clear; sound of hoes or the plough exists); a trace: "Y has been turned over, green stalks in the soil" | new |
| **Rotting** (ripe and not cut) | exists | exists |
| **Trampled, grazed** | herd signs (exist) | exists |

**The farmer's advantage:**
- Knack rows (sow, reap) read plainer for those practised at the craft (the eye: D4-75).
- The lore names the cause. A farmer reads "short and pale for its age" knowing it was sown late; someone without the lore sees only
  that it is short and pale.
- So signs show the state to everyone, and understanding it is what lore and practice give.

## Alternatives considered

- **Keep the windows as refusals (D4-103):** clean, but it tells everyone the rule and removes the lesson. Rejected by Zach.
- **Windows as silent failure (D4-105):**
  - all or nothing;
  - occupies the plot;
  - shown late.

  To be replaced by this.
- **Growth by the weather (warmth, a late frost, drought)** in place of the season: right in the end, and planned. Zach: "season for
  now. flag the second to come back to" (OPEN L-68).

## Open questions

1. Sowing turf at 0.1 (recommended), or clearing as the only way to a field?
2. Green crop's numbers: food 0.15, fodder 0.8, weight by progress. And should green crop dried become hay (a make, or simply its
   fodder kept: spoil 0 when dry)?
3. Should poor quality also show in the grain itself (lighter grain, keeping worse)? Not proposed: grain is grain once threshed.
4. Building order: growth and removal first (they fix the D4-105 trap), signs with them, hay and salt by season last.

## Affects and checks

- The capacity model's crop year calls `grow_night`, and its search over sowing days finds the best windows.
- CROPS `sow_seasons` goes; the lore text comes from the growth table.
- Tests:
  - the outcomes in part 2;
  - the removal acts;
  - each new sign through `perceive.chance_of` at the intended chances (working it, passing it, next door);
  - a bot run and its replay.

## History

- 8 Nov (later): **accepted and built (D4-106).** Zach: "Build this"; green crop dried becomes hay, "yes"; no quality in the
  threshed grain, "I agree". Built as proposed, with these changes found in building:
  - **Values:**
    - seed lying loses 8% a night (4% left winter-sown barley at 0.72, not about half);
    - frost takes 30% a night (15% let half-grown barley through a 6-night winter at 38%).
  - **Quality** leaves out a hardy crop's winter nights. Otherwise rye sown in autumn came out at 0.53, punished for its normal
    winter rest.
  - **Winter grain:**
    - it does not head until it has had 3 winter nights;
    - after a whole growing time without them, it heads at 0.4;
    - a single winter night no longer counts as a winter.
  - **Sowing results:** the result of a sowing no longer says when it will ripen or warn of the winter. The rules told that before;
    signs and lore carry it now.
  - **Plainness:** set through the noticing rule.
    - Working the field: 1.0 for all of them.
    - Passing it: 0.10 to 0.30 at the first values, so plain rows went to own 2.0 and clear rows to 1.2.
  - **A crop sown on a meadow** stands on the parcel as a field's would, outside the holdings of D2-172.
  - **Removal:** turning under goes at the hoe's pace (0.07 of a plot an act), like breaking ground.
  - **Not built:**
    - the sign of green crop heating in a store (it spoils at 0.2 a night; the sign needs a container bundle);
    - the trace of green swathes on the next day.

  Checks:
  - 384 tests;
  - two bot runs (Wenbridge and the valley, 32 days) replay with no mismatch;
  - the bots die as they did on the engine before phase 2.

  Capacity: the farming levels fall 10 to 30% on most worlds; Ferrybank and the valley rise, where late or winter sowings now give
  part of a crop.

- 8 Nov: proposed (37.4) from Zach's "the can should be decoupled from the works" and his answers of 8 Nov (1 yes, with clear signs
  when very bad; 2 by season for now, the weather flagged; 3 asked; 4 green crop, worth much less, its own signs, fodder).

## Sources

engine/farm.py, signs.py (CROP, FIELD), lore.py; guides/senses.md; DECISIONS D4-103, D4-105; OPEN L-68.
