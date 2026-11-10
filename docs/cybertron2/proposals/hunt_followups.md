# The hunt after brief 4: game that remembers, slow recovery, and bringing a kill home: build brief 4b

**Status:** built and gated (10 Nov) by 37.4 on `ecology-hunt2` (`8158674`, 538 tests; older worlds replay; 02zx brief 4b; OPEN Q-41). Not merged: waits on Zach.
`ecology-calibrate`) and brief 5 ([river_and_water.md](river_and_water.md)). It answers what brief 4's gate and 37.2's check found:
- 02zzd's addendum;
- OPEN Q-40 (a) to (c).

**Owner:** 37.2:
- the author;
- stage A is 37.2's ecology (`wild/ecology.py`, `wild/kinds.py`); 37.4 builds it, as for brief 4.

Stage B (the hunt's code, the act's party, led beasts, caching) is 37.4's (§5).

**Affects:**
- spec/environment/wildlife.md;
- on the branch: `wild/ecology.py`, `wild/kinds.py`, `engine/wild.py` (`take`, `_groups`), `engine/verbs.py`, `engine/data.py`
  (the `lead` modifier, `pack_ox`), `engine/things.py`.

## Summary

Brief 4 made the hunt a search over time, but its gate and 37.2's check show four gaps:
- **Unhunted land is a label, not a history.** `wild_tame` (x8) and `home_shy` (x0.3) are factors applied by the area's kind.
- **A hunted-out wood starts refilling the next night,** by deer walking in from next door, with no lag: 38% of the loss is back in
  12 days.
- **Rats, mice, voles and hares** swing threefold within a season, because all births fall on one day.
- **A carcass cannot draw more animals in.**

On the people's side, the carry limit (10 on foot, about 30 kg) means a lone hunter can never bring a red deer home (20 meat,
about 60 kg of meat). Zach (10 Nov) wants that answered "through hunting parties, caching, and perhaps bringing ponies to carry
with a hunting party". Better hunting then becomes coordination, specialised capital, and technique.

## 1. For the builder

**Read:**
- brief 4 and its gate (02zx, brief 4; OPEN Q-40);
- 02zzd's addendum and its scripts (`docs/review/37_growth/02zzd_ev/`: `recover.py`, `rat_check.py`, `rat_check2.py`,
  `ev_sweep.py`, `ev_depletion.py`);
- on `ecology-calibrate`:
  - `wild/ecology.py`: step 3 and 4's births and the background take; step 5's movement; the `busy` suitability;
  - `wild/kinds.py`: `K` (`move`, `breed`, `people`, `shy`), `HUNT`, `HUNTED`;
  - `engine/wild.py`: `take`, `_groups` (`seen_herd`, `fed_at`, `n`);
  - `engine/verbs.py`: crew work, `_out`;
  - `engine/data.py`: the `lead` modifier, `pack_ox`, `hidden: under brush`.

**Do not:**
- label areas;
- name kinds in rule code;
- cap signs.

Dry runs only.

**Branch:** `ecology-hunt2`, from `ecology-calibrate`.

## 2. Stage A: game that remembers, and slow recovery (37.2's ecology)

1. **Wariness, learned and slow.**
   - A new state per kind and area: `wary` (0 upward).
   - Each hunt adds to it in proportion to the ground it covered, as pressure does; each kill adds more.
   - It fades with a half-life of about a year (32 days; calibrate).
   - In the take it sets the ease of finding (`detect / (1 + a x wary)`) and the flight (`flee` raised); in the raid loop, the
     group's boldness.
   - `pressure` stays as it is: it is the short displacement of days.
   - `wild_tame` and `home_shy` are removed. Land that no one has hunted has naive game because no one has hunted it.
2. **The history hunts as people do.**
   - People's background take before day 0 is by each area's distance from the villages and their people (the areas' `xy_km`; a
     day's walk out, falling off with distance), not the same share everywhere.
   - The same take raises `wary`.
   - `busy`'s label table (home 1.0, ring 0.4, wild 0) gives way to the same distance rule.
   - At day 0 the land already shows the gradient: thinner and warier game near people, naive game far out.
3. **Recovery with a lag, from the woods around.**
   - Recovery should be neither instant nor longer than a run. A wood that is hunted with restraint, or left alone, refills from the
     woods around it, but only after a lag.
   - **Kinds that keep a home range** (deer, boar, the wolf; a new `K` trait `fidelity`) move toward emptier land by how empty it
     has been over the last days, not by tonight's count. Their attraction reads a smoothed density with a time constant of about
     4 to 6 days.
     - In the first days after a cull, few come in.
     - Over the next season or two they drift in.
     - The young dispersing after the breeding season add a pulse.
   - **Where the woods around are thin** or cut off (no linked forest, or linked only across open ground), recovery is by the wood's
     own births and is slower.
   - **Targets** (`recover.py`), for a wood with its deer halved and then left alone:
     - very little recovery in the first 3 or 4 days;
     - about half the loss back in one to two seasons (8 to 16 days);
     - most of it back within about a year (32 days);
     - a wood with no forest around it is clearly slower;
     - the natural yearly swing is unchanged.
   - Under steady hunting the wood settles at a lower level that its births and inflow can sustain. Under heavy hunting it stays
     low while the hunting lasts.
4. **Births through the season for fast breeders.**
   - Kinds with several litters a year (rats, mice, voles, hares, rabbits) give birth a share each day of their breeding seasons,
     in place of all on the first day.
   - Once-a-year breeders keep the single burst of births, which is right for them.
   - **Target:** rats swing less than 1.5 times within a season. Brief 2's store losses are rechecked.
5. **Carrion draws carrion eaters.**
   - In the movement step, carrion lying in an area adds to its attraction for the kinds that eat it (wolf, fox, raven, bear), for as
     long as it lasts.
   - A village's group takes its size from the animals actually in its area each season's turn, so more wolves drawn in means a
     bigger pack.

## 3. Stage B: bringing a kill home (37.4's code)

1. **A hunting party is declared, never inferred (Zach, 10 Nov).**
   - **Hunting alone near others makes no crew.** Two people who hunt the same wood on the same day hunt separately. They share
     the game and add to each other's disturbance, so hunting near others without a plan is worse, not better. The crew that brief 4
     counts from the day's events is removed.
   - **`hunt with X`** (any hunting method's act with `with: X`) joins X's party. The party hunts X's way: X's method, place, range,
     target (`looking for`) and units. The follower's own settings are only its fallback.
   - **X accepts followers by default.** X can choose to hunt alone (`alone: true`) or to take only those it names.
   - **If X does not hunt that day,** or refused this follower, or the follower is not at X's node, the follower hunts alone with
     its own settings.
   - **A follower with fewer units than X's hunt** goes out with the party and searches with it for as many units as it has left
     after the walk home, then splits off and heads back.
     - The party's search runs over time: each meeting falls at a time in the search, a keyed draw.
     - At each meeting, only the members still out count: their sweep, eyes, skill and carry.
     - A member who leaves carries home its share of what was taken before it left.
   - **Chains** (A with B, B with C) follow to the one who leads (C).
   - **A circle** (A with B and B with A, or longer) is led by the better hunter: the highest skill in its own chosen method, then
     the familiarity with what it named, then the elder, then a keyed draw. The rest follow that hunter's pattern.
   - **When it is settled:** a party's hunt is settled after the day's acts. This is the pattern of `partner` and `try`, which are
     recorded during the day and settled when both have chosen. The leader and the followers then learn the outcome together in the
     day's results; a hunter alone learns it at once, as now.
   - **How the party hunts:**
     - its ground is the sum of its members' sweeps;
     - it notices with the best eyes among them;
     - each meeting's kill uses the best skill and familiarity in the party for that kind, with the crew's bonus as built;
     - danger is spread across the party.
   - **The catch** is split across the party's hands up to each person's carry, so three hunters bring a red deer home whole. This
     replaces brief 4's deviation 4. Each member spends its units and practises the method; the one whose shot took the beast gains
     the familiarity.
   - **A drive** (`crew: true`) needs a party.
   - **What the members learn.** Each member's result tells the hunt's events in order, worded as signs are (guides/senses.md):
     setting out together, each meeting and how it ended (taken, fled, wounded, turned on them), who turned back and when, and what
     each carried.
     - A member who turned back learns the events up to when it left. What came after it knows only if someone tells it, or by
       what it sees come home.
     - Those who stayed to the end learn all of it.
2. **A led beast carries.**
   - The `lead` modifier (built, for travel: a pack ox, carry 60, D2-133) applies to `gather` as well: a beast led on a hunt adds its
     carry.
   - It costs the party: about +1 unit, and the party is easier for game to notice (`detect` of the party's approach raised; game
     flees more readily; calibrate).
   - A pony (the beast bred for this) comes with horses (OPEN L-36). Until then the pack ox stands in.
3. **What cannot be carried.**
   - **Near:** it is a carcass at the parcel (built). It can be hung, or hidden under brush (`hidden: under brush`, built), to slow
     the scavengers, and fetched later by anyone who finds it.
   - **The wood around and far:** it is left, into the area's carrion pool (as brief 4 built).
   - Caching it at a place in the far land and fetching it later waits on forays, which give the far land places to go back to
     (OPEN L-105; Zach, 10 Nov).
4. **Dressing in the field:** gutting where it fell is part of the kill. Only the dressed meat counts against the carry, and the
   offal is left (brief 3 makes it), drawing ravens.

## 4. Not in this brief

- **Forays and real places in the far land:** L-105.
- **Horses and ponies as kept beasts:** L-36 and husbandry (K6).
- **Dragging over snow or grass:** later, a modifier on near hunting.
- **Hunting rights and shares:** these emerge or not; nothing social is seeded.

## 5. Touches in 37.4's files

- **`engine/wild.py`:** `take` drops `wild_tame` and `home_shy` and reads `wary`; the party's take and its ordered events;
  `_groups`' size by season.
- **`engine/verbs.py`:** the party resolved once, after the day's acts.
- **`engine/data.py`:** `lead` modifying `gather`.
- **37.2's own:** `wild/ecology.py` (wariness, the history's take by distance, fidelity and dispersal, births through the season,
  carrion attraction); `wild/kinds.py` (`fidelity`, the litters, the constants).

## 6. Tests (the gate)

**Stage A:**
- `recover.py`: for a halved wood, little back in 3 or 4 days, about half in 8 to 16 days, and most within 32, against the control's swing. A wood with no forest around it is slower.
- Hunting daily for 8 days, then stopping: the wood refills on the same lag. Hunting every other day: it settles at a lower level.
- At day 0, deer near a village are thinner and warier than in land a day's walk out, in every one of the four test worlds.
- Daily hunting raises `wary`, and it fades over about a year after hunting stops.
- `rat_check2.py`: rats swing less than 1.5 times within a season, and foxes and deer keep their yearly birth burst.
- A carcass raises its area's wolf count while it lasts. Over the two weeks after a cow is left by the fold, in a world where the
  pack did not yet raid the herd, the herd loses more than when the cow is burned.

**Stage B:**
- A party of three brings a red deer home whole; a lone hunter brings about 8 meat, and the rest is left.
- Two people hunting the same wood without a party do no better than alone, and each does a little worse.
- `hunt with X` follows X's method, range, target and units; with X not hunting, the follower hunts alone by its own settings;
  a chain resolves to its leader, and a circle to its better hunter; X accepts followers unless it chose otherwise; a follower with
  fewer units searches with the party for what it has and turns back, counting only at the meetings while it is out, and takes its
  share home; the party's hunt is settled once, after the day's acts, and replays exactly.
- Each member's result lists the hunt's events in order. One who turned back learns only those before it left.
- A led ox lets one hunter bring a red deer home, and costs a unit and some kills.

**Food a unit** (02zzd's harness extended to parties and a led beast):
- A lone hunter far out is about 2 a unit.
- A good party with a beast in naive land reaches about 4 a person-unit. The far master's 4 to 5 is now a party's, not a lone
  hunter's.
- The wood around stays on brief 4's targets.

**Regression:** brief 4's tests; the probe worlds with bots; older worlds replay.

**Gate:** the above and a short dry-run report to Zach.

## Why

- **Zach (10 Nov):**
  - on the label: "There should be larger natural effects of thinning populations from hunting nearby not because of a factor that
    increases it in wild lands ... This should be a natural thing of places that are unexplored, and I think the hunting populations
    should recover a lot more slowly from hunting impacts than natural variations."
  - on carrying: the meat limits "should be resolved through hunting parties, caching, and perhaps bringing ponies to carry with a
    hunting party".
- **The history of hunting:**
  - a red deer was gutted where it fell, then carried on a pole between two people, cut up and carried in trips, cached and
    fetched, or brought out on a pony;
  - hunted deer stay shy for years;
  - deer keep home ranges, and a hunted-out wood fills slowly.
- **02zzd's addendum:** the measurements behind each item.

## Alternatives considered

- **Tune `wild_tame` down:** it is still a label.
- **A bigger pack item:** it reads oddly as the way to bring a deer home, and it makes no reason to hunt together.
- **An area-level cache now, before forays:** considered, and left for forays (Zach, 10 Nov). Places in the far land are what make a cache findable; until then parties and led beasts answer the far hunt. (Earlier text: an area-level cache is enough for
  now.

## Open questions (for Zach)

1. Wariness's half-life (about a year), and whether it also makes raiders bolder or shyer at the fields (proposed: the same
   variable, read by both).
2. ~~Whether 37.2 builds stage A itself.~~ Answered: the brief goes to 37.4 whole (Zach, 10 Nov).

## History

- 10 Nov 2026: written by 37.2 from 02zzd's addendum and Zach's answers on the label, recovery and carrying.

- 10 Nov 2026: Zach: recovery not too slow ("Shouldn't last a full run. Just not too fast. A reasonable amount of restraint should make it be repopulated, if there are surrounding forests for them to drift in from, but with lag"). §2.3 rewritten: inflow by a smoothed density (a lag of days), half back in one to two seasons and most within a year, slower without forest around, a lower steady level under steady hunting; the three-year target dropped.

- 10 Nov 2026: Zach: a party is declared, not inferred: hunting the same place makes no crew; "hunt with X" joins X's party and follows X's pattern; if X is not hunting, one hunts alone. This answers whose settings a party uses. §3.1 rewritten (chains, circles, refusing followers, units, settling after the day's acts like partner and try, the best skill for a kill, the catch shared).

- 10 Nov 2026: Zach: members hunt with the party for as many units as they have, then split off and head back; X accepts followers by default and may choose to hunt alone; a circle (X with Y, Y with X) is led by the better hunter. §3.1 and its tests updated.

- 10 Nov 2026: Zach: members know the order of events (who turned back, what was caught); caching in the far land is flagged for forays (L-105); send to the other agent. §3.1 adds what members learn, §3.3 leaves the far cache to forays; sent to 37.4, who builds both stages (stage A in 37.2's ecology, as for brief 4).

- 10 Nov 2026: built and gated by 37.4 (`8158674`). Recovery of a halved ring 15, 32, 48, 50, 77, 92 and 97% back at days 4 to 28 (cut off from the wild, 46% by day 32); hunting every other day settles at 0.80 to 0.87; rats swing at most 1.18 times in a season; lone hunter near on target (master 1.01, novice 0.08), far master 1.45 (carry), a party of three with an ox about 4.4 a person-unit. Not met: a left carcass does not raise the herd's losses (16 against 16; Q-41 c). Deviation: people's background take only in the history.

## Sources

hunt_and_fixes.md; 02zzd and its addendum; 02zx (brief 4); OPEN Q-40, L-36, L-105; D2-133; brief 3 (carcass_and_decay.md).
