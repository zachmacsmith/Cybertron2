---
id: docs/cybertron2/proposals/river_signs.md
kind: proposal
updated: "2026-11-22"
---
# River signs: the water as people sense it

*proposal · discussion. · `docs/cybertron2/proposals/river_signs.md`*

> The river holds far more state than anyone can sense (audit: review [02zzz2](../../review/37_growth/02zzz2_river_signs_audit.md)). A run is shown as two sight lines at the river parcel, read in the evening, one of them only in the dark and the other only to those who know the trap craft well. The ri


**Status:** discussion.

**Owner:** 37.2 (the wild, the water and the worlds), with 37.4 for the senses and prompt core where §7 names it. Thread: signs of
the river ([[W-72 Signs of the river|W-72]]), under the nutrition worlds ([[W-69 Nutrition worlds|W-69]]). It sits beside the fishing legibility fixes ([[Q-78 Whether to build the fishing legibility fixes|Q-78]]), whose ask it widens.

## Summary

The river holds far more state than anyone can sense (audit: review
[02zzz2](../../review/37_growth/02zzz2_river_signs_audit.md)). A run is shown as two sight lines at the river parcel, read in the
evening, one of them only in the dark and the other only to those who know the trap craft well. The river's flow shows only
through the local weather word. Several lines say the river is empty, broken or frozen when it is not. Fishers are seeded with
nothing about the year they live by, while farmers get the sowing times, their crop every day and a judged ripening date.

This proposal gives the water what the guide asks of every state (guides/senses.md):

1. **One record of the river's night**, kept for each village, so every sign and result reads the same ground truth (§1).
2. **Bundles of signs for each state of the water** (§2): a run coming, passing and slackening, by how thick it is; the flow
   from low to flood; ice and thaw; otters, herons and the fen; the weir full. Each bundle spans the senses, is seen at the water,
   next door and (for the plain ones) from the village, and is graded by familiarity. A draft register of texts is given.
3. **Acts that tell the truth about the water on an axis separate from their success** (§3): what was caught, and separately
   what the water held. Never "empty" unless the water is empty; losses named with what they cost.
4. **Seeded memory for fishers, matched to farmers'** (§4): the runs as family lore read from the engine's own river, a trade
   line that names the work, remembered good and thin years, and the crafts' sentences with their scale (the [[D2-251 Every technique, fitting and thing to build says what it does and why…|D2-251]] ladder).
5. **A nudge without counts** (§5): the signs that make the better act findable (more traps in a run, the weir shut, the lift at
   dawn, the glut kept) without telling anyone what to do.

It does not repeat the methods' fixes of 02zzy2 (hand fishing reaching the run, the set result naming one's traps, the net's
words, the weir's build line), which it assumes.

## The proposal

### 0. Rules carried from the guide

- Every line reads a state value and names the band or threshold that fires it (§2's tables). Where the engine does not decide a
  thing (a moon, a flood over the land, a gull), no line asserts it (§2.12).
- A sign is a change. The standing facts of the river (when the eels come, what a trap holds) go into memory and the craft's
  sentence (§4), not into signs.
- Each row sets `own`, sense, conditions and scope; the chance comes from the one rule ([[D4-75 Every perceived line about the world comes from the one noticing rule|D4-75]]). §8 gives the intended chances.
- Readings come in three rungs. **Anyone** (no key); **one who fishes** (`knows`: any of the water crafts, the trap, the weir or
  the net, from a rough idea up: §7 item 9); **the expert** (`expert:` the same crafts). The elder's rung (`elder`) for what a
  long life on the river remembers.
- No feeling or act is put on a person. People's talk is their own: the bundles give them something to tell, and nothing is
  written for them to say.

### 1. One record of the river's night

The river's night (`wild._runs_night`) already works out, for each village on the river, everything the signs need, and then
throws most of it away. Keep it, overwritten each night like `wild.eaten`:

```
wild.river[node] = {
  "day": d,
  "flow": "low" | "normal" | "high" | "spate" | "flood",       # tonight's, as the wear and the wreck used it
  "flow_was": ...,                                               # last night's (a change is read against it)
  "passed": {kind: heads},                                       # what passed the village's water tonight, by kind
  "band": {kind: "trickle" | "running" | "thick" | "glut"},      # §1.1
  "taken": {gear id: {kind: heads}},                             # by each weir, race and set trap (gear.share_run already returns it)
  "turned": {gear id: kg},                                       # what a full weir or trap turned away (gear.share_run's room)
  "swept": {cid: {kind: heads}},                                 # a trap's catch lost in a spate or flood
  "robbed": {cid: heads},                                        # an otter's take (robbed_by.n, already kept on the trap)
  "first": [kind], "last": [kind],                               # the year's first and last night of a run at this village
}
```

and one function, `river_now(w, node, day)`: the flow class for tonight, from the rain memory the state already holds
(`wild.state.runs.rain`) and the day's weather, which is drawn before the day starts and shown in "Now". It is the reading the
night uses (`runs.flow`), so a sign and a wreck can never disagree. **This answers the deferral "the river high or in spate as a
sign" ([[L-114 The river high or in spate as a sign|L-114]])**, which waited for the flow to be kept in state: the flow class is already a pure function of state. When the
river's own level is built ([[D2-215 The weir's runs the river's level, then re-measure|D2-215]], [[D2-218 Set traps in high water|D2-218]]: 37.2's to decide), it replaces the class behind the same function.

#### 1.1 How thick a run is

A run's band tonight is its heads passing the village against the station's year of that run (last year's tally, or at the first
year the quota and dues at the window's start): under 2% of the year a **trickle**, 2 to 8% **running**, 8 to 20% **thick**, over
20% a **glut** (calibrate). The bands, not the heads, are what the signs read: nobody counts the eels in a river.

### 2. Bundles by state of the water

Each table gives the sign, its sense and own, who reads it, where (W: at the water parcel, with `reach` near or around; F: the
fen or other parcels next to the water; V: anywhere in the village by the rule's far reach), when (dawn: read the morning it
happens, §6; day: rolled in the evening as now; night: sensed in the dark), and the state that fires it. The four kinds of the
guide are marked: doer, near, lingering, conditional.

#### 2.1 Eels running down (a pulse going down at the village tonight)

| Sign | Sense, own | Reads | Where, when | Fires on |
|---|---|---|---|---|
| "dark eels moving in the slack water under the banks of the Isel, all one way, downstream" | sight 1.2 | anyone | W around; day | band running |
| "the shallows of the Isel thick with eels, sliding over one another, all going down" | sight 1.6 | anyone | W around; day | band thick |
| "eels everywhere in the Isel, in the weed, under the banks, against the stakes: more than any hands could take" | sight 2.0 | anyone | W around; day | band glut |
| "the water at the Isel alive with eels in the dark, all going downstream" (kept) | sight 0.6, night | anyone | W; night | band running or more |
| "eels against your legs in the water, cold and strong, all going the one way" | touch 2.0 | the doer: anyone who worked in the water today | W; as it happens | band running or more |
| "eels on the wet grass of Eelmouth Fen at first light, working their way through it toward the river" | sight 1.2 | anyone | F (a fen or wet meadow next to the water); dawn | band thick or more, and rain on the night |
| "slime trails across the mud of the fen's paths, all toward the Isel" | sight 0.8 | anyone | F; lingering, the next day | the same, a day after |
| "a sweetish smell of fish and mud off the Isel" | smell 0.8 | anyone | W and F; day | band thick or more |
| "an eel run in the Isel: every trap in the water tonight will take what it can hold" | sight 0.9 | one who fishes | W near; day | band running |
| "a heavy run: a trap fills in a night now, and the rest go past it" | sight 0.9 | one who fishes | W near; day | band thick or more |
| "a run like this is most of a year's eels in a few nights: what is in the water tonight, and kept, is the winter" | sight 0.7 | expert | W near; day | band glut |

#### 2.2 Salmon and lampreys running up

| Sign | Sense, own | Reads | Where, when | Fires on |
|---|---|---|---|---|
| "salmon going up through the Isel, leaping at the shallows" (kept) | sight 0.9 | anyone | W; day | a pulse going up, 3 heads or more |
| "salmon lying close in the pool below the shallows of the Isel, their backs out of the water" | sight 1.6 | anyone | W around; day | salmon band thick or more |
| "heavy splashing from the Isel all night, fish throwing themselves at the shallows" | sound 2.0, night | anyone | V by steps; night, read at dawn | salmon band running or more |
| "lampreys on the stones of the shallows, clinging by their mouths against the current" | sight 1.0 | anyone | W; day | a lamprey pulse going up |
| "the salmon are running up the river at the Isel: a run night" (kept) | sight 0.7 | one who fishes | W near; day | as the first row |
| "salmon come up behind a spate and lie in the pools: a shut weir takes them; hands and nets seldom do" | sight 0.6 | expert | W near; day | salmon passing and the flow fell from spate or flood |

#### 2.3 A run coming

| Sign | Sense, own | Reads | Where, when | Fires on |
|---|---|---|---|---|
| "the first silver eels of the year in the Isel, fat and dark-backed, going down" | sight 1.5 | anyone | W around; day | `first` eel night at this village |
| "the eel run has reached the Isel: it will pass for many nights now" | sight 0.9 | one who fishes | W near; day | the same |
| "the nights drawing in, dark and still: the eels will move soon" | sight 0.7 | expert, elder | V; dawn | the eel window opens within two days (`RUNS` windows; the set nights where `runs_set_nights`) |
| "the Isel rising and dark after the first heavy rain in weeks" (moved to the water) | sight 1.0 | anyone | W; day | the eel cue (`rain_after_dry`), only where the runs read the weather |
| "an eel night: dark, wet and the water rising after the dry weeks; set the traps tonight" (kept, moved, gated) | sight 0.6 | expert | W; dawn | the same; and under `runs_set_nights`, a set night instead ([[D2-231 The runs world's runs on set nights|D2-231]]) |
| "the first salmon showing in the pool below the shallows" | sight 1.2 | anyone | W; day | `first` salmon night |

#### 2.4 A run slackening and ending

| Sign | Sense, own | Reads | Where, when | Fires on |
|---|---|---|---|---|
| "fewer eels each night in the Isel now: the run is passing" | sight 0.8 | one who fishes | W near; day | tonight's heads under half the run's best night at this village this year, and its window still open |
| "the eel run is over at the Isel for this year: the traps will take little now until next autumn" | sight 0.8 | one who fishes | W near; day after | `last` eel night, two nights past |
| "the eel run was thin this year at the Isel: about half of last year's" (kept) | sight 0.7 | one who fishes | W; the day after the window | as built |

#### 2.5 The flow

Rows fire on a change of class (rising or falling against `flow_was`), or each day in spate or flood. They replace the sky's two
river rows (signs.py:576, 578), which read the local weather word and missed most of the 17 spate and flood nights of the runs
world.

| Sign | Sense, own | Reads | Where, when | Fires on |
|---|---|---|---|---|
| "the Isel low and clear, stones showing at the edges and weed trailing in the current" | sight 0.8 | anyone | W; day | fell to low |
| "the river too low and clear for the eels to move: they wait for rain" | sight 0.6 | expert | W; day | low, the eel window open, where the runs read the weather |
| "the Isel up and coloured, reed and sticks coming down on it" | sight 1.2 | anyone | W around; dawn and day | rose to high |
| "the Isel in spate, brown and roaring, tearing at its banks" | sight 2.0 | anyone | W, F; dawn and day | spate |
| "the roar of the Isel in spate, heard from the houses" | sound 2.5 | anyone | V by steps; dawn and day | spate or flood |
| "the Isel in flood, the whole width of it moving, whole branches turning in it" | sight 2.5 | anyone | W, F; dawn and day | flood |
| "the Isel louder this morning than the rain here explains: it is raining hard upriver" | sound 0.8 | expert | V; dawn | spate or flood tonight while the day's own rain is light (the catchment's rain against the village's) |
| "a spate: wicker traps in the main stream tonight will be torn away" | sight 0.9 | one who fishes | W near; dawn | spate or flood tonight, a trap of one's own in the river |
| "the current drags at your legs: you can barely keep your feet in it" | touch 2.0 | the doer | W; as it happens | high or more, one who worked in the water |
| "the Isel dropping and clearing, wrack and torn reed left high along its banks" | sight 1.0 | anyone | W around; lingering, two days | fell from spate or flood |
| "the river is falling: traps set now will stand" | sight 0.7 | one who fishes | W near; day | fell from spate or flood to high or less |
| "the gap shut in a spate: the river is piling against the wattle" | sight 1.2 | the weir's crew and one who knows the weir | W; dawn | the weir's gap shut and the flow high or more (wear x2 with the gap shut in high water, [[D2-210 The weir in sections, capped, with upkeep by the river|D2-210]]) |

The ambient "water running over stones in {name}" (data.py:167) becomes the flow's and the river's own: "the Isel sliding past,
slow and brown" for a big river at normal; nothing in spate (the spate rows say it).

#### 2.6 Ice and thaw

The engine lets the traps, the weir and the runs go on under ice, and the signs must not say otherwise (§2.12, open question 6).

| Sign | Sense, own | Reads | Where, when | Fires on |
|---|---|---|---|---|
| "the fen's pools skinned with ice, the reeds stiff with rime" | sight 1.0 | anyone | F; dawn | the small waters frozen (`frozen_run` 1 or more) |
| "ice along the edges of the Isel, the main stream still running black between" | sight 1.2 | anyone | W around; dawn | `frozen_run` 1 to 3 on a big river |
| "the ice going out of the Isel in grinding plates" | sight 1.5, sound 1.5 | anyone | W; V by sound; dawn | the first day not frozen after `frozen_run` 2 or more |
| "the ice going out: it will tear at the weir's stakes" | sight 0.8 | the weir's crew and one who knows the weir | W; dawn | the same, a weir standing (thaw wear x2) |
| "the river frozen from bank to bank; birds lying dead on the ice" (reworded unless the engine stops fishing) | sight 1.2 | anyone | W; dawn | the great freeze; reworded to "the Isel frozen far out from both banks, a black lane of water moving in the middle" |

#### 2.7 Otters

| Sign | Sense, own | Reads | Where, when | Fires on |
|---|---|---|---|---|
| "otter tracks in the mud below the bank of the Isel, webbed, with the drag of a tail" | sight 0.6 | anyone | W near; day | otters about the village (`ROB_SETS.least` or more), and the first day one has traps there, or a run passing |
| "an otter rolling and diving in the Isel in broad day, eating as it swims" | sight 1.0 | anyone | W around; day | otters about and band thick or more |
| "otters working this stretch: a trap left full overnight will be robbed" | sight 0.8 | one who fishes | W near; day | as the first row |
| "scales, heads and half-eaten eels along the bank of the Isel where the otters fed" | sight 0.8, smell 0.6 | anyone | W; lingering, the next day | a robbery or a thick run with otters about |
| the robbery itself: §3 (the setter's look names what was taken) | | | | |

#### 2.8 Herons and other fish-eaters at a run

Herons only where the land holds a heronry (`wild.sites`), so the sign reads a state; see open question 1.

| Sign | Sense, own | Reads | Where, when | Fires on |
|---|---|---|---|---|
| "herons standing all along the Isel, more together than you have seen, still as posts" | sight 3.0 | anyone | V (plain from far); day | a heronry at the village and an eel or salmon band thick or more |
| "herons flying down to the Isel from first light, one after another" | sight 2.5 | anyone | V; dawn | the same, the morning after a thick night |
| "the herons have left the heronry for the river: the fish are thick in it" | sight 0.6 | expert | V; dawn | the same |

#### 2.9 The weir

| Sign | Sense, own | Reads | Where, when | Fires on |
|---|---|---|---|---|
| "fish milling against the weir's wattle and turning back, its traps too full to take them" | sight 1.2 | anyone at the water (not the crew only, as now) | W around; dawn | `turned` over 0 for the weir tonight |
| "the weir's traps were full before morning: the rest of the run went past the gap" | sight 0.9 | the crew and one who knows the weir | W near; dawn | the same |
| "the weir's traps heaving with eels: scores of them" / "... a hundred and more" | sight (the look) | the crew | W; as looked | the catch's heads (§3: the count words) |
| the wear, the gap and the ice (kept: signs.py:531, 533; kinds.py:897) | | | | |

#### 2.10 The fen

| Sign | Sense, own | Reads | Where, when | Fires on |
|---|---|---|---|---|
| eels on the wet grass, slime trails, the pools skinned with ice (§2.1, §2.6) | | | F | |
| "the fen's dykes brim but lie still while the Isel tears past" | sight 1.0 | anyone | F; dawn | spate or flood, a fen at the water (only if open question 5 keeps the fen's traps meeting the run) |
| "traps in the fen's dykes stand when the river tears the rest away" | sight 0.7 | one who fishes | F near; dawn | the same |

#### 2.11 Resident fish (worlds that stock them)

- "the water at {nm} is quiet: few fish rising" (signs.py:686) fires only when no run passes. On a run night where the stock is
  low: "few fish of the Isel's own, but the run going through" (sight 0.8, one who fishes).
- "fish rising all along {nm}" (signs.py:691, `p` 0.06) gets an `own` (0.8) and fires on a rise past 0.75 K, not every day.

#### 2.12 What the engine does not hold, and the small fixes

- **No moon** is in state (Zach's "the dark of the moon"): the expert's eel night says "dark, still nights", read from the
  window and the weather. A moon is an engine gap (to add to docs/engine_gaps.md, with the eel cue as its first use).
- **No flood over the land** (environment systems phase 1, [[W-49 Environment systems|W-49]]): the flood rows describe the river, never the fields under it.
- **No gulls** as a kind: none is written (open question 1).
- **The brine spring** (signs.py:737) is in the place's own text; the sign row goes, as a standing fact.
- **"salmons"** (signs.py:2375 through `_kinds_word`): the plural from the kind's family words, "salmon".
- **The trap's nights done** are not "fouled and broken" (signs.py:1315, things.py:373): "wicker traps set in the water at the
  Isel, their nights done, the withies slack" (§3).

### 3. Acts that tell the truth about the water

Every act at the water gives two things: what one got, and, separately, what the water held, read from the river record and
graded by familiarity. The second never depends on the first: a failed act in a glut says it was a glut.

| Act | When | Result (draft) |
|---|---|---|
| **Fishing by hand** (after 02zzy2 fix 1: a run is reached with no resident stock) | a run passing, some taken | "The shallows of the Isel are thick with eels slipping past; your hands closed on two." (band words: §2.1) |
| | a run passing, none taken | "The Isel is full of running eels tonight, but they slid through your fingers: you took none." |
| | salmon passing, none taken | "Salmon were going up past you through the shallows, gone before your hands closed: you took none." |
| | no run, no resident fish | "No fish lie in the Isel to take by hand now." For one who fishes, and the eel window over: "...; its fish come down in the autumn run." Within two days of a window: "...; the eels come down soon." |
| | no run, resident stock at its refuge | "The fish of the Isel are fished out for now; nothing is running." |
| **Angling** | a run passing | "Your line took one fish of the Isel's own; salmon were going up past it all day." Where no resident fish are stocked, the act is refused with that reason before a rod is asked for (02zzy2 fix 1) |
| **Setting a trap** (02zzy2 fix 2 names one's other traps) | a run passing; one who fishes | "...; the eels are running: it will fill as fast as they come." |
| | no run; one who fishes | "...; nothing is running: it will take little until the eels come down." |
| | spate or flood tonight; anyone at the water | "...; the Isel is in spate: it may not stand the night." |
| **Lifting a trap** (take from its tag, or the lift of 02zzy §4) | full last night | "You took six eels from your trap T12 at the Isel (3.5 kg of fish, about a meal and a half). It was full by morning, and eels were still going down past it." |
| | part full | "You took two eels from your trap T12 at the Isel (1 kg, about half a meal); few came down last night." |
| | robbed | "You took two eels from your trap T12 at the Isel; an otter had been at it first: scales on the withies, three gone." |
| | nothing, no run | "Nothing in your trap T12 at the Isel: nothing ran last night." |
| | nothing, a run passed | "Nothing in your trap T12 at the Isel, though eels went down past it in the night." (one who fishes) |
| **A trap lost** (the setter's dawn line, by the rule as now) | swept | "The spate tore your trap T12 from its stake in the night, and the four eels in it with it." With traps elsewhere standing: "...; your traps in the fen stood." Flood says flood |
| | nights done | "Your trap T12 at the Isel has done its nights: the withies slack and sodden. Set again to fish on." |
| **Lifting the weir** | | "You took 150 kg of fish from the weir's traps at the Isel: about two hundred eels and a dozen salmon, about 70 meals. They were crammed: as much again went past the gap." The last clause from `turned`, for the crew |
| **The look at a catch** (things.py:348) | 13 heads or more of a kind | "scores of eels" (13 to 99), "a hundred and more eels" (100 or more), so the look shows the scale |
| **Netting** | | 02zzy2 fix 3 |

The meals come from the food values and the weight already in the result, as the store line gives them ("food worth 17 meals").

### 4. Seeded memory for fishers, matched to farmers'

#### 4.1 The year, as family lore

Farmers are seeded with one line of family lore, the sowing times, read from the engine's own growth (lore.py, [[D4-105 Sowing windows are lore, not rules|D4-105]]). Fishers
get the same thing for the runs, read from the engine's own river:

- **A lore row `runs`** (data.LORE), given to every adult of a household that knows a water craft (trap, weir or net) at any
  level, kept for good with the source "family lore".
- **Its text from `wild.runs.run_lore(w, node)`**, as `lore.sowing_times` reads growth: for each kind that runs the village's water,
  the season and part of it the run passes this village, how long it passes and when it is thickest, worked out from a year of the
  river's calendar (the set nights where `runs_set_nights`, the climate's cue otherwise), and the station's position (a low station
  sees the run for many nights). The lore is the engine, as a family has learnt it.
- **One line a run, each within the 25-word cap**, so nothing is cut. The farmers' sowing line is cut at 25 words today (memory.py:135,
  158: the shown line ends "rye does best sown late in autumn, and well in", and every farming world has lost the beans and the
  winter rule). The same fix serves both: lore is seeded as one line a crop and one line a run (proposed), or lore lines are exempt
  from the cap (alternative).

Draft lines for Eelmouth (runs world, set nights, low on a big river):

1. "The eels come down the Isel in the first dark nights of autumn and pass for about ten nights; then none till next autumn."
2. "The salmon come up the Isel after the autumn spates and into early winter, leaping at the shallows; a shut weir takes them."
3. "A few lampreys come up the Isel in spring, after the spates."
4. "Between the runs the Isel holds little: the year's fish come in a few weeks, and what is not kept then is lost."

And by craft, to those who know it:

5. (the trap) "A wicker trap holds about twenty eels; on a run night it takes a few, on a thick one it fills. Lift at dawn, before
   the otters."
6. (the weir) "A weir across the Isel takes a share of every fish that passes; in a run its traps fill in a night. Lift each dawn."
7. (smoking or salting) "Fresh eels go bad in two or three days; a glut is smoked, salted or dried at once, or it is lost."

In a world whose runs read the weather, line 1 becomes "... on the first dark wet nights of autumn after dry weather". Each figure
in them is the world's: the trap's hold (`WATER_WORKS.trap.hold`, 10 kg) over an eel's weight; the run's nights at this station;
the spoil rate of fresh fish.

Length: the farmer's lore is one line of the times (about 50 words uncut); the fisher's is four short lines of the times and one
or two of the craft (about 90 words), longer because the farmer sees his crop and its signs daily while the fisher's water has
nothing to show between runs, so the craft lines carry the scale.

#### 4.2 Remembered years

The generator writes "Hard winters you remember, when the frost came early and the stores ran out: last winter." from the
history. Add the river's years from the wild history (`wild.HISTORY_YEARS`, ten years before the run): "Good eel runs you remember,
when the traps filled every dawn: three autumns ago." and "Thin ones: last autumn." The history's run tallies are kept by year for
this (the state keeps two years; the history keeps a yearly summary). Only for those of a household that fishes.

#### 4.3 The trade line

`generate.py:378` names the line's first two crafts, basic or not, so every adult of the runs world is "By trade: sowing a field
broadcast and reaping a crop". The trade is the line's first two crafts that are not basic and whose pack is on: at Eelmouth,
"By trade: setting wicker traps in the water and building a fish weir". With farming off (`packs_off: [farming]`, 02zzz), the
sowing crafts leave the list on their own.

#### 4.4 The crafts' sentences, by familiarity ([[D2-251 Every technique, fitting and thing to build says what it does and why…|D2-251]])

[[D2-251 Every technique, fitting and thing to build says what it does and why…|D2-251]] decided one pattern for every technique (a sentence for one who has heard of it, what it gives back for a rough idea, the
specifics for one who knows it); it is built under [[W-70 Verbs and livelihood archetypes, before the engine rework|W-70]] (37.4 with Zach). The water's content, to go in when the pattern is built:

| Craft | Heard of it | A rough idea | Knows it |
|---|---|---|---|
| Wicker traps | "a wicker trap set in the water to catch eels by night" | "one trap a setting; best on run nights, when it fills; lift it with take, from its tag" | "holds about 10 kg, about twenty eels; fishes 8 nights; on a run night it takes a few eels, more as the run is thick; a spate tears away about half the traps in the main stream, a flood most; an otter robs a full trap left overnight" |
| The weir | "stakes and wattle across a river, to catch the fish that run" | "takes a share of every run passing, all lifted in one act each morning; its gap shut to fish" | "12 timber and 24 units by two; the first section takes about a third of a run passing, up to about 100 kg a night, each added section more; wears with the river, most in spate with the gap shut and in ice; mended with timber" |
| Fishing by hand | "groping for fish under the banks" | "takes a little of the resident fish, or of a run passing close in" | "about half a fish a unit at a full stock; in a run, a few heads at best" |
| Angling | "a rod and line" | "takes the water's own fish, not the runs" | "about a fish and a half a unit at a full stock; a rod of timber and hide lasts 30 uses" |
| Smoking | "fish hung in smoke to keep" | as now (data.py smoke fish `manual`) | as now |
| Salting | "fish packed in salt to keep" | "a batch of 4 fish to 1 salt" | the rate, when [[Q-73 Whether salting fish and meat stays at 4 kg a unit of work|Q-73]] settles it |

#### 4.5 Familiarity with the kinds

"you know the eel ... of these parts well: their ways, their signs, where they lie" (methods.py:250) stays, now with something
behind it: the lore lines and the expert's rows are those ways and signs.

### 5. The nudge without counts

What makes the better act findable, each from state, none an instruction:

- **Scale in a run.** "more than any hands could take" (glut), "a trap fills in a night now, and the rest go past it" (thick, one
  who fishes), "eels were still going down past it" (a full trap's lift). Together they say one trap is small against a run.
- **The weir.** "fish milling against the weir's wattle ... too full to take them" to anyone at the water; "as much again went past
  the gap" to the crew. The weir is the method that works (02zzy2), and a full weir is the reason for another section.
- **The lift at dawn.** The otters' rows ("a trap left full overnight will be robbed") and the robbed lift line with its count.
- **The spate.** "wicker traps in the main stream tonight will be torn away" at dawn, then "the river is falling: traps set now
  will stand". A wreck reads as a night to wait out, not a reason to give up (02zzy §2c).
- **The glut kept.** The lore's keeping line, the store's spoil sign (as built), the expert's "what is in the water tonight, and
  kept, is the winter".
- **The year.** The lore lines, the run coming (§2.3) and the run ending (§2.4): when to be ready and when to stop.

### 6. Where it is seen and when

- **At the water** (W): sight with reach near or around, by day, rolled in the evening as now.
- **Next door** (F): the fen and any parcel next to the water, through reach around.
- **The village** (V): sound by steps (the spate's roar, the salmon in the night) and the sights plain from far (herons, own 2.5
  to 3). §8 gives what the rule makes of them.
- **At dawn.** The river's dawn rows (marked "dawn") are written by the river's night as dawn events (`w.event(..., dawn=True)`,
  with `about` the water parcel, its sense and own), which `perceive.dawn` already reads by the one rule from where one is. So a
  run, a spate or ice reaches people the morning it matters, not the morning after. Graded rows at dawn need `perceive.dawn` to read
  an event's `knows`/`lay` as the evening does (a small change in the core, §7 item 8).
- **Results** reach the doer at once (§3).
- **People carry the rest.** Nothing is written for them to say.

### 7. The code, by seam and owner

Kept to the engine's seams ([[D2-244 The engine's reworking into feature packages|D2-244]]): the river's senses are one unit of the water package (feature_packages.md §5: rows added to
the core's subject tables, a context namespace for the water, its process in the night), listed together here so the cut can move
it whole.

| # | Piece | Files | Owner |
|---|---|---|---|
| 1 | The river record and `river_now` (§1): written in `_runs_night`; `gear.share_run` returns what each gear turned away | engine/wild.py, wild/gear.py, wild/runs.py | 37.2 |
| 2 | The bands (§1.1) | wild/runs.py, wild/kinds.py (`RUN` bounds) | 37.2 |
| 3 | The bundles' rows (§2) as data, beside `RUN_SIGNS` (a `RIVER_SIGNS` table keyed by state and band) | wild/kinds.py | 37.2 |
| 4 | Their emitter: `_wild_river` extended with a `river_context` (the water namespace) and the dawn events | engine/signs.py, engine/wild.py | 37.2 writes, 37.4 reviews (signs.py is the core's) |
| 5 | The sky's river rows replaced, the ambient by flow, the WILD fish rows guarded, "salmons", the spent trap's words, the brine row | engine/signs.py, engine/data.py | 37.4 |
| 6 | The results (§3): hand fishing and angling (`run_take`'s words, `knowledge.ready`'s refusal), the set (`set_work`), the lift and the look (`_take`, `_lift`, `look_text`, `catch_words`) | engine/wild.py, engine/knowledge.py, engine/verbs.py, engine/things.py | 37.2 (wild.py), 37.4 (the rest) |
| 7 | The lore (§4.1): `run_lore` from the engine's river; the `runs` row; the cap fix for lore lines (farmers' too) | wild/runs.py, engine/data.py (LORE), engine/lore.py, engine/memory.py | 37.2 (`run_lore`), 37.4 (lore and memory) |
| 8 | Dawn events graded by `knows`/`lay` | engine/perceive.py | 37.4 |
| 9 | A rung for "one who fishes" from a rough idea up, and the weir reading as the trap (`reads_as`) | engine/perceive.py (`practised`), engine/data.py | 37.4 |
| 10 | The remembered years and the trade line (§4.2, §4.3) | engine/generate.py, engine/wild.py (the history's yearly tally) | 37.2 |
| 11 | The runs world's people (no farming trade, the fallback example) as 02zzy's item 5 | specs/make_nutrition_runs.py | 37.2 |
| 12 | The crafts' sentences (§4.4) when [[D2-251 Every technique, fitting and thing to build says what it does and why…|D2-251]]'s pattern is built | engine/data.py, wild/methods.py | [[W-70 Verbs and livelihood archetypes, before the engine rework|W-70]] (37.4 with Zach); content 37.2 |

Tests: one per bundle (the guide's checklist step 5: near certain at the water in daylight, rarer next door and from the Street,
fog lowering sight and not sound, the dawn rows the morning of, the bands), the results' two axes, the lore's text against a world
with set nights and one with the cue, and the cut line fixed; then the cybertron2 suite, a bot run and its replay.

### 8. Intended chances, by the rule

Ordinary eye, clear day, attention 1, from `NOTICING` (presence 0.5 having worked there, 0.3 next door or crossing, 0.05 anywhere
else for own 0.8 or more; sound carries 0.5, 0.45, 0.2, 0.1 by steps; the Street is three steps from the Isel at Eelmouth; fog
x0.3 on sight; night sight x0.1, night sound x1.2). "Someone" is the chance that at least one of 12 people at the Street notices.

| Row | At the water | Next door | From the Street | Someone, from the Street | Fog (water / next door) |
|---|---|---|---|---|---|
| Eels thick in the shallows (sight 1.6, around) | 0.8 | 0.48 | 0 | 0 | 0.24 / 0.14 |
| Herons all along the river (sight 3.0) | 1.0 | 0.9 | 0.15 | 0.86 | 0.45 / 0.27 |
| The spate's roar (sound 2.5, loud) | 1.0 | 1.0 | 0.25 | 0.97 | the same |
| The Isel in spate (sight 2.0) | 1.0 | 0.6 | 0.1 | 0.72 | 0.3 / 0.18 |
| Salmon splashing all night (sound 2.0, night) | 1.0 | 1.0 | 0.24 | 0.96 | the same |
| Eels on the fen's wet grass (sight 1.2, at the fen; fen sight 0.6) | 0.22 (the Isel is next to the fen) | 0.36 on the fen | 0.04 | 0.36 | 0.07 at the water, 0.11 on the fen |
| Otter tracks (sight 0.6, near) | 0.6 | 0 | 0 | 0 | 0.18 |
| A fisher's reading (sight 0.9, near) | 0.9 | 0 | 0 | 0 | 0.27 |
| The doer's touch (touch 2.0) | 1.0 for the doer | | | | |

These are the intended values; the build checks them through `perceive.chance_of` and adjusts `own`, never the result (guide
step 4).

## Why

- **The engine's river is invisible.** The audit (02zzz2 §1, §4): a run seen only at the water in the evening, the flow only in the
  local weather word, nothing of a run coming, slackening, the otters, the weir's overflow or a loss's cost.
- **Several lines mislead** (02zzz2 §2): the "no fish" refusal, "nothing caught" with no word of the water, the spent trap as
  "broken", the weir's hundred as "a dozen or more", the river "frozen" while it fishes.
- **The agents act on what they are shown.** Every model drew the same conclusions from the same lines (02zzy §3); a sign that
  changes what to do today is acted on almost every time, a standing fact almost never (guides/senses.md, "It is worth acting on").
- **Fairness with farming.** Zach: "How much info are farmers already seeded with, and so fishing seems fair too?" (02zzz2 §3).
- **Zach's brief** (21 Nov): signs "should realistically reflect the numbers and state on an independent axis from their actions",
  "definitely shouldn't say the river is empty if it is not", "subtly nudge toward the kinds of activities that might be more
  useful", "all parts and different conditions should have whole bundles of signs like the design intent goes".

## Alternatives considered

- **Tell the fishers the numbers** (the run's heads tonight, a trap's expected take). Rejected: Zach, "still no count should be
  [needed]"; bands and people-scale words (a basket, a few, scores) carry it.
- **A single run line shown to the whole village at dawn.** Simpler, but one line is not a bundle ([[D4-48 A state shows itself as a bundle of signs, not one line|D4-48]]), and it would skip the
  rule ([[D4-75 Every perceived line about the world comes from the one noticing rule|D4-75]]). The bundle gives the same reach through the rule's far rows (herons, the roar), with misses and differences.
- **Wait for the river level ([[D2-215 The weir's runs the river's level, then re-measure|D2-215]]) before any flow sign** (as [[L-114 The river high or in spate as a sign|L-114]] deferred it). Rejected: the flow class the night already
  uses is in state; a sign that reads it cannot disagree with the wreck. The level replaces it later behind one function.
- **Put the runs in a sign each season** rather than lore. Rejected: when the runs come is a standing fact (guide rule 3); signs
  are for the run coming this year (§2.3).
- **Make hand fishing take more of a run** so that the first act agents try pays. Not this proposal: a calibration for Zach
  (02zzy2 fix 1).

## Open questions

1. **Birds at a run.** Herons only where the land holds a heronry, as proposed, or also "the birds working the water" (gulls by a
   big river or the sea) as a named presentation of a thick run with no bird kind behind it, as "crows and magpies going down" over
   a snare's catch already is? Recommended: herons by the heronry only; no gulls until a kind holds them.
2. **The flow for signs now** ([[L-114 The river high or in spate as a sign|L-114]]): read the class the night already uses, before the river's level ([[D2-215 The weir's runs the river's level, then re-measure|D2-215]]) is built?
   Recommended: yes, behind `river_now`, closing [[L-114 The river high or in spate as a sign|L-114]].
3. **Dawn rows for the river** (a run, a spate, ice reach people the morning they matter, through dawn events by the rule)?
   Recommended: yes, for the river's states only, with `perceive.dawn` reading `knows` and `lay` (37.4).
4. **The fishers' lore** as family lore kept for good, like the sowing lore, to every adult of a household that knows a water craft;
   one line a run; and the farmers' sowing lore split one line a crop so it is no longer cut at 25 words? Recommended: yes to all.
5. **A trap in the fen meets the river's run and is never wrecked** (wild.py:965, 3160). Intended, so the fen is the safe place
   to set in a spate and a sign may say so; or a side effect to fix in the engine? Recommended: intended for eels (they run through
   the dykes), at a lower share than the river (calibrate).
6. **Ice.** The engine fishes on under a frozen river. Reword the frozen signs to an open lane (proposed), or make a freeze stop
   the traps and the run's take (an engine change)? Recommended: reword now; the engine change with the environment systems' ice
   ([[W-49 Environment systems|W-49]]).
7. **How plain the nudge.** May the expert's rows say "what is in the water tonight, and kept, is the winter" and the fisher's "the
   rest go past it", or only show the overflow and leave the reasoning to them? Recommended: the rows as drafted, readable only by
   those who fish.

## Affects

- **Spec:** information/signs.md (the river's bundles, the dawn rows), information/noticing.md (dawn events graded by `knows`),
  the water's spec under environment/ (the river record, `river_now`); knowledge/lore (the runs lore, the cap on lore lines).
- **OPEN:** closes [[L-114 The river high or in spate as a sign|L-114]] (the river high or in spate as a sign) if question 2 is answered yes; widens [[Q-78 Whether to build the fishing legibility fixes|Q-78]] (the fishing legibility
  fixes); relates to [[Q-77 Whether to tune how often the river reads spate or flood now|Q-77]] (how often the river reads spate or flood), [[Q-73 Whether salting fish and meat stays at 4 kg a unit of work|Q-73]] (salting's rate), [[W-70 Verbs and livelihood archetypes, before the engine rework|W-70]] ([[D2-251 Every technique, fitting and thing to build says what it does and why…|D2-251]]'s ladder).
- **docs/engine_gaps.md:** a moon (the eels' dark nights); a flood over the land ([[W-49 Environment systems|W-49]]).
- **guides/senses.md:** the river under "Known gaps" until built; the bundle tables as a second worked example.
- **Code:** §7.

## History

- 22 Nov 2026: accepted in part: [[D2-265 The river's signs|D2-265]] (The river's signs (proposals/river_signs.md), as answered: herons at a run where).
- **21 Nov 2026: drafted at Zach's request** (37.2, subagent), from the audit 02zzz2. Zach (21 Nov): "Fishing is currently
  terribly low right now. I think (a) we need to add a richer tapestry to potential signs. If they are in the rivers or near and in
  [the fen] etc their interactions should realistically reflect the numbers and state on an independent axis from their actions.
  E.g. if they hand fish and fail but during a run it should maybe say something along the lines of 'the river teems with fish but
  your hands aren't enough to catch' or that sort of gist, and definitely shouldn't say the river is empty if it is not. I do also
  think fishing people should be seeded with the longer term memories that the runs come and should be prepared for with weirs
  etc. How much info are farmers already seeded with, and so fishing seems fair too? Actually check and compare. But yeah I think
  signs need to be fleshed out a lot more. Doesn't need to necessarily make everything way more obvious, because still no count
  should be [needed], but should reflect the ground truth and not mislead, and if anything subtly nudge toward the kinds of
  activities that might be more useful. Dig into all the different types of state of the river and how much is currently
  reflected in signs. Ideally all parts and different conditions should have whole bundles of signs like the design intent goes."

## Sources

- The audit: review 37_growth/02zzz2_river_signs_audit.md; with 02zzy_why_they_did_not_fish.md, 02zzy2_fishing_methods_compared.md,
  02zzz_live_runs_world.md, 02zzw_water_fixes.md.
- docs/cybertron2/guides/senses.md; proposals/river_and_water.md (brief 5), signs_pass_17nov.md, feature_packages.md §5, §9.
- DECISIONS [[D2-209 Brief 5 (river and water) is built|D2-209]], [[D2-210 The weir in sections, capped, with upkeep by the river|D2-210]], [[D2-213 A set trap holds at most about 3 food a night|D2-213]], [[D2-215 The weir's runs the river's level, then re-measure|D2-215]], [[D2-218 Set traps in high water|D2-218]], [[D2-231 The runs world's runs on set nights|D2-231]], [[D2-244 The engine's reworking into feature packages|D2-244]], [[D2-251 Every technique, fitting and thing to build says what it does and why…|D2-251]], [[D2-258 The food values are put on one physical basis|D2-258]]; [[D4-48 A state shows itself as a bundle of signs, not one line|D4-48]], [[D4-53 Every sign and every event is noticed by the one noticing rule|D4-53]], [[D4-71 A slaughter shows itself|D4-71]], [[D4-74 Events and their aftermath show themselves as bundles|D4-74]], [[D4-75 Every perceived line about the world comes from the one noticing rule|D4-75]], [[D4-105 Sowing windows are lore, not rules|D4-105]].
- OPEN [[L-114 The river high or in spate as a sign|L-114]], [[Q-73 Whether salting fish and meat stays at 4 kg a unit of work|Q-73]], [[Q-77 Whether to tune how often the river reads spate or flood now|Q-77]], [[Q-78 Whether to build the fishing legibility fixes|Q-78]]; WORK [[W-49 Environment systems|W-49]], [[W-69 Nutrition worlds|W-69]], [[W-70 Verbs and livelihood archetypes, before the engine rework|W-70]], [[W-72 Signs of the river|W-72]].
- Code: engine/signs.py, engine/perceive.py, engine/things.py, engine/knowledge.py, engine/verbs.py, engine/wild.py, engine/lore.py,
  engine/memory.py, engine/generate.py, engine/prompt.py, engine/data.py; wild/kinds.py, wild/runs.py, wild/gear.py, wild/methods.py.
- The live runs: scratchpad `live/runs_{low,medium,high}/`.

*Current as of 21 Nov 2026.*
