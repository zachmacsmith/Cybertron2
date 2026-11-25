# What else the wave broke: an audit against the engine before it (37.2, W-109, 24 Nov 2026)

At Zach's ask (24 Nov): "check there aren't other things you broke like this in the current wave of updates". "Like this" is the
prompt: a general path (every act read from `VERB` and `MODIFIERS`) replaced by hand-written text, so that what was not written in
vanished from what agents see. That case (the act list and its arguments) is W-109's own (`iface_brief.md`, `prompt_compare.md`)
and is not re-audited here.

**The baseline** is f728a3b7 (23 Nov, before W-97), against `main` at a217daab: 128 commits, 100 code and test files, +33,548 lines
-1,310 (`git diff --stat f728a3b7..a217daab -- cybertron2/ tests/ tools/`). Both were checked out as worktrees and run side by side.
Probes are in `wave_regressions_probes/` beside this file (each runs from the repository root with `PYTHONPATH=.`).

**How it was checked.** (1) Ten worlds made before the wave run for 2 days with the scripted bots at both commits, two of them
also for 20 days, with their replays and frames; (2) the system and the first two turn prompts of one founder of each world diffed
at both commits, section by section, and Eelmouth's main and old arms' turn prompts diffed at main; (3) the `VERB` table, the
modifiers and the techniques diffed as data; (4) the code diff read for each of the paths named in the brief (renderers, signs,
perception, the evening, the book, the stores, the fill and founders, the gate check); (5) the stage reports' "what was built" and
"Not done" set against the diff; (6) the test diff read for deletions, skips and widened assertions; (7) the gate check and the dry
probe run on five old worlds at both commits.

## The findings, by harm

### 1. Old fishing worlds can no longer set traps in the water at all (breaks a run)

**What:** setting gear now lays wicker traps from the hands (`engine/placed.py:130`, "You have no wicker traps in hand"), and the
traps are made goods whose craft (`engine/gear.py:61`, `making wicker traps`) is not basic. The worlds made before the wave seed
neither. In `water/river` 26 people know `trap in water`, in `water/lake` 14, in `water/runs` 45; none holds a trap and none knows
how to make one, so no one in those worlds can ever trap, for the whole run.

**How it shows:** `wave_regressions_probes/old_fishing_worlds.py` on each world: at f728a3b7 "You set traps in the water at
Saltwell Water; they will catch by night for about 8 nights"; at main "Refused: gather: You have no wicker traps in hand", and with
withies in hand "Refused: make: making wicker traps is not among your crafts: you have never learned it". (Angling still works: a
rod is basic, withies 0.1.) The 20-day bot run of `water/runs` ends with 8 alive at main against 12 at f728a3b7 (the generic bots,
not evidence about behaviour, but in the same direction).

**Introduced:** 653737c4 (W-98, "placed gear set from the hands", fault 12) on 8ad7c50f (W-98, gear as goods).

**Reported?** Half. Stage 2's gate table (`stage2_report.md` §7) lists M6 on `water/river`, `water/lake` and `water/runs` and says
"the M6 findings on the older water worlds are their missing making crafts, which U11's livelihood rows will seed". Stage 4 (U11)
seeded only Eelmouth; its gate table shows only the people checks, and nothing records that the older water worlds still cannot
trap. `python3 -m cybertron2.landgen.gate_check cybertron2/specs/water/river.yaml` today refuses the world (M6 x6), but `World()`
loads and runs it regardless (stage 2 "Not done": a refused world raising in `World` was U11's; not built). It also goes against
D2-314's "old worlds keep the 38".

**And the dry probe now hides it** (finding 9): at f728a3b7 `python3 -m cybertron2.landgen.gates cybertron2/specs/water/river.yaml`
listed `snare` and `trap in water` as working at Saltwell and Millham; at main they sit under "not now (the moment or inputs)",
because "in hand" was added to `SITUATIONAL`.

### 2. The state of one's gear never reaches anyone in a beliefs-view world (hides something agents need)

**What:** u3 §3.5's "Of your gear: 6 wicker traps: 1 broken, wanting mending; the rest new" (shown, not sensed) was added to
`prompt.turn_prompt` (`engine/prompt.py:775`), which a world with `view: beliefs` does not use. The beliefs view builds "## You" in
`engine/view.py:94-112`, which has the meal line, the age and the rest line but not the gear line. Eelmouth (both arms) and every
live run is a beliefs world.

**How it shows:** `wave_regressions_probes/gear_line.py`: with one of Peter's traps worn to broken, `prompt.turn_prompt` shows it,
`view.turn` (opening and not) does not. In a 2-day Eelmouth bot run, 0 of 16 turn prompts carry the line. A fisher learns a piece
broke only from a tend's result, and never how much life the rest has.

**Introduced:** 8ad7c50f (W-98). Stage 2's file table says "`engine/prompt.py`: ... 'Of your gear: ...' for one's worn gear in hand",
true of a path no live world takes.

### 3. Crafts lost their hints and their sources in the crafts lines, in the old prompt too (hides something agents need)

**What:** `knowledge.crafts_lines` used each technique's full label for the crafts one knows, is capable of or has a rough idea of;
`craft_line` (`engine/knowledge.py:451`, used at :498-501) uses `label(tech)`, which cuts the label at " (". Eighteen non-basic
techniques carry their working hint there: `drive` (beaters and spears; others with you; dangerous), `den work` (spades and a dog
help), `stalk` (slow, downwind, close in for the shot), `milk` (a cow in milk), `wall` (a dry-stone wall), `weir` (stakes and
wattle across the river, wicker traps in its gap), `medium room` and `hall` (timber on stone, or stone), `creel`, `keep box`,
`gill nets`, `dip net`, `sack`, `salting tub`, `barrel`, `chest`, `hurdle`, `brine pan`. The rough and capable lines also lost where
the craft came from ("(from your upbringing)", or who taught it), which says whom to ask.

**How it shows:** system prompts at both commits. `water/lake`, Basilia: "digging out a den or trapping at a lodge (spades and a dog
help) (novice)" becomes "digging out a den or trapping at a lodge (known, novice: 3 units; on forest or ...)"; `hollins2_s8`, Sibyl:
"milking (a cow in milk) (from your upbringing)" becomes "milking (a rough idea: no materials, on pasture or ...)".

**Introduced:** 07eec413 (W-98, "craft lines by level (D2-263)"). `prompt_compare.md` §4 notes the loss for the core prompt's
shapes; this is the other path, `crafts_lines`, which the old prompt (every old world, and Eelmouth's comparison arm) reads. The
W-109 rebuild should cover both.

### 4. A cairn costs nothing, anywhere, and each act begins another (changes what agents can do; contradicts a report)

**What:** MONUMENTS `cairn` went from 6 stone to `materials: {}` (`engine/data.py:417`, "stones got on the spot (D2-306)"), but
gathering at the site is stage 5's and is not built, so a cairn now needs no stone at all. A cairn is a monument with 3 lines to
write. Since nothing gates it, every `build cairn` act begins a new one.

**How it shows:** `wave_regressions_probes/cairn.py` on `valley_s5` with no stone at the node: f728a3b7 "Refused: build: it needs 6
stone"; main three acts give three unfinished cairns (`b13`, `b17`, `b21`). The old system prompt renders it "cairn (, 3 units of
work, a monument: no room, 3 lines)" (`engine/prompt.py:167` joins the empty materials).

**Introduced:** 28f05dbc (W-97). `stage1_report.md` §6 says "Fences, walls, clearing, terraces, the burial cairn: their materials
stay in today's counts"; the burial's `method: cairn` kept its 3 stone, the cairn monument did not.

### 5. Signs: the river's run rows hand-written per kind, and fitted to Eelmouth (cosmetic now; a new run kind gets no sign)

**What:** the run rows were generic over `RUNS` (`wild/kinds.py` RUN_SIGNS `down`/`up`: "the {kind} are running at {place}
tonight", "{kind} going up through {place}"). `signs._wild_river` now skips them for every world (`engine/signs.py:2476`, `key in
("down", "up")`) and `wild/river.py:193` DAY writes rows for eel, salmon and lamprey by name. A kind added to `RUNS` would run unseen;
the "knows" row for a run going up (salmon, lamprey: "a run night") has no counterpart. The sky's two flood rows are off wherever the
river keeps a record (`engine/signs.py:575, 577`), so the old runs worlds get the new flow rows instead, whose `own` was raised "to
land from the Street" (Eelmouth's geometry; `river.py` comment, stage 4 §3).

**How it shows:** 20-day bot runs. `water/runs`: river lines in turn prompts 0 at f728a3b7, 64 "the roar of ... in spate, heard from
the houses" at main (of 100 matching lines); `runs_high` 0 and 45. No eel or salmon run line reached a prompt at either commit in 20
days, so the run rows themselves could not be compared live.

**Introduced:** ada5c3a4 (W-100). `stage4_report.md` §4 says "the new behaviour sits behind `prompt: core` and `learning: record`,
which no older world sets"; u8's river rows are not behind either, and they change every runs world.

### 6. "Fish" hard-coded where the engine holds meat or anything (cosmetic, misleading in a meat world)

- `engine/process.py:678`: a smokehouse tended after its lots are done says "the fish on the racks have had their smoke", whatever
  hangs (0965a4d0, W-99). The valley worlds' smokehouses hang meat.
- `wild/kinds.py:564` EATEN_SIGNS `hung`: "something has been at the fish hanging in {place}" for any hung lot (3a1962e3, W-99).
- `engine/signs.py:857`: the smell is "fish" or else "meat" (ada5c3a4); the sight row no longer names what hangs ("smoke rising from
  ... this morning", u8 §5, decided; its test was changed in stage 4 §4).

### 7. The smokehouse's fire risk is no longer told in the old prompt (hides a risk)

The smoke meat and smoke fish cards ended "a wattle smokehouse can catch fire" (data.py at f728a3b7, lines 629 and 635); the rows'
`manual` now comes from `process.py` and does not say it. The fire still rolls (`process.catch`, tested). Eelmouth's keepers are told
in their seeded line (`founders.py:480`, "a wattle hut can catch and burn"); a person in an old world is not. Introduced 0965a4d0 (W-99).

### 8. Founders' fisher lines assume an eel run on any water (latent: wrong lore on the next world)

`FI1` (`engine/founders.py:333`: "The eels go down to the sea in autumn ... can look empty all summer and still run thick then") and
`FI2` check only that the household has water; `HH10` (:297, "when the eels run in {water}"), the neighbour line `NB["fisher"]`
(:1769, "they know when the eels run ... in late autumn they have fish to spare") and `_BUSY`/`_busy_season` (:1657, :1674, "the eel
run") likewise. The helper that asks whether eels run there exists (`_runs_here(c, "eel")`, used for the mill at :1263) and is not
used. True of Eelmouth; a fill of a lake or salmon village (stage 5's Hollinford maker) would seed false lore word for word, for life.
Introduced 0012b5ea (W-100), dfa4b58f (W-105).

### 9. The gate check: loosened and fitted (hides world faults at design time)

- `landgen/gates.py:29-32`: `SITUATIONAL` gained "in hand" and "here you can use", substrings broad enough to pass any refusal for
  want of gear, and the dry probe's exit code no longer flags it (finding 1). M8 also passes any refusal containing "spring", "racks"
  or "full" (:357). eff4c7e9 (W-98).
- M3 checks only `trap in water` (`SEASON_GEAR`, six a setter: D2-330's C5 for Eelmouth); snares, gill nets and set lines before
  their season are not checked. M7's need is written as numbers (`10 * 0.25 + 5 * 0.25 * ...`), not read from `WATER_WORKS`. M3's
  "about 47 units to make them" is computed at a rough hand even where M6 says no one can make them. `_first_run_day` swallows every
  exception and returns None (:229), which skips M3 silently. `cuts = ... or True` (:285) is a dead test.
- `landgen/gate_check.py:102` (P14) passes a head's lines only if they contain the founders' own words ("Our store at", "go first or
  go off", "whoever heads it after me"): a hand-written world's head lines fail it, and a rewording in `founders.py` breaks it.
  0012b5ea (W-100).

### 10. The book's morning lines only at the opening in a beliefs world (hides a little)

`engine/view.py:110` shows `PR._house_lines` (which carries `here.book_lines()`: "Waiting today: ... (rule n)", "Not done by the rules
yesterday", "Against the household's rule n") only on a full turn; otherwise only the empty chores (`book_empty_lines`). In Eelmouth
the evening's "## The standing rules" carries the day's misses and breaches for a head with rules, so what is lost on an ordinary
morning is "Waiting today". 13f8a0e0 (W-104).

### 11. The old prompt carries two grammars for rules (cosmetic)

The rules block (D2-339: set, keep, first, share, do, drop) now opens every old world's system prompt, and its verb list still shows
`rule {"rule": go | keep | hold back | first | eat | move | tend | chore | drop, ...}` (`engine/verbs.py:102`, 3a1962e3), the kinds
D2-339 replaced (converted when read, so they work). `prompt_compare.md` §5 notes this for the core prompt; it is in the old one too.

### 12. The generic bots on old worlds no longer work or make (smoke coverage)

`knowledge.doable` (`engine/knowledge.py:522`, 8c6560c6, W-97) keeps the shortfall test but no longer filters by sites ready now, and
`run.bot_plan` takes the first four sorted: four gathers fill every plan. `valley_s5`, 2 days: work 14 and make 5 at f728a3b7, 0 and
0 at main; refusals 100 and 105. A smoke run on an old world no longer exercises working or making.

### 13. Reported, but larger for old worlds than the reports say (for the record)

Each of these is in a stage report or a decision; none was read against the old worlds' designs, whose scarcities they move:

- **Carrying:** on foot 10 (kg) against goods now in kg (timber 25, stone 25, firewood 10, withies 10): in a multi-village old world
  no timber or stone can be carried on foot (was 5 timber); a pack basket makes 25. An Eelmouth fisher's six seeded traps weigh 15 kg.
  Turn prompts read "weight 185.9 of the 10 you can travel with". (Stage 1 §4; stage 4 "Not done": the carry line in kg.)
- **Heat:** Hollins' heat bound went from 14 people to 199.5 (stage 1 §4, `test_cybertron2_package_f.py`); the old worlds where fuel
  bound now bind on food alone.
- **Building:** a wattle room 8 timber to 36 timber and 35 withies; an upgrade to timber 18 timber to 360 timber, 135 stone, 33.7
  withies and 168.7 straw; a stone room 30 stone to 1,600 (stage 1 §1).
- **Stores:** bins no longer hold fresh food (u5), so it lies on the floor; the fallback stands until changed and units left are
  "rested" in old worlds too (D2-301).
- **The water's notice group** (`wild/kinds.py:418`, `"water": []`, a24dbf8e) is still empty: set gear and the edge on water turn up
  no incidental finds. Stage 1 said "U8 writes them"; stage 4 did not, and no deferral row records it.

### 14. Tests: what was loosened

No existing test was skipped; two new modules skip without live run 1's record on the machine. No test was deleted without a
replacement. Widened or weakened, each with its reason in the test:

- `test_cybertron2_water5_keep.py`: the hearth-rack-only glut's loss band 0.18 to 0.40 became 0.30 to 0.55 (D2-336's fresh rate);
  the household-sees test no longer asserts the untended-fire warning (it is still built, `process.py:672-673`); "dry overnight, put in
  the store" is gone (a done lot stays on its rack, u4).
- `test_bots_livelihood.py`: the setting tests moved from the low arm to the medium arm (the low arm holds no traps), with a weaker
  low-arm test ("cuts withies or makes traps"); "≥ 10 settings" became "≥ 6"; "nobody's traps but one's own" checks a different
  phrase ("not yours to take from").
- `test_cybertron2_water_bodies.py`: "fish by hand" at each body became angling with a hand line (the edge draws the shallows, u1).
- `test_cybertron2_wild_calibrate.py`: the hearth rack's dried meat test became a test that a night by a cold hearth does not count.

## Checked and found fine

- **Old worlds load, run, replay and render:** `valley_s5`, `wenbridge`, `water/river`, `water/lake`, `plenty/brookend`,
  `peoples/w1`, `hollins2_s8`, `ladder/ladder_b13`, `nutrition/runs_high`, `combe`, 2 days with bots at both commits, no errors
  (`two_commits.sh`); `water/runs` and `runs_high` 20 days, no errors; replay of `water_river` and `valley_s5` at main, 16 steps, no
  mismatch; `frames` at both commits for three of them. Eelmouth cannot load at f728a3b7 (`KeyError: 'hand line'`), as expected.
- **The verb table:** no verb and no argument key removed between the commits (`rule` and `tend` added); no modifier removed; no
  technique removed; the only technique change in kind is the weir, no longer basic (fault 4, reported).
- **The old turn prompt:** besides the options list (D2-286, decided), it changed only by the meal line, the store by portion, the
  new crafts and the kg figures. Eelmouth's main and old arms' turn prompts are the same but for the kept lines and the closing line.
- **Stores and spoiling:** a failing building still spoils as the open and a gappy one by its damp (`stores.rates`); the smokehouse
  still catches and spreads by structure (tested, `process.catch`); a neighbour's lot waits for them.
- **The evening:** free acts allowed at any units, priced acts still checked against units left; rules at the evening (D2-319).
- **Perception:** the dawn's duplicate-text skip, the fisher's reading of water signs (D2-325), rules not attendable (D2-341).
- **Ice:** `water.ice` falls back to "open" on an exception, but `wild.frozen_run` raised on none of four worlds over a year.
- **Old runs worlds' river signs** fire (the flow rows); worlds without a river record keep the sky's flood rows.
- **No engine code names Eelmouth's places** (grep for Eelmouth, the Isel, the Marsh Smokehouse, Clay Field outside comments and
  the name lists).
- **The book in an old world:** no books, no effect on the meal or the stores.

## What to do (for Zach; nothing changed here)

Finding 1 wants a choice: seed the older water worlds' trappers with traps and the craft (as `make_nutrition_runs.py` does for the
runs arms), or have `World()` refuse what the gate check refuses. Findings 2, 3 and 11 belong in W-109's rebuild (the beliefs view's
"## You" and `crafts_lines` are interface paths the brief does not name). Finding 4 wants the cairn's 6 stone back until D2-306's site
gathering is built. Findings 5, 6 and 8 want the rows and lines read from the data (`RUNS`, the lot's item, whether eels run there).
Finding 9 wants `SITUATIONAL` narrowed and M3 to M7 read from the data.
