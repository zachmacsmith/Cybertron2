# The hunt after brief 4: game that remembers, slow recovery, and bringing a kill home: build brief 4b

**Status:** draft (10 Nov), for Zach's go. **Build brief 4b**, between brief 4 ([hunt_and_fixes.md](hunt_and_fixes.md), built on
`ecology-calibrate`) and brief 5 ([river_and_water.md](river_and_water.md)). It answers what brief 4's gate and 37.2's check found:
- 02zzd's addendum;
- OPEN Q-40 (a) to (c).

**Owner:** 37.2:
- the author;
- stage A is 37.2's ecology, which 37.2 can build itself (`wild/ecology.py`, `wild/kinds.py`).

Stage B (the hunt's code, the act's party, led beasts, caching) is 37.4's (§5).

**Affects:**
- spec/environment/wildlife.md;
- on the branch: `wild/ecology.py`, `wild/kinds.py`, `engine/wild.py` (`take`, `_groups`), `engine/verbs.py`, `engine/data.py`
  (the `lead` modifier, `pack_ox`), `engine/things.py`.

## Summary

Brief 4 made the hunt a search over time, but its gate and 37.2's check show four gaps:
- **Unhunted land is a label, not a history.** `wild_tame` (x8) and `home_shy` (x0.3) are factors applied by the area's kind.
- **A hunted-out wood is full again within a year,** by deer walking in from next door. That is less than the wood's own yearly
  swing.
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
3. **Slow recovery.**
   - Kinds that keep a home range (deer, boar, the wolf; a new `K` trait `fidelity`) no longer drift a share a day into emptier
     land.
   - Their movement is mostly the young dispersing once a year after the breeding season, a share by attraction.
   - A daily trickle stays, only toward much better land.
   - **Target:** a wood whose deer were halved makes back about half its loss in a year and most of it in about three years, with
     no hunting. The natural yearly swing is unchanged.
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

1. **A party hunts together and shares the carry.**
   - People who hunt together (the same method at the same place and range on the same day, as crew work already counts them) are
     resolved as one take.
   - The crew's sweep and kill bonus are as built.
   - A kill's goods are split across the party's hands up to each person's carry. Three hunters bring a red deer home whole.
   - This replaces brief 4's deviation 4 (the whole catch into the acting hunter's hands).
2. **A led beast carries.**
   - The `lead` modifier (built, for travel: a pack ox, carry 60, D2-133) applies to `gather` as well: a beast led on a hunt adds its
     carry.
   - It costs the party: about +1 unit, and the party is easier for game to notice (`detect` of the party's approach raised; game
     flees more readily; calibrate).
   - A pony (the beast bred for this) comes with horses (OPEN L-36). Until then the pack ox stands in.
3. **Caching and fetching.**
   - What cannot be carried is cut and left, not lost.
   - **Near:** it is a carcass at the parcel (built), and it can be hung or hidden under brush (`hidden: under brush`, built) to slow
     the scavengers.
   - **The wood around and far:** it becomes a carcass thing at the area where it fell, recorded with who left it. A `fetch` the next
     days (the range's travel units and a unit to find it) brings it home, less what the area's carrion eaters took meanwhile (brief
     3's rules and the carrion flow above).
   - Only the one who left it, or someone they lead there, can fetch it.
   - Real places to cache at in the far land come with forays (OPEN L-105).
4. **Dressing in the field:** gutting where it fell is part of the kill. Only the dressed meat counts against the carry, and the
   offal is left (brief 3 makes it), drawing ravens.

## 4. Not in this brief

- **Forays and real places in the far land:** L-105.
- **Horses and ponies as kept beasts:** L-36 and husbandry (K6).
- **Dragging over snow or grass:** later, a modifier on near hunting.
- **Hunting rights and shares:** these emerge or not; nothing social is seeded.

## 5. Touches in 37.4's files

- **`engine/wild.py`:** `take` drops `wild_tame` and `home_shy` and reads `wary`; the party's take; the cache thing at an area;
  `_groups`' size by season.
- **`engine/verbs.py`:** the party resolved once; `fetch`.
- **`engine/data.py`:** `lead` modifying `gather`; `fetch`; a `cached` thing.
- **`engine/things.py`:** a carcass at an area (not a parcel), scavenged by the area's carrion eaters.
- **37.2's own:** `wild/ecology.py` (wariness, the history's take by distance, fidelity and dispersal, births through the season,
  carrion attraction); `wild/kinds.py` (`fidelity`, the litters, the constants).

## 6. Tests (the gate)

**Stage A:**
- `recover.py`: a halved wood recovers about half its loss in a year and most of it in three years, against the control's swing.
- At day 0, deer near a village are thinner and warier than in land a day's walk out, in every one of the four test worlds.
- Daily hunting raises `wary`, and it fades over about a year after hunting stops.
- `rat_check2.py`: rats swing less than 1.5 times within a season, and foxes and deer keep their yearly birth burst.
- A carcass raises its area's wolf count while it lasts. Over the two weeks after a cow is left by the fold, in a world where the
  pack did not yet raid the herd, the herd loses more than when the cow is burned.

**Stage B:**
- A party of three brings a red deer home whole; a lone hunter brings about 8 meat and leaves the rest cached.
- A cache fetched the next day is mostly there in winter and partly eaten in summer.
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
- **Caching only with forays:** it leaves the far hunt without an answer until forays are built. An area-level cache is enough for
  now.

## Open questions (for Zach)

1. Wariness's half-life (about a year), and whether it also makes raiders bolder or shyer at the fields (proposed: the same
   variable, read by both).
2. Whether 37.2 builds stage A itself (proposed) while 37.4 builds stage B.

## History

- 10 Nov 2026: written by 37.2 from 02zzd's addendum and Zach's answers on the label, recovery and carrying.

## Sources

hunt_and_fixes.md; 02zzd and its addendum; 02zx (brief 4); OPEN Q-40, L-36, L-105; D2-133; brief 3 (carcass_and_decay.md).
