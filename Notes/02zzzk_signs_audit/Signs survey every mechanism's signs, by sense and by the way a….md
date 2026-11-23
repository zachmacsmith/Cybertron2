---
id: docs/review/37_growth/02zzzk_signs_audit/survey.md
kind: note
updated: "2026-11-23"
---
# Signs survey: every mechanism's signs, by sense and by the way a person meets them

*note · `docs/review/37_growth/02zzzk_signs_audit/survey.md`*


23 Nov 2026. Session 37.2, a subagent on thread [[W-103 Signs and what people can know of the state of things|W-103]] (records: [[W-103 Signs and what people can know of the state of things|W-103]], [[W-104 Build the after-runs list from live run 1|W-104]]). Zach asked for "a survey of the current state of all the various different types of signs and how each different mechanism has different signs across the full distribution of attending to working with passing by etc". The design that follows from it is [design.md](design.md).

**Read with:** [guides/senses.md](../../../cybertron2/guides/senses.md) (what a good sign is; every row below is judged by it);
[02zzzh_hunt_fish/sign_timing.md](../02zzzh_hunt_fish/sign_timing.md) (when signs reach people); [02zzz2_river_signs_audit.md](../02zzz2_river_signs_audit.md)
(the river on 21 Nov; much of it is built since, as u8's rows in `wild/river.py`). The rules kept throughout: experts' signs
observe and never direct ([[D2-269 Experts' signs are observations of what is happening now, which may…|D2-269]]); the engine never detects or announces a breach or a theft (Zach, [[L-174 Remove the engine's automatic detection and telling of breaches and…|L-174]]); rules are not
attendable ([[D2-341 Rules are not something one attends to|D2-341]]); the night's meal is told each morning ([[D2-342 Each morning a person is told what they ate the night before|D2-342]]).

**Sources.** Code on `main` as of 23 Nov (commit 8cbbf125), file:line below. Live run 1's five model arms in `/home/user/live1/`
(set A: `live1_A_pre`, `live1_A_old`, `live1_A_new`, 18 days; set B: `live1_B_pre`, `live1_B_new`, 40 days), measured by
[live1_signs.py](live1_signs.py) (output [live1_signs.txt](live1_signs.txt)) and every attend given in the two new-prompt arms with
what it resolved to ([attend_targets.txt](attend_targets.txt)). Lines shown at the hearth are read from each mind's `days[].saw_day`,
lines shown the next morning from `days[].saw`, in each run's `state.json`. No model calls.

## The short answer

- **The engine signs a great deal of its state, and the river now best of all** (u8's 18 dawn rows and 31 evening rows,
  `wild/river.py:173-252`). Crops, beasts, the dead, events and the wild kinds have full bundles across the four kinds of sense.
- **What it hardly signs are the second-order facts people plan by:** how long a store's fresh fish will keep, how many nights a
  trap has left, what the weir turned away, how much a member ate, how a pool or a willow bed comes back, how worn a pan is. The
  state holds every one (`stores.rates`, gear pieces' `life` and `rot`, `river.record`'s `turned` in kg, the meal's draws, the
  stocks' S and K, `wear.used`); no row reads them, or a row reads only a yes or no.
- **Attending is mostly wasted in the new prompt.** People attended in 34% (set A) and 44% (set B) of turns, to specific things
  ("the soft salt fish in our Marsh House store", "Petronel, who is gaunt and unsteady"), but `perceive.resolve_target`
  (`perceive.py:659-687`) matches only an exact name, so **128 of 213 attends (60%) fell back to "the place in general"** and got
  the covers' ambient lines. Those lines are not grounded: "cattle lowing on the Leaze" was shown 88 times in set B's new arm and
  35 in set A's in a village with **no herds at all**, "the ring of picks from the Scar" 40 times where one man quarried on one day.
- **Nobody ever spent units to look harder: there is no such act.** Attending is free and one target a day; the only unit-spending
  looks are `watch` (a day beside a person, to learn) and a "search" (attending to the parcel one works on: attention x5,
  `things.py:548-555`). No row exists that only a closer look reads.
- **Working with a thing shows less than working at its place.** The "acting" pass (`perceive.py:598-613`) reads what one worked on
  at attention x6, but writes it only into beliefs, seen the next morning as "(you saw yesterday: ...)" in the layout; set things
  (traps, nets, the weir's traps) are excluded from it, so a fisher learns of his gear only from the tend result and the look.
- **The meal is unseen.** A full meal on an ordinary day writes no line; a hard day's says only "you ate 1.28, where a lighter day
  would have needed 1" (`run.py:629-648`). The store's draw shows only as the morning's diff, "roots -19.4 (now 31.1)"
  (`view.py:155-168`), and people read it as loss: "Roots are vanishing from the store, about 19 gone yesterday, so they may be
  rotting or mice are at them" (Oliver, set B new, day 3; Peter the same day: "about 19 a night, far more than we eat. That must
  be rot or mice"). Brook House's five ate 4.72 food that night, 17.9 roots at 0.263 a root; 1.5 roots spoiled (days.jsonl day 2).
- **Announcing and directing lines remain** in a few places (listed in §4): an expert's "watch the gap and you meet them", "a
  terrier or a raised floor", "go in with others or not at all"; the thief told "You think you were seen"; the witness given the
  exact quantity taken; the head told "Against the household's rule n".

## 1. How a person meets a sign: the modes

Every perceived line goes through one rule ([[D4-53 Every sign and every event is noticed by the one noticing rule|D4-53]], [[D4-75 Every perceived line about the world comes from the one noticing rule|D4-75]]; `perceive.chance_of`, `things.spot_chance`, `things.py:578-608`):
base chance x knack x own x the sense's visibility x presence x attention x the eye. The modes Zach named map onto its inputs and
onto when the line is shown (sign_timing.md):

| Mode | What the rule gives (NOTICING, `data.py:1150-1176`) | Shown | Code |
|---|---|---|---|
| **At dawn** | dawn events, by the rule from where one slept or the place | that morning, "This morning", before planning | `perceive.dawn` `perceive.py:366-397`; river `DAWN` `river.py:173-191` |
| **Working at the place** | presence by what the work draws: game 1.0, plants 0.7, herd or other work 0.5 | that evening's hearth, "What stood out" (5 at most, `NOTICE_MAX`, by salience and relevance) | `things._presence_here` `things.py:523-545` |
| **Working with the thing** | the parcel or building one worked on, attention x6 (`working`), up to 4 lines; not things, events or ambient | the next morning only, as "(you saw yesterday: ...)" in the layout or "Since your last morning" | `perceive.py:598-613`; `view.py:46-60`, `126-152` |
| **The act's own result** | not perceived: the result line | that evening ("Your day"), again the next morning | verbs, `placed.tend_one` `placed.py:208-296` |
| **Passing by** | crossing to where one worked, or one's own house's parcel: 0.3 | the hearth | `things.py:536-541` |
| **Elsewhere at the place** | 0.05, only for own 0.8 or more; sound and smell by steps (`carry`: 0.5, 0.45, 0.2, 0.1, 0.05; smell 0.5, 0.3, 0.12, 0.05, 0) | the hearth | `things.py:500-521` |
| **Next door** | 0.3, only for own 0.5 or more (sight); the carry above for sound and smell | the hearth | `things.py:542-544` |
| **In the village** | rows open to all at the node (the sky, `everyone`), through the open air | the hearth | `spot_chance` `everyone` |
| **Inside / of the household** | presence 1 for those who live in the house (a house's rows, `inside`), and things in one's own house x3 | the hearth; the house's own lines daily without a roll (`house_known`, `prompt.py:610-637`) | `things.py:596-602` |
| **Attending (free)** | one target a day: a person, building, parcel, herd, a tagged thing, the sky, "the village" (its layout) or "the place" (its ambient lines); presence at least 0.5, attention x5 (x3 for the place), up to 9 lines | that evening's hearth, "You paid close attention to ..." | `perceive.py:500-524`, `resolve_target` `659-687` |
| **Attending with units** | does not exist. The nearest: `watch` (a day beside a person: you learn their craft, they may feel it, `verbs.py:2619`); a "search" (attend to the parcel one also works: x5 instead of x3, `things.attention` `things.py:548-555`); a heap "looked over" is counted only when attended (`reach: count`, `signs.py:1429`) | — | — |
| **At the evening hearth** | everything rolled after the day's work, plus the day's results and talk | "What you saw today", "Your day" (`evening.py:77-93`) | [[D4-82 The day's sightings at the hearth|D4-82]] |
| **The next morning** | the night's events (a second pass that skips what the hearth showed), one's house and stores without a roll, the store's diff | "Since last evening", "Since your last morning" (`view.py:126-176`) | `run.py:1115` |
| **Told by someone** | only speech: nothing is passed on but what a person says (and lines passed on in care, [[D2-340 Passing on through care|D2-340]]) | the talk, the hearth | — |

Two consequences run through every table below. A sign of own under 0.5 is seen only on its own parcel; under 0.8, never from
elsewhere at the place. And a line about a thing one handles ("near", `reach`) is read only on that parcel, by the rule's close
look.

**Keys in the tables.** D dawn; W working at the place; T working with the thing (or its result); P passing by; N next door; E
elsewhere at the place; V the village (open to all); I inside (the household); A attending; H the hearth; M the next morning.
**Gaps**, marked in bold in the last column: **unshown** (state held that no sign shows), **no mode** (a mode with nothing to
see), **unknowable** (a sign stating what the person could not know), **advises / announces**.

## 2. The mechanisms

### 2.1 The river and the runs

| State held | Signs (file:line, sense, own) | Modes | Gaps |
|---|---|---|---|
| Flow class each night from the catchment's rain (`runs.flow`), last night's flow (`river.record` `river.py:113-159`) | low and clear (221, sight 0.8); up and coloured (225, sight 2.9, around); in spate (226, 2.0); in flood (227, 2.5); the roar (228, sound 3.3, and dawn 179); the current drags at one's legs (229, touch, doer); dropping and clearing (231, 2.4 around); falling: traps stand (233, fish, near); louder than the rain explains: raining upriver (dawn 183, expert, sound 0.8); gap shut in a spate (184, crew) | roar: D H at the houses (carries); sight: W P N; the drag: T (one in the water) | none in the flow; the old sky rows retired for river villages (`signs.py:575-579`, `not x.river`) |
| The runs as pulses by day, band against the station's year (trickle, running, thick, glut; `river.py:18-41`) | dark eels moving (194, 2.9 around); thick (196, 3.8); everywhere (198, 4.8); alive in the dark (200, 0.6, night); against your legs (202, touch, doer); the smell of fish and mud (204, smell 0.8); herons along the water (205); every trap takes a few (207, fish, near); a heavy run, most goes past (208, fish, near); most of a year's eels in a few nights (210, expert, near); salmon going up (211), lying in the pool (212, 3.8), lampreys (216), the first silver eels (218, 3.6) | W P N; the fish and expert rows only on the parcel (near); the dawn cue (eel night, 175-176) at D for experts, the place | **unshown:** the density in heads (a band only; the bands are judged against the station's own year, so a glut reads the same in a thin year and a fat one) |
| The window, the run coming (`RUNS`, `runs._window`) | the nights drawing in (dawn 174, expert, elder); the first heavy rain after the dry weeks (dawn 175, all) | D | fine ([[D2-269 Experts' signs are observations of what is happening now, which may…|D2-269]]: an observation) |
| Slackening, ended, the year's tally (`runs.tally`) | fewer each night (236, fish, near); the run is over (238, fish, near); the year thin or good (`kinds.py:906-907`, knows) | W, the day after the window | **no mode** away from the water: the tally read only on the parcel |
| Fish held below a shut dam | leaping at the dam (`kinds.py:905`, 1.2); crowding in the pool (906, knows) | W P N | fine; no mill in Eelmouth |
| The catch carried home (5 kg or more of fresh fish) | "{who} came up from {water} with their creel full" (`river.py:254`, `carried` 470-508) | P N E: others who see the carrier | fine |
| Ice: `water.ice` by water type (`water.py:116-165`) | fen pools skinned (dawn 185); ice along the edges, the main stream running (dawn 186); frozen over (dawn 187); the ice going out (dawn 188, sight and sound); it will tear at the weir (dawn 190, crew); "frozen from bank to bank; birds lying dead" (`kinds.py:536`, the great freeze) | D for all at the place | the great-freeze line still says the river is shut while traps and the weir fish on (02zzz2 §2) |
| `RUN_SIGNS` "down" and "up" (`kinds.py:903-906`) | — | — | dead rows: `_wild_river` skips them since u8 (`signs.py:2476`) |

### 2.2 The shallows and resident fish

| State held | Signs | Modes | Gaps |
|---|---|---|---|
| `res.shallows` {S, K} by water type (`water.py:21`, `79-115`): small fish, loach, crayfish at the margins; renews by season, not under ice | nothing darts in the margins (`signs.py:696`, 0.7, bare); fished over (698, 0.5, under 0.35 K); fry back, too small yet (701, 0.3, fish by hand knack); cold margins still till spring (704, 0.3); ice along the margins (707, 1.2) | W only (own under 0.8; under 0.5 not next door) | **unshown:** a fished-down pool coming back (S between 0.35 and 1, how many days to come back); plenty (no row above 0.75 K); the take's result line says kg, not the pool's state |
| `res.fish` {S, K}, one record a water body ([[D2-229 One fish stock per water body|D2-229]]) | quiet, few fish rising (687, rule p by thinness, eye); fished hard (689, angle knack); rising all along (692, p 0.06) | W | fine (now with "few fish of the Isel's own, but the run going through", `river.py:251`) |
| The refusal at the bare pool | "the shallows of X are fished out for now, and nothing is running" (`knowledge.py:247`) | T | fine (true) |
| The land memory | "you found little shallows left (summer day 4)" in the layout (`prompt.py:388-392`, `remember_land`) | T, then M daily | fine: a finding, dated |

### 2.3 The weir

| State held | Signs | Modes | Gaps |
|---|---|---|---|
| Sections {material, foot, level}, gap, crew, wear in `broke` (`wild/gear.py`; `prompt.py:410-424`) | the layout every day: "3 sections (timber sound, timber worn, timber worn); worked by Nichola, Peter"; stakes torn out (`signs.py:531`, 1.0); ice against it (533); the thaw will tear it (dawn, crew) | layout daily; sign W P N | **unshown:** how near a worn section is to failing (only the level word) |
| Its share of a run, its hold in kg, what it took (`river.record` `taken`), **what it turned away in kg** (`turned`, `river.py:143-151`) | crammed full: whatever comes down goes past (`signs.py:2531`, crew only, at the parcel); scales and torn weed piled against the wattle: more came down than its traps would hold (`river.py:246`, 2.9 around; 19 times in set A new) | full: W for the crew; turned: W P N | **unshown:** how much went past (kg held, shown only as a yes); the emptying result gives kg and a count capped at "a dozen or more" (`things.py:364-371`, `placed.py:355-376`) |
| The gap set | "the gap of the weir shut, the wicker traps in it" (`kinds.py:909`) | W P N, that day and the next | fine |

### 2.4 Set gear: traps, snares, nets, lines

| State held | Signs | Modes | Gaps |
|---|---|---|---|
| A set thing: method, gear pieces laid (each with `life` and `rot`, `gear.py:196-230`), state (fishing, idle, spent, up), its night (`run`, `full`), catch by kind and night, `robbed_by` (otter, n), `robbed` (a person), `lost` (spate, flood, thaw, rotted) | the setter's look (`signs.py:1328`, `things.look_text` 374-396: "four eels in your wicker traps at the Isel", "torn at the neck ... something has had what was in them", "lifted and emptied by someone, and put back crooked", spent); one who knows it (1330); a stranger's glimpse and close look (1332-1341); crows at a catch (1342); the otter's spraint and its reading (`kinds.py:914-915`); traps smashed in a spate (`signs.py:2538`, the setter); broken wicker in the reeds (2541, others) | W (the look needs the parcel); P N for the crows | **unshown:** a piece's remaining life and rot: `gear.state_words` (`gear.py:595-613`, "2 broken, wanting mending; the rest good for about 8 more nights set") is shown only in the old turn prompt (`prompt.py:774`), never in the beliefs view live run 1 used (0 lines in A new, 1 in B new); the made result says "good for about N nights set" once (`gear.life_words`) |
| The tend result | "You tended your wicker traps in Eelmouth Fen (T1, 6 wicker traps): an eel, about 0.5 kg of fish (food worth about 1 meal). Fish were running past them in the night. An otter had been at them first: scales on the withies, 1 gone. You set them again." (`placed.py:225-296`) | T (H, M) | **unknowable:** "1 gone" counts what an otter took, which the setter did not see; **unshown:** how near each piece is to wearing out (only "worn past use and wants mending" once broken) |
| The remembered line | "your wicker traps at the Isel (T2) (6 standing), with an eel caught in them (as you saw it on summer day 4)" (`things.set_line` `407-441`) | M, "Lying about, that you know of" | fine |
| Iced gear | "The water is frozen at the edges: nothing has come to them" (`placed.py:271`); "frozen in" (`things.py:430`) | T | fine |
| Working with gear | set things are excluded from the acting pass (`perceive.py:601`, `not f.get("thing")`) | — | **no mode:** working at one's traps adds nothing beyond the result and the look |

### 2.5 The wild: game, predators, scavengers, fowl

| State held | Signs | Modes | Gaps |
|---|---|---|---|
| Populations by area and kind (`wild.state.pop`), groups and their leaders, traces on parcels (edge, raid, turned, tried), wariness, carrion, condition (fat, wary, hunger words) | `SIGNS` by kind and trace (`kinds.py:206-257`: the boar's rooting, deer slots, wolf tracks and howling, the fox at the hens; lay, knows, all, conditional snow and night); `RAID_SIGNS` (369-378); `EXPERT_SIGNS` (381-397); `WATCH_SIGNS` (547-550); `PRESENCE` by density (612-631: kestrels and voles, owls, rats, wolves howling, boar, deer, ravens); ravens over carrion (632); `HUNT_NOTICES` while hunting (580-603, the expert reads numbers, condition and wariness); game grown shy (`signs.py:2402`); the hunted kill bundle (`signs.py:441-452`); a carcass (316-357) | H for traces at the edge (own 0.6 to 2.5); presence rows at a wood or scrub parcel (own 0.5, so W P N); hunt notices T | **advises:** "watch the gap and you meet them" (`kinds.py:383`), "a new scare or a dog turns them; the same fire won't for long" (384), "hunting the wood by day keeps them off it" (387), "a terrier or a raised floor" (`kinds.py:620`), "the swine could be turned into the wood" (571), "go in with others or not at all" (`kinds.py:428`). **No mode:** presence rows are placed on the village's first wood or scrub parcel (`signs.py:2039`), a presentation choice; a presence row's sense is guessed from its words ("calling" or "howling" make it sound, `signs.py:2066`), so "a raven pair croaking over the crags" is read as sight |
| Wildfowl pushed by frost onto open water (`OPEN_WATER`) | packed thick on the open water (`kinds.py:357`); frozen over, fowl gone (360); back with the thaw (`signs.py:2437`, fewer for fowlers after the great freeze, 2441) | W at the water | fine |
| Otters (`pop.otter`), the rob (`kinds.ROB_SETS`) | otter tracks (`river.py:240`, 0.6 near); an otter diving in broad day in a thick run (242); otters working this stretch (244, fish, near); after a rob, spraint and scales (`kinds.py:914`) | W | fine |
| Sites: heronries, rookeries, lodges, dams (`SITE_SIGNS` `kinds.py:491-510`) | back, gone, the dam, the pond, harm | W at the site, its first day | fine |
| Loads (slugs, aphids, moles ...), the year's markers, mast, disease (`LOAD_SIGNS` 712, `MARKERS` 738, `MAST_SIGNS` 567, `DISEASE_SIGNS` 786) | as each rises past its mark, on the day | W P N (own 0.5 to 0.8) | fine |

### 2.6 Woods and willow

| State held | Signs | Modes | Gaps |
|---|---|---|---|
| `res.wood` (standing timber), `res.dead` (dead wood), `res.young` (young growth) {S, K} | no standing timber (`signs.py:710`); thinned (712); the good straight trees gone (715, fell knack); tall straight timber (717); the trees roar in a gale (719); picked clean of sticks (722); dead wood scarce (725); fallen branches thick (727); branches down after a gale (729); young shoots browsed (731); shoots springing from stumps (733); axes (739); chips and stumps (741); a wood no longer (743); charcoal (745-747) | W (most at p 0.06 to 0.3); axes by sound N E | **unshown:** how long dead wood or the young growth takes to come back once low |
| `res.willow` {S, K, K0}, cut lowers K in summer, back on the first night of spring (`wild/willow.py:15-73`) | none | — | **unshown:** the whole stock: no sign that a bed is cut over, nor that summer cutting harms the stools (K lost a tenth of a bundle a bundle), nor its coming back in spring; the cut result names only the bundles |
| Wild cord (no stock; 0.04 kg a unit in summer, `data.py:537-543`) | the result "You took 0 cord at the Street." (`verbs.py:905`, `show` rounds 0.04 to 0) | T | **unknowable the other way:** the line says nothing came when 0.04 kg did; 130 such lines by fallback in set B new; "Twisting cord at Clay Field gave nothing: four tries and no cord. I do not yet know why" (set A new, evening) |

### 2.7 Fields, crops and herds

Eelmouth has no fields in crop and no herds (state.json: `herds` empty in every arm); the evidence for these is the guide's
seven-run measure (senses.md §2: ripeness, mould, rain on ripe barley, beasts in a crop acted on 0.77 to 0.97).

| State held | Signs | Modes | Gaps |
|---|---|---|---|
| A crop's stand, progress, ripe day, window, weeds, frost, quality, trampling (farm.py) | `CROP` (`signs.py:32-115`, about 40 rows, the reaper's "fit to reap in about N days"); `FIELD` (118-162, soil, works, ploughing); `TRAMPLED` (232-240); `ASTRAY` (248-269); `EMPTY` (270-277, holders only); `FENCE` (278-297) | W P N; the sickles and the plough by sound E | **advises (mild):** "it wants cutting" (101), "it wants draining" (151), "they want mending" (159, 290), "they want feeding" (206): judgements of the state, which senses.md allows; under [[D2-269 Experts' signs are observations of what is happening now, which may…|D2-269]] they are not an expert's direction |
| Grass on pasture and meadow, dung | `PASTURE` (165-185) | W | "the grass on Eelmouth Fen is long enough to cut for hay" fires on a fen with grass (seen in set B new) |
| A herd: head, hunger, calving, milk, bull, watched | `HERD` (188-227); slaughter (369-399), driven (492-501), calving | W P N E (the bellow, own 2) | fine |
| **Covers' ambient lines** (`data.py:228-241`): "cattle lowing on {pasture}", "dung and trodden grass", "the ring of picks from {rock}", "voices and work about the houses", "water running over stones" | emitted for every parcel of that cover, whatever is on it (`perceive.py:169-172`); read only when attending to "the place" (501-504) | A (the place) | **unknowable, false:** cattle with no herd (88 lines in B new, 35 in A new), picks with nobody quarrying (40 in B new; one man quarried, day 36), water over stones for a broad slow river in flood. Standing ambience, never a change |

### 2.8 Buildings, rooms and fittings

| State held | Signs | Modes | Gaps |
|---|---|---|---|
| Condition or level (5 to 0), the wear accumulator between levels, breaks (`night._wear_night`), works under way, rooms, tier, fire, warmth, beds and who sleeps | the level's own rows (`signs.py:772-781`: a draught at the hearth; light through the wall; a breach a fox could use; the roof half fallen); poor repair, rain coming in, gale at the thatch (782-789); a ruin (790); mended (793, 850); a frame going up (814-817); new (818); crowded (820); the far end cold (822); smoke hangs (824); the break bundle (516-524: the crack in the night, a fresh crack down the wall); fire (457-471); tiers (884-889); works (891-894); fittings (895, p 0.05: a standing fact) | I for those who live there; W P N for others; the crack in the night by sound | **unshown:** how close a worn house is to its next break (the wear store); a fitting's wear (a brine pan's uses, `wear.py:32-55`) is said only once worn, in the act's result ("worn: half as much until mended") |
| The layout line (`prompt.building_line` `prompt.py:397-429`): structure, rooms, spaces used and free, gap, sections, holders | daily, without a roll | M | fine (a layout, not a sign) |
| Writing on buildings ([[D2-169 Buildings carry what their people write|D2-169]]) | read where one went in (`buildings.read`) | T, M | fine |

### 2.9 Stores and containers; vermin

| State held | Signs | Modes | Gaps |
|---|---|---|---|
| A store's goods by portion (granary, cellar, bins, floor; sacks, baskets, chest, salting tub: `stores.portions` `stores.py:188-243`), each portion's spoil and vermin rates (`stores.rates` `276-298`) | one's own store by portion, daily, without a roll ("735 grain (400 in the chest, 300 in 6 sacks, 35 loose on the floor)", `stores.store_line` `370-403`, in `prompt._house_lines` 681-687); the diff since the last morning ("roots -19.4 (now 31.1)", `view.py:155-168`); food worth N meals; a cat in the store (`prompt.py:619`); fish going soft (`signs.py:875`, smell 1.2 near, the morning after it spoiled); a stink of rot, flies (878-880); through the open door (898, p 0.05, peek); the bins look near empty (901) | I M; others W (near) | **unshown:** how long each portion keeps (the rate the night will apply is in `stores.rates`, read for no line): fish "will not keep" is said only after it has spoiled. Glut, set A new day 9: 47 kg of fresh fish (24 food) went off in Marsh House's store while the Brook and Shepherd smokehouses had no lot on their racks (days.jsonl day 9, `smokehouse`); the next morning said "fish +76.8 (now 76.8)". Set A old the same night: 85 kg (41 food) |
| What the meal drew (`night._eat` `night.py:494-513`: the book's `first`, then needs-no-fire, then the most perishable, from hands, then the home store, then other stores one may take from) | none | — | **unshown** ([[D2-342 Each morning a person is told what they ate the night before|D2-342]]): mixed into the diff with spoilage, vermin and others' takings (§5 below) |
| Vermin: rats and mice by area (`wild.state.pop`), stores' exposure by portion (`stores.exposure`, `vermin_portions` 312-324), stops (a dog, a cat, an owl hole), the night's take by where (`b.vermin`) | the take by where: "grain scattered and trodden into the floor of X, mouse droppings in it" (`kinds.py:557-563`), sacks gnawed (561), the chest (562), fish hanging chewed (564); presence (`kinds.py:618-620`); the rats' illness factor on adults (`stores.illness` 344-353) | I W, the morning after; presence W | **unshown:** which portion is exposed before it is eaten (a sack on the floor against one in the chest); how much the vermin took (a share, `wild.eaten`); the illness factor (no sign at all) |
| A theft from a store | "someone has been at the {item} in X's store: there is less than there was" (`signs.py:507`, inside); footprints in snow, mud (509-511) | I, M | fine (what is sensed) |

### 2.10 Racks, lots, fires and the salt pan

| State held | Signs | Modes | Gaps |
|---|---|---|---|
| Lots on racks (process.py): item, kg waiting and done, nights left, the fire lit or out, tended today, fuel tonight against fuel there, room on the racks (`process.house_lines` `process.py:640-683`) | the household's lines, daily, without a roll: "on the smoke racks: 0 kg of smoked fish, done 3 nights ago, waiting to be taken down; room on the racks for 250 kg more"; "the fire not tended today: it dies tonight unless someone tends it"; "not enough firewood for tonight's fire (3 bundles needed, 1 there)"; "the fire died last night: what hung there lost a night's smoke and spoiled a little" | I M | fine; the "0 kg of smoked fish" line rounds a little to 0 (`process._n`) |
| Others' smokehouses | smoke rising this morning (`signs.py:855`, own 3.6); the smell of smoke and fish (857, around, carries); smoke low in fog (859); no smoke though fish hang: its fire has gone out (861) | W P N E (own 3.6); smell by steps | fine |
| A rack outside, rain on it | rain on the drying fish: wet and slimy, flies at it (`signs.py:1447`) | W only, while it rains | fine |
| The brine pan: boiling (`keeping.py`), its wear (`wear.py`, 60 uses) | steam and smell (865); the salter's fire (867); burned all day (869); white crusts, 2 days (871); the spring itself (754, own 0.15: a standing fact) | W P N | **unshown:** the pan's wear; **standing fact as a sign:** the spring line repeats ("you saw yesterday: a spring welling up at Eelmouth Fen", in the layout daily) |

### 2.11 People: hunger, health, work, care, children

| State held | Signs | Modes | Gaps |
|---|---|---|---|
| Hunger stage (0, -1, -2), missed meals in a row, frailty, wounds, stage, pregnancy, infants carried, a beast led, arrived, failing, ate raw, partner, blood, childbed, sat up, slept out, cared for (`signs.person_context` `signs.py:1127-1162`) | `PERSON` (`signs.py:905-957`): well fed (p 0.08), drawn and hungry (0.35), gaunt (0.6), sat down twice (0.3), stiff and bruised, slow in the cold, carries a club, a load, heavy with child, a baby on the hip, leads a beast, just come in, failing, chewing raw grain, keep close together, bloodied, childbed, heavy-eyed, slept out, kept a child close all day | I (the household sees its own) W P N (own 1, sight) | **unshown:** how many nights a person has gone short; what they ate; a member's hunger is read by chance even in one's own household (p 0.35 x presence); an adult's illness has no state (senses.md, known gap) |
| Oneself: the night's meal, work's hunger (`labour.work_need`), tiredness | "Your hard day's work left you ravenous: you ate 1.28, where a lighter day would have needed 1." (`run.py:648`); pushed past your strength (645); a missed meal (633-636); less than a cold night asks (641); "You are fed" in "## You" | M | **unshown** ([[D2-342 Each morning a person is told what they ate the night before|D2-342]]): which goods, which store, which rule; a full ordinary meal writes no line |
| Children: stage, grows, fed, cared for, what they hold to keep ([[D2-340 Passing on through care|D2-340]]) | the family lines (`prompt._family_lines` `prompt.py:822-866`): "Basilia, a child of your household: fed, looked after yesterday by Petronel; grown in 8 days." | M daily | fine (known to the household) |
| Others at work | "In passing": "X spent the day at Y" (`perceive.py:530-540`, presence of a person own 2.0) | H | fine; 385 to 664 lines an arm, acted on 0.2 to 0.3 |
| Being watched | "You had the feeling X was watching you today" (`perceive.py:541-546`) | H | an act or feeling? It is a felt sign of another's act, read by the rule: fine |

### 2.12 The household book and its rules ([[D2-341 Rules are not something one attends to|D2-341]]: shown, never attended)

| What is held | Where shown | Attendable today? |
|---|---|---|
| The household's rules and one's own, numbered (`book.rules`) | the system prompt's rules block (`book.rules_block` `book.py:1332-1353`); the evening's "The standing rules" with what they did that day (`evening.py:84-90`) | No: `resolve_target` has no rule subject (`perceive.py:659-687`): "rule 2" resolves to "the place in general (you could not find 'rule 2' to attend to)" and gets the ambient lines. No attend in live run 1 named a rule (0 of 213 in the new arms). Keep it so ([[D2-341 Rules are not something one attends to|D2-341]]); see design §0.1 for the fallback |
| A rule's firing | "Rule 3 (the household): Petronel: work care at Basilia, with units left over ..." in "You did" (`book._run` `1281-1319`); the day's firings in days.jsonl `book.fired` | shown as a result |
| What waits by the rules | "Waiting today: ... (rule n)" (`book.morning_lines` `1356-1370`) | shown |
| A rule not done, a rule gone against | "Not done by the rules yesterday: ..."; **"Against the household's rule n: Peter's own rule takes the salt fish the household keeps back"** (`book.day_lines` `1373-1386`, `_against` 1108-1111) | **announces** a breach ([[L-174 Remove the engine's automatic detection and telling of breaches and…|L-174]]) |
| A rule's `seen` condition | reads the members' own noticed lines for the set's words (`book.seen` `1123-1137`), never the hidden state | grounded: fine |
| A chore that yields nothing | fires on: "You took 0 cord at the Street." 130 times in set B new (days.jsonl `book.fired`, fallback true) | flagged in the live run report |

### 2.13 Weather and ice

| State held | Signs | Modes | Gaps |
|---|---|---|---|
| The day's weather values (temp, low, rain, wind) and tomorrow's (`climate`, `environment`), snow lying, wet days, dry spells, storms moving | the "Now" line (the weather words, to all awake); `SKY` (`signs.py:563-633`): the first frost, ice on the butts, bitterly cold, a killing frost, heat, drizzle, a downpour, wind, the turn; tomorrow's for the sky-reader (sow knack: rain, snow, gale, clearing); a storm coming (623, own 1.5); `WEATHER_LEADS` (`kinds.py:403-415`: plovers, swallows) | V (open to all) | forecasts were never acted on (senses.md); fine as they are |
| Ice on the water | river and shallows rows (above) | D W | fine |

### 2.14 Travel and roads

| State held | Signs | Modes | Gaps |
|---|---|---|---|
| A road's stretches, terrain, landmarks and their challenges, the weather on the road, traces (tracks, ruts, ashes, a fight), travellers on the same stretch, meetings that pass | `ROAD` (`signs.py:1507-1599`), `TRACE` (1603-1654, the hunter reads numbers and age), `TRAVELLER` (1657-1678), `PASSING` (2716-2739), the night's break-in for those woken (`NIGHT` 1681-1720), a party on the last stretch in (`_road_coming` 2359-2387), a grand building ahead (`GRAND_AHEAD` 1066) | on the road ("On the way", up to five on arrival); the village's built parcel for those coming in | not exercised in live run 1 (nobody travelled); "you passed a ford" each night (p 1) is a standing fact as a sign |

### 2.15 Events and their aftermath (across mechanisms)

The [[D4-74 Events and their aftermath show themselves as bundles|D4-74]] bundles (`signs.py:403-559`: fight, raid, hunted, fire, birth, guard, driven, theft, broke, weir broke, burial, dogs) and
the slaughter (369-399) are the model the guide holds up: to the doer, nearby, lingering, conditional. Two of their lines go
beyond what is sensed:

- **The witness of a theft is given the thief's name, the exact quantity and a manner** ("Oliver slipped into Brook House and came out
  with 3 grain", `settle.py:309-310`; from set gear, `settle.py:338`), and the theft is shown to them with chance 1 (`perceive.py:428`).
  A witness sees a person go in and come out carrying something; the quantity is not seen. **Unknowable** ([[L-174 Remove the engine's automatic detection and telling of breaches and…|L-174]]).
- **The thief is told "You think you were seen ..."** (`settle.py:313-314`) whenever anyone saw: the engine tells a person of
  another's noticing. **Announces.**

## 3. What live run 1 shows about the modes

From [live1_signs.txt](live1_signs.txt). "Acted on" is the guide's crude measure (two of a line's content words of four letters or
more, a short stoplist removed, reappear in the next morning's reply or that evening's own talk); read it as a contrast within an
arm, not as a level.

| | A pre | A old | A new | B pre | B new |
|---|---|---|---|---|---|
| Turns | 171 | 179 | 179 | 301 | 344 |
| Attend given | 88% | 88% | 34% | 88% | 44% |
| Resolved to a named subject | 100 | 109 | 27 | 183 | 58 |
| "The village" (its layout) | 40 | 26 | 0 | 56 | 0 |
| Not found: the place in general | 10 | 22 | 33 | 27 | 95 |
| Attended lines a day attended | 5.2 | 4.5 | 3.9 | 4.5 | 3.3 |
| Units spent to look (watch, search, look) | 0 | 0 | 0 | 0 | 0 |
| Hearth lines: stood out / attended / in passing | 796 / 782 / 288 | 916 / 712 / 325 | 928 / 232 / 385 | 1491 / 1201 / 438 | 1828 / 510 / 664 |
| Next-morning lines | 435 | 673 | 679 | 611 | 1170 |
| Meal lines (the hard-work line, a missed meal, a cold night's short) | 62 | 69 | 52 | 116 | 120 |
| "Store since you last looked" lines | 162 | 186 | 189 | 311 | 294 |

**What people tried to attend to** in the new arms ([attend_kinds.py](attend_kinds.py), output [attend_kinds.txt](attend_kinds.txt);
every attend in attend_targets.txt): of the 128 not found, a store's goods or its vermin 39 ("the soft salt fish in our Marsh
House store", "the roots in the Marsh House store, which fell by about 20 overnight", "the rats at the sacks"); a wall, a crack or
a cold end of a house 28; set gear and its catch 15 ("my six wicker traps, and how heavy the night's catch is", "Henry's traps T8
and T10"); racks and their lots 13 ("the tags on each heap at the Marsh Smokehouse"); a person's body 6 ("Petronel, who is gaunt
and unsteady on their feet"); the water and the weir after a spate 6; a person at a craft, to learn 6 ("Oliver, and how he sets
his hands to fish by hand"; several more name a person first and are counted under what they name after); greens, grass, beans 6;
offers and leave 5; the fog 2. These are the facts design.md proposes; today none of them can be reached by attending, and the
place's ambient lines answer instead.

**Which lines are used.** Within each arm, lines about set gear (0.6 to 0.85), racks and lots (0.6 to 0.9) and the weir when attended
(0.6) are the most used; in-passing lines (0.2 to 0.4), ambient lines (0.0 to 0.07), travel and the layout's standing lines (0.0 to
0.14) the least. The guide's pattern holds: a change one can act on today is used; standing facts and ambience are not.

## 4. The gaps, gathered

**State held that no sign shows** (ranked by how often the live run's people asked for it, design.md ranks by decisions):
1. What the night's meal drew, from which store, by which rule ([[D2-342 Each morning a person is told what they ate the night before|D2-342]]).
2. How long each store portion keeps (`stores.rates`): fresh fish is said to go off only after it has.
3. A gear piece's remaining nights and rot (`gear.state_words` exists and is not in the beliefs view).
4. What the weir turned away (`river.record` `turned` in kg) and how full its traps were (shown to the crew at the parcel only).
5. A member's nights gone short, and what they ate.
6. How a fished-down pool, a picked wood, dead wood and a cut willow bed come back.
7. The willow stock at all.
8. A house's wear toward its next break; a fitting's uses toward its wear (the brine pan).
9. Which store portion is exposed to vermin before the take; the rats' illness factor.
10. The density of a run in heads (a band only).

**Modes with nothing to see:** attending to a store, to set gear by its noun, to the run, to a person described in a sentence
(all fall to the place's ambient lines); attending with units (no act); working with one's set gear (excluded from the acting
pass); next door and the village for the store's spoil and the shallows (own under 0.5); the tally of a run anywhere but the
water.

**Signs that state what the person could not know:** the covers' ambient lines (cattle, picks, water over stones); the otter's
"1 gone" in the tend result; the theft witness's exact quantity and "slipped"; "You took 0 cord" for 0.04 kg.

**Signs that advise or announce:** the six expert or lore lines in §2.5; "Against the household's rule n" (book.py:1384); "You
think you were seen" (settle.py:313); the theft shown to its witnesses at chance 1 (perceive.py:428).

## 5. The meal: what it tells now (for [[D2-342 Each morning a person is told what they ate the night before|D2-342]])

- **Engine.** `night.night` (`night.py:136-176`) feeds each person in `book.meal_order` (a share rule's order first, [[D2-339 The household book's grammar|D2-339]]): the
  need (`needs.food` with work, cold, shelter, a child's ration), the book's `first`, `ration` and `skip` (`book.meal`
  `book.py:1065-1088`), then `_eat` (`night.py:494-513`) destroys goods "eaten" from the person's hands, then the home store, then
  every other store they may take from, in `first` then `eat_order` (needs no fire first, then the most perishable, `night.py:489`).
  It records only the total: `rec["ate"][name]`, and `short`, `missed`, `work` (need, base, units). The goods, their quantities,
  the containers and the rule that set the order are not kept.
- **Lines.** `run.night_lines` (`run.py:620-690`): a missed meal; a ration but short of the work; less than a cold night asks; the
  hard day's "ravenous: you ate 1.28, where a lighter day would have needed 1" (only when 6 or more units were used); raw food
  without a fire. **An ordinary full meal writes nothing.** The morning's "You are fed" is the hunger stage.
- **The store.** The diff since the last morning (`view.py:155-168`) mixes the meal, the night's spoilage, vermin, others' takings
  and one's own deposits: "Brook House's store since you last looked: dried meat -0.1 (now 17.5), egg +0.9 (now 3), firewood -4
  (now 38), roots -19.4 (now 31.1)". "Its store: ... those who eat from it eat about 2 a night" (`prompt.py:685`) counts eaters, not
  food.
- **Read as vanishing:** set A new, day 2 Oliver ("the roots are going fast"), day 3 Hamon, day 3 Peter ("about 16 a night to rats
  and rot"); set B new, day 3 Oliver and Peter (above); set B pre, days 2 and 3. Two households set "eat the roots first" rules on
  that reading.

## Open questions for Zach

1. **Should a target that cannot be found fall back to nothing rather than the place's ambient lines?** Today 60% of the new
   prompt's attends get "cattle lowing" and "the ring of picks", lines the state does not hold.
2. **Should the covers' ambient lines be kept at all?** They are standing ambience (never a change) and several are false where no
   herd, no quarrying or no stony stream is; acted on near 0 in every arm.
3. **Should a witness to a theft see the quantity taken**, or only that a person went in and came out carrying something ([[L-174 Remove the engine's automatic detection and telling of breaches and…|L-174]])?
4. **Should a thief be told that someone saw them**, or learn it only from how others act?
5. **Should "Against the household's rule n" stay** while [[L-174 Remove the engine's automatic detection and telling of breaches and…|L-174]] waits, or go now with the other announcements?
6. **Should one's own gear's remaining life be shown daily in the beliefs view** (as the old turn prompt does), or only when one
   handles the gear?
7. **Are "it wants cutting", "it wants draining", "they want mending", "they want feeding" judgements of the state (allowed) or
   directions ([[D2-269 Experts' signs are observations of what is happening now, which may…|D2-269]])?**
