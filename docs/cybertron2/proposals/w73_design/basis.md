# The basis sheet: the numbers and words every part of the wave shares

**Status:** the decided rows are decided (each cites its decision); the rest are defaults or open, marked. **Owner:** 37.2.
**Thread:** the wave's integrated design (W-85), under the fishing, hunting and materials network (W-73).

Every component spec of this design uses these values and these words, and cites this sheet rather than restating a number. A
component that needs a value not here adds a row (marked default or open) before it uses it. The overnight notes disagreed because
there was no such sheet (wave_conflicts.md C1, C21, C30 and others).

Marks: **decided** (a decision cites Zach's words); **default** (taken by 37.2 to write on, to be confirmed); **open** (asked, not
answered; the component writes on the default shown and says so); **calibrate** (decided in shape, its number set in live runs).

## 1. Time and work

| Item | Value | Mark |
|---|---|---|
| The clocks | day (a night; real rates), year (32 days, seasons of 8; real durations about 1/11.4), life (a world's lifespan) | decided: D2-273 (spec/core/clocks.md) |
| A unit of work | 2 hours; 7 units a day in summer, 6 in autumn, 5 in winter; youths and elders fewer | decided: D2-275 |
| Durations | more than a few real days compress with their clock (about 1/11.4); a day or two keeps its real nights as a floor | decided: D2-273 |
| Process times | compressed whole at 1/11.4, at least one night (a keeping smoke 1 night; a hard cure 2 to 3; liming 2 to 4; tanning 16 to 48; retting in water 1, dew 3 to 4) | decided in rule (D2-273); the nights default (wave1 §2.4) |
| Quantity work and duration work | work that scales with what is handled (hanging, salting, scraping) is at real hours; work that scales with a process's length (tending a fire, feeding a pit) is its real hours over the real days times 1/11.4 | default (wave3_keeping §2.5; W80-Q4) |
| Making capital | real hours times the capital factor; things used up in one go or a few uses at real hours; materials real | decided: D2-276 |
| The capital factor | target about 1/7, staged from today's about 1/40 through about 1/15 | decided: D2-281; staging with its companions: open (§7) |
| Lives | a life in acts of work at the capital factor; a life counted in nights (set gear, tents, bedrolls) at the calendar's 1/11.4 | open (wave1 q4; default as stated) |
| The 1-unit floor | every act costs at least 1 unit; things under a unit are made in batches "up to" the batch | default (O-2, Zach's conditional go; wave2 W2-6) |
| Learning | practice set at a 64-day lifespan and scaled with a world's lifespan | decided: D2-267; the engine's base (32) re-based to 64: default (audit q8) |

## 2. Weights and handling units

| Good | Unit | Mark |
|---|---|---|
| Food goods | about 1 kg a unit (bread about 1.4 kg); a unit of fish 0.86 kg of whole eel, 0.46 food a unit | decided in rule (D2-264: weights in kg); values from data.py |
| Timber | a 25 kg load (a pole or a hewn length, what one person shoulders) | decided: D2-288 |
| Stone | a 25 kg building stone | decided: D2-288 |
| Firewood | a 10 kg bundle | decided: D2-288 |
| Straw | a 16 kg truss | decided: D2-288 |
| Hay | 10 kg (a beast's day) | decided: D2-288 |
| Charcoal | 20 kg | decided: D2-288 |
| Withies, bark | 10 kg bundles | decided: D2-288 |
| Cord | 1 kg | default (wave2 §2) |
| Hide | by the beast (a deer's about 6 kg green; a stoat's a pelt, not a hide) | default (wave2 §1, answering wave1's "one hide from a stoat or a deer alike") |
| Every recipe | rewritten in real kilograms on these units | decided: D2-288 |

## 3. Food, fuel and keeping

| Item | Value | Mark |
|---|---|---|
| The food unit | 1 food = 2,500 kcal; an adult 1 a night, a child 0.6, an elder 0.8; more for hard work, cold, nights out | decided: D2-292 |
| Fuel a night | about 10 kg (a bundle) a normal night, about 30 kg a cold one | decided: D2-290 |
| Kinds of fuel | firewood, timber, charcoal: heats and uses revisited with the timber economy (W-76) | decided to revisit: D2-290 |
| Smoking fuel | about 1 to 2 kg of wood a kg of fish hung (0.1 to 0.2 bundles a fish; 0.25 for a hard cure) | default, unsourced estimate (smokehouse_capacity §4); calibrate |
| Shelf life to a nightly loss | "keeps d days" = about a quarter lost by then, on nights = min(d, 2) + (d − 2)/11.4 | decided: D2-289 |
| The keeping order | fresh fish 1.5 nights; hot smoke 2.4; keeping smoke 9.7; hard cure 25.5; salt fish 33.8; dried 41.3 (curve nights) | follows D2-289, D2-271 |
| A food's base rate | its rate well kept; stores remove outside penalties, never slow below base | decided: D2-272 |
| Depths of cure | separate goods: hot-smoked, smoked, hard-cured, salt and dried fish and meat, each with its weight, food a kg and shelf life | decided: D2-295 |
| Salting | about 20 kg an hour (40 kg a unit) with gutting; salt 1 to 4 for fish, 1 to 8 for meat | decided: D2-283 |
| Smoke racks | about 250 kg of fish a set, on 1 space; the building caps the sets (a wattle hut 1, timber or stone by room size); material sets depths, life, fire risk | decided: D2-284, D2-291 |
| Hanging | about 30 kg a unit, splitting included | default (smokehouse_capacity; wave1 §3.1) |
| Gutting | in salting's and hanging's rates, never paid twice | default (audit C25) |
| Base rates a night (D2-289's arithmetic) | fresh fish 0.17, fresh meat 0.13, hot smoke 0.11, keeping smoke 0.029, hard cure 0.011, salt 0.0085, dried 0.0069 | follows D2-289 (u4 §2) |
| A lot in the smoke | base 0.03 a night while the fire is tended; the fresh rate when it dies | default, calibrate (u4) |
| Hard cure | 3 nights after salting; hard-cured meat 0.85 of the salt meat's weight, 0.67 food a kg | default (u4) |
| Hanging salted or gutted fish; taking down | about 60 kg a unit; about 120 kg a unit | default, estimates (u4) |
| The hearth rack | 1 night | default (u4; wave1 §2.4) |
| The smokehouse's work floor | 1 space kept free in a hut room, 2 in any other room (a hut 1 set; a small room 4; a medium 10) | default (u4 §4) |
| The salting tub | 120 kg in brine, 3 a space, a life of 5 world years; no cooper | default (u5; G10) |
| Vermin's sudden illness | an adult's 0.001 a night x (1 + 2 x min(1, rats a km2 / 120) x the household's exposure, 0.2 to 1) | default, a first magnitude (u5; G11) |

## 4. The water and the wild

| Item | Value | Mark |
|---|---|---|
| The catch basis | as calibrated: a set trap holds 10 units a night; a weir's first section 30% of a run passing, up to 100 units, each added section 7%, up to 70, at most 3; runs sized to a real river x 32/365 | decided: D2-293, D2-297 (kept; calibrated in live runs with the rest of the wave) |
| A run's gluts | surplus for keeping, trade and growth; the run is a finite stock shared by every trap and weir on it | decided in intent: D2-297 |
| One set act | lays up to about 6 traps | decided: D2-264 |
| The water's stocks | shallows, open water, runs; their relative sizes by kind of water | decided: D2-264; the numbers by water type: open (audit G6) |
| A freeze | stops fishing (set gear idle, edge and bank lines refused, the weir icing and wearing, a run's night held over to the next open night) | decided: D2-265; the detail: default (audit q14) |
| The wild's clock | on the year clock | decided: D2-273 |

## 5. Carrying and moving

| Item | Value | Mark |
|---|---|---|
| On foot | 10 kg (real 15 to 20; a named departure) | default (wave1 §4) |
| Creel, pack basket, frame | +5, +15 (25 in all), +20 (30) | decided in kind: D2-281; numbers default |
| Pack ox, handcart, cart | about 100 kg, 100 to 150 kg on a track, about 900 kg | open (wave1 q5; default as stated) |
| Moving between buildings | about 1 unit per 800 kg a parcel step, provisional | decided provisional: D2-274; re-set from the carry limit: open (audit q11) |
| Moving within a building | free, except hanging and taking down (quantity work) | default (audit q11) |
| Building materials to a site | carried on the day clock at these limits | open (wave1 q5) |
| Chores | quantity work at the rates above; fractions carried until whole; at least 1 spare unit to start; cascades at most 3 rounds a day; "whoever has time" is the members at the node with spare units, most spare first | default (u6 §5) |

## 6. Words the prompt and the engine share

| Word | Meaning | Mark |
|---|---|---|
| **tend** | going back to one's set gear: check, empty, re-set, take up; lift, check, empty, walk and collect read as tend | decided: D2-294 |
| **set** | lay gear from one's hands; refused with no gear in hand, naming one's gear already standing | default (wave3_taking §0) |
| A technique named alone | tends if one's own gear stands at the place, sets if not | default (wave3_taking; corrects wave4 §5.2) |
| The target | the thing, by tag or known name; unnamed, only one's own; another's only when named | Zach's 21 Nov answer in Q-80's notes; to be recorded (audit q9) |
| Several of one's own at a place | a tend takes all of one's own of that kind; an act that uses a thing up asks | open (Zach said "several: asked"; audit q9) |
| A household's things | count as every member's own | default (audit q9; G12) |
| Rules | one book per household and per person: go, keep, hold back, first, eat, move, drop; `when` on lasting states the household knows | decided: D2-274, D2-282 |
| Fallbacks | assignable by the household's book as chores; a person's own standing fallback first | decided: D2-296 |
| The options list | gone from the code | decided: D2-286 |
| Recipes shown | at capable and known: inputs with batch, what it gives, units, place or fitting | decided: D2-263 |
| Intent wording | no horizon word ("what you mean to do and why", "Decide what to do.") | open (steering.md §4; default as stated) |

## 7. Open at the basis level

- The capital factor's staging and its companions (builders as a trade, cheaper crop protection, clearing a plot at a time):
  building_clock.md; audit G7 to G9; W-82.
- Lives in nights against lives in acts (§1).
- Carrying limits and moving building materials (§5).
- Several of one's own at a place (§6).
- The shallows' stock by water type (§4).

*Current as of 22 Nov 2026: D2-263 to D2-300; rows from u4 to u6 added.*
