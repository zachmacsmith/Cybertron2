---
id: docs/review/37_growth/02zzv_carrying_in_runs.md
kind: note
updated: "2026-11-20"
---
# 02zzv: carrying in the live runs

*note · `docs/review/37_growth/02zzv_carrying_in_runs.md`*


20 Nov 2026, 37.2 (subagent; the thread on how carrying works in the live runs ([[W-71 How carrying works in the live runs|W-71]]), under [[W-64 Food, weight and work on one basis|W-64]])

Zach (20 Nov): "Check how often their weight is refused. Maybe I also need to seed more transport infra. They seem to almost always
just carry things by hand between villages even tho their hands are quite limited." And: "Look on the river run for share that's
the most recent big world." Read-only. No model was run. Everything below is read from the runs' own journals on the dataset
`zachmacsmith/cybertron2-runs`, against the engine on `main` (ae1dc6a6).

## 1. What the engine does

- **Capacity** is `World.capacity` (world.py 486): on foot `PHYSICS.carry.foot` = 10; plus the best carrying item held: a pack
  +10 (weight 1; made from 1 hide and 1 timber, 1 unit, a basic craft everyone knows), a handcart +30 only on a road with a track;
  or a led pack ox, 60 (it replaces, it does not add). Transport spec: economy/transport.md ([[D2-135 Carrying capacities (OPEN C-1)|D2-135]], [[D2-136 The pack ox|D2-136]], [[D4-32 Too heavy to set off|D4-32]]).
- **Where a load is refused or capped.** Four places, and one where it is not:
  1. **The travel act** (verbs.py `_travel`, line 2048): load over capacity is refused. In the day's work (run.py 1012) the refusal
     starts a one-call **lighten** wave (prompt.py `lighten_prompt`: "You meant to set off for X tonight, but you carry W weight and
     you can carry C: set down at least ..."), in which the agent may give, move or leave goods and travel again. In the **evening**
     (evening.py 141) the same refusal is only a line, "Refused: travel: you carry 10.5 weight; you can carry 10 on this road, so set
     down at least 0.5", with no lighten call: the traveller stays the night.
  2. **A find by the road** (roads.py `_ch_take`, 729): what is taken is capped by room; nothing taken gives "You could carry nothing
     more."
  3. **The hunt** (wild.py `carry_of`, 2214, and `hunt`, 2364 to 2495): each hunter brings home at most foot + pack (+60 with an ox);
     the rest is left ("you could carry no more, and left 11 meat"). It counts only the hunt's own kill, not what the hunter already
     holds, and it adds pack and ox where `World.capacity` takes the larger.
  4. **Nightfall departure is not checked again** (night.py `departures`, 251). Goods given to a traveller after its travel act
     (another's give, later in the day or in another's lighten call) go with it uncounted. In pw1 three departures left over
     capacity this way (25.1 of 20, 11.8 of 10, 11.1 of 10); Everard's 25.1 came from two other travellers lightening their own
     loads onto him.
  5. **Inside a village nothing is capped.** Moving, taking, reaping or gathering into one's hands has no limit; the 10 bites only
     at a road. In the river run 174 of 1,043 adult person-dawns (24 people) held more than 10, up to 73.1.
- **What the prompt shows.** The system prompt: "on foot you carry at most 10 weight, more with a pack, more again with a cart on a
  road with a track; weights: ..., timber 2, stone 3, ..., everything else 1". Every day's "You" block: "You carry: 1 crude weapon
  (weight 1 of the 10 you can travel with)". The make list names "pack;" bare: neither its inputs nor what it adds. The travel verb:
  `"lead"?: a herd of yours here with an ox, to lead an ox as a pack ox (a harness in hands; it carries 60)`.

## 2. How it was measured

For each run, every committed step's checkpoint (journal/checkpoints.parquet) was read for each person's hands, place and transit,
the led herds and every container holding a pack, handcart or harness, and the runner's day results (blobs resolved). Aborted
attempts were dropped. A **trip** is one `depart` change. The load on setting off is the hands at the previous checkpoint with the
step's transfers, creates and destroys up to the `depart` change applied, plus 2 a carried infant; capacity is recomputed from the
frozen tables (journal/data.parquet). A **refused departure** is a committed `lighten` request, or a "Refused: travel: you carry"
result on a day with no lighten call. Reasoning is from responses (parsed replies and thinking). The scripts are in the session's
scratchpad (`carry_tools/`), not kept.

## 3. The river run (headline)

`water_runs_models_r1_d23`, the continuation of `water_runs_models_r1` (its days 0 to 6 agree: 3 trips, the same 3). Spec
`water_runs_models`, 100 days, run to day 23. Three villages a day apart in a line, **Highpool, Middleham, Lowstrand**, with
Stanwood, Hartcliffe, Thornholt and four wild nodes; 45 people in 9 households, each household on its own model (Fable 5.2,
Opus 4.5, 5 and 5.5, Sonnet 4.5, 5 and 5.5, Haiku 4.5 and 5.5). (The brief named Holtham, Stanmoor, Corneby and Weirford: those are
the wild region run, in §4.) 12 roads, none with a track.

**Seeded means of carrying:** no packs, no handcarts; 5 oxen (Field 2 at Middleham, Wood 2 at Lowstrand, Shepherd 1 at Highpool)
and 5 harnesses, all in byre or house stores. Hides and timber for packs: timber in every house; a hide in Marsh House from day 5,
2 to 4 in Fletcher House from day 10, 2 in Wright House from day 16, and Henry Hart held one in hand from day 3.

| Measure | River run, days 0 to 23 |
|---|---|
| Trips between nodes | 31, by 13 people (Tobin 6, Peter 5, Payn 4; six others 2; four 1) |
| Routes | all between the three villages: Highpool-Middleham 20, Middleham-Lowstrand 11; none to an unsettled node |
| Capacity on setting off | 10 on every trip |
| Load on setting off | mean 6.2, median 7.1, max 10.0 |
| Load over capacity | up to 10%: 7 (5 under 0.5); 10 to 50%: 3; 50 to 90%: 7; **90 to 100%: 14**; over: 0 |
| Refused departures | **8** (7 lighten calls in the day's work, 1 in the evening), by 4 people: Peter 3, Tobin 2, Basilia 2, Payn 1; one in four departures |
| How far over | 0.1, 0.1, 0.1, 0.5 (Tobin, the evening one), 0.9, 1.1, 4.0, 6.7: four of eight at 0.5 or less. Tobin set down too little on day 17 and was refused again at 0.3 |
| What came next | every one set down about the minimum and left: 7 the same day, 1 the next morning. None made a pack or fetched an ox |
| Set down to get under | 14.8 weight: 6.5 into the traveller's own house, 8.3 in the open (Tobin 6.7 of firewood and grain on Middleham Green, Basilia 1.6 at South Wood) |
| Capped takes, hunt meat left | 0 and 0 |
| Packs made, carts made | 0, 0 |
| Pack oxen led | 0 trips. Harness moved once: Odo took the Woods' 2 for ploughing (day 21). Annora asked to lead an ox on a hunt and was refused, no harness in hand (day 12) |
| Weight moved between villages | **192.5, all by hand** (firewood 77.5, salt 38, grain 23.8, timber 20.1, meat 8.7, the rest under 6 each) |

The households that held oxen and harnesses (Field, Wood) made no trips at all. The Shepherds, with an ox and a harness at Highpool
until wolves killed the ox (about day 16), made 9 trips and never led it. The travellers were mostly youths going to court and
Peter Brook carrying salt to trade.

**From the agents' reasoning:**

- Peter (Fable 5.2), day 8: "I can carry only 10 weight: my weapon, 7 salt and 2 smoked fish." Day 14: "The 2 grain and 2 salt are
  more than I can carry: use what you need, and bring the rest to Brook House if you come home."
- Wilmot (Opus 5), day 6, sending his brother off: "stone is 3 weight each and you carry 10, more with a pack: so MAKE A PACK
  before you go or you will carry two stone and your supper."
- Matthew (Opus 5) wrote "MAKE A PACK" into his plans and memory day after day from day 7 to day 11 ("Stone weighs 3, four is 12
  and I carry 10: MAKE A PACK"), offered a day's work for a pack (O979, day 5, unanswered), and never made one or tried to.
- Payn (Opus 5), refused on day 17: "I am 1.1 over what a man carries without a pack ... so the meat goes back into our own bins,
  not into a ditch." His house held 2 hides that day and he carried 2 timber.
- Alard (Haiku 4.5), day 2: "I'm carrying 24.4 weight but can only carry 10 ... So I must already be over capacity or there's
  something I'm missing."
- Peter, day 13: "pick up my pack so I can carry it home" → "Refused: take: you looked over Middleham Green and found no pack lying
  there". What he had seen was the engine's own line, "a pack lies at Middleham Green, with firewood in it (you put it there)".

## 4. The other runs

| Run | World | Days | Trips (people) | Load ≥ 90% of capacity | Refused departures | Capped takes; hunt meat left | Weight moved: by hand / pack / ox | Means made or used |
|---|---|---|---|---|---|---|---|---|
| **river** (`water_runs_models_r1_d23`) | 3 villages, 45 people | 24 | 31 (13) | 14 | 8 (26%) | 0; 0 | 192.5 / 0 / 0 | none |
| `wild_region_s7` | Corneby, Weirford, Holtham, Stanmoor, 37 people | 30 | 24 (8) | 11 | 7 (29%) | 0; 0 | 78.3 / 0 / 508.3 (6 with a pack as well) | 3 packs made (Clement 2, Herbert 1); 12 trips leading an ox (Ivo 6, Herbert 4, Clement 2) |
| `pw1_opus_sonnet_r1` | Ashford, Brockley, Middlemead, 20 people | 100 | 200 (24) | 68, and 3 over | 51 (26%) | 1; 11 meat once | 1,199.2 / 381.3 / 0 | 1 pack made (Everard, day 26), which he used on 23 trips; no ox led |
| `wb3_wenbridge` | Wenbridge, 12 people | 10 | 1 (1) | 0 | 0 | 0; 0 | 8 / 0 / 0 | none |
| `p2_brookend` | one node, no roads | 48 (to day 14) | none | | | | | |

No road in any of these worlds has a track, and no verb builds one, so a handcart could not help anyone in any run; the hand specs
of October (two_valleys, wide) had tracks, the generated worlds have none.

In the wild region the means were used because the world gave them a reason and an owner: two households (the Woods of Corneby, the
Dyers of Weirford) were seeded with the trade "carrying goods along the roads with a pack ox, and trading them", their own oxen and
harnesses; Herbert Moor had to bring 15 copper ore (3 weight each) from Scarley ("too much for a pack, so I'll lead one of our oxen
in harness"). Clement learned the pack's inputs from a refusal on day 0 ("I tried to make a pack, but it needs 1 hide and I had
none") and bought two hides to make two. In pw1 the one pack made was used by its maker on most of his trips, and he was still
refused 10 times, 6 of them with the pack, 3 of those within 1 of his 20.

## 5. Findings

1. **The weight is refused about one departure in four, in every run that travels** (8 of 31, 7 of 24, 51 of 200), and the load is
   binding when it matters: 14 of the river's 25 trips that carried 1 or more left at 90% to 100% of 10. But a refusal never stops a
   trip: every refused traveller set down about the minimum and left the same day or the next. It shaves the load; it does not
   change the means.
2. **Half the refusals are rounding, not choice.** The prompt shows the load floored to a tenth (`show`, world.py 59) and hides
   holdings under 0.05, while the check uses the exact load and the lighten prompt rounds up. Peter packed "8 salt and 2 hazel nuts",
   shown as weight 10 of 10, and was 0.1 over from 0.02 firewood he could not see. Four of the river's eight refusals were 0.5 or
   less (three exactly 0.1); 11 of pw1's 51.
3. **Seeding oxen and harnesses alone did not change behaviour.** The river run had 5 oxen and 5 harnesses and hides and timber for
   packs at four houses for most of the run; nobody made a pack, led an ox or used a harness to carry. The means sat with the
   households that stayed home, and the households that travelled had none, or, like the Shepherds, did not think of it. Where a
   household was given a carrier's trade with its own ox and harness (the wild region), 87% of the weight moved between nodes went
   by ox.
4. **The pack is barely legible.** The prompt says "more with a pack" but not how much, and lists "pack" among things to make
   without its inputs; agents learn the recipe only by trying and being refused (Clement). The same word names the engine's
   set-down bundle ("a pack lies at Middleham Green, with firewood in it", things.py 189), wolves ("a pack of 3"), and an alias for
   one's hands in `move` (verbs.py 1545); Peter tried to take a "pack" that was a pile of his own firewood. The lead option says "a
   herd of yours" and "an ox of your household's" though any ox at the place may be led ([[D4-114 What is physically there can be used|D4-114]]), and the harness has to be moved
   into one's hands first, which only the word "in hands" hints.
5. **There is little freight to carry.** The river's trips are mostly courtship and small trade: 192.5 weight between three villages
   in 24 days, about 8 a day for 45 people. Each village feeds itself; the one bulk errand that would have needed more than 10 (stone
   for Lowstrand, which has none) was planned for ten days and never made. The capacity is binding on the trips that happen, but it
   is not what keeps trips from happening.
6. **The rule is inconsistent across places.** Unlimited in a village, 10 at the road; the evening's refusal gives no chance to
   lighten; goods handed to a traveller after its travel act are not weighed at nightfall; the hunt adds pack and ox where travel
   takes the larger.

## 6. What would change behaviour

- **Legibility first (cheap, and acts on every run):** show the load and the holdings rounded up, or to two places, and never hide a
  holding that counts; state the numbers ("on foot 10, with a pack 20 (a pack is 1 hide and 1 timber), leading a pack ox 60, a
  handcart 40 on a road with a track"); put "you can carry about 4 more timber" in the "You" block, as transport.md's "What agents
  see" already says; rename the set-down bundle ("a bundle", which the signs already use) so "pack" means one thing; say that any ox
  at the place may be led, and that the harness must be in hand; give the evening's refused traveller the lighten call; weigh again
  at nightfall.
- **Seeded packs, or a hide in each house:** a pack per household, or a hide beside the timber every house already has, would let
  the agents who already reason about packs (Matthew, Wilmot, Payn) carry 20. On the river evidence it would raise the loads on the
  trips that happen; it would not create trips.
- **Pack oxen with a carrier:** in the wild region oxen were used because a household's trade was carrying and it held the ox and
  harness. Seeding a carrier household in each world, or putting the harness in a traveller's hands at the start, is the step most
  likely to move bulk by ox.
- **Roads with tracks, and carts:** no generated world has a track and no verb builds one, so handcarts are dead data now. Seed
  tracks on the main roads between villages (and a handcart or two) where the design wants bulk to move, or give a way to make a
  track; flag it in OPEN if wanted (it touches the roads and the generator).
- **A reason to move bulk:** a chokepoint good that one village has and another needs in quantity (stone, ore, salt, grain after a
  failed harvest) is what made the wild region's caravans. Without it, more transport mostly carries the same 6 or 7 weight.

My view: it is mostly legibility and demand, not a shortage of transport. The river run already had oxen, harnesses and the makings
of packs and used none; the run that used them had carriers and freight. Fix the display and the words first, seed a carrier with
its ox, harness and packs in the hands of whoever travels, and give the world a bulk good to move; tracks and carts are worth adding
only once there is freight for them.

## 7. What could not be measured

- **Trips not taken because of weight.** Only the reasoning shows it (Matthew's stone errand); a planned trip that was never made
  leaves no event.
- **Whether a refused traveller would have carried more with a pack.** There was no pack in the river run to compare against; pw1's
  only pack is one man's.
- **Meat left on far hunts** goes into the wild's carrion pool without a create; I counted the hunters' lines ("could carry no
  more, and left ..."): none in the river or the wild region, one in pw1 (11 meat).
- **Food spoiling or eaten inside a step** is applied from the changes, so the load on setting off is exact for goods, but decay
  inside a step, if any, is not.
- **Per model:** 31 trips across nine models is too few to say anything by model.

Current as of 20 Nov 2026.
