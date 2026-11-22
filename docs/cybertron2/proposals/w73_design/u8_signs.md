# U8. Signs and senses: the river's signs with their leads, keeping's signs, experts' signs as observations

**Status:** discussion (component spec of the integrated design, W-85). Parts decided cite their decisions; nothing built. **Owner:**
37.2 writes the river's rows and their emitter (wild/kinds.py, the river's part of engine/signs.py and engine/wild.py); 37.4 owns
the senses core (engine/signs.py, perceive.py, the PERSON rows) and reviews and is named on every merge there. **Thread:** W-85,
under W-73; the river's signs are W-72's.

## Extends

Read in full:

- **proposals/river_signs.md** (W-72): the night's record of the river (§1), bundles by state of the water (§2), acts that tell the
  truth on a separate axis (§3), seeded lore (§4), the nudge without counts (§5), where and when signs are seen (§6), the code by
  seam (§7), intended chances (§8), and its seven open questions. **D2-265** answered them in part: herons at a run only where a
  heronry is (q1); the river's flow class used for signs now (q2); dawn signs for the river (q3); a freeze stops fishing (q6: the
  engine changes, not the signs' wording only); fishers' lore decided with the founders' starting sets (q4). **D2-269** answers q7 in
  substance: experts' signs are observations of what is happening now, which may imply an act but never direct one.
- **docs/cybertron2/guides/senses.md**: what senses are for, what makes a good sign, the four kinds of sense, the rule for chances
  (D4-53, D4-75), the checklist, the measured evidence (signs that change today's act are acted on; standing facts and forecasts are
  not).
- The audit **docs/review/37_growth/02zzz2_river_signs_audit.md** (every state of the water against what reaches a person).
- **proposals/hunt_fish_materials.md** §9 (what people sense), §7.5 (pollution signs: U10's).
- The drafts: wave3_taking.md §4 (leads, the carried catch, the reworded rows, the freeze, the guide check); wave3_keeping.md §2.6
  (keeping's signs); wave_conflicts.md C12, E4.
- Decisions: D4-35 (signs are local), D4-48 (bundles), D4-53, D4-75 (every line by the one rule), D4-68 (tags), D4-71, D4-74, D2-211,
  D2-218, D2-231 (set nights), D2-264, D2-265, D2-268, D2-269, D2-279 (vermin's signs: U5's), D2-297 (signs are introduced and the
  catch read in live runs together).
- Records: L-114 (the river high or in spate as a sign: closed by D2-265's flow class), Q-78 (the fishing legibility fixes), L-141
  (seeded memory by livelihood), W-72.

## Departures

| From | What it said | This spec | Why |
|---|---|---|---|
| river_signs §6, §8; wave3_taking §4.2 | dawn rows read at the water reach those there "at dawn" with presence 0.5 (working there) and 0.3 next door | at dawn the rule reads presence from where one is: one's house (things.presence, `_presence_here`, things.py:457-502). A sight row at the water reaches the houses only at "elsewhere" (0.05 × own, own 0.8 or more). So the dawn lead to the village comes from rows plain from far (herons, the roar, splashing in the night) and from rows that read the sky and the calendar, which are open to everyone at the place as the weather lines are; rows at the water are by day | the guide's rule (D4-75); the drafts assumed a presence the state does not give at dawn |
| wave3_taking §4.2 (the carried catch: "his creel heaving with live eels") | the kind and "live" | "{who} came up from {water} with their creel full of fresh fish" | the hands hold `fish`, not eels, and nothing in hand is alive (D2-211 keeps fish alive only in a trap or weir) |
| river_signs §2.1 ("a heavy run: a trap fills in a night now, and the rest go past it"); RUN_SIGNS down (kinds.py:890: "the traps and the weirs on the river will fill") | traps fill | a trap takes a small share of a run: "the traps take what they meet of it, and most of it goes past" | on the calibrated basis a trap lands about 1 kg a run night and up to about 3 on a big one against its 10 kg hold (catch_basis §0, §1; D2-297); a trap seldom fills. The full sign stays where the state says full (signs.py:2499) |
| river_signs §2.1 expert ("... what is in the water tonight, and kept, is the winter") | | "a run like this is most of a year's eels in a few nights" | "is the winter" is a claim about a household's food the state does not hold (a farming household's winter is its grain) |
| river_signs §2.5 ("a spate: wicker traps in the main stream tonight will be torn away"; "the river is falling: traps set now will stand"), §2.7 ("a trap left full overnight will be robbed") | certainties | graded by the state: half or more in spate, nearly all in flood (WATER_WORKS trap wreck 0.5, 0.85); "traps in the main stream stand in water like this" (no wreck below spate); "they go to traps with fish in them" (`_robbers` reads a held catch) | a sign may not assert more than the state holds (guide rule 1) |
| river_signs §2.3 ("the nights drawing in, dark and still") | "still" | "the nights drawing in" | the wind is drawn by the weather; "still" is false on a gale |
| river_signs §2.6 (ice rows that keep the fishing going) | | rows by U1's ice state; the great freeze row read from it (frozen over, or a lane left) | D2-265 |
| river_signs §2.8 (expert: "the herons have left the heronry for the river") | | dropped | herons feed at the river whatever the run; it is not a change worth acting on beside the anyone row |
| river_signs §3 (results), §4 (lore) | in this proposal | results are U2's (with the water's words from §1 here); the lore lines are U9's (D2-265, D2-268); this unit says only what lore reads | the units split; nothing dropped |
| kinds.py WEATHER_LEADS eel row (kinds.py:410-413) | read in the evening at the village's first wood or scrub parcel, on `rain_after_dry` even under set nights | written by the river's night as a dawn event open to everyone at the place, on tomorrow's cue (or the set night, D2-231) | the audit (02zzz2 §1a): the lead was zero and in the wrong place |

## Purpose

The river holds far more than anyone senses (02zzz2): a run was two sight lines at the water in the evening, after the day's acts were
spent; the flow showed only through the local weather word; nothing showed a run coming, slackening, the otters, the weir's overflow or
what a loss cost. A trap is set by day for the night, so a sign of tonight's run that arrives after the day's acts is no use. This unit
gives each run **four leads**, each grounded in state and taking its chance from the one rule (D4-75):

1. **lore**, held and not rolled: the year as the family knows it (a season ahead);
2. **the dawn cue**: the morning of a run night, before the day's acts, read from the houses (the same day);
3. **the run itself**, at the water by day, at the fen, by night, and village-wide through herons and the sound of salmon;
4. **the catch carried home**, in the evening, to those who never went to the water (the next night).

Then the other states of the water (flow, slackening, ice, otters, the weir, the fen) in bundles; keeping's signs; and the rows that
direct an act, reworded as observations (D2-269).

## The design

### 0. Rules carried from the guide

- Every row reads a state value and names the threshold that fires it; where the engine does not decide a thing (a moon, a flood
  over the land, a gull), no row asserts it (guide rule 1; river_signs §2.12).
- A sign is a change; the standing facts of the river (when the eels come, what a trap holds) are lore (U9) and the craft's sentence
  (D2-263, U9), never signs (guide rule 3).
- Each row sets `own`, sense, `when`, scope (`who`), `reach` and `night`; no `p` on a new row; the chance comes from the rule; the build
  checks the intended chances through `perceive.chance_of` and adjusts `own`, never the result (guide rule 5, checklist 4).
- **Rungs:** anyone (no key); **one who fishes** (`knows: "fish"`): any water craft (wicker traps, the weir, a gill net, a set line,
  line fishing) **from a rough idea up** (question 2); **the expert** (`expert`: the same crafts at the expert's reading,
  NOTICING `expert_at`); **the elder** (`elder`).
- No act or feeling is put on a person; people's talk is their own (guide rule 1; D4-72).
- **D2-269:** a row says what is happening now; it may imply an act; it never says what to do.

### 1. The river's night record, `river_now`, and the bands

Kept for each village on a river, overwritten each night by `_runs_night` (wild.py:3072), as `wild.eaten` is (river_signs §1, with
two fields added for U1's freeze):

```
w.s["wild"]["river"][node] = {
  "day": d, "flow": low | normal | high | spate | flood, "flow_was": last night's,
  "passed": {kind: heads}, "band": {kind: trickle | running | thick | glut},
  "best": {kind: the year's most heads in one night here},           # for "slackening"
  "taken": {gear id: {kind: heads}}, "turned": {gear id: kg},        # gear.share_run returns what each turned away
  "swept": {cid: {kind: heads}}, "robbed": {cid: heads},
  "ice": open | edges | over, "held": [kind],                          # U1 §4: the run waiting under ice
  "first": [kind], "last": [kind]}                                     # the year's first night at this village; the window's end
```

`river_now(w, node, day)`: the flow class for a night, from the catchment's rain memory (`runs.state.rain`) and the day's weather,
which is drawn before the day starts (`runs.flow`, runs.py:282). It is the reading the wreck and the wear use, so a sign and a wreck
cannot disagree (closing L-114 under D2-265). When the river's level is built (D2-215) it replaces the class behind the same function.

**Bands:** a run's heads passing tonight against this station's year of that run (last year's tally, `runs.tally`; in the first year
the quota and dues at the window's start): under 2% of the year a **trickle**, 2 to 8% **running**, 8 to 20% **thick**, over 20% a
**glut** (river_signs §1.1; calibrate). Nobody counts eels in a river; the bands are what the rows read.

### 2. The four leads

#### 2.1 Lore (a season ahead; held, not rolled)

Lore is memory: kept lines seeded with the founders (D2-268), dropped and replaced like any kept line, never rolled. Its lines and who
gets them are U9's (wave4_people §3.5.1: FI1, FI6, FI7, FI9 and the rest; the remembered good and thin years of river_signs §4.2).
What they **read**, so that the lore is the engine's river as a family has learnt it: `RUNS` windows and cues (kinds.py:872; the set
nights under `runs_set_nights`, D2-231), the nights a run passes this station and when it is thickest (a year of the river's calendar,
`run_lore(w, node)` in wild/runs.py, 37.2), the trap's hold (WATER_WORKS trap `hold`), the wreck shares, the fresh fish's keeping
(basis §3). Lore that advises in the family's voice ("sets many before the nights come") is lore, not a sign; whether it may advise is
U9's question (wave3_taking question 12).

#### 2.2 The dawn cue (the same morning)

Written by the river's night as dawn events (`w.event(..., dawn=True)`, as run.py:423 writes the season's), for the morning after,
reading what the state already holds for that day: the pulses written for day d + 1 by `RU.advance`, tomorrow's weather (drawn and
used for the cue the night before: `weather(w, nodes, w.d + 1)`, wild.py:3171), and `river_now`. `perceive.dawn` (perceive.py:350)
reads them by the rule from where each person is at dawn; graded rows need `perceive.dawn` to read `knows` and `lay` as the evening
does (37.4; river_signs §7 item 8).

| Row | Sense, own | Who | Spot | Fires on (state) | The lead |
|---|---|---|---|---|---|
| "the nights drawing in: the eels will be moving soon" | sight 0.35 | expert, elder | everyone at the place (as the weather lines) | the eel window opens within 2 days (`RUNS.eel.seasons`), and the village is on a river the eels run | days ahead |
| "the first heavy rain after the dry weeks" | sight 0.4 | anyone | everyone at the place | tomorrow's eel cue met at this stretch (`runs.cued`, `rain_after_dry`); only where the runs read the weather | the same morning |
| "the first heavy rain of the autumn after the dry weeks, and the night coming on dark: an eel night" | sight 0.3 | expert | everyone at the place | the same; under set nights (D2-231), a set night of the eel window instead, with the text "the dark nights of the autumn come, and the river full: an eel night" | the same morning |
| "herons flying down to {water} from first light, one after another" | sight 2.5 | anyone | the water parcel | a heronry at the village (`wild.sites`, not gone) and last night's band thick or more (D2-265) | the run, the same morning |
| "the roar of {water} in spate, heard from the houses" | sound 2.5 (loud) | anyone | the water parcel | `river_now` tonight spate or flood | the same morning |
| "{water} roaring in spate: wicker traps in its main stream are torn away in water like this, half of them or more" (flood: "nearly all of them") | sound 2.5 | one who fishes, with set traps of their own (or their household's) in a river parcel | the water parcel | the same | the same morning |
| "heavy splashing from {water} all night, fish throwing themselves at the shallows" | sound 2.0, night | anyone | the water parcel | last night's salmon band running or more | read at dawn |
| "eels on the wet grass of {fen} at first light, working their way through it toward {water}" | sight 1.2 | anyone | the fen beside the water | last night's eel band thick or more and rain on that night | read at dawn |

#### 2.3 The run itself (by day at the water; at night; village-wide)

Rolled in the evening as now (`_wild_river`, signs.py:2417), from today's pulses at the stretch and the record.

| Row | Sense, own, reach | Who | Fires on |
|---|---|---|---|
| "dark eels moving in the slack water under the banks of {water}, all one way, downstream" | sight 1.2, around | anyone | eel band running |
| "the shallows of {water} thick with eels, sliding over one another, all going down" | sight 1.6, around | anyone | eel band thick |
| "eels everywhere in {water}, in the weed, under the banks, against the stakes: more than any hands could take" | sight 2.0, around | anyone | eel band glut |
| "the water at {water} alive with eels in the dark, all going downstream" (kept, kinds.py:889) | sight 0.6, night | anyone | band running or more |
| "eels against your legs in the water, cold and strong, all going the one way" | touch 2.0 | the doer: anyone who worked in the water today | band running or more |
| "a sweetish smell of fish and mud off {water}" | smell 0.8 | anyone | band thick or more |
| "herons standing all along {water}, more together than you have seen, still as posts" | sight 3.0 | anyone | a heronry at the village and a band thick or more |
| "an eel run in {water}: every trap in it takes a few tonight" | sight 0.9, near | one who fishes | eel band running |
| "a heavy run in {water}: the traps take what they meet of it, and most of it goes past" | sight 0.9, near | one who fishes | eel band thick or more |
| "a run like this is most of a year's eels in a few nights" | sight 0.7, near | expert | eel band glut |
| "salmon going up through {water}, leaping at the shallows" (kept, kinds.py:891) | sight 0.9 | anyone | a salmon pulse going up, 3 heads or more |
| "salmon lying close in the pool below the shallows of {water}, their backs out of the water" | sight 1.6, around | anyone | salmon band thick or more |
| "salmon come up behind a spate and lie in the pools: a shut weir takes them; hands and nets seldom do" | sight 0.6, near | expert | salmon passing, and the flow fell from spate or flood |
| "lampreys on the stones of the shallows, clinging by their mouths against the current" | sight 1.0 | anyone | a lamprey pulse going up |
| "slime trails across the mud of {fen}'s paths, all toward {water}" | sight 0.8, lingering a day | anyone | the dawn fen row's state, the day after |
| "the first silver eels of the year in {water}, fat and dark-backed, going down" | sight 1.5, around | anyone | `first` eel night at this village |

#### 2.4 The catch carried home (the evening; the next night's lead)

A new PERSON row (signs.py:888-902; `person_context`, signs.py:1107-1145), 37.4's:

| Row | Sense, own | Who | Spot | Fires on (state) |
|---|---|---|---|---|
| "{who} came up from {water} with their creel full of fresh fish" (no creel: "with a good load of fresh fish", 5 to 10 kg; 10 kg or more: "with as much fresh fish as they can carry") | sight 1.0 | others (never the carrier: guide rule 7); the household inside | the carrier's house ground (a presentation choice: the engine does not place a person in the evening; people go home to sleep, and the house's ground is where a load is carried to. Deterministic) | 5 kg or more of fresh `fish` in hand or creel at evening (ITEMS fish weight 1 kg a unit), and work today on a water or fen parcel (`today["worked"]`) |
| "{who} came in from {place} with a good load of fresh meat" (10 kg or more: "with as much fresh meat as they can carry") | sight 1.0 | as above | as above | 5 kg or more of fresh meat in hand, and a hunt today (`hunted` kills by them) |

It reads a body and its load and the day's work, which the guide allows ("signs of a person's body are fine"); it puts no act or
feeling in anyone's mouth (no "hurried", no "pleased"). It is the reach that was missing: in the live runs the households who never
went to the water never learned there was a run (wave3_taking §4.2). The existing load row ("{who} has a load: ...", signs.py:901, a
`p` row) gives way to it where it fires.

### 3. The other states of the water

#### 3.1 The flow (by `river_now`; replacing the sky's two river rows, signs.py:576, 578)

| Row | Sense, own | Who | When | Fires on |
|---|---|---|---|---|
| "{water} low and clear, stones showing at the edges and weed trailing in the current" | sight 0.8 | anyone | day | fell to low |
| "the river too low and clear for the eels to move: they wait for rain" | sight 0.6, near | expert | day | low, the eel window open, the runs reading the weather |
| "{water} up and coloured, reed and sticks coming down on it" | sight 1.2, around | anyone | day | rose to high |
| "{water} in spate, brown and roaring, tearing at its banks" | sight 2.0 | anyone | day | spate |
| "{water} in flood, the whole width of it moving, whole branches turning in it" | sight 2.5 | anyone | day | flood |
| "the roar of {water} in spate, heard from the houses" | sound 2.5 | anyone | dawn (§2.2) and day | spate or flood |
| "{water} louder this morning than the rain here explains: it is raining hard upriver" | sound 0.8 | expert | dawn | spate or flood tonight while the day's own rain is light (the catchment against the village) |
| "the current drags at your legs: you can barely keep your feet in it" | touch 2.0 | the doer in the water | as it happens | high or more |
| "{water} dropping and clearing, wrack and torn reed left high along its banks" | sight 1.0, around, lingering two days | anyone | day | fell from spate or flood |
| "{water} falling and clearing: traps in its main stream stand in water like this" | sight 0.7, near | one who fishes | day | fell from spate or flood to high or less |
| "the gap shut in a spate: the river is piling against the wattle" | sight 1.2 | the weir's crew, one who knows the weir | dawn | the gap shut, flow high or more (wear ×2, WATER_WORKS `gap_high`) |

The ambient "water running over stones in {name}" (data.py:167) becomes the flow's own: "{water} sliding past, slow and brown" for a
big river at normal; nothing in spate (37.4).

#### 3.2 A run slackening and ending

| Row | Sense, own | Who | Fires on |
|---|---|---|---|
| "fewer eels each night in {water} now: the run is passing" | sight 0.8, near | one who fishes | tonight's heads under half the year's `best` here, the window open, a run passing |
| "the eel run is over at {water} for this year" | sight 0.8, near | one who fishes | the day after the window's end (`runs.ended`) |
| "the eel run was thin this year at {water}: about half of last year's" / "a good eel run this year" (kept, kinds.py:895-896) | sight 0.7 / 0.6 | one who fishes | as built |

#### 3.3 Ice and thaw (U1 §4; D2-265)

| Row | Sense, own | Who | When | Fires on |
|---|---|---|---|---|
| "{fen}'s pools skinned with ice, the reeds stiff with rime" | sight 1.0 | anyone | dawn | the fen's ice `edges` or `over` |
| "ice along the edges of {water}, the main stream still running black between" | sight 1.2 | anyone | dawn | `edges` on a river |
| "{water} frozen over from bank to bank" | sight 2.0 | anyone | dawn | `over` |
| "the ice going out of {water} in grinding plates" | sight 1.5 and sound 1.5 (two rows) | anyone | dawn | the thaw |
| "the ice going out: it will tear at the weir's stakes" | sight 0.8 | crew, one who knows the weir | dawn | the thaw, a weir standing (thaw wear ×2) |
| the great freeze (kinds.py:534-536) | as built | as built | as built | its text by the village water's ice: `over` "the river frozen from bank to bank; birds lying dead on the ice"; `edges` "{water} frozen far out from both banks, a black lane of water moving in the middle; birds lying dead on the ice" |

What a freeze does to a person's own gear is told in U2's results ("frozen in: nothing has come to them"; the refusals); no sign
repeats it. The fowl rows are as built (kinds.py:357-361; signs.py `_wild_thaw`).

#### 3.4 Otters, the weir, the fen, resident fish

| Row | Sense, own | Who | Fires on |
|---|---|---|---|
| "otter tracks in the mud below the bank of {water}, webbed, with the drag of a tail" | sight 0.6, near | anyone | otters about the village (`ROB_SETS.least` or more) and set traps there or a run passing |
| "an otter rolling and diving in {water} in broad day, eating as it swims" | sight 1.0, around | anyone | otters about and a band thick or more |
| "otters working this stretch: they go to traps with fish in them" | sight 0.8, near | one who fishes | as the tracks |
| the robbed traces (kept, kinds.py:901-902) | as built | as built | as built |
| "scales and torn weed piled against the weir's wattle: more came down in the night than its traps would hold" | sight 1.2, around, lingering a day | anyone at the water | last night's `turned` over 0 for the weir (the scales and weed are the trace's presentation, named) |
| "the traps at {water} crammed full: whatever comes down now goes past" (kept, signs.py:2499) | as built | the keepers | as built (the state says full) |
| "the fen's dykes brim but lie still while {water} tears past" | sight 1.0 | anyone | spate or flood, a fen beside the water (U1 §6) |
| "traps in the fen's dykes stand when the river tears the rest away" | sight 0.7, near | one who fishes, at the fen | the same |
| "the water at {name} is quiet: few fish rising" (signs.py:686) | as built | as built | only when no run passes |
| "few fish of {water}'s own, but the run going through" | sight 0.8, near | one who fishes | a run passing and the open water low |
| "fish rising all along {name}" (signs.py:691) | `own` 0.8 in place of `p` 0.06 | anyone | the open water rising past 0.75 of K, not every day |

### 4. Rows that direct an act, reworded (D2-269)

Found by reading every sign row in wild/kinds.py and engine/signs.py for an instruction:

| Row now | Where | Reworded |
|---|---|---|
| "an eel night: dark, wet and the water rising after the dry weeks; set the traps tonight" | kinds.py:412 | §2.2: "the first heavy rain of the autumn after the dry weeks, and the night coming on dark: an eel night" |
| "{kind} crowding in the pool below the dam at {place}: net them, or draw the hatches and let them up" | kinds.py:894 | "{kind} crowding in the pool below the dam at {place}, more each hour, unable to get up past it" |
| "the {kind} are running at {place} tonight: the traps and the weirs on the river will fill" | kinds.py:890 | replaced by the banded fisher rows (§2.3) |
| "the wolves will come back to the herd that fed them: watch it or bring it in" | kinds.py:389 | "the wolves will come back to the herd that fed them" |
| "{the} in {nm} cannot stand much longer: it must be cut tomorrow or lost" | signs.py:104 | "{the} in {nm} cannot stand much longer: a day or two more and it will be lost" |

Kept as observations that imply an act: "the frost has driven the fowl off the frozen ground onto the open water: nets at the water's
edge take them now" (kinds.py:358; "nets" becomes "fowling nets" with U2's split); "the boar can't root, and will come to the clamps
and the stores" (kinds.py:280); "rain beating on the ripe barley in {field}: it wants cutting" (signs.py:100-102: the crop's state, not an order to a person).

### 5. Keeping's signs (wave3_keeping §2.6; the state is U4's)

The household knows its own containers without a roll (`keeping.house_lines`, keeping.py:139-166, generalised by U4 to every
processing container), so these rows are for others; nothing about a lot being cured goes to anyone else (it is not visible).

| Row | Sense, own, reach | Who | Fires on (U4's state) |
|---|---|---|---|
| "smoke rising from the smoke hut by {house} this morning" | sight 1.5 | anyone | a smokehouse or smoke hut with a lot on its racks and its fire kept today |
| (fog) "smoke lying low about the smoke hut by {house} in the fog" | sight 1.0, around | anyone | the same, in fog (conditional) |
| "the smell of smoke and fish about the smoke hut by {house}" | smell 1.2, around | anyone | the same, any weather, day or night |
| "the fish on the rack by {house} wet through" | sight 1.0, near | anyone | an open drying rack with a lot on it and rain that day (conditional) |
| the hut burnt | the fire bundle (D4-74) | | + ", and the fish on its racks with it" when lots were lost |

The retting and tanning stinks and the fouled water below are U10's (hunt_fish_materials §7.5); vermin's signs are U5's (D2-279).

### 6. Intended chances, by the rule

Ordinary eye, clear day, attention 1 (near rows ×2 for the close look), from NOTICING (data.py:1010-1035): presence 0.5 having worked
on the parcel, 0.3 next door (own 0.5 or more), 0.3 crossing one's own house ground, 0.05 elsewhere (own 0.8 or more); sound carries
0.5, 0.45, 0.2, 0.1 by steps and smell 0.5, 0.3, 0.12, 0.05; fog ×0.3 on sight; night sight ×0.1, sound ×1.2. The layout is
Eelmouth's: the Street (the houses) three steps from the Isel, the Fen next to the Isel and two steps from the Street. "Someone" is
the chance that at least one of 12 at the Street notices. At dawn, presence is from the houses. Computed by hand; the build checks each
through `perceive.chance_of` and moves `own` until it lands.

| Row | At the water (worked there) | Next door | The Street | Someone, the Street | Fog (water / Street) |
|---|---|---|---|---|---|
| eels running in the shallows (sight 1.2, around) | 0.6 | 0.36 | 0 | 0 | 0.18 / 0 |
| eels thick (1.6, around) | 0.8 | 0.48 | 0 | 0 | 0.24 / 0 |
| eels in a glut (2.0, around) | 1.0 | 0.6 | 0 | 0 | 0.3 / 0 |
| herons standing all along (sight 3.0) | 1.0 | 0.9 | 0.15 | 0.86 | 0.45 / 0.045 |
| herons flying down at first light (sight 2.5, dawn) | (few there at dawn) | 0.75 | 0.125 | 0.80 | 0.0375 (someone 0.37) |
| the roar (sound 2.5, dawn and day) | 1.0 | 1.0 | 0.25 | 0.97 | the same |
| the fisher's spate reading (sound 2.5, dawn) | 1.0 | 1.0 | 0.25 for each fisher with traps in the river | | the same |
| splashing all night (sound 2.0, night, at dawn) | 1.0 | 1.0 | 0.24 | 0.96 | the same |
| the smell of a run (smell 0.8) | 0.4 | 0.24 | 0.04 | 0.39 | the same |
| eels on the fen's grass (sight 1.2, dawn, at the fen) | | 0.36 (living by the fen) | 0.06 | 0.52 | 0.018 |
| the fisher's band reading (sight 0.9, near) | 0.9 | 0 | 0 | | 0.27 / 0 |
| the expert's glut (0.7, near) | 0.7 | 0 | 0 | | 0.21 / 0 |
| eels in the dark (sight 0.6, night) | 0.03 (sleeping there) | 0 | 0 | 0 | |
| the touch to the doer (touch 2.0) | 1.0 for the doer | | | | |
| the window near (everyone at the place, 0.35) | 0.35 for each expert or elder, wherever they are at the place | | | | 0.105 |
| the first heavy rain (everyone, 0.4) | 0.4 for anyone | | | 0.998 | 0.12 |
| the expert's eel night (everyone, 0.3) | 0.3 for each expert | | | | 0.09 |
| {water} in spate (sight 2.0) | 1.0 | 0.6 | 0.1 | 0.72 | 0.3 / 0.03 |
| {water} in flood (sight 2.5) | 1.0 | 0.75 | 0.125 | 0.80 | 0.375 / 0.0375 |
| ice along the edges (sight 1.2, dawn) | | 0.36 | 0.06 | 0.52 | |
| frozen over (sight 2.0, dawn) | | 0.6 | 0.1 | 0.72 | |
| the ice going out (sound 1.5, dawn) | 0.75 | 0.68 | 0.15 | 0.86 | the same |
| otter tracks (sight 0.6, near) | 0.6 | 0 | 0 | 0 | 0.18 |
| the carried catch (sight 1.0, at the carrier's house ground) | the household 1.0; one on that ground that day 0.5; a neighbour whose house stands there 0.3; next door 0.3 | | | 0.96 of the other 9 adults when every house is on the Street | |
| smoke from the smoke hut (sight 1.5) | 0.75 on its parcel | 0.45 | 0.075 | 0.61 | 0.225 / 0.02 |

What the table says: on the first night of a run at Eelmouth the village learns of it at dawn only through herons (where a heronry
is), the roar (where the run came on a spate) and the night's splashing (salmon); an expert reads the eel night from the sky. Those who
work at the water learn it by day; everyone else hears of it from the carried catch that evening and from each other. A village whose
houses stand by the water learns much sooner. That is the layout working through the rule, not a flaw to tune away.

### 7. Checked against the guide and D2-269

| Test (guides/senses.md) | How the bundles meet it |
|---|---|
| reads only what the state holds | each row names its state (§1, §2 to §5); the moon is not in state ("the night coming on dark" is the season and the weather); the carried catch reads hands, weight and the day's work; the weir's overflow names its trace as a presentation |
| points at the right thing | the fisher's spate reading goes only to those with traps of their own in a river parcel; the carried catch only where fish are in hand after work at the water |
| worth acting on | each row sits at a lead an act can use: dawn rows before the day's set and tend; by-day rows for the next night; lore for the season's making |
| a change, not a standing fact | when the eels come is lore; the sign is this year's run coming, passing, thinning, ending |
| a bundle across senses | each state has sight, sound or smell, touch for the doer, a lingering trace and a conditional row (fog, rain, ice) |
| the chance from the rule | `own` set, chances intended (§6), checked at build |
| concrete, counts only where people count | bands and scale words, a creelful, "half of them or more" |
| not repeating what the doer knows | results are U2's; the carried catch is for others |
| quiet when nothing matters | no ambient river line in spate; the quiet-water row only between runs; slackening and ending once |
| no act or feeling put on a person | no row says anyone hurried, rejoiced or ran |
| D2-269 | the five directing rows reworded (§4); the expert's rows say what is happening and what it implies |

## Code changes

| File, line | Change | Owner |
|---|---|---|
| engine/wild.py:3072-3183 (`_runs_night`) | write the river's record (§1); the dawn events of §2.2 and §3 for the next morning, after `RU.advance`; `river_now` | 37.2 |
| wild/gear.py:172-196 (`share_run`, `_pass`) | also return what each gear turned away (kg over its room) | 37.2 |
| wild/runs.py:316-432 | the bands (`band(st, g, kind, n, year)`), the year's best night, `first`, and `run_lore(w, node)` for U9 | 37.2 |
| wild/kinds.py:403-413 (WEATHER_LEADS), :888-902 (RUN_SIGNS), :534-536, :389, :412, :894 | a `RIVER_SIGNS` table by state and band (the rows above, own, sense, reach, who, when); the eel lead moved to the dawn events; the great freeze by ice; §4's rewording | 37.2 |
| engine/signs.py:2417-2513 (`_wild_river`) | read the record; emit the banded rows, the flow, the ice, the otters, the weir's trace, the fen | 37.2 writes, 37.4 reviews |
| engine/signs.py:888-902 (PERSON), :1107-1145 (`person_context`) | the carried-catch rows (`x.catch_load`, `x.from_water`, `x.creel`), the carrier excluded, the spot at the house ground | 37.4 |
| engine/signs.py:576, :578, :686, :691, :104; data.py:167 | the sky's river rows replaced by §3.1; the resident fish rows guarded and given `own`; the reap row reworded; the ambient by flow | 37.4 |
| engine/perceive.py:350 (`dawn`) | read a dawn event's `knows` and `lay` as the evening does | 37.4 |
| engine/perceive.py:289 (`practised`) | the "fish" rung: any water craft from a rough idea up, via `reads_as: ["fish"]` on each water technique | 37.4 |
| engine/keeping.py (U4's containers) | the keeping rows of §5 | 37.2 writes with U4, 37.4 reviews |

The river's senses are one unit of the water package (D2-244; feature_packages.md §5): rows as data beside `RUN_SIGNS`, a context for
the water, the record written by the river's night.

## Tests

Per the guide's checklist step 5:

- `test_river_record_is_kept_and_agrees_with_the_wreck`: the record's flow is the class the wreck and the wear used that night.
- One test per bundle: near certain at the water in daylight for the plain rows; rarer next door and from the Street; fog lowering
  sight and not sound; the night rows at night only; the lingering rows the day after; the conditional rows only under their state.
- `test_dawn_river_rows_reach_the_houses_by_the_rule`: on an eel cue night under the climate, the expert's eel night reaches an expert
  at the Street at about 0.3; under `runs_set_nights` it fires on a set night and never on rain alone; the herons row reaches someone
  of 12 at the Street at about 0.8 with a heronry and not at all without one.
- `test_the_carried_catch_reaches_the_village`: a bot tends traps at the Isel and carries 6 kg of fish home; the other households on
  the Street see the row about 0.3 to 0.5 each; the carrier never sees it; 3 kg fires nothing; fish from the store fires nothing.
- `test_bands_by_the_stations_year`: pulses of 1%, 5%, 12% and 25% of last year's tally read trickle, running, thick, glut.
- `test_no_sign_directs_an_act`: no row text in wild/kinds.py or the sign tables of engine/signs.py carries an imperative of an act
  (a short list: "set the", "net them", "draw the", "bring it in", "must be", "lift the", "take them").
- `test_ice_rows_follow_U1s_ice`: edges, over, thaw and the great freeze's two texts.
- The whole cybertron2 suite (`python3 -m pytest -q tests/ -k cybertron2 -p no:cacheprovider`); a bot run and its replay with no
  mismatches.

**What live runs should read** (D2-297: the signs come in with the rest of the wave; read against the null arm with an end-state
reading): the share of sign lines acted on by row (the guide's measure: two content words of the line in that day's reasoning, plan
or speech), and above all whether households that never went to the water set traps the day after a carried-catch row; the night of
the run on which each household first set; how often traps are moved to the fen on a spate dawn.

## Basis rows needed

| Row | Value | Mark |
|---|---|---|
| A run's bands | trickle under 2%, running 2 to 8%, thick 8 to 20%, glut over 20% of the station's year | calibrate (river_signs §1.1) |
| The carried catch | 5 kg or more of fresh fish (after work at the water) or fresh meat (after a hunt) in hand at evening; "as much as they can carry" from 10 kg | default (W-81 question 13) |
| Scale words | "scores of" 13 to 99; "a hundred and more" from 100 | default (river_signs §3) |
| One who fishes | any water craft from a rough idea up | open (question 2) |

## Gaps

- **The moon** is not in state: the eels' "dark of the moon" cannot be read; an engine gap for docs/engine_gaps.md (river_signs
  §2.12), the eel cue its first use. Not designed here.
- **A flood over the land** (environment systems, W-49): flood rows describe the river only.
- **Gulls** and birds other than herons at a run: none until a kind holds them (D2-265 kept herons by the heronry).
- **News from upriver** (a village above sees the run a day or more sooner, on its lag): carried by people only; no row.
- **Smell has no visibility** (guide, known gaps; D2-101): rain and wind do not touch the run's smell or the smoke hut's.
- **Keeping's rows wait on U4's state** (lots, the fire kept); the tan pits and retting on U10; vermin on U5.
- **The remembered good and thin years** (river_signs §4.2) need the history's yearly tally kept past two years: U9 and U11.

## Open questions for Zach

1. **The catch carried home as a sign** (W-81 question 13, not yet filed; W-72). Someone seen at the houses in the evening with a load
   of fresh fish, after work at the water, tells those who never went that a run is on; the same for fresh meat after a hunt.
   Options: (a) yes, for fish and meat over about 5 kg; (b) no: news of a run travels only by talk. Recommended: (a): it reads a body
   and a load, puts no act in a mouth, and is the missing reach from the water to the houses. Default taken: (a). Blocks: the run's
   village-wide bundle.
2. **Who reads the fishers' signs** (river_signs §7 item 9). Today a row for "those who know" needs the craft at the level "known", so
   in the low arm, where the adults have only a rough idea of the traps, no adult read the run's fisher's lines (02zzz2 §1a). Options:
   (a) any water craft from a rough idea up reads them; (b) "known" only, as now. Recommended: (a): a rough idea is knowing what a trap
   is for, enough to read a run. Default taken: (a). Blocks: the graded rows of every bundle (37.4's `practised`).

## Sources

- Code (main, 22 Nov): `cybertron2/engine/signs.py` (104, 576, 578, 686, 691, 783, 836, 888-910, 1107-1145, 1261-1264, 2361-2513),
  `engine/perceive.py` (216-300, 350-372), `engine/things.py` (20-35, 457-502), `engine/data.py` (167, 376-390, 957, 1010-1035),
  `engine/run.py` (393-423), `engine/keeping.py` (139-166, 236), `engine/wild.py` (1196-1275, 2211, 3072-3183, 3185-3228),
  `wild/kinds.py` (280, 355-361, 389, 399-413, 476-495, 534-536, 592, 882-902), `wild/runs.py` (195-300, 316-432), `wild/gear.py`.
- docs/cybertron2/proposals/river_signs.md (in full), hunt_fish_materials.md (§7.5, §9), w73_design/README.md, basis.md;
  docs/cybertron2/guides/senses.md; docs/review/37_growth/02zzz2_river_signs_audit.md.
- docs/review/37_growth/02zzzh_hunt_fish/wave3_taking.md (§4, §8 questions 12, 13), wave3_keeping.md (§2.6), wave4_people.md (§3.5.1),
  wave_conflicts.md (C12, E4), catch_basis.md (§0, §1).
- DECISIONS D4-35, D4-48, D4-53, D4-68, D4-71, D4-72, D4-74, D4-75, D2-101, D2-211, D2-215, D2-218, D2-231, D2-263, D2-264, D2-265,
  D2-268, D2-269, D2-279, D2-297; OPEN L-114, Q-78, L-141; WORK W-49, W-72, W-85.

*Current as of 22 Nov 2026.*
