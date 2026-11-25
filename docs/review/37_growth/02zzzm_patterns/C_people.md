# Survey C: people and society against the patterns (W-110)

Session 37.2, 24 Nov 2026, survey agent C. Brief: [brief.md](brief.md). Files: `cybertron2/engine/` life, learning, knowledge,
memory, founders, livelihoods, book, agreements, exchange, settle, parties, roads, here, run (the day's order), evening, journal,
bots_livelihood (11,262 lines; 4,787 added in the wave since f728a3b7). The branch count is [C_branches.py](C_branches.py)
(`python3 -I docs/review/37_growth/02zzzm_patterns/C_branches.py --list`). No engine code, spec or design file was changed.

## Summary

**Mechanisms: 126 counted** (table 1), by their main fit today:

| Fit today | Count | Examples |
|---|---|---|
| G: general over rows | 63 | stages on LIFE's clock, the book's grammar, agreements' legs over any good, signs on the road |
| GF: general, with fitted constants in code | 21 | conception and deaths, fights, learning classes, the memory budget |
| N: a special case by name | 20 | `knowledge.ready`'s eleven stock thresholds, `HL`'s six holding kinds, fill's fisher gear, landmark challenges |
| W: a word-list or regex parse | 12 | `book.seen` matching sign text, `book.target`, `parse_legs`, `KNOWN_SOMEWHERE`, `PE2` reading relations |
| H: hand-written text | 9 | 117 founders' templates, the evening prompt's act list, `age_line`, the old craft card |
| S: a silent skip | 1 | a founder's line dropped when a technique name is absent |

Of the general ones, a further 11 carry a branch by name, 3 a word parse and 5 hand-written lines (marked "G + N" and so on in the
table). 59 of the 126 came or changed in the wave.

Besides its fit, **9 mechanisms write state outside the chokepoint** (learning records, teaching's skill, a road stop, a guest's
bed), so those changes reach the journal only in checkpoints, never in its `changes` table (journal.py:274).

**Named branches in function code: 375** (C_branches.py), **282 of them (75%) added in the wave**. By file: founders 195,
livelihoods 41, knowledge 40, life 31, bots_livelihood 29, book 19, roads 10, settle 4, run 4, exchange 1, here 1. By kind (a name can be in several registries): life stages 75, crafts 54, fittings 46, covers 20, stocks 20. On top of those come **module-level name tables
inside code modules**, which the AST count does not see: `learning.CLASS_OF` (31 crafts), `book.KIND_GOODS` (33 goods),
`book.GOOD_SYNONYMS` (15), `book.SEEN` and `SEEN_NAMES` (36 words), `founders.NB` (13 livelihoods), `_BUSY` (4), `KEEPER` (10), and
three disagreeing lists of verb names (`verbs.FREE` 24, `book.FREE_OR_TRAVEL` 25, `evening.NIGHT_VERBS` 25).

**What does not fit.** About half of area C is not physics, and the hypothesis is a set of physics patterns. Four kinds of
mechanism have no pattern:
1. **records with terms and a settling step:** agreements and debts, offers, claims and inheritance, household offices and
   succession, the book's rules;
2. **matched intentions:** two people choosing the same thing the same day at one place (partners, trying for a child, teaching
   and learning, joining and admitting, a hunting party, care, offers taken);
3. **familiarity records with a curve:** crafts, landmarks crossed, wild kinds, places and kin;
4. **one condition grammar** shared by the book's rules, the pulses, landmark trouble, the founders' lines and the signs.

Two further things are missing that the hypothesis assumes exist: **the day's order** as a declared phase list, and **one name
resolver** (area C alone has at least nine).

**Verdict for area C: too few, and partly wrongly cut.**
- **Too few:** the eight mechanisms cover the demography (pulses and lives), the road (pulses and signs) and the founders'
  generation (pattern 5). They leave out the social records, matching, familiarity and conditions above, which are most of the
  area's lines.
- **Wrongly cut:** learning is filed under (e) "lives and wear on a clock", but it is a curve on practice with fading on a clock.
  It is better cut as one familiarity pattern, which landmarks and wild familiarity already half-share. The book (h) is not a pattern
  of its own: it is one kind of record, and its conditions are the general condition grammar that (b) pulses and (g) signs also need.
- **Strongest evidence:** the wave's household book reads "seen" conditions by matching words against the text of noticed lines
  (book.py:1135-1148). This happens because signs have no stable names to read. The design specified sign rows (u6_book.md §3, "each
  a named set of U8's sign rows"). As built, "few fish rising" (data.py:259) and "smoke rising from ..." (signs.py:855) satisfy a rule
  on "the river rising", and "ants running up and down the bean stems" (wild/kinds.py:720) satisfies one on "the run".

**Under D2-354's balance:**
- **A primitive should own the behaviour** for conditions, records with terms, matching, familiarity and name resolution. Each is
  re-implemented two to nine times today.
- **A system legitimately owns** the founders' prose (D2-268 decided hand templates), the scripted bots' policies, the memory
  instructions and the journal. They should keep those specifics inside their own folder, read numbers from rows, and declare their
  conditions rather than branch on names.

**The restructuring's cost for area C:**
- **Size:** about 7,700 lines moved and 2,000 to 2,600 rewritten, plus about 600 new for the shared condition grammar, the record
  base, matching and the resolver.
- **Time:** 8 to 12 builder-days, of which about 3 are already in feature_packages.md §10 phase 1 (phases, `today` keys, `Here`
  namespaces).
- **Risk:** highest in `book.target` (twelve call sites read every rule through it) and in merging the two learning paths, whose
  old path must stay for replay.

## 1. The mechanisms

Fit: **G** general over rows; **GF** general with fitted constants in code; **N** a special case by name; **H** hand-written
text; **W** a word-list or regex parse; **S** a silent skip. **B** marks a write outside the chokepoint. Pattern: the brief's
3(a) to 3(h), 4 (resolver), 5 (generated worlds); **none** where no pattern applies (§3 names the one it needs). Wave: changed or
added after f728a3b7.

| # | Mechanism | Where | Pattern | Fit | Wave |
|---|---|---|---|---|---|
| L1 | stages by days since birth, each its share of the lifespan | life.py:24-75 | (e) | G | |
| L2 | one's age and what lies ahead, in words | life.py:82-103 | (g) | H | |
| L3 | dawn: a stage changes, a child comes of age | life.py:111-126 | (e) | G | |
| L4 | a household's two days to name a head end | life.py:127-138 | none (record, office) | GF | |
| L5 | a youth's model chosen at coming of age | life.py:142-157 | none (cast) | N (`"claude-haiku-5-5"` twice, 150, 152) | |
| L6 | coming of age: childhood lines kept, the household's crafts as aware | life.py:158-173 | none (familiarity) | G, B (170) | |
| L7 | care's food and the passing on of lines | life.py:177-216 | none (matching) | G (food by `ITEMS.food`) | partly (D2-340) |
| L8 | partnerships both chose today | life.py:220-231 | none (matching) | G | |
| L9 | children do the household's standing order | life.py:234-256 | none (a second standing-rule system beside the book's `do`) | GF | |
| L10 | rations by stage, pregnancy's extra | life.py:260-270 | (e) | GF (youth 0.8 as a `.get` default, 269) | yes (D2-330) |
| L11 | late pregnancy, a unit fewer, showing | life.py:273-308 | (e) | G | |
| L12 | infants carried add weight | life.py:299-302 | (e) | GF | |
| L13 | conception from both trying, same roof, fed | life.py:350-376 | (b) | GF | |
| L14 | a late pregnancy lost on the road | life.py:379-390 | (b) | GF | |
| L15 | birth's risks by shelter, food, cold, help | life.py:393-421 | (b) | GF + N (`structure == "camp"`, 400) | |
| L16 | infants' and children's deaths by care, hunger, cold | life.py:424-458 | (b) | GF + N (camp, 441) | |
| L17 | who is told of a death in the night | life.py:461-471 | (g) | G | |
| L18 | old age and sudden illness (vermin raise it) | life.py:474-498 | (b) | GF | yes (`SR.illness`, 481) |
| L19 | what a child was present for becomes memory | life.py:501-517 | none (memory) | N (six event kinds, 515) | |
| L20 | succession and inheritance on a death (inside `p_die`, world.py:927) | life.py:521-563 | none (record) | N (`("field", "pasture", "meadow")`, 552, a copy of `farm.LAND`, farm.py:235) | |
| L21 | whole plots among heirs | life.py:566-579 | none (record) | G | |
| LR1 | three learning classes as rows | learning.py:29-39 | (e) as cut; familiarity | G | yes |
| LR2 | a craft's class: the row's, else a dict of 31 names, else basic | learning.py:46-81 | (e) | N (`CLASS_OF`; 15 of 161 rows carry `class`) | yes |
| LR3 | the two-part skill curve and its inverse | learning.py:88-112 | familiarity | G | yes |
| LR4 | a try's odds and materials by class and level | learning.py:115-121 | (f) | G | yes |
| LR5 | a try or practice: score, practice, skill, peak, a level | learning.py:131-168 | familiarity | GF, B (142-158) | yes |
| LR6 | a lesson session | learning.py:171-204 | familiarity, matching | GF (class names, 185), B (191-203) | yes |
| LR7 | fading on the life clock (applied in labour.py:73-84) | learning.py:207-211 | (e) | GF | yes |
| K1 | basic crafts known to all, of the packs on | knowledge.py:14-17 | (a)-row property | G | |
| K2 | a technique from what was written | knowledge.py:24-37 | 4 | G (one of nine resolvers) | |
| K3 | the old skill curve; the hunt's `curve: hard` path | knowledge.py:41-72 | familiarity | GF (a third curve) | |
| K4 | a youth learns the hunt faster | knowledge.py:75-84 | familiarity | N (stage `"youth"`, 82) | |
| K5 | seeding a person's crafts; a seeded mason walls | knowledge.py:88-103 | 5 | N (`"mason"`, `"wall"`, 100-103) | |
| K6 | a craft known somewhere given to one whose trade fits | knowledge.py:106-125 | 5 | W (trade words in free text, 118) | |
| K7 | the `learn` primitive's body | knowledge.py:128-137 | (f) | G | |
| K8 | where a craft can be done | knowledge.py:174-194 | (f) | G + N (`"body"`, `"carcass"`, 182-184) | |
| K9 | which stock a craft draws, with `draws_else` | knowledge.py:197-205 | (a) | G | yes |
| K10 | whether a site is ready, and why not | knowledge.py:208-306 | (a), (f) | N: a farm list of 14 yield kinds (214), 11 stocks each with its own threshold and words (227-249), three process names (287), the weir by monument name (296); H (every refusal) | partly (ice, run, shallows, willow) |
| K11 | what is to hand, inputs, a batch's share | knowledge.py:309-341 | (f) | G | partly (held back, u6) |
| K12 | what a craft is short of | knowledge.py:344-393 | (f) | G + H (`gear_x`: "no line to fish with", 367-368) | partly |
| K13 | a craft's card by level (old prompt) | knowledge.py:396-414 | (g) | H | |
| K14 | crafts as one's level shows them | knowledge.py:445-519 | (g) | G + H ("a third", 490) | yes (D2-263) |
| K15 | the bots' candidates | knowledge.py:522-537 | none | G | yes |
| K16 | speech makes one aware of a craft named | knowledge.py:540-550 | familiarity, 4 | W | |
| K17 | the old practice: two successes a level | knowledge.py:554-583 | familiarity | G, B (565-574) | partly |
| K18 | seeing it done gives a rough idea | knowledge.py:586-597 | familiarity | G, B (594) | |
| M1 | rewrite or append by the model's name | memory.py:50-56 | none (cast) | N (by model prefix: config) | |
| M2 | the memory budget over a life | memory.py:63-75 | (e) | GF | |
| M3 | the stretch's request, keeping and cutting | memory.py:92-127 | none (the agent's own text) | H + G | |
| M4 | places kept for good, opening over adult life | memory.py:170-190 | (e) | GF | |
| M5 | the kept-for-good request and its keep and drop | memory.py:197-244 | none (the agent's own text) | G | |
| F1 | the founders' 117 templates and 13 neighbour lines | founders.py:91-1782 | (g) as cut; seeded lines | H (D2-268) + N (45 name comparisons; 84 subscripts into 57 named rows) | yes |
| F2 | a feud or a debt read from the relations | founders.py:180-194 | none (record) | W (three regexes over prose) | yes |
| F3 | the household's holdings line | founders.py:1784-1842 | seeded lines | N + H (six holding kinds in an if/elif, each fact written in) | yes |
| F4 | the neighbours' busy seasons | founders.py:1657-1690 | seeded lines | N (`_BUSY` and four livelihood names) | yes |
| F5 | the lines a founder is given before the cap | founders.py:1879-1941 | 5 | G over `ROWS` (stage and role names) | yes |
| F6 | the cap and its drop order | founders.py:1849-2001 | 5 | GF (ids with lambdas) | yes |
| F7 | the founder's ration (a copy of L10 with 0.8 written in) | founders.py:84-90 | (e) | N | yes |
| F8 | a line waiting on a build | founders.py:709-723 | seeded lines | S (a line drops when a technique name is absent) | yes |
| V1 | livelihoods as rows (15) | livelihoods.py:16-130 | (a) | G (no load check: names are checked at fill time) | yes |
| V2 | holdings as rows, found by lambdas on fitting names | livelihoods.py:132-158 | (a) | N (code in the rows: `smoke racks`, `brine pan`, `water wheel`, `anvil`, the weir by name) | yes |
| V3 | an ox team from a household's herds and plough | livelihoods.py:172-191 | 5 | GF | yes |
| V4 | bands, experts, levels, skills, keepers, apprentices | livelihoods.py:226-420 | 5 | G (constants SIZE_RULE etc., 202-208) | yes |
| V5 | fill clears nine named crafts before refilling | livelihoods.py:393-396 | 5 | N | yes |
| V6 | fill places the gear | livelihoods.py:428-441 | 5 | N (`wicker trap`, `gill net`, `hand line`, `core[0] == "fisher"` twice, `weir_and_nets`, four `copper hook`) | yes |
| V7 | the cast by tier and chokepoint | livelihoods.py:443-457 | 5 | G (CAST, 208) | yes |
| V8 | neighbours aware of each other's broad crafts | livelihoods.py:458-470 | 5, familiarity | G | yes |
| V9 | "You live by ..." | livelihoods.py:475-524 | seeded lines | H + N (`monument == "weir"`, 517) | yes |
| B1 | books as records through the `book` primitive | book.py:70-98 | (h) | G | yes |
| B2 | goods, kinds of goods, synonyms | book.py:102-131 | 4 | W (`KIND_GOODS`, `GOOD_SYNONYMS`; `"oats"` is no item and silently matches nothing) | yes |
| B3 | a condition read from words (old records) | book.py:147-198 | (h) | W | yes |
| B4 | a rule's place read from words | book.py:245-269 | (h), 4 | W + N (`tub`, `brine`, `hearth`, `rack`, three process names), read at every rule evaluation | yes |
| B5 | (process, good) to its technique | book.py:272-278 | (c) | N (eight pairs in a dict) | yes |
| B6 | named sets of people, goods and places | book.py:281-340 | (h) | G (people sets by stage names) | yes |
| B7 | a condition object checked, refused naming its form | book.py:378-438 | conditions | G | yes |
| B8 | whether a condition holds now | book.py:441-484 | conditions | G (starving is `hunger <= -2`, 459) | yes |
| B9 | "seen": a member noticed the run, frost, the river rising, rats | book.py:1135-1148 | conditions, (g) | W (word lists against sign text) | yes |
| B10 | a rule read field by field | book.py:562-658 | (h) | G | yes |
| B11 | old kinds converted | book.py:706-767 | (h) | W (through B3, B4) | yes |
| B12 | goods arriving go where a `keep` puts them (a hook on `create`) | book.py:944-991 | (h) | G | yes |
| B13 | the sort, the floor held back | book.py:994-1046 | (h) | G | yes |
| B14 | the meal and its order by rules | book.py:1065-1117 | (h) | G | yes |
| B15 | spare units after every plan | book.py:1231-1390 | (h), (f) | G | yes |
| B16 | the rules block and the morning lines | book.py:1401-1470 | (g) | H rendered from records | yes |
| A1 | legs read from what agents write | agreements.py:42-74 | none (record) | W (regexes) | |
| A2 | offers made and taken, both or neither | agreements.py:137-263 | none (record), matching | G (any good; land through `FM.LAND`) | |
| A3 | a debt counted paid | agreements.py:275-297 | none (record) | G | |
| A4 | daily settlement and arrears | agreements.py:321-364 | none (record) | G | |
| A5 | a give credited against open legs (a hook on `transfer`) | agreements.py:373-409 | none (record) | G | |
| X1 | export, import, publish through the privacy gate | exchange.py:58-246 | none (infrastructure) | G + N (`cover == "field"`, 123) | |
| S1 | raids at night | settle.py:11-91 | (b) | GF + N (`structure == "stone"` x2, `door == "barred"` x1.5, 42) + H | |
| S2 | one sets on another | settle.py:121-162 | (b) | GF | |
| S3 | teaching matched by day | settle.py:165-188 | none (matching) | G | partly |
| S4 | three teaching paths (old day, hunt over days, lesson) | settle.py:191-260 | familiarity | GF, B (223, 255) | partly |
| S5 | joins matched with admits | settle.py:263-283 | none (matching) | G | |
| S6 | who saw a theft | settle.py:286-339 | (g), (b) | G (`TH.spot_chance`) + W (attending by a name in the attended text, 305, 334) | partly |
| P1 | hunting parties: leaders, circles, followers | parties.py:74-143 | none (matching) | G + W (a second person resolver by first name, 40-47) | |
| P2 | a party's hunt settled once | parties.py:162-208 | (b) | G | |
| R1 | stretches and landmarks from rows | roads.py:27-39 | (a) | G | |
| R2 | a landmark's trouble tonight | roads.py:72-87 | (b) | N (three challenge kinds with their own conditions in code) | |
| R3 | landmarks known and crossed | roads.py:103-118 | familiarity | GF (0.5^(n/5)) | |
| R4 | good places: stopping, gathering | roads.py:184-231 | (a), (b) | G + N (`"wild food"`), B (194) | |
| R5 | trouble's risk and the party's choice | roads.py:243-297 | (b) | N (`handcart` x4, `ford`, `snow`) | |
| R6 | what travellers notice | roads.py:315-359 | (g) | G (signs rows) + N (snow x3 on tracks, 334) | |
| R7 | finds on the road | roads.py:368-387 | (g) | G | |
| R8 | loose herds and splits | roads.py:401-447 | (g), (b) | G + W (searching by herd words, 390-398) | |
| R9 | meetings on a stretch | roads.py:450-498 | (b) | G (`meet` on rows) + N (fog, 468) | |
| R10 | the road's urgent calls | roads.py:518-800 | (f) | G (a registry by decorator) | |
| R11 | traces left and fading | roads.py:172-181 | (e) | G | |
| H1 | `Here` and `Mind`: what agent code may see | here.py:13-797 | none (view) | G, but by feature: 26 methods added in the wave (river, sets, processes, book); `Mind.know` hands out the live record (767) | partly |
| H2 | a person, building, parcel by name | here.py:166-247 | 4 | W (three more resolvers) | partly |
| RU1 | the day's order | run.py:905-1132 | none (phases) | N (each feature's step placed by hand: 1079-1106) | partly |
| RU2 | the day's intentions (`today`) | run.py:40-42 | matching | G | |
| RU3 | talk and what it mentions | run.py:248-371 | familiarity | W (through K16) | |
| RU4 | the prompt's closing line spliced by string | run.py (wave: `users[n].replace(cl, blk + cl)`) | (g) | H | yes |
| RU5 | the memory step | run.py:1132-1180 | none (the agent's own text) | G | |
| E1 | where one spends the evening | evening.py:29-39 | none | G | |
| E2 | what waits on one's answer tonight | evening.py:48-71 | matching | H | |
| E3 | the evening prompt, with the night's acts written in prose | evening.py:74-101 | (f), (g) | H (duplicates `NIGHT_VERBS`) | partly |
| E4 | the night's acts allowed | evening.py:19-21, 153 | (f) | N (a third verb list; `book.FREE_OR_TRAVEL` adds write, erase, attack, offer; this one adds set, fire, try, move) | |
| E5 | speech at the hearth, a name heard | evening.py:122-130 | none | W (a name by regex, 127) | |
| E6 | a guest let in sleeps there | evening.py:166-171 | (f) | G, B (171) | |
| E7 | asked again at dawn only if something new | evening.py:194-208 | (g) | G | |
| E8 | witnessed at a meeting | evening.py:231-235 | none (memory) | G | |
| J1 | the journal: inputs, requests, checkpoints, events, changes | journal.py:82-286 | none (infrastructure) | G | |
| BL1 | livelihood bots: the policy registry and the runs policy | bots_livelihood.py:55-800 | none (a player) | N by design (29 branches); `RUN_SEEN` copies a signs threshold (356) | partly |

## 2. The named branches and what each becomes

375 branches (C_branches.py `--list`), each assigned to one group by hand from the list; the 195 in founders.py are all counted in group 9.

| # | Branches | Where | Becomes | Under | Count |
|---|---|---|---|---|---|
| 1 | life stages by name (`"youth"`, `MINOR`, `"adult"`, `"elder"`) | life, learning, knowledge:82, livelihoods, founders, book people sets | **legitimate core default:** the stages are LIFE's rows. Replace each list of names with a stage property (`minor`, `works`, `agent`, `fertile`, `eats`) so a world with other stages works | (e) | 60 (and 15 inside founders.py, counted in 9) |
| 2 | a stock's exhaustion and its words (`willow`, `dead`, `young`, `grass`, `dung`, `seam`, `plants`, `fish`, `shallows`, `wood`, `wild plants`) | knowledge.py:227-249 | the stock row's `exhausted: {below: n \| share of K \| refuge}` and `words.out` (RESOURCES already has `low` and `high` words) | (a) | 18 |
| 3 | farm yield kinds dispatched to `farm.ready` | knowledge.py:214 | the yield kind row's `ready` hook (the yields registry, area B) | (f) | 10 |
| 4 | process names, container words (`keeping smoke`, `hard cure`, `hearth rack`, `tub`, `racks`, `hearth`, `brine`) | knowledge.py:287, book.py:245-278 | the process row's `container`, `aliases` and `techniques: {input good: technique}` (removes `book._tech`) | (c) | 17 |
| 5 | holdings by fitting or monument name (`smoke racks`, `brine pan`, `water wheel`, `millstones`, `anvil`, `weir`) | livelihoods.py:139-149, 517; knowledge.py:296; founders HL | a holding row's `of: {fitting: x}` or `{monument: x}` (declarative), and its `fact` clause and `keeper words` | (a) | 12 |
| 6 | a livelihood's seeded gear (`wicker trap`, `gill net`, `hand line`, `copper hook`, `fisher`, `weir_and_nets`) and the crafts cleared | livelihoods.py:393-441 | the livelihood row's `gear: [{good, n, if: {craft, level}}]`, the specialism's `gear` | 5 | 12 |
| 7 | covers held in plots (`field`, `pasture`, `meadow`), `field` fertility | life.py:552, exchange.py:123 | the cover row's `plots: true` (one list, today written twice: farm.py:235 and life.py:552) | (a) | 4 |
| 8 | structure and door strength (`stone` x2, `barred` x1.5), camp as half shelter | settle.py:42, life.py:400, 441 | the structure row's `defence` and `shelter` (BLUEPRINTS has the rows) | (a) | 3 |
| 9 | the founders' conditions and fills (`cover == "water"`, `"fen"` as willow, `"wolf"`, salmon by river class, `TECHNIQUES["hay"]`, `FITTINGS["smoke racks"]` and 55 more rows) | founders.py | **system-owned text, declared conditions:** each template a row `{id, band, stage, when: <condition>, fills: {slot: row.property}}`; the prose stays by hand (D2-268); `NB`, `_BUSY`, `HL`'s facts move onto the livelihood and holding rows (ROWS already carry an unused `neighbour_line` id) | seeded lines | 195 |
| 10 | road items and weather (`handcart` x4, `ford`, `snow`, `fog`, `wild food`) | roads.py | an item's `cart: true`; a landmark row's `alternative` (go round by a ford); a weather row's `meet` and `trouble`; the good place's `gives` | (a), (b) | 10 |
| 11 | event kinds a child remembers | life.py:515 | the event kind's `memorable: true` (EVENT_EXTENT has event rows) | memory | not counted by the script (six event kinds) |
| 12 | a mason walls (`mason`, `wall`) | knowledge.py:100-103 | the technique row's `implies: [wall]` | familiarity | 3 |
| 12b | the dead: a cairn over a grave (`cairn`) | knowledge.py:282, 347 | a method row of `bury` with `after: buried` | (f) | 2 |
| 13 | the bots' livelihood play | bots_livelihood.py | **legitimately by name:** a scripted player of one livelihood; read thresholds from the signs (`RUN_SEEN`) rather than copy them | none | 29 |
| | **total** | | | | **375** (+ name tables: 192 entries) |

The **name tables in code modules** become row properties too:

| Table | Where | Becomes |
|---|---|---|
| `CLASS_OF`, 31 crafts | learning.py:46-54 | `class` on the technique rows (15 of 161 carry it; the rest fall back by name, then by `basic`) |
| `KIND_GOODS`, 33 goods | book.py:47-51 | the item row's `kinds: [fish, fresh food, ...]`; the rule grammar reads them |
| `GOOD_SYNONYMS`, 15 | book.py:53-55 | `aliases` on item rows (no item carries one today), read by the one resolver |
| `SEEN`, `SEEN_NAMES`, 36 words | book.py:43-57 | a sign row's `topic: run \| frost \| river rising \| rats`; `seen` reads the topics of the signs noticed, never their text |
| `NIGHT_VERBS`, `FREE_OR_TRAVEL`, `verbs.FREE` | evening.py:19, book.py:41, verbs.py | the verb row's `free: true` and `when: [day, evening, road]`; the evening prompt rendered from it |
| `NB`, `_BUSY`, `KEEPER` | founders.py:1657, 1769, 1849 | the livelihood row's `neighbour_line` text and `busy` season rule; the holding row's `keeper_line` (already there) |

## 3. What does not fit, and the pattern each needs

| # | Mechanic | Members in area C | What a pattern would need |
|---|---|---|---|
| 1 | **Records with terms** | agreements' legs (A1-A5), offers, claims and inheritance (L20, L21), offices and succession (L4), the book (B1-B16), relations written as prose (F2) | feature_packages.md §2's **Record** category made a pattern: `{kind, parties, terms (typed legs or fields), where and when made, since, until, status}`. It needs a **settle hook** on a declared phase (agreements at "settle", succession at dawn, the book at its five moments) and **one renderer** from fields (leg_text, rules_block, the relations). The generator writes relations as records, not prose, so F2 reads fields (a debt is an agreement with legs; a feud is a relation record) |
| 2 | **Matched intentions** | partners (L8), trying for a child (L13), teach and learn (S3), join and admit (S5), care and care's food (L7), hunting parties (P1), offers taken (A2), a meeting called and attended (E7) | an **intention row** `{verb, by, with, at, day}` in `today`, and a **match rule** per verb: both sides the same day (partner, try, teach), one side's consent (admit, accept), or a leader and followers (party). It settles at its declared phase with one refusal line ("did not set aside time") rendered from data. Today there are seven matchers, each with its own `today` key and its own "nobody ... today" line |
| 3 | **Familiarity with a curve** | crafts (K3, K17, LR3-LR7, S4: three curves and three teaching paths), landmarks crossed (R3), wild kinds (`wild/methods.teach_familiar`), places and kin (`Mind.places`, `kin`), crafts heard of (K16), coming-of-age awareness (L6, V8) | one **mind record** `{subject, level, score, practice, skill, peak, seen, source, since, practised}` on a **curve row** (class: simple, practised, skilled, hard, landmark) with **ways in** (practice, watching, hearing, teaching, growing up) and **fading** on the life clock. It is written through one primitive, so the journal records it (today 9 writes go round the chokepoint) |
| 4 | **One condition grammar** | the book's conditions (B7, B8), the pulses' conditions (L13-L16, S1), landmark trouble (R2), the founders' conditions (F1, F8), signs' `if`, the evening's needs_morning (E7) | a **predicate** language over declared state: amounts in a container, a process's state, the calendar, a person's condition, a sign topic noticed, a row's property (`cover has plots`), a world setting. It is validated at load (refused naming the field, as B7 does), read by rules, pulses, signs and templates alike. B7 and B8 are its first half, built for the book only |
| 5 | **The day's order** | RU1: dawn, decide, talk, work, parties, teaching, evening, settle (partners, children's work, agreements, joins, thefts), night (roads, fuse, night), memory | feature_packages.md §6's **phase list**: each step names its phase with `after` and `before`, and the `today` keys it reads and writes. D2-343 moved teaching before the evening and joins after it by moving lines in run.py (1081, 1104) |
| 6 | **The agent's own text** | the memory rewrite (M3), kept lines (M5), notes, speech (E5, RU3), childhood lines (L19), witness lines (E8) | not a physics pattern: a **text store with a budget and a source**, already general (memory.py). It needs only the matching rule for names heard (one resolver) and the memorable event property (group 11) |
| 7 | **Seeded lines** | the founders' templates (F1-F4, F8), "You live by ..." (V9), customs | the signs' renderer applied to a different sense: being told. A **line row** `{id, audience, when, fills, text}` with the same condition grammar (4) and fills by row property, and a load check that each fill names a row that exists (replacing F8's silent drop) |
| 8 | **Resolving names** | K2, K16, H2 (person, someone, building, parcel), P1's first-name match, B2, B4, `book._building`, `book.SEEN_NAMES` | the hypothesis's pattern 4, which **does not exist yet**. The rules disagree today: `Here.person` is exact (here.py:166-169), `parties._person` takes a first name (parties.py:40-47), `book._building` takes the longest name found in a phrase (book.py:230-242) |

**Checked against the brief's candidates:**

| Candidate | Verdict |
|---|---|
| agreements and debts | misfit 1 |
| claims and holding | misfit 1, plus pattern 5 in the fill |
| households and offices | misfit 1, plus the book |
| learning and fading | misfit 3, which replaces (e)'s cut |
| care and children | (e) and (b) for the lives, misfit 2 for care itself |
| travel and roads | fit: (a) rows, (b) pulses, (g) signs, with N branches |
| eating and hunger | the book's meal fits (h); rations by stage fit (e) |
| theft and witness | fit: (b) and (g) through the one noticing rule, but attending is matched by text |
| evenings and talk | the phase list (5) and the agent's text (6) |
| notes and memory | misfit 6, legitimately its own system |
| the journal and replay | infrastructure, outside the patterns, already general |

The calendar (seasons by name in the book and founders) is area A's. Buildings with rooms and fire are area B's.

## 4. Taxonomy for area C

### 4.1 Types of thing

| Category (feature_packages.md §2) | Kinds in area C | Where they live |
|---|---|---|
| Type rows | life stages and shares (LIFE), learning classes (CLASSES), techniques (TECHNIQUES, shared), livelihoods (15) and specialisms (31), holdings (9), landmarks (8), terrain (7), founders' templates (117 + HL + 13 NB), memory instructions (7), verbs (VERB, with FREE and NIGHT_VERBS beside it) | data.py, learning.py, livelihoods.py, founders.py, memory.py, verbs.py |
| Body | person (stage, sex, born, parents, partner, pregnant, father, gap_until, cared, model, band, specialism, apprentice, livelihoods, transit) | `w.s["people"]` |
| Record | household (offices, heir, succession, rules, order, model), claim (thing, claimant, rights, grounds, plots, joint, until), offer, agreement and its legs, book (rules, proposals), relation (prose today), tree and history (generator) | `w.s["institutions"]`, `claims`, `offers`, `agreements`, `books`; world file |
| Mind | technique record, landmark record, familiarity by kind, places, kin, memory (rewritten), kept lines, childhood lines, lasting, notes, today's held lines | `w.s["know"]`, `w.s["mind"]` |
| Happening | events (kind, actor, target, about, concerns, salience, tags); acts (`w.s["acts"]` with `for`); the day's intentions (`today`) | `w.s["events"]`, `acts`, `today` |
| Infrastructure | journal tables (12), the exported views, the dataset | journal.py, exchange.py |

### 4.2 Types of property

| Group | Properties read in area C |
|---|---|
| Quantities | ration by stage, pregnancy food, child's work share, care units, infant weight; skill, score, practice, peak, tries; leg qty, paid, arrears, prepaid, lots; plots; memory budget (lo, hi, k), kept words and places; cap lines and words; seeded traps; strength (attack, defence), a weapon's value |
| Rates and clocks | lifespan and stage shares, pregnancy days, gap, the old-age doubling, conception's base and k; learning's tau, mark, fade after, rate, span, the scale s = 64/L; landmark experience (5 crossings); trace days; legs' `by`, `every`, `times`, `next`; succession days; the memory stretch; seasons (8 days) |
| Conditions | shelter (housed, camp, out), cold and fire, fed or missed, same roof, present at one node; a craft's season, ice, run, a stock's level; the book's amounts, process states, arrives, season, seen, starving, home; landmark challenge (high, down, snowed); weather (fog, snow); a world setting (`children`, `learning`, `evening`, `ages`, `skills.depth`) |
| Capabilities | a technique's level (aware, rough, capable, known), `basic`, `crew`, `class`, `curve: hard`; a band (broad, capable, expert); the rights of a claim (withdrawal, alienation); a verb's `free` and `when`; a holding's `chokepoint`; a livelihood's `status` (built, later), `apprentice` |
| Links to other rows | a technique's `at` (covers, fittings, building, things), `draws`, `draws_else`, `tools`, `inputs`, `gives`, `home_fittings`, `gear_x`; a livelihood's crafts by band, specialisms, `capital`, `keeper_lines`, `depends`; a holding's working and mending crafts; a template's ids in DROP and KEEPER; a person's parents, partner, household; a leg's from and to |
| Words | labels and aliases (techniques only); `words.lives`; landmark words; CHALLENGE_WORDS; the book's GRAMMAR and FORM strings; refusal lines (written inline everywhere); the templates; the memory PROMPTS; SKILL_WORDS |

### 4.3 Families of mechanism that could be generalised

| Family | Members today | What they share | What a general version reads |
|---|---|---|---|
| Nightly chances | conception, road loss, birth, infants' and children's deaths, old age, raid, duel, theft seen, meeting, landmark trouble | a keyed draw against `base x product of factors from conditions` | a pulse row: `{base, factors: [{when: condition, x}], outcome: primitive, event: words}` |
| Learning curves | knowledge's exp curve, the hunt's geometric curve, learning's two-part curve, landmark halving, the memory budget's saturating curve, kept places | `lo + (hi - lo) f(practice / tau)` with a scale | a curve row by class |
| Teaching and becoming aware | `_teach_day`, `_teach_days`, `LR.taught`, `saw`, `mentions`, coming of age, neighbours aware, `KNOWN_SOMEWHERE` | a way into the mind record with a source | the familiarity record's `ways` |
| Matching | seven matchers in settle, life, parties, agreements, evening | two intentions the same day at one place | the intention row and match rule (misfit 2) |
| Standing rules | the book's `do`, the household's standing order for children (L9), one's fallback, the bots' policies | an act fired by a condition on spare units | the book's grammar alone: the children's order a `do` rule with `who: children` |
| Rendering from records | leg_text, offer_text, rules_block, reading, crafts_lines, livelihood_line, HL, age_line, the evening's requests | fields to words with plural and person agreement | one renderer per record kind, from field templates |
| Resolving names | nine resolvers (misfit 8) | a phrase to a row id | one resolver over every row's `name` and `aliases`, scoped by `Here` |

## 5. History: how area C was built

**Commit activity on area C's files:** 66 commits on 23 and 24 Oct (the general core, life, roads, memory, the journal); then 1 to
18 a day through Nov; then 25 on 23 Nov (the W-73 wave's build: W-97 to W-105). The area grew from 6,628 lines at f728a3b7 to 11,262.

**Three ways a mechanism came in:**

| Way | Dated examples |
|---|---|
| **Built into an existing general system** | 23 Oct (6eaf51bb, 82de469d): agreements' legs over any good, and paying a debt as a give through a hook on the chokepoint. 23 Oct (a1db4346): roads' stretches and landmarks as rows, notices from sign bundles. 1 Nov (e2b79dd4): kept lines, a general store for the agent's own text. 17 Nov (47774a08): `death_told`, one rule for who hears of a death |
| **Generalised and extended an existing one** | 7 Nov (cfd79789, 92cfdbf6, D4-103/D4-104): crafts of a pack off are not known (`PK.on`), and "any stock the data names" replaced per-stock refusals with one check (knowledge.py:226). 23 Nov (07eec413): `draws_else` and `ice` as technique properties. 23 Nov (9e6a3d3f, bd923195, W-102): the book's rules rebuilt from word-read records to a grammar of fields refused by field (D2-337, D2-339). 23 Nov (0012b5ea, dfa4b58f, W-105): keeper lines moved from a list in founders to the livelihood and holding rows |
| **A new ad hoc system** | 2 Nov (6f8b2502, D4-97): a seeded mason walls, by name. 10 Nov (2bcdbe80, brief 4): the hunt's `curve: hard`, a second curve inside knowledge. 14 Nov (71c00896, brief 4c): `_teach_days`, a second teaching path for the hunt only. 10 Nov (d8982b22): hunting parties, a matcher of their own beside the four already in settle. 23 Nov (74741c83, W-100): learning.py, a third curve and a second practice path beside knowledge's, switched by a world setting, with `CLASS_OF` by name. 23 Nov (3a1962e3, W-99): the book's `SEEN`, `KIND_GOODS`, `target` word parsing and `_tech`. 23 Nov (0012b5ea, W-100): founders' 195 named branches and the fill's fisher gear |

**The trend is mixed, and worse in volume.**
- **Better in kind:** each time a word parse was found out it was replaced by fields. The book's rules went from words to records
  in one day (W-99 to W-102), and refusals now name the field (D2-337).
- **Worse in volume:** 75% of the area's named branches came in the wave's three days. The parallel systems grew from one curve and
  one teaching path (23 Oct) to three of each (23 Nov). Each was added beside the old one rather than replacing it, to keep old
  worlds replaying (learning.py:6-7; knowledge.py:557-559).

**Which went ad hoc because the general system could not be extended:**
- **`book.seen`:** signs have no stable names to read (feature_packages.md phase 1b, not built), so text was the only handle.
- **The hunt's teaching over days, and learning.py's classes:** knowledge's curve took no class or curve row; it held two
  constants (SKILL's basic and trade).
- **The day's new steps (D2-343):** there is no phase list, so steps can only be placed by hand in run.py.

**Which went ad hoc although they could have been extended:**
- **`CLASS_OF`:** the technique rows take any field; 15 carry `class` already.
- **`KIND_GOODS` and `GOOD_SYNONYMS`:** item rows could carry kinds and aliases.
- **The fill's gear:** livelihood rows exist and carry `capital`.
- **`HL`'s if/elif:** HOLDINGS rows exist.
- **The mason:** a technique row could carry `implies`.
- **`life.py:552`:** a copy of `farm.LAND`, which already existed.
- **Three verb lists:** VERB rows exist.

## 6. What in the process let ad hoc systems in

| Cause | Evidence |
|---|---|
| **Designs specified rows; the build fell back to names when the needed core piece was missing, and nothing flagged it** | u6_book.md §3 says "seen" reads "a named set of U8's sign rows". It was built as words matched to text (book.py:43, 1135), because sign names (phase 1b) do not exist. There is no OPEN row or engine_gaps entry for the departure |
| **Briefs named feature units (D2-244) but not the rule against named branches** | u9_people.md:9 lists "feature units: three, each with its data, acts, lines and process listed together". The unit rule says where code goes, not that it must read properties: learning.py is a clean unit whose `CLASS_OF` is a dict of names. D2-353, which states the rule, is dated 24 Nov, after the build |
| **A decided "by hand" read as licence for names in conditions** | D2-268 decided hand templates (u9 §5.1: "a template by hand"). The conditions (`[big river]`, `[holds a weir]`) were written as code per template, not declared, so 195 branches followed. The decision was about the prose |
| **Replay kept old paths alive beside new ones** | learning.py:6-7 ("a world without it keeps knowledge.py's rules ... so old worlds replay"); book.py's `convert` for OLD_KINDS. No decision says when an old path may go, so each new system is added, never substituted |
| **No load check on registries** | ROWS' crafts are checked only at fill time and reported (livelihoods.py:388-390); `"oats"` in KIND_GOODS is no item (book.py:47); `founders._built_technique` drops a line when a name is absent (F8). A load check would refuse all three |
| **No guard on named branches, chokepoint writes or verb lists** | Nothing in tests/ counts named branches (D2-353 asks for a guard; none exists yet). Writes round the chokepoint pass because `Mind.know` is the live dict (here.py:768). Three verb lists drift (§2) |
| **Speed of the wave** | 25 commits on 23 Nov across 11 area files. The calibration of live runs, not structure, was each brief's acceptance (u9 §5.1's test checks figures against state, not where they come from) |

## 7. The verdict under D2-354

**Where a general primitive should own the behaviour:**
1. **Conditions:** one grammar, starting from book.py:378-484. Pulses, landmark trouble, signs' `if` and templates move onto it.
2. **Records with terms:** one base with typed terms, a settle hook and a renderer. Agreements are the model, and are already
   general over goods.
3. **Matching:** one intention row and match rule for partner, try, teach, join, party and accept.
4. **Familiarity:** one mind record and curve rows. Merge K3, K17, LR3-LR7, S4 and R3, keeping the old curve as a class for replay.
5. **Names:** one resolver over every row's `name` and `aliases`.

**Where a system legitimately owns specifics, and how to keep them inside it:**

| System | What it owns | How to keep it there |
|---|---|---|
| The founders' templates | the prose (D2-268) | template rows with declared conditions and fills; numbers from rows only; `NB`, `_BUSY` and `HL`'s facts onto the livelihood and holding rows; a load check that every fill names a row |
| The livelihood bots | their play by livelihood | read the signs' thresholds and the rows; never copy a constant |
| Memory | its instructions and budget | leave as it is |
| The journal and export | infrastructure | leave as it is |
| The life package | its stages | stage properties (`minor`, `works`, `agent`) in place of lists of stage names |
| The roads | a landmark kind's own trouble | a landmark row declares its condition and its alternative in the condition grammar, rather than code per kind |

**Extension points each primitive needs,** so that new features extend it rather than bypass it:

| Primitive | Extension points |
|---|---|
| The condition grammar | registerable condition kinds, each declaring what state it reads and the words it renders |
| Records | registerable term kinds (goods, work, land and later office or service), each with its own settle and words |
| Matching | registerable match rules (mutual, consent, lead) |
| Familiarity | registerable curve classes and ways in (practice, watch, hear, teach, grow up) |
| Sign rows | stable names and a `topic` (phase 1b), so rules read signs without reading text |
| The day | a phase list with `after` and `before` |
| The resolver | registerable kinds of thing (person, building, parcel, good, craft, set) |

## 8. The restructuring's cost for area C

In feature_packages.md §9 and §10 terms. Lines are from `wc -l`; rewrites are estimates from the tables above.

| Work | Lines moved | Lines rewritten | Lines new | Risk |
|---|---|---|---|---|
| Packages `life` (life.py), `teaching` (knowledge, learning), `households` (book, offices), `exchange` (agreements), `roads`, `evening`, `founding` (founders, livelihoods), the hunting party into `wild` | about 7,700 | | | low (moves) |
| Named branches groups 2 to 8, 10 to 12b (89) to row properties; the name tables (192 entries) to rows | | about 450 | about 100 (fields, load checks) | medium: the stock thresholds change refusal wording; the golden journals catch it |
| The condition grammar from the book's, used by pulses (L13-L16, S1), landmark trouble (R2), templates | | about 400 | about 250 | medium |
| `book.target`, `seen`, `_tech`, `_goods` onto process rows, sign topics, item kinds and the resolver | | about 250 | | **high:** every rule evaluation reads `target` (12 call sites); `seen` changes which rules fire (a decided change: it fixes the false matches) |
| Familiarity: one record and curve rows; the two practice paths and three teaching paths merged, the old one kept as a class | | about 450 | about 100 | **high:** replays of worlds without `learning: record` must stay byte-identical |
| Matching: seven matchers onto one rule | | about 250 | about 80 | low to medium |
| Founders: template rows with declared conditions (prose unchanged) | | about 600 | about 50 | low (the founders' lines are tested against state, D2-268) |
| The day's phases, `today` by package, `Here` namespaces (already counted in §10 phase 1) | | about 500 (of §10's 1,500 and 400) | | as §10 |
| One resolver (here, parties, book, knowledge) | | about 200 | about 150 | medium: what agents' words resolve to may change; checked on the live replies of W-102 |
| **Total for area C** | **about 7,700** | **about 2,000 to 2,600** (about 500 of it already in §10 phase 1) | **about 600 to 750** | |

**Builder-days:**
- **Moves:** about 4 days at §11's 2,000 lines a day.
- **Rewrites:** 6 to 8 days at 300 to 400 a day, of which about 1.5 to 2 are §10 phase 1's.
- **In all:** about 8 to 12 builder-days for the area, against the 4,787 lines the wave added in three days.

**What it saves:**
1. **The false firings of the book's "seen" rules are fixed.** Today a rule on the river rising fires on "few fish rising", and
   rewording a sign silently changes which rules fire.
2. **One place to add a stage, a learning class, a livelihood's gear, a holding, a kind of goods or a verb's timing,** in rows,
   checked at load.
3. **The journal records every change of a person's knowledge,** where today 9 writes go round the chokepoint.
4. **Three verb lists, three curves and nine resolvers stop drifting apart.**
5. **New social features land as rows and registrations** (a new office, an apprenticeship term, a debt kind, a new match rule),
   not as new modules beside the old.
   - On §11's measure, area C's edits in the wave to files it shares with other features (run, here, knowledge, settle, life,
     evening: 405 lines added) against about 4,400 in its own new files is under a tenth. That is lower than the wild layer's quarter.
   - The coupling cost is elsewhere: in name tables and parallel paths inside its own files.
