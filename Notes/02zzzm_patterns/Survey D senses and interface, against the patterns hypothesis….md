---
id: docs/review/37_growth/02zzzm_patterns/D_senses.md
kind: note
updated: "2026-11-24"
---
# Survey D: senses and interface, against the patterns hypothesis (thread W-110)

*note · `docs/review/37_growth/02zzzm_patterns/D_senses.md`*

> **Mechanisms (70, §2), by how well they fit today** (each counted by its weakest part: a general mechanism with named branches counts as "by name"):


Session 37.2, agent D, 24 Nov 2026. Brief: `brief.md` beside this file. Surveyed `main` at `6b609f48` (after the wave), against the
wave's baseline `f728a3b7` (23 Nov). Files: `engine/signs.py` (2,752 lines), `perceive.py` (794), `prompt.py` (1,001), `core.py`
(150), `shapes.py` (523), `view.py` (232), `views.py` (231), `layout.py` (344, its renderers), `evening.py` (235), `wild/river.py`
(508, its signs), with the display half of `knowledge.py` and `modifiers.py` (shared with C) and the sign tables of `wild/kinds.py`
(275 entries). 6,770 lines in the area proper. The interface rebuild on `w109-interface` (`/home/user/c2-iface`, 5 build commits
on 24 Nov, not merged) is described in §9 and is not counted in the tables. The root-level `cybertron2/perceive.py` and
`cybertron2/prompt.py` are the round-based engine before `engine/` (only `tests/test_cybertron2.py` imports them) and are out of
scope. The counter for §3 is `D_branches.py` beside this file (`PYTHONPATH=. python3 docs/review/37_growth/02zzzm_patterns/D_branches.py [--hits] [--root DIR]`).

## Summary

**Mechanisms (70, §2), by how well they fit today** (each counted by its weakest part: a general mechanism with named branches
counts as "by name"):

| Fit | Count | Examples |
|---|---|---|
| general over rows | 17 | the sign row and its tables (536 rows); the sky's context; the noticing step's inputs; `knowledge.craft_line` ([[D2-263 A craft a person knows at capable or known shows, where they look|D2-263]]); the craft resolver; the run views |
| general with fitted constants | 3 | the noticing rule (`NOTICING`), relevance, hidden ways found |
| special case by name | 22 | the parcel, building, person and thing contexts; the subject walker; `practised` (`WATER_CRAFTS`); the place repute; `building_line`'s weir; the craft-named "made" rows; the river's rows per run |
| hand-written text | 17 | the reply schema's keys, the core lines, `reply_text`, the `SHAPES` sentences, the house and family lines, the evening, fuse, build and old system prompts |
| a word-list parse | 6 | `normalize`'s word lists, `resolve_target`'s phrases and `RULE_WORDS`, the lasting memory by keyword, a wild sign's sense from its own words, a drying rack by an item's name prefix, a note's title |
| no pattern of the hypothesis | 5 | the mind's records (places, kin, beasts, land, beliefs, things known) and the morning's diff |

Silent skips (a second flag, on 4 of them): a sign whose condition raises is dropped without a word (`signs.py:1235`, `2674`,
`river.py:442`), and an unfound attention target falls back to "the place in general" (`perceive.py:696`).

**Named branches in function code** (§3): 508 hits in the area with `knowledge.py` and `modifiers.py` (475 in the area proper):
259 in functions, 159 in sign rows' conditions, 90 in module-level tables. At the wave's baseline the area had 390; the wave added
85 (77 of them in its three new files: `core.py`, `shapes.py`, `river.py`). In functions, per thousand lines, the rate has risen
at every snapshot: 24.7 (24 Oct), 26.7 (2 Nov), 28.1 (9 Nov), 31.3 (17 Nov), 31.4 (23 Nov), 33.4 (24 Nov). Of the 259 in
functions, about 150 should become a property of a row (§3, table 3.2); about 40 are a sign's binding to a state value and stay;
about 70 are words or stage names that belong in a words table.

**What does not fit** (§4): the hypothesis's set is **too few, and its signs pattern is cut wrongly**, for this area. It has no
pattern for: (a) **the observer**, how knowledge, stage, office and holding select what is seen and shown (three separate
implementations today: `perceive.practised`, `shapes._universal`/`_holds_gear`, the rebuild's `iface.WHO`); (b) **the mind's
records**, dated observations and the "as you last saw it" rendering with its diff (seven stores, seven renderers); (c) **subjects
and their walkers**, where the candidates a sign could be about come from (about 20 walkers and 14 context builders, about 1,500 lines);
(d) **lines known without a roll** (one's own house, body, family: `house_known`, `_family_lines`); (e) **the reply in**, the
schema and the parse of a free reply. And "signs" is not one pattern: rows about a subject's state, bundles bound to an event or
an act, and the one noticing rule are three, and the second belongs on the acts' and crafts' rows, not in `signs.py`.

**Verdict for area D.** The hypothesis is right where it is applied (one row format, one rule for chance, the craft lines by
level, the act registry of the rebuild) and the area shows what happens without it: four sign formats, five name resolvers, two
copies of the fence, stage and number words, and a rising rate of named branches. But as a set it is not enough here: add the
observer gate, the mind record, the subject registry with its context namespace (P3's "the context its signs read" made a slot),
known lines, and the reply schema from the registry; and move event signs to the acts and crafts. With those, about 85% of the
70 mechanisms are rows on general mechanisms; the rest is the frame (the core lines) and the systems' own contexts, legitimately
code.

**The restructuring's cost** (§10): about 15 to 20 builder-days for the area, about 4,000 of its 6,770 lines touched; 8 of those
days are already in feature_packages.md §10 (phase 1b, and phase 4's signs walker, prompt slots and view), the rest is the five
patterns above. The largest risk is not code: every change to a rendered line is a change to the experiment's stimulus, so it
needs prompt snapshots and a decision on which runs it invalidates, and phase 1b's keyed draws change what everyone notices.

**The balance ([[D2-354 The architecture is a healthy balance, not a strict one|D2-354]])** (§8): the noticing rule, the row schema, the observer gate, the resolver and the reply schema should
each be one primitive; the water system, the wild layer and the buildings legitimately own their contexts, their walkers and their
sign texts, kept in their own folders behind seven named extension points. From the history: the wild layer's walkers (9 Nov), the
river's row format (23 Nov) and the house lines (14 Nov) went ad hoc because the general system had no slot for them; the
`WATER_CRAFTS` list, the named hearths, the fence words and the shapes' hand sentences went ad hoc though the property or the
registry already existed.

## 1. Method

1. Read every file in the area, and `docs/cybertron2/guides/senses.md`, feature_packages.md §1 to §5, §9 to §11, the [[W-109 The prompt's interface restored|W-109]] brief
   and `prompt_compare.md`.
2. Listed each mechanism (a function or table that reads or changes what is perceived or shown, or parses a reply) with file:line,
   its pattern and fit. A mechanism is "in the wave" when its lines blame to a commit after `f728a3b7` (checked with `git blame
   f728a3b7..HEAD` for each cited line; whole files absent at the baseline: `core.py`, `shapes.py`, `wild/river.py`).
3. Counted named branches with `D_branches.py`: a string constant naming a row of the engine's tables (fittings and their aliases;
   rooms, blueprints, monuments, fences, structures, tiers; covers; techniques; items; resources; wild kinds; crops; weather;
   terrain; stages) used in a comparison, a literal list, a dict key or a keyed lookup; text, docstrings and tag lists are skipped,
   and a record's own field that shares a row's name (a parcel's `fence`, a herd's `pack`) is excluded. The same script was run on
   the area's files at six commits (§6).
4. History from `git log --all` on the area's files (152 commits from 23 Oct; `main`'s history before 13 Nov is squashed into
   `d21510a0`, so `--all` is needed).

## 2. The mechanisms

Fit: **R** general over rows; **F** general with fitted constants; **N** special case by name; **T** hand-written text; **P** a
word-list parse; **S** a silent skip; **X** no pattern of the hypothesis. Pattern: the hypothesis's numbers (1 typed rows, 2
properties, 3f acts, 3g signs, 3h the book, 4 the resolver, 5 generated worlds), or "-". Wave: **W** in the wave (23 to 24 Nov).

### 2.1 Signs (`signs.py`, `wild/river.py`, `wild/kinds.py`)

| # | Mechanism | Where | Pattern | Fit | Wave | Note |
|---|---|---|---|---|---|---|
| 1 | the sign row: `when`, `text`, `sense`, `own`, `p`, `tags`, `knack`, `knows`, `lay`, `reach`, `night`, `who`, `eye`, `land`, `peek`, `gate` | `signs.py:32-960`, `1323-1724`, `2716` | 3g, 1 | R | | 536 rows in 35 tables. No loader check; no required fields; the id is the table and index (`signs.py:1239`, `:1843`), so any row added shifts the ids after it |
| 2 | a parcel's context | `signs.py:964-1047` | 3g | N | part (`:1045` [[W-98 Build stage 2, taking and making|W-98]]) | crafts worked today by name: fell `:981`, charcoal `:983`, plough, hoe, reap, quarry, mine `:987`, sow `:1003`; the shallows by cover `:1045`; holding records through `farm` |
| 3 | a building's context | `signs.py:1072-1124` | 3g, 2 | N | | `fire_place` by naming hearth and fire ring `:1084` though both rows carry `fire: True`; salt by the fitting's `spring` property `:1117` (the right way); the monument's look by a dict of names `:1122` |
| 4 | a person's context | `signs.py:1127-1162` | 3g, 2 | R+N | | gear by the items' `seen` and `camp` properties (right); bloodied by reading two parcel records by name `:1148-1152` |
| 5 | the sky's context | `signs.py:1170-1195` | 3g | R | part (`river`, W) | from the weather's values; the river flag added by u8 |
| 6 | the subject walker `facts` | `signs.py:1221-1300` | 3g | N+S | | a fixed list of subjects; dispatch by cover name (`field` `:1252`, `pasture`/`meadow` `:1266`); `HOLDING_ROWS = range(3, 10)` `:961`, a row's meaning by its position; table names by `id()` `:1227`; a raising condition dropped `:1235` |
| 7 | herds astray, empty pastures, fences, trampling | `signs.py:1198-1218` | 3g | R | | |
| 8 | event bundles (slaughter, fight, hunt, burial, fire, raid, theft, break, birth, guard, driven) | `signs.py:1880-2020` | 3g | R+N | | rows general; each event kind its own branch of code reading its own parcel or building record (`p.get("fight")`, `"hunted"`, ...) |
| 9 | a thing's context | `signs.py:1732-1789` | 3g, 2 | N+P | | `SEED_GOODS` `:1729` a list of goods; meat by name `:1763`; a rack drying by the item's name prefix `"drying "` `:1778` |
| 10 | a carcass's, herd's, fence's context | `signs.py:1792-1866` | 3g, 2 | R | | the fence's word from `FENCES` (right; `prompt._fence_words` repeats it by hand) |
| 11 | "made here today" rows | `signs.py:830-848` | 3g | N | | the sound or smell of a making, by craft names: bread, grind, mill, smelt, coin, dry meat, crude weapon, tent, harness. The sign of a craft, held in the building table |
| 12 | how a tier looks | `signs.py:1050-1070` | 1 | N | | `TIER_LOOK`, tier by structure: words of the tier rows, kept beside them |
| 13 | the wild walkers (presence, traces, eaten, mast, loads, when, sites, wary, thaw, rare, sick, road coming) | `signs.py:2023-2604` | 3g | R+N+P | | rows on the kinds (`kinds.SIGNS`, `RAID_SIGNS`, `EXPERT_SIGNS`, `HUNT_NOTICES`, `LOAD_SIGNS`, `MARKERS`, `SITE_SIGNS`, `DISEASE_SIGNS`, `RUN_SIGNS`: 275 entries) in their own format `R(read, sense, own, ages, text, cond)`; the sense guessed from the words, "calling" or "howling" `:2066`; `read` mapped to `knows` by hand `:2089` |
| 14 | the river's signs | `river.py:167-508`, `signs.py:2445-2543` | 3g | N+S | W (u8) | a third row format `_row(read, sense, own, text, ...)` `river.py:167`, a fourth for the dawn `:173`, templates `CARRIED` `:254`; rows per run by name (`x.eel`, `x.salmon`, `x.lamprey` `:193-252`) though the runs are rows of `kinds.RUNS`; `_knows` maps "fish", "expert", "elder", "crew" to readings `:261`; raising conditions dropped `:442` |
| 15 | the road, traces, travellers, the night, a meeting passed | `signs.py:1507-1724`, `2605-2660`, `2716-2752` | 3g | R+N | | classes of weather and terrain by lists of names (`x.terrain in ("plain", "farmland", "marsh", "river valley")` `:1512`) |
| 16 | true rows, readable, roll | `signs.py:2660-2715` | 3g | R+S | | `roll`'s `mult` and `least` beside the one rule (feature_packages §5 "one code path") |

### 2.2 Noticing and the mind (`perceive.py`)

| # | Mechanism | Where | Pattern | Fit | Wave | Note |
|---|---|---|---|---|---|---|
| 17 | ambient lines of a cover | `perceive.py:178-180` | 3g, 1 | R | | `COVERS[...]["ambient"]`, tuples: a fifth sign format |
| 18 | the facts of a node | `perceive.py:158-198` | 3g | R | | |
| 19 | an event's extent | `perceive.py:201-220`, `data.EVENT_EXTENT` | 3g, 1 | R | | by event kind, from a table |
| 20 | the noticing rule | `perceive.py:223-239`, `things.spot_chance` | 3g | F | | [[D4-53 Every sign and every event is noticed by the one noticing rule|D4-53]], [[D4-75 Every perceived line about the world comes from the one noticing rule|D4-75]] |
| 21 | a sign's scope (setter, seen, stranger; happened to one) | `perceive.py:242-262` | 3g | R | | |
| 22 | relevance | `perceive.py:265-281` | 3g | F | | by tags |
| 23 | a knack | `perceive.py:284-293` | 3g, 2 | R | | names a technique; ×2, ×1, ×0.5 |
| 24 | the readings one has (`practised`) | `perceive.py:296-324` | - | R+N | part (`:301` W) | known crafts, `reads_as`, the expert's threshold, familiar kinds: general; "elder" a reading by stage `:299`; the river's `WATER_CRAFTS` `:301`, a list of nine names, though `reads_as` exists for this |
| 25 | a sign by skill tag | `perceive.py:362` | 3g | R | | legacy (`skill` in interests) |
| 26 | dawn, the evening's notice, attending, acting, glimpses, feeling watched, learning by seeing | `perceive.py:368-627` | 3g | F+N | | caps `NOTICE_MAX`, `ATTEND_MAX`; event kinds by name: theft `:432`, `:472`, `ROUTINE` `:26` |
| 27 | what one attends to | `perceive.py:664-696` | 4 | P+S | part (`:661` [[W-104 Build the after-runs list from live run 1|W-104]]) | phrases for the village, the place, the sky `:674-680`; `RULE_WORDS` a regex `:661`; anything unfound becomes "the place in general" |
| 28 | a place's repute (`describe`) | `perceive.py:127-155` | 2 | N | | resources by name with their words `:139-140`; fittings by name, anvil and cellar `:145` |
| 29 | places, kin, beasts, land known; a place found | `perceive.py:42-125`, `337-360`, `630-648` | - | X | | each its own store in the mind |
| 30 | lasting memory | `perceive.py:722-728` | - | P | | a line lasts if it contains "killed", "died", "beat", "gave", ... |
| 31 | beliefs, dated | `perceive.py:740-754` | - | X | | |
| 32 | notes, pin, forget | `perceive.py:757-794` | 3h | R+P | | structured fields, a fuzzy title match |
| 33 | seeding the mind | `perceive.py:42-113` | 5 | R | | customs, lore, ways, kept lines from the spec |

### 2.3 The prompt (`prompt.py`, `core.py`, `shapes.py`, `view.py`, `evening.py`, `layout.py`)

| # | Mechanism | Where | Pattern | Fit | Wave | Note |
|---|---|---|---|---|---|---|
| 34 | the reply schema | `prompt.py:15-125` | 3f | T+R | part | the keys hand-written (42 action keys), the enums from what one knows; the core prompt's edits `:113-118` |
| 35 | a craft's note (old prompt) | `prompt.py:140-186` | 3f, 1 | R+N | | from the rows; copper and bare hands by name `:149-151`; structures listed `:159` |
| 36 | the verb lines (old prompt) | `prompt.py:189-236` | 3f, 1 | R+N | | over `VERB` and its ways: complete; `_verb_extra` by verb name `:189-202`; world facts in `doc` (D5-2) |
| 37 | what else building can do | `prompt.py:239-266` | 3f | T | | |
| 38 | the old system prompt | `prompt.py:502-567` | - | T+R | | numbers from the physics and the item rows |
| 39 | labour's lines | `prompt.py:292-323` | 2 | R+T | | wear over the fittings' rows |
| 40 | a parcel's line | `prompt.py:335-394`, `448-465` | 2 | R+N | | what one can do there from the crafts' `at.covers` and `draws` (right); covers by name `:342-356`; `_fence_words` a dict of fence kinds `:450` repeating `FENCES` |
| 41 | a building's line | `prompt.py:397-429` | 2 | R+N | | tiers from `TIERS` (right); the weir and the mill by `WL.is_weir` `:412-423` |
| 42 | one's beasts as last known | `prompt.py:432-445` | - | X | | a mind store's renderer |
| 43 | one's house, known without a roll | `prompt.py:589-692` | - | N+T | part (`:672` [[W-99 Build stage 3, keeping, stores and the household book|W-99]]) | hearth and fire ring by name `:617`, `:635`, `:682` (rows carry `fire: True`); smoke racks and brine pan `:634`; the cat by name `:619`; `process.house_lines` its own unit (right) |
| 44 | family lines | `prompt.py:823-867` | - | T+N | part (`:851` [[W-104 Build the after-runs list from live run 1|W-104]]) | stage names; care's instructions in prose |
| 45 | things one knows lie about | `prompt.py:870-880` | - | X | | a mind store |
| 46 | the urgent call | `prompt.py:883-918` | 1 | T | | `FUSE` rows give the choices; what each does is a dict in code `:892-907` |
| 47 | talk, meeting, road, lighten and memory prompts | `prompt.py:921-1001` | - | T | | |
| 48 | a person as seen | `prompt.py:816-820` | - | N | | stage words |
| 49 | the core lines | `core.py:16-77` | - | T | W | the frame (legitimately text); variants by index (`lines[4]`, `lines[6] = None` `:69-73`), against P6 |
| 50 | the reply format | `core.py:81-106` | 3f | T | W | repeats the schema by hand |
| 51 | the core system prompt | `core.py:114-137` | - | T+N | W | stage words `:119`, a copy of `prompt.py:507` |
| 52 | the eleven shapes | `shapes.py:23-65` | 3f | T | W ([[W-100 Build stage 4, signs, people and worlds|W-100]]) | hand sentences in place of the registry; faces as a map to verbs (data) |
| 53 | the free act read | `shapes.py:117-392` | 4 | P | W ([[W-100 Build stage 4, signs, people and worlds|W-100]], [[W-102 Fix the act shapes' interface faults found in live run 1's rebuilt arm|W-102]]) | `KEEP` `:68`, `RULE_DO` `:117`, `BOOK_KINDS` `:118` (a copy of `book.KINDS`), `PEOPLE_KEYS`, `CRAFT_KEYS` `:119-120`, `DOOR_TO` `:121`, prefixes `:143` |
| 54 | a craft from a word | `shapes.py:87-101`, `136-165` | 4 | R | W | by name, aliases and labels, known first: the hypothesis's resolver. Four more resolvers: `knowledge.resolve`, `perceive.resolve_target`, `placed.method_of`, `Here.person`/`building`/`parcel` |
| 55 | crafts by shape, universal crafts, gear held | `shapes.py:396-455` | 3f, 2 | R+N | W | youth by name `:419`, `:447`; set gear by `gear.SET_GEAR` |
| 56 | "What you can do" | `shapes.py:457-495` | 3f | T+N | W | the head's and the youth's lines by hand `:487-490`; replaced on `w109-interface` |
| 57 | the reply's example | `shapes.py:505-523` | 3f | R+N | W | firewood by name `:522` |
| 58 | a processing container | `shapes.py:498-502` | 2 | N | W | the `process` property, or the name "smoke racks" |
| 59 | the belief view, its snapshot and diff | `view.py:115-232` | - | X+N | part | the cat by name `:164-171` |
| 60 | roads from here | `view.py:76-84` | - | T | | the night's food from the physics |
| 61 | how the village fits together | `layout.py:254-276` | 1 | R | | covers' and layout's words |
| 62 | a building named on arrival | `layout.py:279-287` | 2 | N | | tiers "rich" and "grand" by name |
| 63 | what one sees first arriving | `layout.py:290-327` | 1 | F+N | | fittings from `LAYOUT["seen"]` (right); covers by name `:314` |
| 64 | hidden ways found | `layout.py:191-243` | 3g | F | | by the rule |
| 65 | the evening prompt | `evening.py:74-101` | 3f | T | part | the night's acts in prose, a copy of `NIGHT_VERBS` `:19` |
| 66 | what waits on one's answer | `evening.py:48-71` | 3f | T | | a line per kind of request |
| 67 | a morning meeting, witnessing | `evening.py:212-235` | - | T | | writes lasting lines |
| 68 | a craft by level | `knowledge.py:445-520` | 1, 2 | R | | [[D2-263 A craft a person knows at capable or known shows, where they look|D2-263]] over inputs, gives, hours, batch, season |
| 69 | a craft's card, its shortfall | `knowledge.py:344-416` | 1 | R | | |
| 70 | the run's views | `views.py:23-231` | 3h | R | | SQL over the journal |

Counted by the weakest part of each: R 17 (1, 5, 7, 10, 16, 17, 18, 19, 21, 23, 25, 33, 54, 61, 68, 69, 70), F 3 (20, 22, 64), N 22,
T 17, P 6 (9, 13, 27, 30, 32, 53), X 5 (29, 31, 42, 45, 59); a silent skip on 4 (6, 14, 16, 27).

## 3. Branches on named things

### 3.1 Counts

| File | All | in functions | in sign rows | in tables | By category |
|---|---|---|---|---|---|
| `signs.py` | 309 | 99 | 157 | 53 | weather 101, craft 48, building part 45, cover 37, terrain 25, resource 19, good 17, fitting 9, stage 6 |
| `perceive.py` | 23 | 17 | 0 | 6 | resource 10, craft 5, fitting 3, stage 2 |
| `prompt.py` | 51 | 43 | 0 | 8 | craft 13, fitting 13, building part 11, stage 7, cover 5 |
| `core.py` | 3 | 3 | 0 | 0 | stage 3 |
| `shapes.py` | 9 | 5 | 0 | 4 | craft 4, stage 3 |
| `view.py` | 2 | 2 | 0 | 0 | good 2 (the cat) |
| `views.py` | 0 | | | | |
| `layout.py` | 12 | 12 | 0 | 0 | cover 7, building part 3 |
| `evening.py` | 1 | 1 | 0 | 0 | fitting 1 (beds) |
| `wild/river.py` | 65 | 44 | 2 | 19 | resource 19, craft 15, good 8, cover 8, weather 7, stage 5 |
| `knowledge.py` (display and readiness) | 30 | 30 | 0 | 0 | craft 16, resource 7 |
| `modifiers.py` | 3 | 3 | 0 | 0 | craft 3 (the way "for") |
| **total** | **508** | **259** | **159** | **90** | weather 108, craft 104, building part 66, cover 58, resource 55, good 32, stage 29, fitting 29, terrain 25 |

The 159 in sign rows are mostly a row bound to a value of the state it is about (`x.weather == "fog"`: a sign about fog), which is
what a sign row is: 73 lines name one value. 32 lines name a class by a list (`in ("rain", "heavy rain")`, terrain in four names):
those are properties of the weather or terrain row (wet, muddy). The 90 in tables are tables keyed by row names kept outside the
rows (`TIER_LOOK`, `river.CARRIED`, `perceive.LAND_DRAWS`, the shapes' faces).

### 3.2 What each group should become

| Group (count, in functions unless said) | Where | Property of which row | Mechanism |
|---|---|---|---|
| fire at a fitting: hearth, fire ring (9) | `signs.py:1084`, `:1094`; `prompt.py:617`, `:635`, `:682` | `FITTINGS[f].fire` (exists) | building context, known lines |
| beds as dwelling (13) | `signs.py:1076`, `:1092`, `:1931`; `prompt.py:617-674`; `evening.py:36`; `layout.py:285`; `river.py:488`; `perceive.py:131` | a fitting's `sleeps` (today the name "beds" is the property); legitimately a core default if beds stay one row | contexts, known lines |
| processing and its fittings: smoke racks, brine pan (5) | `shapes.py:501`; `prompt.py:634`; `signs.py:1112` | `FITTINGS[f].process` (exists), `.apart` (exists) | known lines, visibility of tend |
| crafts worked today, read by name (13) | `signs.py:981-1003`, `:1079`, `:1964` | a technique's `sign` key (what its work shows: "furrows", "felling", "picks") | parcel and building context, or better the craft's own event bundle (§4.3) |
| crafts made today, read by name (24, in rows) | `signs.py:830-848` | the craft's own signs: `TECHNIQUES[t].signs` (sound "hammering", smell "baking") | event bundle on the craft |
| place repute: game, seam, quarry, brine; anvil, cellar (11) | `perceive.py:139-145` | `RESOURCES[r].repute`, `FITTINGS[f].repute` (words) | describe |
| water and fishing: `WATER_CRAFTS`, eel, salmon, lamprey, otter, fen, water (55 in `river.py`) | `river.py:23`, `193-252`, `339-437`; `perceive.py:301` | `TECHNIQUES[t].reads_as: ["fish"]` (exists for the hunt); the run's rows per `kinds.RUNS[kind]` with `{kind}` in their words; the covers' `water: True` | readings, river subject |
| covers by name in renderers (27) | `prompt.py:342-356`; `layout.py:307-316`; `signs.py:1045`, `:1252-1266`, `:2039-2593` | `COVERS[c].ground`, `.plots`, `.grazing`, `.wood`, `.water` | place line, overview, subject dispatch |
| tiers rich and grand, the monuments' look (12) | `layout.py:283-286`; `prompt.py:405-409`; `signs.py:1122` | `TIERS[t].named_on_arrival`, `.grand`; `MONUMENTS[m].look` | tier words, building line |
| the weir and the mill in the building line (6) | `prompt.py:412-423`; `river.py:94-138` | the building's gap (`has_gap` exists); the water system's line fragment (§8) | building line |
| fence kinds (3) | `prompt.py:450` | `FENCES[k].words` (exists, used by `signs.fence_context`) | place line |
| stages: youth, child, infant, elder (29) | `core.py:119`, `prompt.py:507`, `:819-836`, `shapes.py:419-490`, `perceive.py:299`, `river.py:268`, `:481` | `STAGES[s].words`; the act rows' `who` (`iface.WHO` "grown", "not youth") | words; the observer gate |
| goods by name: cat, meat, fish, seed goods, copper (20) | `view.py:164-171`; `prompt.py:619`; `signs.py:1729`, `:1763`, `:1778`; `river.py:257-258`, `:497-499`; `prompt.py:151` | `ITEMS[i].beast` (the cat is a beast in a store), `.seed` (exists in `SEED_CROP`), `.fresh: fish|meat`, a tool's `tier` | contexts, store diff |
| weather and terrain classes by list (32 lines in rows) | `signs.py:563-635`, `1507-1600`; `river.py:219-238` | `WEATHER[w].wet`, `.dark`; `TERRAIN[t].mud`, `.open` | sky and road rows |
| the ways' keys by name: "for", "on trouble", "meeting" (6) | `prompt.py:81-122`; `modifiers.py:45-93` | the way rows already hold `key` and `values`; the schema should read them for every way | reply schema |

Legitimately by name (core defaults): the six subject kinds (`parcel:`, `building:`, `herd:`, `person:`, `thing:`, `sky`), the
four levels of knowing, the seasons. They are the core's own categories, not rows of content.

## 4. What does not fit

### 4.1 The observer: what a person can perceive and is shown

Every line shown is gated by the observer: a row's `knows`, `lay`, `knack` (`perceive.py:284-324`, `signs.py:2660`), the expert's
threshold (`NOTICING.expert_at`), a kind one is familiar with (`wild.methods.familiar_of`), being old (`"elder"` as a pseudo-craft,
`perceive.py:299`), being the setter of a thing (`for_me`, `:242`), being of the holding household (`EMPTY` rows' `only`, `signs.py:1212`),
and for the interface the level of a craft ([[D2-263 A craft a person knows at capable or known shows, where they look|D2-263]], [[D2-350 Every act and every technique a person can take is registered with…|D2-350]] to [[D2-352 Familiarity and the interface|D2-352]]), the stage (`shapes._universal`, `:409`), holding gear
(`_holds_gear`, `:422`), being head (`shapes.py:487`), and on the rebuild `iface.WHO` (11 named conditions). These are three
implementations of one thing, and none is a row field the hypothesis names. **Pattern needed: an observer gate**, one registry of
predicates over the person's record (knows t at level ≥ l; reads as r; expert at r; familiar with k; stage in S; office o; holds
i; set it; holds the subject), named, each row (sign, act face, craft line, known line) carrying `seen_by: [predicate ...]` and
the rule's chance. The rebuild's `WHO` is the right shape for the interface; `practised()` should become its sign half.

### 4.2 The mind: dated records and "as you last saw it"

Seven stores, each with its own writer and renderer: beliefs by subject (`perceive.py:600-626`, `:740`), places (`:116`, `:630`),
kin (`:57-66`), beasts (`:337-354`, `prompt.py:432`), land (`:357`, `prompt.py:457`), things known (`things.remember`,
`prompt.py:870`), lines read (`buildings.read`, `prompt.py:694`), plus the lasting lines, chosen by keyword (`perceive.py:726`),
and the belief view's snapshot and diff (`view.py:115-178`). The hypothesis's "the book: structured fields only" is about rules,
not memory. **Pattern needed: a mind record**, `{subject, day, source (saw, worked, heard, seeded, told), lines, fields}`, one
writer called by the noticing step with the subject key, one renderer "as you last saw it, n days ago", one diff against the last
view; a line's lastingness as a property of the event kind or the sign row (`lasting: true`), never a word search.

### 4.3 Signs are three patterns, not one

1. **Rows about a subject's state**, over a context (the crop ripening, the store going down, the sky). This is the hypothesis's
   "signs: rows bound to a state property and a sense". It fits, if "a state property" means a field of a context namespace
   computed by code (P3's "the context its signs read").
2. **Bundles bound to an event or an act** (slaughter, a fight, a theft, a making, a reaping, a run going down). Today they are
   rows in `signs.py` read through a branch of code per event kind (`_aftermath`, `signs.py:1934-2020`), rows naming crafts
   (`:830-848`), and 95 hand-written event lines with a salience in the handlers (`w.event(...)`: 42 in `verbs.py`, 14 in
   `settle.py`, 9 in `farm.py`, across 15 files). **Pattern needed: an act's or a craft's own bundle**, rows on its registry row
   (`VERB[v].seen`, `TECHNIQUES[t].signs`, with the four kinds: to the doer, nearby, lingering, conditional), the event record
   carrying its age, so a new craft brings its sounds and smells with it.
3. **The noticing rule.** General, one code path but for `roll`'s `mult` and `least` (feature_packages §5): it fits.

And the subjects themselves: `facts` walks a fixed list (`signs.py:1221-1300`) and every system since adds its own walker (13 wild
walkers `signs.py:2023-2604`; the river's `day_signs`, `dawn_events`, `carried`). **Pattern needed: a subject registry**, each
subject kind with a walker (which instances are at this place), a context namespace, and its tables (feature_packages §5 has the
tables and namespaces; it lacks the walker as a registration).

### 4.4 Lines known without a roll

One's house (its store, door, fire, racks, goods at its door: `prompt.house_known` `:610-638`, `_house_lines` `:640-692`), one's
body (`view._self`), family (`prompt._family_lines`), one's beasts, one's agreements. Brief 4c §6.4 names them "known without a
roll". They are hand-written f-strings with named fittings. **Pattern needed:** the sign row with a scope `known: holder | self |
household`, read with chance 1 (the noticing rule already has `inside` and `happened_to` for this); or, if kept apart, a "known
line" row bound to a property, rendered from data. Either way one row format.

### 4.5 The reply in: schema and parse

The reply schema's 42 action keys are hand-written (`prompt.py:15-58`) and repeated in prose (`core.reply_text`, `prompt.REPLY_LINES`);
the free act is read by word lists (`shapes.py:68-143`). The hypothesis's resolver (4) covers a craft from its aliases
(`shapes.resolve`, the right way) but not the act faces, option values ("shut", "closed", "set shut" → barred: `DOOR_TO`), key
synonyms (`PEOPLE_KEYS`, `CRAFT_KEYS`), or the five other resolvers. **Pattern needed:** the schema assembled from the act rows'
arguments (the rebuild's `iface` arguments are the data for it), and one resolver over every row's `aliases`, including faces and
options.

### 4.6 The brief's candidates, for this area

| Candidate | Fits? | What it needs |
|---|---|---|
| evenings and talk | no | the evening prompt is prose (`evening.py:74-101`) with the night's acts listed by hand beside `NIGHT_VERBS`; needs a phase's prompt slot and the act rows' `when: night` |
| notes and memory | no | §4.2 |
| the journal and replay | yes | `views.py` is general SQL over the journal (3h); replay is the engine's |
| weather and the calendar, as shown | yes | sky rows over the weather's values (3g), once the classes are properties |
| theft and witness | mostly | witnessing is a scope (3g); theft is special-cased by event kind (`perceive.py:432`, `:472`): an event kind's `witnessed_only` |
| households and offices, as shown | partly | the head's lines by hand (`shapes.py:487`); the observer gate's office predicate (4.1) |
| care and children, as shown | no | `_family_lines` prose; the care act's interface is on the rebuild |

**Verdict: too few, and wrongly cut for signs.** Add four patterns (observer gate, mind record, subject registry with walker and
context, the reply schema from the registry) and split "signs" into subject rows and act bundles; known lines join the sign row as
a scope.

## 5. Taxonomy of the area (Zach's addition 1)

### 5.1 What is sensed or shown

| Kind | Members today |
|---|---|
| subjects of signs | parcel (crop, field, pasture, wild ground), herd (on its ground, astray, its empty home), building, person, thing (body, heap, pack, cache, set gear, grave, carcass), sky, road (stretch, landmark, trace, traveller), the night, a passing party, a hidden way, a wild kind's numbers by area, a wild group, a run at a water, a site (heronry, rookery, lodge), a load or marker of the year, a disease |
| prompt sections, system | who you are, the place, your people, how life goes (core), the rules, what you can do (shapes; old: verb lines and crafts), other places, the reply |
| prompt sections, morning | memory, Now, what happened yesterday, what you saw, this morning, what you read, Here as you see it (or what changed), You (body, meals, age, family, beasts, house), offers, agreements, as you last saw them, notes, closing |
| other calls | the evening, its answer wave, a meeting, the road's meeting waves, the urgent call, lightening one's load, memory at a stretch's end, talk |
| kinds of line | a sign noticed (with a chance); an event witnessed; an ambient line; a line known without a roll; a dated belief; a seeded or kept line; a line read on a building; a result of one's act; a refusal; a craft line by level; an act's interface; a rule's line |

### 5.2 What those lines read

| Group | Members |
|---|---|
| quantities | a stock's S/K (`x.r`, grass, the shallows), a store's goods and food in meals, a heap's bulk, a herd's head, a run's count against its year (bands), fuel in heat, beds against sleepers, ground spaces |
| rates and clocks | the day, the season and days left, ages since an event (`x.age`, `rec_age`), a crop's progress and ripe day, a lot's nights, the days since last seen, a fitting's wear |
| conditions | weather type and values, snow lying, cold, dark, ice, flow (low to flood), fenced and gate, lying, rotting, hungry, wounded, pregnant, the was/now of a flow or a store |
| capabilities (of the observer) | a craft's level and skill, readings (`knows`, `lay`, `knack`, expert, familiar), the eye, stage, office, holding, set it |
| links to other rows | a crop's crop row, a building's fittings, a thing's items, a herd's species, a carcass's killer kind, an event's craft, a claim's holders |
| words | covers' words and ambient, fittings' labels, fence words, tier words, stage words, numbers, skill words, layout words, the kinds' sign texts |

### 5.3 Families of mechanisms that could be one

| Family | Members today | What they share | A general version reads |
|---|---|---|---|
| sign row formats | the dict row (`signs.py`), `kinds.R(...)`, `river._row` and `DAWN`, `COVERS.ambient`, `PASSING`, event lines | a text, a sense, a plainness, a scope, a reading, conditions | one row schema with required fields and a loader check |
| subject walkers | `facts`, `_herds_out`, `_slaughtered`, `_aftermath`, 13 `_wild_*`, `river.day_signs`, `dawn_events`, `carried`, `things.at_node` | find instances here, build a context, emit rows | a subject kind's registered walker and context namespace |
| contexts | `context`, `building_context`, `person_context`, `sky_context`, `thing_context`, `herd_context`, `fence_context`, `carcass_context`, `slaughter_context`, `event_context`, `road_context`, `trace_context`, `night_context`, `river.day_context` | a namespace of fields from state | namespaces per package (`x.water.flow`), lazy (feature_packages §5) |
| observer gates | `practised`, `readable`, `knack`, `for_me`, `only`, `shapes._universal`, `_holds_gear`, `iface.WHO`, `crafts_lines`' levels | whether and how a person sees a row | one predicate registry, `seen_by` on rows |
| name resolvers | `shapes.resolve`/`craft_in`, `knowledge.resolve`, `perceive.resolve_target`, `placed.method_of`, `Here.person/building/parcel/herd`, `tags.thing_by_tag`, `apply_notes`' title match | a word to a row or an instance | one resolver over rows' names, labels and aliases, and the instances known to the person |
| mind stores | beliefs, places, kin, beasts, land, things known, read, lasting, own, days | a dated observation of a subject | one record and one renderer |
| known lines | `house_known`, `_house_lines`, `_family_lines`, `_beast_lines`, `view._self`, `here.meal_lines`, `book_lines` | lines about what is one's own | rows with `known: self/household/holder` |
| words tables | `NUM` (`signs.py:1303`), `NUMBERS` (`layout.py:330`), stage words (`core.py:119`, `prompt.py:507`, `:819`), `_fence_words`, `TIER_LOOK`, `_land_words`, the fuse choices' words | a row's or a value's words | words fields on the rows |
| act lists | `VERB`, `SHAPES` faces, `KEEP`, `NIGHT_VERBS`, `FUSE` choices, the evening's prose list, `REPLY_LINES`, `reply_text` | which acts exist, when, how said | the act rows (the rebuild's `iface`) with `when` and phase |

## 6. History (Zach's addition 2)

### 6.1 How the area was built

| Dates | What came | How |
|---|---|---|
| 23 Oct | the core: `Here`, `Mind`, perception (909 lines); signs as bundles per state (216), for buildings and people (103), the sky and wild resources ("every state now speaks through signs.py"); things, the road, traces, travellers and the night (577) | **new general system**: rows with `when`, `text`, `sense`, `knack`, read by one walker |
| 24 Oct | [[D4-53 Every sign and every event is noticed by the one noticing rule|D4-53]] one noticing rule with an extent by event kind; [[D4-59 Every newer system shows itself through signs|D4-59]] signs for the newer systems; [[D4-56 One knows one's beasts by memory and noticing, not by a list|D4-56]] beasts known by memory | **built into** the general system (rows), and the **first ad hoc mind store** (beasts) |
| 1 Nov | [[D4-71 A slaughter shows itself|D4-71]] slaughter (104), [[D4-74 Events and their aftermath show themselves as bundles|D4-74]] the 18 event bundles (308), [[D4-75 Every perceived line about the world comes from the one noticing rule|D4-75]] every line by the one rule (160); the belief view (222); the evening (205) | rows **generalised** (the one rule); event bundles **ad hoc per kind in code** (`_aftermath`); the view **new**, with its own diff |
| 2 to 8 Nov | plot shares (92: `HOLDING_ROWS`), graves, weather values read by the senses | **built into** rows, with one **positional hack** |
| 9 Nov | the wild layer: expert readings, signs sweep (105), waves 3 to 5 (loads, markers, disease, sites; about 230), `reads_as` | **new parallel system**: the kinds' own sign format and a walker per wave; one **generalisation** (`reads_as`) |
| 14 Nov | brief 4c: set things' looks (62), one's house known without a roll (89) | **built into** the thing rows; known lines **ad hoc** |
| 16 to 17 Nov | brief 5: the weir, the mill's gap, the smokehouse, the brine pan; the signs pass (171) | weir lines **ad hoc by name**; salt **by property** (`spring`); fish signs from the stock **into** rows |
| 23 Nov (the wave) | [[W-100 Build stage 4, signs, people and worlds|W-100]] u8 the river (529), u9 the prompt core and shapes (486); [[W-102 Fix the act shapes' interface faults found in live run 1's rebuilt arm|W-102]] the shapes read live replies (239); [[W-104 Build the after-runs list from live run 1|W-104]] rules not attendable; [[W-98 Build stage 2, taking and making|W-98]], [[W-99 Build stage 3, keeping, stores and the household book|W-99]] | the river a **new ad hoc system** (two formats, a name list); the prompt **from general back to hand-written** (the shapes replaced `verb_lines`); the parse **by word lists** |
| 24 Nov | [[W-109 The prompt's interface restored|W-109]] (branch): every act's interface in the registry, the renderer from it, a loader check | **generalised** |

Some dated examples of each:
- **New ad hoc system:** the beasts known (24 Oct, `perceive.remember_beasts`, a store of its own); the wild kinds' signs (9 Nov,
  `kinds.SIGNS` and 13 walkers); the house known without a roll (14 Nov, `prompt.house_known`); the river's record and signs (23
  Nov, `river.py`); the shapes' sentences (23 Nov, `shapes.SHAPES`).
- **Built into an existing general system:** [[D4-59 Every newer system shows itself through signs|D4-59]]'s signs for pregnancy, babies, led beasts, crowded houses (24 Oct, rows in
  `PERSON` and `BUILDING`); graves (4 Nov, rows in `THING`); a water's fish thin or plentiful from its stock (17 Nov, `WILD` rows
  over `x.r`); the shallows' ice (23 Nov, `x.ice`).
- **Generalised and extended:** every line by the one rule (1 Nov, [[D4-75 Every perceived line about the world comes from the one noticing rule|D4-75]]); `reads_as` (9 Nov); salt by the fitting's `spring`
  property (16 Nov, `signs.py:1117`); the interface from one registry (24 Nov, [[W-109 The prompt's interface restored|W-109]]).

### 6.2 The trend

Named branches in the area's function code, per thousand lines, at six commits (the area's files only; current tables):

| Commit | Date | Lines | In functions | per 1,000 | In rows | In tables |
|---|---|---|---|---|---|---|
| `c37df55d` | 24 Oct | 3,118 | 77 | 24.7 | 135 | 36 |
| `9e0c1b98` | 2 Nov | 4,423 | 118 | 26.7 | 149 | 57 |
| `e79309c8` | 9 Nov | 5,021 | 141 | 28.1 | 151 | 58 |
| `b30abc0b` | 17 Nov | 5,499 | 172 | 31.3 | 156 | 61 |
| `f728a3b7` | 23 Nov (baseline) | 5,506 | 173 | 31.4 | 156 | 61 |
| `6b609f48` | 24 Nov | 6,770 | 226 | 33.4 | 159 | 90 |

**Getting worse in function code, steadily**, and fastest in the content waves (the wild layer, brief 5, the wave); sign rows are
flat (the row format held). The infrastructure passes ([[D4-75 Every perceived line about the world comes from the one noticing rule|D4-75]] on 1 Nov, [[W-109 The prompt's interface restored|W-109]] on 24 Nov) generalise, but each comes one to two weeks
after the spread it repairs, and the content waves between them add more than the pass removes. Sign formats went from one (23
Oct) to five (9 Nov: the kinds' `R`; 23 Nov: the river's two; the ambient tuples were there from the start).

## 7. What in the process let ad hoc systems in (Zach's addition 3)

1. **No check at load, no required fields.** A sign row has no schema, no name and no loader check (`signs.py`; feature_packages
   §5 proposes names and a declaration test, phase 1b, not built). A row whose condition raises is silently dropped
   (`signs.py:1235`, `:2674`; `river.py:442`), so a row reading a field that does not exist passes every test. Nothing refused a
   new format, so the wild layer and the river each made one.
2. **The guide told builders to write code per bundle.** `guides/senses.md` checklist step 2: "Add any state the conditions need
   the way similar systems do", reading its context builders; nothing says "as a property of a row" or "never a name". The
   module's own rule, "New states add rows here, not code ([[D4-24 The world grows by data, and agents explore and learn it|D4-24]])" (`signs.py:6`), was read as "rows for the signs", while the
   contexts grew by name.
3. **Briefs specified content, not shape.** The wild briefs, brief 5 and u8 asked for signs by kind and by run, with texts and
   chances, and were done to the letter (`kinds.SIGNS` "Data in the kinds' rows", `signs.py:2025`); none named the row format or
   the readings to reuse, so `WATER_CRAFTS` (`river.py:23`) was written beside `reads_as` (9 Nov). [[D2-244 The engine's reworking into feature packages|D2-244]]'s feature units (20 Nov)
   put each feature's rows in its own module, which is right for locality, but with no core row schema it multiplied formats.
4. **The prompt rebuild was reviewed for words, not for coverage.** [[W-100 Build stage 4, signs, people and worlds|W-100]] (u9) replaced the registry-read `verb_lines` with eleven
   hand sentences; its tests checked the rendered text, not that every act and option appears (prompt_compare.md §1 to §3: 7 acts
   never named, 6 reduced to a word, options of 5 shapes gone). The coverage test came with [[W-109 The prompt's interface restored|W-109]].
5. **Live failures were fixed at the parse.** [[W-102 Fix the act shapes' interface faults found in live run 1's rebuilt arm|W-102]] (239 lines) answered live run 1's replies with word lists in `normalize`
   (`KEEP`, `DOOR_TO`, `PEOPLE_KEYS`, `CRAFT_KEYS`), the fastest fix for a run in hand; no alias field on the rows took them.
6. **Known faults were recorded and left.** The feature_packages inventory (16 Nov) named `HOLDING_ROWS = range(3, 10)`, the
   lowest-index rule, lasting memory by keyword and the shared notice sequence; phase 1b (2 to 3 days) was postponed ([[D2-244 The engine's reworking into feature packages|D2-244]]), and
   the wave built on them. [[D2-353 Everything new in the engine is built within the agreed architecture…|D2-353]] (24 Nov) adds the guard test on named branches; it did not exist before.

## 8. The balance ([[D2-354 The architecture is a healthy balance, not a strict one|D2-354]])

**Where a general primitive should own the behaviour.**
- The noticing rule (owns it already) and one code path for chance (`roll`'s `mult` and `least` as rows declared exempt).
- One sign row schema, named rows, `rank` and `replaces`, a loader check, a declaration test; known lines as a scope of it.
- The observer gate: one predicate registry for signs and interface.
- One resolver over rows' names, labels and aliases (faces, options) and the instances a person knows.
- The reply schema from the act rows' arguments.
- The mind record and its renderer.
- Words of rows (stages, numbers, fences, tiers) on the rows.

**Where a system legitimately owns specifics, and how to keep them inside it.**
- The water system owns the run's bands and windows, the flow, the weir's sections and gap, the readings "a run night" and "the
  river too low for the eels": its context namespace (`x.water.*`), its walker (a run at this water), its rows in its folder. Kept
  in: no name of its rows in `perceive.py` or `prompt.py`; the building line takes its gap words through a fragment it registers.
- The wild layer owns its population thresholds, groups, legends, markers and the expert's readings of a kill: its walkers and
  contexts, its rows (converted to the one format) in `cybertron2/wild/`.
- Buildings own tiers, rooms, storeys and the monument's look; farming owns holdings and the shares' words; life owns the family
  lines' facts (whether a child was fed and cared for). Each keeps its words in its rows and its lines as known-line rows.
- The prompt core owns its frame (the twelve lines): hand-written and legitimately so, but as named lines with `requires`, not
  variants by index.

**Extension points a primitive needs, so features extend it instead of bypassing it.**
1. A subject kind: walker, context namespace, tables (the wild layer and the river needed it and made walkers instead).
2. Readings on a technique row (`reads_as`, an expert threshold) and named observer predicates (stage, office, holding).
3. Signs on an act or craft row (`seen`, `signs`), for the doer, nearby, lingering and conditional.
4. A line fragment slot on the building and place lines, by property (`has_gap` → the water system's words).
5. A known-line scope (`known: household`), so a new container's state shows in one's house without code in `prompt.py`.
6. Aliases on act faces and argument options, for the parse.
7. Named prompt lines and sections with `requires`, and a phase's prompt slot (the evening, the urgent call).

**From the history: ad hoc because the general system could not be extended.** The wild walkers (9 Nov: no subject registry, so
`_aftermath` gained calls), the kinds' and the river's row formats (no way to declare "read by an elder" or "by the crew", so
`_knows` and the `"elder"` pseudo-reading), the weir in the building line (16 Nov: no fragment slot), the house known without a
roll (14 Nov: no known scope), the evening's request lines (no pending-answer registry).

**Ad hoc though the general system could have taken it.** `WATER_CRAFTS` (23 Nov; `reads_as` existed since 9 Nov); hearth and
fire ring by name in four places (`fire: True` on both rows); `f == "smoke racks"` beside the `process` property (`shapes.py:501`);
`_fence_words` (`FENCES[k].words` existed and `signs.fence_context` uses it); the stage words copied into `core.py` from
`prompt.py`; `BOOK_KINDS` copied from `book.KINDS`; the shapes' sentences (23 Nov; `VERB` had args, doc and cost and the old
prompt read them); the craft-named "made" rows (a craft's own row could hold its sound).

## 9. The interface rebuild (`w109-interface`, not merged)

**What it covers:** every act's interface in the registry (`verbs._IFACE` into `VERB[v]["iface"]`: faces with shape, word,
arguments and every option, what it does, needs, cost, who); the set everyone knows as data (`verbs.EVERYONE`); the crafts' and
ways' interface fields (`data.py`: `does`, `args`, `takes`); a loader check (`iface.check`, raising `RegistryError`); who is shown
what as named conditions (`iface.WHO`); the renderer reading only the registry (`iface.lines` replaces `shapes.lines`);
familiarity per [[D2-352 Familiarity and the interface|D2-352]] (aware: the name only; rough: the minimum interface; known: the full line); the shapes' sentences cut to a
grammar line each; `look_up` back; a coverage test of every act, argument, option and way, a replay of live replies. Measured on
the branch: `iface.py` has 4 named branches (stages in `WHO`); `shapes.py` 8 (from 9).

**What it leaves:**
- the reply schema's keys, hand-written (`prompt.py:15-58`), and `core.reply_text`'s prose;
- the parse's word lists (`shapes.py:68-143`) and the other four resolvers; only `_said_with_what` reads the registry;
- the core lines' variants by index (`core.py:62-74`);
- the evening prompt and its prose act list beside `NIGHT_VERBS`, the request lines, the urgent call's choice words, the meeting
  and road prompts;
- the morning message: house, family, place, building and beast lines (`prompt.py`, `view.py`), with their named fittings;
- everything about signs and noticing, the observer's readings (`perceive.practised`), the mind's stores;
- the old prompt (`verb_lines`, the old system prompt), kept for old worlds ([[D2-314 The eleven act shapes are the verb list|D2-314]]);
- two things it introduces to watch: the interface fields are written onto rows by name in a block in `data.py`
  (`TECHNIQUES[_k].update(...)`, `data.py` on the branch) rather than in the rows themselves, and `iface._sets` reaches
  `shapes._containers`, which still names "smoke racks".

## 10. The restructuring's cost for the area

In feature_packages.md §10's terms (a builder-day: about 300 to 400 lines a day for rewritten shared-file code, 2,000 for moves):

| Step | Lines touched | Builder-days | Behaviour | In §10 already? |
|---|---|---|---|---|
| 1b: sign names on about 860 rows (signs.py, kinds, river; mostly generated), `rank` and `replaces` for `HOLDING_ROWS` and the lowest-index rule, keyed notice draws, the declaration test in place of the silent excepts | about 900 | 2 to 3 | changes noticing draws (decision, open question 4) | yes |
| one sign row format: the kinds' `R`, the river's `_row` and `DAWN`, the ambient tuples, `PASSING` converted; loader check | about 500 | 1.5 | none once draws are keyed | no |
| subject registry and namespaced contexts: `facts`, 13 wild walkers, the river's walkers as registered subjects; the about 150 function-code branches of table 3.2 as properties | about 1,500 | 4 to 5 | none if exact; golden journals | partly (signs walker and contexts, about 1,000) |
| event and craft bundles on the rows: `_aftermath`'s kinds, the "made" rows, the 95 event lines (mostly B's handlers) | about 600 | 2 | none if the texts are kept | no |
| observer gate: `practised`, `readable`, `knack`, `iface.WHO`, `shapes._universal` | about 250 | 1 | none | no |
| mind record: seven stores, one renderer and diff; lasting by flag | about 500 | 2 | prompt text changes | no |
| prompt slots and known lines: core lines by name, house, family, building and place lines as rows, the evening and fuse prompts from rows; the schema from the act rows | about 900 | 3 to 4 | prompt text changes | yes (prompt into slots about 700, view about 200) |
| one resolver; the parse's word lists to aliases on rows | about 400 | 1.5 to 2 | the replay test ([[W-109 The prompt's interface restored|W-109]]) must show no reply refused that was accepted | no |
| **total** | **about 4,000 of 6,770** | **about 15 to 20** | | about 8 of them |

**Risk.** (1) The prompt is the stimulus: a reworded line changes what agents do, so each step that changes rendered text needs a
prompt snapshot and a decision on which runs it invalidates, and should land on a named day with the others (as §9.1 proposes for
1b). (2) Keyed draws change what everyone notices. (3) Two prompts are live (old worlds keep the old one, [[D2-314 The eleven act shapes are the verb list|D2-314]]): migrating both
doubles the work; freeze the old path (`verb_lines`, the old system and turn prompts, about 500 lines) rather than move it.
(4) The parse: a reply accepted today must not be refused; the [[W-109 The prompt's interface restored|W-109]] replay of live run 1 is the guard.

**What it saves.** In this area a feature today costs its own module plus edits to three to five shared files: the water system (brief 5
and u8) put 508 lines in `river.py` and about 100 in `signs.py` (`_wild_river`), with a name list in the readings
(`perceive.py:301`) and a branch in the building line (`prompt.py:412-423`); the wave added 85 named branches in a day and two sign formats. After: rows, a context namespace and a walker
in the feature's folder, no edit to `signs.py`, `perceive.py` or `prompt.py`, and the guard tests (loader check, declaration test,
named-branch guard, coverage) catch what review missed. `signs.py` and `prompt.py` are two of the five hub files (47 and 48 of 208
engine commits, feature_packages §11), so this area is where concurrent sessions meet most.

*Current as of 24 Nov 2026.*
