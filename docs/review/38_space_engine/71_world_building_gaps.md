# 38.71: From "a world with these properties" to a world: what went wrong building the peoples worlds

Session 37.4, 14 Nov 2026. Zach: "write up an analysis of the gaps / what didn't work well / what kind of features would have made the
generation part of world and people better from the kind of 'specify we want a world with these types of properties' to creating the
world". Sources: the build (38.69, D4-115 to D4-118, branch `peoples-worlds`), the run (38.70, 38.70b) and this session's conversation.

## 1. What was asked

Zach's properties for the peoples worlds (13 Nov):
- **Size:** a world much larger than the starting area, with "further, nicher areas with rare resources or different environments", so
  that a people must "balance off expanding and intensifying".
- **Home:** carrying capacity that "should comfortably support" the starting people "even just in their village".
- **People:**
  - about 10 to a people, "almost all of them early adults";
  - a youth takes its household's model.
- **Horizon:** long; lifespan 64.
- **Roads:** travel distances in whole days.
- **Design:** the worlds designed by hand ("you should be deciding the actual worlds"), realised with the land generator and places
  pinned.

Every item on that list is a property. The tools take mechanisms (positions, field sizes, a food share, birth dates, settings). I
translated one into the other by hand, and checked only part of the translation.

## 2. What went wrong, by layer

### 2.1 Settings: no base world

- **Four standard settings were left out:** `view: beliefs`, `evening`, `tags`, `ages`. make_peoples was copied from the generator's
  spec, not from a current builder. So the run used the old morning message, with no evening and no age line (38.70 flaw 5).
- **The cause:** every builder writes its own settings block, and nothing compares a world against the current standard.
- **Fixed since:** a run prints its settings at the start and warns when a standard one is off.

### 2.2 People: the cast did not fit the lifespan or the aim

- **The founders were too old.**
  - They were born 28 to 36 days before the run, and at lifespan 64 adulthood ends at day 64, so every founder turned elder between
    run days 28 and 36.
  - Nothing compared birth dates with the adult span and the run's length.
  - This decided the run.
- **The generator's people did not fit.** Its cast assumes one society, with kin, debts and memories across households. The peoples
  needed separate societies, so `cast()` was written by hand:
  - two houses of 5;
  - the four trades given equally;
  - a crude tool each (added only after the settle probe found nobody could clear ground);
  - `household_models`.
- **The aim did not carry.** It was a fixed kept line on the founders. Kept lines do not pass at coming of age, so no youth ever held
  the aim (38.70b §8).
- **My own errors here:**
  - a 64-day year nobody asked for (reversed);
  - "comfortable" set at 2× without asking (Zach accepted it afterwards).

### 2.3 Food and time: checked as a rate, failed as a timeline

- **The stores ran out before the first harvest.**
  - The homes were calibrated to feed about 2× their people at "worked", which is a rate over a year. They started with the
    generator's usual stores, about a week of grain, and the first barley ripened on day 15.
  - The famine of days 30 to 50 grew from this, through Brockley's green reaping and Ashford's eaten seed.
- **Winter came on the first infants.** A spring start put winter on the run's days 24 to 32, where the children born early were
  still infants.
- **The check existed and I did not run it.** The capacity tool reports a food horizon from the stores: the first short day, the days
  short, the meals short. It is the `run_horizon` that 37.2's `make_wild_region.py` uses as `horizon()`. It would have flagged the
  first-harvest gap before the run.
- **Calibration was a search, not a solve.**
  - Fields come in steps, so the mirror-symmetric homes came out at 17.5 and 21.3.
  - Parallel calibration runs raced on one file (calibration.json), which was rebuilt by hand from the logs.
  - A per-home `food_share` was the dial, which is a fudge.
- **The heat target reads a shorter year than the world's,** so the homes' wood was pinned by hand (`heat_share`: proposal open
  question 4).
- **The capacity tool's "as it stands" level** first read 7 to 9 of 10 people, because it counted only the one field in crop. The
  levels are fixed definitions of farming, not a reading of the world. That took a round of discussion to sort out.

### 2.4 Land: the generator had to be taught to take a design

What the generator lacked, and what I added or worked around:

| Need | What happened | State |
|---|---|---|
| Places with land but no people | There was no such kind. | Added: `vacant` places (room, land, mix, cells, a one-cell clearing). |
| Roads as designed | The generator built its own roads, and stopped any road over 1.5 days at a stopping place (t1, t2). | Added: `roads:` pins. Stopping places are still added. |
| Positions | `at` pins had no radius. | Added: `within`. |
| Whole-day roads | The geometry was fitted by hand (`design.py`: 18 km a day, 15 over hills, `km` overrides for steep roads). Hill roads first came out short. | Fitted by hand. The generator does not check a road's days against the design. |
| Soil | A pin failed where the site lacked the soil. | Added: base fertility set in range instead. |
| Coasts | Inlets narrower than 0.02 never reached the sea. | Shore constraint added in `fit()`. |
| Lakes | Hollows rarely fill. | Lakes became meres on a river (OPEN L-75). |
| Fens | A fen cannot be on a river. | That pin was dropped. |
| Rivers | A river ended on a home site (W3's Barrowby), leaving it nowhere to sit. | Rerouted by hand. |
| Fish and salt | Landgen never stocks them. | `water_stocks()` adds them after generation. Some streams hold no fish. |
| Copper | The settle probe's copper check looked at the wrong rock. | Fixed. |
| Vacant mix | A key mismatch ("wildwood" against "wood"). | Fixed. |
| Capacity check | It refused the designed worlds, because `warn_only` was ignored. | Fixed. |

W2, W3 and W5 were generated once and are not finished.

### 2.5 The wild: present, but not what the design assumed

- **Predators never came near people or herds** in 100 days. No attack and no beast taken.
- **Hunting gave almost nothing:** 285 hunts for 10.7 meat. Snares gave 18.7.
- **Raiders took about 7% of Ashford's crop.** Ashford's own cattle trampled more.
- So the wild added none of the dependence it was meant to (guarding herds, shared hunts). 37.2's brief 4c (W-36) takes up hunting
  rates and predators reaching villages.

### 2.6 Value the agents could not see

- **Middlemead, the designed prize (the best soil, the only mill site), looked poor from a walk.** Everard's report: "mostly acorns
  ... about one fish ... a night out in this cold eats 2 food".
- Its value pays only once the land is farmed, and nothing in what a visitor perceives says so.
- No one proposed farming it. The design's central choice, to expand or to intensify, depended on information the agents never got.

### 2.7 Verification: what was checked, and what was not

| Checked before the run | Not checked |
|---|---|
| Roads at their designed days (11/11, 20/20) | Founders' ages against the adult span |
| Each place's land against its type | The food horizon (stores to the first harvest) |
| Homes at about 2× "worked" | The season of the first births and the first winter |
| The settle probe at every vacant place | The settings against the current standard |
| 6-day bot dry runs: no errors, no missed meals | The aim reaching youths |
| | Whether a designed place's value is perceivable |
| | Predator reach and hunting yield |
| | Any run long enough to include births, a harvest and a winter |

The checks were static and local. The failures were all temporal: ages against the calendar, stores against the harvest date, winter
against births. A 6-day bot run cannot show any of them.

## 3. The pattern

1. **Properties went in by hand.** "Comfortable", "early adults" and "whole days" were turned into numbers by me, with no record of
   which number stood for which property, and no check that the property held.
2. **The checks tested the world at one moment, not over the run's first year.**
3. **There is no base.** Each builder restates settings, cast and stores, so anything not restated is silently lost.
4. **The land and people generators were built for one society.** Peoples, vacant land and designed roads were all bolted on.
5. **Design and perception are separate.** A place's designed role (prize, chokepoint, rare resource) is not tied to what an agent
   learns there.
6. **My process:** I did not list every setting and every choice I made unasked before the run. I spread the work over five worlds
   and finished two.

## 4. Features that would have made it work

In order of how much they would have saved.

1. **A world brief with checks.**
   - A declarative file of properties, each with a target and a tolerance. For example:
     - `home.worked_ratio: 2.0 ± 0.1`;
     - `home.stores_to_first_harvest: ≥ 1.2`;
     - `founders.adult_days_in_run: ≥ 40`;
     - `road(Ashford, Middlemead).days: 1`;
     - `first_winter_after: youngest_cohort ≥ child`.
   - The builder fits what it can, and reports each property as met or missed, with the number.
   - The report is written into the world file and published with the run. The brief replaces `design.py`'s hand fitting and my
     memory of what each number meant.
2. **A standard base profile.** Settings, eating, stores rule, cast rule and packs, which every builder inherits and overrides
   explicitly, plus a parity check against it. The settings line built on 13 Nov is the first half of this.
3. **A first-year timeline check, before any run.** A deterministic projection, by home and by day, from the capacity model and the
   life rules:
   - food in store at maximum births and full rations;
   - harvest dates;
   - who is adult and who is elder when;
   - the season of each cohort.
   - The `run_horizon` already does the food part.
   - It would have caught all three fatal flaws in seconds.
4. **A peoples cast generator.** Its parameters:
   - people per people;
   - ages relative to the lifespan ("fresh adults" means born an adult age before the run);
   - couples;
   - trades and tools spread evenly;
   - no kin across peoples.
   - The aim becomes a household custom that passes at coming of age (an engine change: kept or custom lines inherited, or the standing
     rules of `proposals/standing_rules.md`).
5. **Stores sized to the first harvest by default** (`stores_by_land`, as in `make_wild_region.py`), with the margin in the brief.
6. **Calibration solved, not searched.**
   - Capacity is close to linear in field area, so solve the area directly and allow part plots.
   - A symmetric world gets identical homes by construction (generate one half and mirror it, or pin the same site twice).
   - One process, not parallel runs on one file.
7. **Land features that hold at the scale asked:**
   - lakes that fill;
   - fens with a river;
   - coasts that reach the sea;
   - rivers that avoid named sites;
   - pinned roads whose length the generator checks in days, with stopping places only where asked.
8. **Resources stocked by the generator,** with a check that each designed resource is usable: fish and salt from water, game from
   the wild, and copper reachable with the given trades and tools (mine, smelt, tool), proved by a probe.
9. **A competent-bot long dry run.** A scripted household that farms well, keeps seed, keeps stores and has children when it can,
   played for 100 days. It shows the world supports growth when played well. It gives the reference curve agents are read against (a
   null arm for the benchmark), and it costs nothing in model calls.
10. **A legibility check.** The arrival message at each designed place, generated and read before the run, to confirm the place's role
    can be perceived (soil quality, a mill site, a copper seam). Where it cannot, the design or the senses change.
11. **Ecology targets in the brief:** hunting yield per unit, and predator visits per season to a village. These are 37.2's brief 4c
    numbers, checked like the rest.
12. **A pre-run sheet for Zach.** The brief's report, the settings line, and every choice made without his word, sent before any paid
    run.

## 5. What I would do differently now

- **One world, finished, checked over a simulated year, before a paid run.** Not five half-built.
- **Before a run:** run the `run_horizon` and the ages check on every world, and send Zach the settings line and the list of unasked
  choices.
- **Build features 1 to 4 before the second peoples run.** They are mostly assembly of pieces that exist: the capacity model, the
  `run_horizon`, `stores_by_land`, the settle probe and the settings line. The rest (land features, legibility, ecology targets) can
  follow.

*Current as of 14 Nov 2026.*
