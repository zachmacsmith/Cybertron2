---
id: docs/review/37_growth/02zzy2_fishing_methods_compared.md
kind: note
updated: "2026-11-21"
---
# Fishing methods compared: why hand fishing, and what the villagers made of the others

*note · `docs/review/37_growth/02zzy2_fishing_methods_compared.md`*


21 Nov 2026, 37.2 (subagent)

This note extends `02zzy_why_they_did_not_fish.md`. It does not repeat that note. It answers Zach's questions: "Why do they try
hand fishing so much? In every single run? Do they not know other options exist? Do other options exist? Is it somehow pushed to
them? Is it not obviously inferior?" and "How did agents react in this or past runs when they tried other fishing methods and
compared to hand fishing?"

**Runs read:**
- Tonight's three runs-only arms, all finished: `runs_low` (day 54, all dead), `runs_medium` (day 55, all dead) and `runs_high`
  (day 64, 10 alive, 3 dead).
- Four past runs from `zachmacsmith/cybertron2-runs`:
  - `water_runs_models_r1_d23`: the river run, with three villages and nine model versions, Fable among them. Thinking was kept
    for the older models.
  - `water_lake_r1` and `water_lake_r2`: a lake village.
  - `wild_region_s7`: Weirford on the Mere. This world has the wild pack but not the water pack.

Thinking is withheld for every 5-5 model, so their reasons come from `why`, talk, notes and kept lessons. The scripts are in the
scratchpad under `fishing/tools/`.

## The short answers

- **Why so much?**
  - Tonight, hand fishing is not the method they tried most. Planned acts, with fallback acts in brackets:

    | | low | medium | high |
    |---|---|---|---|
    | Traps | 15 (+6) | 36 | 39 (+4) |
    | Hand fishing | 16 (+10) | 10 (+1) | 21 (+10) |
    | Nets | 0 | 16 (+5) | 26 (+13) |

  - Hand fishing is mostly Haiku and Sonnet work. Haiku planned 9 of the 16 acts in low and all 10 in medium. Opus planned 5 of the
    21 in high.
  - It is tried for four reasons:
    - It is a basic craft that the prompt says everyone knows.
    - In the low arm it is the only fishing craft the adults are told they know well.
    - The heads order it on the first days.
    - The run signs show fish in the water, so reaching in by hand is the obvious reply.
  - In the past water worlds it actually worked, and it was by far the most used fishing act: 244 acts written in the river run,
    57 and 115 in the lakes.
- **Do they know other options exist?** Yes. Every prompt lists angling, traps, nets and the weir.
  - The weir is listed as a craft everyone knows, in every arm.
  - Nobody in low or medium ever mentioned a weir.
  - Nobody in high built a second one.
- **Do other options exist?** Yes, five of them (table in §1). In the runs world two of them can never take a fish:
  - hand fishing, because of an engine gap (§1);
  - angling.

  Nets met 48 salmon and took none. Traps paid about 0.2 to 0.3 food a unit. The weir paid about 5.7 food a lift.
- **Is it pushed?** Not by the order of the list or by the examples. It is pushed by these:
  - its place in "Everyone knows";
  - being the only "known" fishing craft for the low arm's adults;
  - its lack of any description, so it reads as plain "fish";
  - the run signs.
  - Of the "no fish" result lines (32, 34 and 82), only 14, 10 and 20 come from hand fishing or angling (§2).
- **Is it obviously inferior?** Not from what they are shown.
  - The prompt shows labels and a food value for a unit of fish, never what a unit of any method gives.
  - In the runs world hand fishing gives nothing, but only because of the engine gap.
  - In the past worlds it was not inferior. It gave about as much food a unit as gathering in the river and the first lake, and
    three times as much in the second lake. It gave more than traps did as the agents worked them.

## 1. The methods, what they need, and what they gave

**What the data says.** From `engine/data.py` (TECHNIQUES, BUILDINGS, WATER_WORKS) and `wild/methods.py`:

| Method | Verb, units | Needs | Who knows it | Where | What it takes |
|---|---|---|---|---|---|
| fish by hand ("fishing by hand (tickling trout, groping under the banks)"; aliases "fish", "fishing", "catch fish") | gather, 1 | nothing | everyone (`basic`) | water | the parcel's resident `fish` stock: 0.6 a unit at full stock, ±50%. Also a run passing (`run: True`, brief 5 §3a.2, `wild.run_take`), but only once the stock check has passed |
| angle ("fishing with a rod and line") | gather, 1 | a fishing rod in hand (made from 0.5 timber and 0.1 hide in 1 unit; lasts 30 uses) | everyone (`basic`) | water | resident stock only: 1.5 a unit at full stock |
| trap in water ("setting wicker traps in the water overnight") | gather, 1 a set; the lift is a `take` from the trap's tag, 1 unit | nothing | by arm: none in low (the adults have a rough idea, the youths Nigel and Petronel are novices), capable in medium, skill 1.6 in high | water, fen | one trap a set, 8 nights, holds 10 kg; resident small water kinds and a share of a run passing; wrecked by a spate (0.5) or a flood (0.85) |
| net ("netting birds with nets and decoys") | gather, 2 | nothing | medium, high | fen, water, meadow, saltmarsh | flocks: wildfowl and pigeons, and also salmon (a run is a "flock", `kinds.TRAITS`). The label never says fish |
| weir ("a fish weir (stakes and wattle across the river, wicker traps in its gap)") | build, 24 units by a crew of 2, 12 timber; mended; its gap set shut; lifted by `take` | a river parcel | everyone (`basic: True` in BUILDINGS, so it is listed under "Everyone knows" in all three arms); it stands built only in high, held by the Marshs | river water | the first section takes 30% of a run passing, up to 100 kg a night; one lift takes all of it |

**The engine gap.** The runs world stocks no resident fish, so the Isel's `res` is empty (`state.json`). `knowledge.ready` refuses
any technique whose `draws` resource is missing from the parcel, with "there is no fish at the Isel". It does this before
`verbs.gather` reaches `run_take`. So:
- Hand fishing is refused even on run nights, although the code means it to take from a run. In the river run, which has resident
  fish, the same act returned "From the run in the water you took 3 eels" (Gervase, Opus 4.5, day 9).
- Angling is refused the same way. Peter (Opus, high, day 0) had no rod and got "there is no fish at the Isel", not "needs a rod".

**Measured, tonight** (the runs world; fish 0.46 food a unit):

| | low | medium | high |
|---|---|---|---|
| Hand fishing and angling | 14 refusals, 0 fish | 10 refusals, 0 fish | 20 refusals, 0 fish |
| Nets at the Isel (2 units each) | none | 19 acts, 0 catch (26 salmon and 4 fowl met, all got away) | 34 acts, 0 catch (22 salmon and 16 fowl met, all got away) |
| Traps: sets / lifts that took fish / kg lifted | 23 / 21 / 19.4 | 36 / 19 / 21.3 | 44 / 24 / 45.7 |
| Traps: food a unit of setting and lifting | about 0.20 | about 0.18 | about 0.31 |
| Weir: lifts / kg | none | none | 80 / 991 (about 456 food, 5.7 a lift) |
| Snares (meat caught, food) | 59 | 48 | 84 |
| Gathering wild food, food an act | 0.14 | 0.18 | 0.13 |
| Deaths | 13 | 12 | 3 |

**Measured, past runs** (fish was 1 food a unit then, and the wild foods had the values of their day; each column is read in its
own run's table):

| | river (d23) | lake r1 | lake r2 | wild region s7 |
|---|---|---|---|---|
| Hand fishing acts written (plan + fallback) | 244 | 57 | 115 | not offered (no water pack) |
| Hand fishing, fish a unit | 0.25 (plus run eels on about 30 tries) | 0.24 | 0.69 | |
| Angling, fish a unit (catches) | 0.72 (9) | none | 1.75 (4) | |
| Angling refused for want of a rod, or rod refused for want of hide | 17 / 9 | 2 / 1 | 3 / 1 | |
| Traps: sets / lifts / fish a unit of both | 102 / 25 / about 0.05 | 4 / 0 / 0 | 20 / 9 / about 0.16 | 8 / 0 / 0 |
| Gathering wild food, food an act | 0.39 | 0.31 | 0.22 | 0.29 |

**What the prompt shows.**
- The "Food, in meals a unit" line gives fish 0.46 (1 in the past runs).
- The gather line lists "...gather wild food; dung; fish by hand; angle; salt pan; hunt the wild (...); stalk (...); snare (...);
  net (spread nets and decoys where flocks come down, best at the water); trap in water (set wicker traps in the water at dusk;
  they fish by night for some nights, best when things run: come back to your traps and take what is in them, or it rots there or
  another finds it); den work (...)".
- Hand fishing and angling carry no description at all.
- No method shows what a unit gives. Results show it only afterwards ("You took 0.5 fish at the Brook").
- The weir appears only under build, as "weir (12 timber, 24 units of work, a monument: no room, 3 lines)", and under `set` for its
  gap. Nothing says what it takes.

So nothing in the prompt makes hand fishing look inferior. What would have made it look inferior is a result, and in the runs
world its result is a refusal that reads as a fact about the river.

## 2. Is hand fishing pushed?

**What does not push it:**
- The order of the gather list is TECHNIQUES order. Hand fishing comes before traps, but snares and nets come before traps too.
- The reply schema's examples do not name it. The fallback example is "(say, gather firewood)".
- No agent wrote "fish" or "fishing" as the `what`, which would resolve to hand fishing by alias. Every act was written "fish by
  hand".

**What does push it:**
- **It is in "Everyone knows"** in every arm and every water world, next to angling and making a rod.
- **In low it is the only fishing craft the adults know well.** The adults' "You know" lists hold no fishing craft. Traps are under
  "You have a rough idea of: setting wicker traps in the water overnight ... You could try these, at a cost in materials and a risk
  of failing". The heads' first fishing orders were for hand fishing:
  - Oliver (Opus, low, day 1): "Today I'll fish by hand at the Isel to add food."
  - Gunnild (Haiku, low, day 1): "Hamon asked me to fish the Isel by hand."
  - Nigel (Haiku, low, day 1): "Peter asked me to fish the Isel by hand."
  - Nichola (Sonnet, low), alone after day 24, never set a trap.
- **It has no description**, so it reads as plain fishing: "try a rod or my hands for fish" (Katherine, Sonnet, high, day 1).
- **The run signs invite a reach into the water.** "the water at the Isel alive with eels in the dark", "salmon going up through
  the Isel, leaping at the shallows". Of the 47 planned hand-fishing acts tonight, many follow a run sign:
  - Henry (Haiku, low, day 19): "The salmon are running, so I'll try for them by hand".
  - Nichola (Sonnet, low, day 31): "Lampreys run in the Isel; try fishing by hand for better food than greens."
  - Katherine (Sonnet, high, days 52 and 57).
  - Gunnild (Haiku, high, day 52).
- **It worked in every earlier water world.** In the river and the lakes it was the steady fishing act. Its yield matched
  gathering, or beat it, and it took eels from the runs. The same prompt line now leads to a refusal.

**The "no fish" lines, by the act that produced them** (result lines containing "no fish"):

| | low (32) | medium (34) | high (82) |
|---|---|---|---|
| gather (hand fishing or angling): "there is no fish at the Isel" | 14 | 10 | 20 |
| take from the place: "found no fish lying there" | 4 | 10 | 12 |
| take from a trap tag: "T3 holds no fish" | 2 | 1 | 7 |
| take from the weir: "you find no fish in the weir" | 0 | 0 | 6 |
| move: "there is no fish in your hands" | 5 | 8 | 14 |
| their own words (said or told) | 7 | 5 | 23 |

So most "no fish" lines are failed lifts and failed moves, not hand fishing.

**What followed a hand-fishing refusal.** Plans of the next three days:

| | low (12 cases) | medium (10) | high (20) |
|---|---|---|---|
| No fishing at all | 8 | 5 | 4 |
| Traps | 3 | 5 | 10 |
| Hand fishing again | 2 | 2 | 7 |

Low, where people know no other fishing craft well, is where the refusal most often ended fishing.

## 3. Reactions, by run

**Tonight, low** (Opus heads; traps at a rough idea for the adults):
- **Peter (Opus) made the one clean switch, for the wrong reason.**
  - Day 8, evening: "Salmon are running up the Isel and leaping at the shallows. Tomorrow I check the snares at first light, then
    fish the Isel."
  - Day 9: "With the units left I fish the salmon run by hand." Result: "Refused: gather: there is no fish at the Isel". Evening:
    "the Isel gave no fish by hand. The eels are running now, though. Tomorrow I'll set new wicker traps in the river."
  - Day 10: three trap sets.
  - Days 12 to 15: he lifted by `take` (3.4, 1.1, 3.9 and 5 fish into the store).
  - Kept for good (day 10): "Fishing by hand at the Isel gave nothing in spate; eels run on wet nights, so wicker traps are better
    there."
  - He blamed the spate, not the river's lack of resident fish. On day 19, starving, he went back to "fish by hand at the Isel
    while the salmon run". He died on day 19.
- **Nichola (Sonnet), alone from day 24.**
  - Day 31: "Lampreys run in the Isel; try fishing by hand" (refused).
  - Day 41: "Salmon are running; try fishing by hand" (refused).
  - Day 42: "Keep fed: gather wild food at the Fen with all units, as the routine has worked."
  - She never tried the traps she had a rough idea of, and died on day 54.
- **Denise (Haiku), day 15**, refused at the height of the eel run: "Father, where are the fish running? If there are none, Henry
  and I will set snares".

**Tonight, medium** (traps and nets capable, smokehouses):
- **Katherine (Sonnet) tried to lift by setting.**
  - Days 2, 3, 4, 5 and 10: "collect from my traps" or "check my traps", written as `gather trap in water`. Each time the result
    was "You set traps in the water at the Isel; they will catch by night for about 8 nights".
  - Day 2: "My traps at the Isel caught nothing".
  - Days 4 and 5: "Hamon took fish from my traps". Others lifted her catch with `take`.
  - Day 16: "Sorry: my trap action only set new traps; it didn't lift the eels. There are six eels in the traps at the Isel now.
    Oliver, how did you lift yours? Tell me".
  - Kept for good (day 18): "Lift eels with 'take' fish from the Isel, not 'gather trap in water' (that only sets new traps)".
- **Hamon (Opus)** had the lesson on day 4: "Gathering 'trap in water' or 'snare' again only resets them; to collect the catch, use
  take from the trap's tag first thing."
- **Henry (Haiku), day 13**: "I set new traps at the Isel today instead of taking yours and mine, so no fish has come home yet."
- **Nets.** Peter (Opus), kept on day 13: "Do not try netting fowl at the Isel; it failed every time. Snares and traps feed us
  better." Hamon (Opus), day 19: "Netting at the Isel in winter caught nothing; wicker traps and snares feed us better."
- **Nigel (Haiku)**, kept on day 27, puts the two methods together: "The Isel traps are fouled and empty; the otter takes what they
  catch, and fishing by hand gave nothing."
- Across medium, about 19 of the 36 trap sets came on a day whose `why` speaks of lifting, checking or emptying, with no `take` of
  fish in the plan. This is a crude word match. The repeated sets are part of why 8 traps stood in the water on day 6.

**Tonight, high** (master skill, the weir):
- **Hamon (Opus) wrote the river off before the run, from the nets and one empty trap, not from hand fishing.**
  - Day 0: he set a trap, then a net. The net's result was "You hunted the Isel and came on nothing." Evening: "the traps are in the
    Isel, but the fowl and fish there are hunted thin."
  - Day 1: "Refused: take: T3 holds no fish". Evening: "the traps held nothing, so the Isel is fished out."
  - Day 2: snares.
  - Kept on day 19: "Netting at the Isel in winter failed; salmon ran but escaped. Wicker traps or snares feed better."
- **Peter (Opus) moved to the weir.**
  - Day 8: "The traps on the Isel were smashed in the spate, so don't bother with them. I'll see to the weir."
  - He made 44 of the 80 weir lifts and fed the other houses with salt fish. Basilia (Haiku), kept on day 26: "Peter of the Marsh
    household gave the Brooks salt fish in hunger".
  - Kept on day 31: "Between runs the weir and river give almost nothing; then net fowl, snare, hunt or forage instead."
  - Nichola (Sonnet), kept on day 57: "Peter's wicker traps ... were empty when otter raided them; rely on the weir instead."
- **A rod that could not work.** Katherine (Sonnet), day 3: "No rod: it needs hide and we have none." She, Oliver and Petronel then
  spent parts of days 3 to 10 looking for 0.1 hide for it. In this world angling can never take a fish.
- **No second weir.** Hamon and Gunnild of the Shepherds are master weir builders by their own prompt, and the Shepherd store held
  28 timber. Hamon kept on day 1: "I am a master at ... building fish weirs: my best road to winter food." Nobody built a second
  weir. The Brooks lost three people on day 17.

**Past: the river run (d23).** The most explicit comparisons are here.
- **Mabel and Lambert (both Fable 5.2, Highpool), day 1.**
  - Mabel: "Hand fishing gave me under 2 fish for four units. Lambert, what did the traps yield? If better, I set more tomorrow."
  - Lambert had "lifted" with `gather` and set new traps: "Traps gave nothing yet, Mabel; keep to hand fishing, it is our best."
  - Lambert, day 3: "Netting and traps keep failing".
  - Lambert, day 9: "the spate smashes traps; snares are what pay".
  - Lambert, day 12, wrote "take fish from the Brook". The engine read it as Brook House: "Refused: take: you find no fish in Brook
    House". The river's name collides with the house's.
- **Lucy (Opus 5, Lowstrand) measured, and taught.**
  - Day 11: "Twice now I have gone down to Lowstrand Water meaning to LIFT the traps, and twice what I actually did was SET MORE
    TRAPS".
  - Gervase (Opus 4.5), day 12: "I lifted the traps as Lucy taught me. Only 0.4 fish, but it is FISH IN HAND, not wasted units
    setting more wicker."
  - Lucy, day 12: "FOUR-TENTHS OF A FISH. Wilmot got one and three-tenths for three units in the shallows". Then: "The wicker pays
    four-tenths of a fish and the room buys a bed".
  - In that world the comparison favoured the hand, and she was right.
- **Aldric (Opus 5) reasoned his way to the weir, planned it for three days, and never built it.**
  - Day 7: "On a run night the hand is not the tool — WICKER IS, and a WEIR is better than wicker".
  - Day 8: "Gervase — you have been in that water with your fingers three days running; come out of it and walk a trap line
    instead".
  - The plan was "twelve timber out of our twenty-seven". The timber went into a promised room instead. His own "walk my wicker"
    acts set new traps.
- **Jory (Opus 4.5) got angling working.**
  - Thinking, day 11: "Checking the traps at Lowstrand Water turns out to be the same action as setting them". He read the verb
    note ("come back to your traps and take what is in them") as saying that gathering again lifts.
  - Day 12: "I keep SETTING new traps instead of COLLECTING".
  - He got a hide from a dead calf and made a rod on day 14.
  - Day 15: "I CAUGHT FISH! 1.6 fish with my new rod! It WORKS!"
  - He then angled nearly every day, at about 0.7 fish a unit. He also compared places, day 17: "Olive caught 2 salmon in 2 units!
    That's 1 fish per unit, much better than Lowstrand Water."
  - Alard (Haiku 4.5, Middleham) also got a rod, from a calf slaughtered for its hide. He angled once (0.4 fish) and went back to
    his hands. The result line for angling reads exactly like hand fishing's.

**Past: the lakes (r1, r2).** Hand fishing worked, and it was the bulk of the fishing.
- In r1, Haiku planned 35 of the 39 hand-fishing acts. Four traps were set and none lifted.
- In r2, traps gave 0.2 to 0.6 fish a lift. Hand fishing gave about 0.7 a unit.
  - Isabel (Haiku), day 4: "Fishing by hand brought in about 3.4 fish, and the traps are set for 8 nights."
  - Joan (Sonnet), day 5: "I wasted the day: the rod needs hide, which I haven't got. Tomorrow I'll fish by hand".
  - Nigel (Opus) taught netting to Olive. Day 5: "The netting at the water caught nothing".

**Past: the wild region (s7).** Without the water pack there is no hand fishing to try. Sabina (Sonnet) wrote "Lift the wicker
traps at the Mere" on days 13, 14 and 15, and each act set new traps. Day 14: "the traps have caught nothing so far". No trap was
ever lifted in that run.

**Do they generalise "the river is empty"?**
- Yes, but mostly not from hand fishing alone. The generalisations came from:
  - nets reported as "You hunted the Isel and came on nothing";
  - a first-night trap with nothing in it;
  - traps that were never lifted because the agents "lifted" by setting.

  Each of these reads as an empty river.
- Hand fishing's refusal adds to it, and in low it often ended fishing outright (§2).
- Some did find out that the traps work and switched to them. Peter in low, Hamon, Oliver and Peter in medium, and Katherine by day
  18, all wrote it down as a lasting lesson.
- Only the high arm found the weir, because it was already built. Nobody anywhere built one, though everyone is told they know how.

**Teaching and telling.**
- No formal teaching of a fishing craft took place tonight ("taught 0" in every arm).
- Lifting was passed on by word:
  - Lucy to Gervase (river);
  - Oliver (Opus, high) to his house: "When you empty your traps, take only from yours. Look at the tag before you take anything";
  - Katherine (medium) asked Oliver how he lifted his.
- Netting was taught in the river run (Lambert) and in lake r2 (Nigel). Nobody taught trapping, although in low the two youths knew
  it and the adults did not.

## 4. Models

**Tonight:**
- Opus set most of the traps (11, 13 and 24 planned) and all of the high arm's weir work. Opus also wrote the lasting lessons
  about lifting (Hamon in medium on day 4, Oliver in high on day 4).
- Opus also reached the "fished out" conclusion fastest (Hamon, high).
- Sonnet was steady at traps in medium and high (11 and 14). It learned the lift late: Katherine wrote it on day 18 in both arms.
- Haiku did most of the hand fishing: 9 of 16 in low, all 10 in medium, 9 of 21 in high. Most of it was on orders or in answer to a
  run sign, and Haiku youths repeated it after refusals.

**River run, by planned acts:**
- Fable 5.2 did the most hand fishing (40). Its two Highpool agents ran the clearest hand-against-trap test and chose the hand.
- Opus 5 set the most traps (33) and did the most reasoning about methods (Aldric, Lucy, Wilmot).
- Opus 4.5 (Jory) did the most angling.
- Haiku 4.5 hand fished and followed its heads.

The differences in method between models are smaller than the difference the prompt and the verb make. Every model, Opus
included, "lifted" by setting.

## Conclusions

1. **Hand fishing is not irrational given what they are told.** It is the one fishing act everyone is told they know. It carries no
   cost and no description. In every water world before this one it paid about as well as gathering. In the runs world it can
   never pay, because the resident-stock check refuses it before the run take is reached. That is an engine gap, not a design
   choice.
2. **The traps' worst problem is the lift, not the yield.** In every one of the seven runs, `gather trap in water` meant as a lift
   set new traps instead (by the word match in "What I could not read"):
   - about 38 of 97 trap acts in the river run;
   - about 19 of 36 in medium;
   - all of Sabina's in the wild region;
   - fewer elsewhere: 4 in low, 11 in high, 2 and 9 in the lakes.

   The result line never says that the old traps are still standing. The agents then read the unlifted traps as empty: "Traps
   gave nothing yet ... keep to hand fishing, it is our best". What they compared was hand fishing against traps nobody had
   lifted.
3. **Nets are a lure at the river.** They are labelled for birds, and they met 48 salmon in medium and high without taking one. Each
   result reads "You hunted the Isel and came on nothing" or "came on a salmon, but it got away". That fed the high arm's "hunted
   thin".
4. **Angling cost days of hunting for hide** in high, the river run and lake r2. In high it could never have worked. Where it did
   work (Jory), it was the best active method.
5. **The weir is the method that works, and the only one nobody builds.** Everyone in every arm is told they know how to build it.
   It costs 12 timber, and the stores held 27 to 29. The prompt never says what it takes. Where it already stood (high), the
   village lived.

## Fixes that follow

These are grounded in state, following `guides/senses.md`. They are additions to 02zzy's list, not repeats of it.

1. **Let hand fishing reach the run where there is no resident stock** (engine, `knowledge.ready` against `verbs.gather`). For a
   technique with `run: True` on a water parcel where a run passes tonight, a missing resident `fish` resource should not refuse.
   - The run take then decides the catch.
   - Its rate against traps is a calibration for Zach (brief 5 §3a.2 means the hand to take a little of a run).
   - Between runs the refusal stays, worded as 02zzy fix 1 has it.
   - Angling should either be left out of the gather list where the parcels hold no resident fish, or refused with that reason, so
     that no one hunts a hide for a rod that cannot fish.
2. **Make the set result tell the setter what the state holds** (guide rule 7: the doer reads the result).
   - "You set a wicker trap at the Isel (your 3rd there). Your traps of autumn day 5 and 6 still stand, with fish in them: take
     from T12 or T13 to lift them."
   - Every fact in it is held on the set things (`by`, `set_day`, contents, tag).
   - The verb note should name the lift. "Come back to your traps and take what is in them" reads as "gather again" (Jory's
     thinking). It should read "lift a trap with take, from its tag; setting again lays a new trap".
3. **Give the net its own result words and a true label.**
   - The result should read "You spread your nets at the Isel and took nothing", not "You hunted the Isel".
   - If nets are meant to take salmon shoals, the label should say so ("netting birds, or fish in a shoal"), and 48 meetings with
     no take needs a check in `wild.take` (wariness? the run share?). If they are not meant to, salmon should not be met by nets.
4. **Say what the weir does where it is offered.**
   - The build line should read "weir: takes a share of every run passing the river, lifted in one act; 12 timber, 24 units by
     two".
   - Separately, check whether "building a fish weir" should be `basic` at all in the runs arms. The README gives the weir craft
     to the high arm only, but BUILDINGS makes it known to everyone. That is a world-design question for Zach: either the low and
     medium arms really could build one, or they are being told they could.
5. **Resolve a place name before a building whose name only shares a word with it** (`take` "from the Brook" gave Brook House).
   This is the same family as 02zzy §2e, the take by place that reached the weir.
6. **Give the methods' yields as lore, not as signs.**
   - Those who know a fishing craft could remember what a day of it gives in its season: "between the runs a trap takes little; on
     a run night, a few eels a trap; a weir takes a share of the whole run".
   - It is a standing fact, so it belongs in memory or the craft card (guide rule 3), grounded in `RUNS` and `SETS` (02zzy fix 1,
     extended to every method).

## What I could not read

- **Thinking** for every 5-5 model: tonight's runs, both lakes and the wild region. Only the river run's older models kept theirs.
- **Why nets took none of 48 salmon.** I did not trace it. The take-chance arithmetic suggests about one in five, so the cause is
  likely elsewhere (wariness, or the run share).
- **Hand against angling on mixed days** in the past runs. Both results read "You took N fish at X". I attributed by the day's
  plan, and dropped the 17 result lines from mixed days from the angling rates.
- **"Meant to lift"** is a word match on the day's `why` (lift, check, empty, collect, walk the line). It is a rough count, not a
  reading of each case.
- **The past runs used older food values** (fish at 1, wild food at 1). I compare within each run only.

**Sources:**
- scratchpad `live/runs_{low,medium,high}/` (turns.jsonl, days.jsonl, run.db, run.json);
- scratchpad `fishing/` (extracts of the four past runs: `*_days.jsonl` built from journal requests, responses and checkpoints;
  the scripts in `fishing/tools/`);
- `cybertron2/engine/data.py`, `wild/methods.py`, `wild/kinds.py` (RUNS, RUN_SIGNS, TRAITS);
- `engine/knowledge.py` (`ready`, `shortfall`), `engine/verbs.py` (gather), `engine/wild.py` (`set_work`, `run_take`,
  `take_chance`);
- `specs/make_nutrition_runs.py`;
- 02zzy_why_they_did_not_fish.md, 02zzw_water_fixes.md;
- docs/cybertron2/guides/senses.md.
