# The design wave read against itself and the code: conflicts, gaps and questions (W-79)

22 Nov 2026, 37.2 (subagent, overnight). Thread: design wave, conflicts and consistency (W-79), under fishing, hunting and their
materials (W-73). A review note: no proposal, spec, record or code was changed and nothing was committed. Zach asked for
"conflicts and questions, lots of questions for me in the morning".

**Read:** the W-73 pack (`tools/records.py pack W-73`); the wave's proposals (hunt_fish_materials, building_clock, store_rules,
verb_grammar, trying_and_learning, knowledge_in_their_own_words, acts_on_owned_things, river_signs); `spec/core/clocks.md`, and
the spec files the wave's decisions are cited in (economy/goods.md, production.md, buildings.md, agents/work.md,
agents/standing_orders.md, information/memory.md, process/how_we_work.md); decisions D2-263 to D2-285 (D2-283 to D2-285 were added
during the night); the OPEN rows of the thread (Q-73, Q-79, Q-80, Q-81, Q-82, Q-83, Q-84, Q-27, Q-69, L-148, L-150, L-153, L-154,
L-157, O-2, W-70, W-76, W-77, W-78, W-80, W-81, W-82); the research notes in this folder (building_clock, smokehouse_capacity,
storage, store_management, engine_audit, fishing_ladder, learning_times, founders_knowledge, household_skills in part); 37.4's
proposals standing_rules.md and livelihood_archetypes.md and the board; the code in `cybertron2/engine/` and `cybertron2/wild/`.
**The sibling notes** that landed while I worked (wave1_physical_basis.md and wave4_people.md about 08:18, wave3_keeping.md 08:25,
wave3_taking.md 08:29) are read and checked in §7: the first three in their summaries, conflicts and questions and the sections
cited; wave3_taking.md, which landed as I finished, in its §0, §4.5 and §7 only. building_clock_bots.md (W-82) did not exist at
08:30, so it is not checked.

**Severity:** **blocks** (the build cannot go ahead until it is settled), **number** (changes a number someone will build to),
**wording** (a stale or misleading line; the rule itself is not in doubt).

---

## Summary

- **The proposals were written before the day's decisions and have not caught up.** hunt_fish_materials prices its gear and works
  at real hours (a net 30 units, a trap 2.5, the withy bed 10) though D2-276 puts capital at about 1/7; it lists tanning as left out
  though D2-281 brings it in; it still asks whether shelf lives are compressed though D2-273 decided it; its summary states the rule
  D2-273 replaced. river_signs keeps fishing going under ice though D2-265 says a freeze stops it. trying_and_learning sets
  learning at lifespan 96 though D2-267 says 64, and the code's base is 32.
- **Two numbers are stated two ways in decisions themselves.** The smoke racks hold 500 kg a set (Q-83, answered "yes") or 250 kg a
  set (D2-284, answered "yes" the same day). Barrels are in D2-279's set of stores and "later" in the same decision.
- **The three wave notes disagree with each other on the basis.** A firewood unit is 10 kg in wave 1 and 60 kg in wave 3 (a factor of
  6 on every fuel cost); "keeps a season" is a half-life in wave 1 and a quarter lost in wave 3 (a factor of about 2 on every keeping
  rate); a set of racks takes 1 space in wave 1 and 2 in wave 3.
- **The rule underneath every number has no decision.** "1 food = 2,500 kcal, children 0.6, elders 0.8" is a default taken on Q-69;
  D2-275 closed Q-69 with the unit's length only, and wave 3 cites the kcal basis to D2-258, which does not state it. The reverse
  also happens: Zach's 21 Nov answer on acts defaulting to one's own sits only in Q-80's notes, with Q-80 still open, and the wave's
  notes have since gone against one clause of it ("several: asked").
- **Nine of the wave's 23 decisions have no spec home, none says what it replaces,** and several decide inside 37.4's areas (the
  standing rules, the buildings' costs, the prompt and memory, the archetypes) with no board post since 19 Nov.
- **Couplings nobody priced:** a weir's glut costs 3 to 6 person-days of keeping per peak night once fuel is cut at wave 1's weights;
  hot smoke is worth under a night more than fresh under the floor rule; the year clock puts the withy bed (96 nights to full yield)
  and tanning (16 to 48 nights) beyond the 30-day live runs; the staging to 1/7 is written only for things that get dearer.
- **The code holds several things the design assumes it does not:** a live expert sign that says "set the traps tonight"
  (`wild/kinds.py:412`) against D2-269; skill fading on the year clock (`clocks.py:31`) against D2-273's life clock; the livelihood
  bots never build (`bots_livelihood.py`), so W-82 cannot read "does building still happen" from them as they stand.
- **Twenty-four questions for Zach** are in §6, ranked by what they block. The first five: the bulk goods' units in kilograms; how
  "keeps for X" becomes a nightly loss; the racks' load and floor; lives counted in nights against lives counted in acts; and
  whether smoking is a make act or a processing container.

---

## 1. Contradictions between documents

| # | What | One side | The other side | Severity |
|---|---|---|---|---|
| C1 | **The racks' load.** | Q-83 (closed "2. yes"): "about 500 fish on 2 spaces", 250 fish a space; hunt_fish_materials §7.3 ("about 500 fish a set of racks on 2 spaces"); smokehouse_capacity §0 and §8; storage.md §0 and §11 (hut 500, timber house 1,500). A fish unit is about 1 kg gutted (smokehouse_capacity line 20), so 500 fish is 500 kg. | D2-284 (closed "2. yes"): "about 250 kg of fish a set ... a wattle hut one"; hunt_fish_materials open question 10(a) ("each set of racks holds about 250 kg"; a house of 750 kg); wave1 §3.6 (250 on 1 space; a timber house 750 to 1,000). | **number** (blocks the racks' `holds`) |
| C2 | **Gear and works priced on the old scale.** | hunt_fish_materials §4.1 (withy bed about 10 units), §4.2 (retting pit about 10), §5 (wicker trap 2.5, snares 1, line 0.5, net about 30, fowling net about 30, creel 1, pack basket 2, hurdle 1.5), §6 (weir base 8 units, wattle section 16, timber 25): real hours or today's engine. river_signs §4.4 (the weir "12 timber and 24 units by two"; the rod "of timber and hide lasts 30 uses"). | D2-276 and building_clock.md (net 2 to 3 plus its cord, a line of 6 traps about 2, hurdles about 7 a unit, a weir section 1 to 3, or 7 to 22 sized to a large river's take); wave1 §3 (net 3 to 4, a trap 0.3 to 0.6, a hurdle 0.2, the withy bed 1.5, the rod of withies). | **blocks** (D2-263 shows each craft's units in the prompt) |
| C3 | **Hurdles a unit.** | building_clock.md stage 1: "hurdles about 7 a unit". | wave1 §3: 0.2 units each (5 a unit); trying_and_learning §1: "an old hand's 2.5 to 3" a day (about 3 hours each, so about 5 a unit at 1/7). | number |
| C4 | **What a snare line is.** | hunt_fish_materials §5: "a line of 5 nooses", 0.02 cord, "about 10 sets"; §4.2: "a line of snares 0.02". | §7.7 (written in by D2-264): "a bundle of about 25 snares (about 0.15 cord)", each used up when torn or rotten, a set lays up to about 25. Cord a noose 0.004 against 0.006 kg. D2-276 puts "a snare line" among things used up (day clock), §5 gives it a life of 10 sets. | number |
| C5 | **The second act on set gear is named two ways.** | "lift" (hunt_fish_materials §5, river_signs §3, wave4 §5.1). | "tend" (hunt_fish_materials §7.7, verb_grammar §1, wave3_taking §0.2 row 3, which recommends it). | wording (the prompt's word) |
| C6 | **Several of one's own at a place, no target named.** | Zach's own words in Q-80's notes (21 Nov): "several: asked"; acts_on_owned_things §3: refused, listing the tags. | hunt_fish_materials §5: a lift "takes the catch from all of one's own sets at a place"; wave4 §5.3 and wave3_taking §0.2 row 1: a lift or tend takes all, a consuming act (slaughter, a take from a pile) is refused or asked. | **blocks** (the resolver) |
| C7 | **Whether shelf lives are compressed.** | D2-273 decided it ("how long goods keep" on the year clock); clocks.md records it. | hunt_fish_materials §7.3 heading "Which clock shelf lives run on (open)" and open question 1. | wording |
| C8 | **The floor rule's shape.** | D2-273: "a duration of more than a few real days compresses with its clock; one of a day or two keeps its real nights as a floor". | wave1 §2.1: a continuous curve, nights = min(d, 2) + (d − 2) / 11.4, because the literal floor gives 2 nights to everything from 2 days to 3 weeks. A refinement of a decided rule, not yet put to Zach as one. | number |
| C9 | **How "keeps for X" becomes a nightly loss.** | wave1 §2.1: "keeps d days" is a half-life (a keeping smoke 9.7 nights, about 0.07 a night). | wave3_keeping §5.1 and W80-Q1: a quarter lost by then is used and recommended (a keeping smoke 0.035 a night); at spring a household has 12, 29 or 41 food left as it means half, a quarter or a tenth. | **blocks** (every shelf life) |
| C10 | **The learning lifespan.** | D2-267: practice and learning set at a 64-day lifespan and scaled; clocks.md "64 days in current worlds" (true of `make_peoples.py:29`, `make_water_worlds.py:64`; the goal-probe worlds use 96). | trying_and_learning §2 ("practice tau (units, at lifespan 96, scaled)", "about 580 units at lifespan 96"); learning_times.md; the engine's base is 32 (`data.py:1130`, D2-153's default; `knowledge.py:80-81` scales by 32 / lifespan). wave4 §4.2 rescaled to 64. | number |
| C11 | **The salmon's return.** | D2-209: "the salmon's three-year return is compressed to one world year". | D2-273: durations on the year clock compress at 1/11, so three real years are three world years (as D2-264 keeps the withy bed's three). D2-209 is now a departure from D2-273 that neither names. | number |
| C12 | **Fishing in a freeze.** | D2-265: "a freeze stops fishing"; hunt_fish_materials §2 ("ice stops set gear and crowds fowl to open water"). | river_signs §2.6: "The engine lets the traps, the weir and the runs go on under ice, and the signs must not say otherwise"; D2-210's weir wears faster in ice (it is working); fishing_ladder §2: eels were speared through ice in winter. | **blocks** (the ice rows) |
| C13 | **Experts' signs that direct.** | D2-269: experts' signs are observations "which may imply an act but never direct one". | river_signs §2.3: the expert's "an eel night ...; set the traps tonight" (kept from the code, `wild/kinds.py:412`); §2.5 "the river is falling: traps set now will stand"; §3's spent-trap result "Set again to fish on." | wording (a decided rule broken in live code) |
| C14 | **Kept lines.** | D2-266: about 40 words, a place each stretch. | river_signs §4.1: lore "one line a run, each within the 25-word cap"; spec memory.md (D4-64: about five places over adult life); `memory.py:135` (25 words, 5 a lifespan). | number |
| C15 | **The kept-line budget over a life.** | knowledge_in_their_own_words §3: "over a 64-day life about 20 lines, roughly 800 words". | wave4 §2.6 and §3.2: up to 20 seeded lines a founder, which do not take the stretch places (about 21 more), so about 40 lines and 1,600 words by old age. | number (prompt length) |
| C16 | **The told-knowledge arm.** | D2-266: "a told-knowledge comparison arm in early testing, not for every experiment". | knowledge_in_their_own_words, Risks 1: "Every experiment on this has a paired arm with the knowledge told"; open question 5. | wording |
| C17 | **Who writes seeded lines.** | D2-268: "templates are written by hand and tested, filled from the engine's state where they state a fact". | knowledge_in_their_own_words, Risks 4: "read from the engine's own state, never written by hand". | wording |
| C18 | **Whether the core says knowledge dies unless passed.** | knowledge_in_their_own_words §5: "The core says plainly that what one knows dies with one unless it is passed on". | wave4 §1.4 and §8 Q1: left out of the core and made a cultural strand (BS8) to be varied, as Zach's 22 Nov words suggest. | number (the core) |
| C19 | **Tanning.** | D2-281: "Tanning comes in this build, with bark as a new good". | hunt_fish_materials §2 ("oak bark (with tanning)" deliberately not added now), §10 ("bark and tanning, leather ... a tanning step after this"), §11 (no tanning unit), §12 phase 6 ("then tanning"), open questions 5 and 9. | wording (build scope) |
| C20 | **The pack.** | D2-281: the withy pack basket and the leather-strapped frame replace today's pack; hunt_fish_materials §7.6 ("a frame of timber and leather") and open question 6 (basket +15, frame +20). | hunt_fish_materials §5's row "pack basket (frame and straps)": 1 withies and 0.1 hide, one item mixing the two. | wording |
| C21 | **Fuel for smoking.** | hunt_fish_materials §7.3 and smokehouse_capacity §0: "1 firewood per 60 fish (about 1 kg of wood per kg of fish)", on a 60 kg firewood; wave3_keeping §2.5 and §5.1 use the same (1 firewood, "about 60 kg, prov."). | wave1 §1.3: a firewood is a 10 kg bundle; its smokehouse §3.6 burns 25 to 50 firewood for 250 fish. At 10 kg, the proposal's figure is 6 times too little wood. | **number** (every fuel cost) |
| C22 | **A timber's weight.** | building_clock.md stage 4: "a timber is about 240 kg, so a small room's 8 timber is about 65 loads"; smokehouse_capacity line 22. | wave1 §1.3: a 25 kg pole; the 240 kg came from compressing a year's fuel into the engine's year (02z), which D2-273 now puts on the day clock. | **blocks** (every recipe in timber) |
| C23 | **Moving goods in a store.** | store_rules (D2-274's labour, provisional): "free within a building (rooms, storeys, cellar, containers)"; wave3_keeping §5.1 "taking down free within the building (D2-274)" (D2-274 says only that the rates are provisional). | hunt_fish_materials open question 10(d): "hanging is real work (about 30 fish a unit), so it is a chore from spare units or an act, not a free move". | number |
| C24 | **The moving rate against the carry limit.** | store_management §4: 1 unit per 800 kg a parcel step, from "a sack of about 40 kg on the back". | the engine carries 10 on foot (`data.py:812`), 20 with a pack (`data.py:105`); wave1 §4.1: on foot about 10 kg (a named departure), with a basket 25, a frame 30. At 25 kg a trip the rate is about 500 kg a unit a step. | number |
| C25 | **Gutting paid twice on a hard cure.** | D2-283: salting at about 20 kg an hour "with gutting". | the hanging rate of 30 fish a unit is the Fraser rate "splitting included" (smokehouse_capacity lines 148-151; wave3_keeping §2.2, "splitting and gutting included"); a hard cure is salted first, then hung. hunt_fish_materials §7.3: gutting "folded into each keeping technique". | number (small) |
| C26 | **Barrels.** | D2-279: barrels are in "the stores of storage.md ... as the set". | D2-279 also: "barrels later"; hunt_fish_materials §10 (barrels "next step"); storage.md §7: salt fish out of brine at twice its base, removed only by a barrel; wave1 #20; wave3_keeping W80-Q9. | number (salt fish's keeping) |
| C27 | **Smoking as an act or a container.** | wave4 §5.1: "smoke fish" is a **make** technique, "a batch over nights"; its lore lines FI16 and FI17 read `smoke_batch` and `smoke_nights`. | hunt_fish_materials open question 10(d, e) and wave3_keeping §2 to §4: racks as processing containers holding lots, hanging as quantity work, the cured state firing D2-282 rules. | **blocks** (W-78 and W-80 design the same act two ways) |
| C28 | **Where a done lot goes.** | `keeping.py` docstring and code: a done batch goes into the smokehouse's store at once if the hanger is of the household. | hunt_fish_materials open question 10(d): with no rule, cured fish stay hanging and fill the racks; wave3_keeping W80-Q11 recommends that. | number (proposal against code; open) |
| C29 | **Rules: when they are changed, and what they cover.** | 37.4's standing_rules.md §5 (changed "by an act at the evening") and §7 (not for "trade, trips, loans"). | store_rules.md ("a free `rule` act", any turn; open question 4: travel in the same book, "when to push on or turn back"; L-152). | wording (37.4's area) |
| C30 | **Smoked fish today.** | hunt_fish_materials §7.3: "half gone after about 139 nights" (the rate in hand). | wave1 §0 and wave3_keeping §0: about 460 nights (the house rate, × 0.3). | wording |
| C31 | **A cottage's price at 1/7.** | building_clock.md: "a cottage of about 500 real hours costs about 36 units"; its table: a small timber room 20 to 32. | wave1 §3.5: a wattle cottage 19 to 39, a timber small room 32 to 51. | number |
| C32 | **Racks' materials.** | D2-271 and hunt_fish_materials §6: "2 withies, 1 timber". | storage.md §0: "racks of 4 withies, 1 timber and 2 units"; wave1 §3.6: 2 withies and 2 timber (25 kg poles). | wording once timber's unit is settled |
| C33 | **Superseded lines left standing.** | hunt_fish_materials Summary: "It rests on one rule decided first: the wild produces per day what it produces per real day (§1)"; §4.3: "Fish stay gutted at no work until the salting rate (Q-73) decides"; open questions 1, 2, 4, 5, 6, 7 (decided by D2-273, D2-284, D2-283, D2-281); verb_grammar open question 4 (decided by D2-266). | D2-273, D2-283, D2-284, D2-281, D2-266. | wording |
| C34 | **Statuses.** | hunt_fish_materials "Nothing decided"; knowledge_in_their_own_words "Nothing decided, nothing built"; river_signs "discussion"; store_rules "accepted in part: D2-274". | their own History entries record D2-264, D2-271, D2-272, D2-279, D2-281, D2-283, D2-284 (hunt_fish), D2-266, D2-268 (knowledge), D2-282 (store_rules); D2-265 accepted river_signs as answered. | wording |

---

## 2. Decided rules with no owner, no spec home, or a spec that says otherwise

| # | Finding | Where | Severity |
|---|---|---|---|
| S1 | **The food's energy basis has no decision.** "1 food = 2,500 kcal, children 0.6, elders 0.8" is a `default_taken` on Q-69. Q-69 was closed by D2-275, which states only that a unit is 2 hours. The wave cites it to D2-258 and D2-259 (hunt_fish_materials Summary; wave3_keeping §5.1), and neither states it (no "2,500" anywhere in DECISIONS.md). Every food number in the wave rests on it. | `items/Q-69.md`; DECISIONS D2-258, D2-275 | **blocks** in principle (nothing breaks, but the basis is unrecorded) |
| S2 | **No spec home** for D2-263 (recipes shown), D2-265 (the river's signs), D2-266 (knowledge in their own words), D2-268 (the founders' knowledge), D2-269 (experts' signs), D2-270 (household skills), D2-282 (conditional rules), D2-283 (salting's rate), D2-284 (the racks). Likely homes: information/prompts.md or agents/actions.md (D2-263; 37.4's), information/signs.md (D2-265, D2-269; 37.4's) or environment/wildlife.md, information/memory.md (D2-266, D2-268; 37.4's), seeding/populations.md (D2-268, D2-270), agents/standing_orders.md (D2-282; 37.4's), production.md (D2-283), buildings.md (D2-284; it has no smokehouse at all). | grep of `spec/` for each id | wording |
| S3 | **goods.md lists D2-272, D2-274 and D2-279 at its top, but its body still says the old rule:** "The rate in a house is multiplied by every condition that applies", and the grain row "0.5% (D2-58; bins, cellar, granary lower)". Its "Current as of" is 24 Oct. | `spec/economy/goods.md:84-90`, `:122` | number |
| S4 | **buildings.md states D2-155's cellar** "4 stone, 6 units ... at a quarter of the house rate" (line 81) and D2-166's costs (hall 200 units, water wheel 250), which D2-272, D2-276 and D2-279 replace. Neither D2-155 nor D2-166 is marked "replaced by". "Current as of 3 Nov". | `spec/economy/buildings.md:27, 49-51, 80-81, 180` | number |
| S5 | **standing_orders.md (37.4's) says standing orders bind "only itself"** (38.07 §5, D4-16). D2-274 gives each household a book that binds its members unless they override it. D4-16 is not marked amended. | `spec/agents/standing_orders.md:16` | **blocks** the merge (37.4's spec) |
| S6 | **memory.md states D4-64's kept places** (about five over adult life, the places' schedule); D2-266 opens one a stretch at about 40 words. D4-64 is not marked amended. | `spec/information/memory.md:16-17, 39-44` | number |
| S7 | **None of D2-263 to D2-285 fills the Replaces column,** though at least these replace or amend earlier rows: D2-272 (D2-58's lower store rates, D2-155's cellar quarter, D2-87's house multiplier), D2-276 (D2-155, D2-166, D2-210's section costs, D4-114's fence), D2-266 (D4-64), D2-274 (D4-16), D2-264 (D2-204's single `net` method), D2-265 (D2-210's weir working through ice, at least in reading), D2-273 (D2-209's salmon return, C11). | DECISIONS.md (awk of the Replaces column) | wording |
| S8 | **Spec "Current as of" lines are stale:** production.md (20 Nov, its list ends at D2-262 though D2-264, D2-271, D2-278 and D2-281 are appended above it), goods.md (24 Oct), how_we_work.md (20 Nov; D2-277, D2-280, D2-285 appended). | the three files' last lines | wording |
| S9 | **production.md's D2-52 note says skill fading "is not built".** It is (`data.py:756-757`, `knowledge.py:459`, D4-105), on the year clock. | `spec/economy/production.md:159-160` | wording |
| S10 | **work.md (the units a day) does not say a unit is 2 hours** (D2-275 is only in clocks.md). | `spec/agents/work.md:25` | wording |
| S11 | **production.md's trap row:** "can be emptied by whoever checks it". Q-80 (open) proposes the opposite default. Not a contradiction yet; it becomes one if Q-80 is answered yes. | `spec/economy/production.md:90` | wording |
| S12 | **Decisions inside 37.4's areas with no board post.** D2-274 and D2-282 decide much of 37.4's standing_rules.md (still "discussion (13 Nov)"); D2-266 and D2-270 decide parts of 37.4's livelihood_archetypes.md (still "discussion (16 Nov)") and tie the build to W-70, which is 37.4's and waits on the verb list (Q-27, open since 23 Oct); D2-276 reprices 37.4's buildings and `room_cost`; D2-263 changes 37.4's prompt. The board's last post is 19 Nov (`docs/coord/BOARD.md`). CLAUDE.md: "If it touches another session's area, post on the board." | BOARD.md; the two proposals' status lines | **blocks** any merge |
| S14 | **A rule Zach answered sits only in an ask's notes.** Q-80's notes record "Zach, 21 Nov: yes to the concrete proposal: the target is the thing ..., unnamed acts touch only one own (one: that; several: asked; none: refused ...)". Q-80 is still open, the proposal says "Nothing decided", and there is no D2 number; wave 3 (taking) rests its whole design on it (its §7 #1). CLAUDE.md: a question he answers is a decision "only when he states it"; this reads as stated. | `items/Q-80.md`; acts_on_owned_things.md status | **blocks** the target rule |
| S13 | **A decided staging rests on deferred and queued work.** D2-276 brings the factor in "by stages with builders as a trade, cheaper ways to protect crops and clearing a plot at a time"; building_clock.md puts these companions "before any work is raised". Clearing a plot at a time is L-153, deferred and open; builders as a trade belong to the timber economy (W-76), queued after this wave; cheaper crop protection has no row at all. W-82 is already reading the 1/15 stage. | `items/L-153.md`, `W-76.md`, `W-82.md`; building_clock.md "The stages" | **blocks** the staging as decided |

---

## 3. Couplings nobody priced

| # | Coupling | The arithmetic | Severity |
|---|---|---|---|
| K1 | **A weir's peak night against the hands and the wood.** | A peak night at Lowstrand offers 333 kg (smokehouse_capacity §6, 02zzu_lookup). Keeping it smoked: hanging at 30 kg a unit, about 11 units; tending 1; fuel at wave1's real 1 to 2 kg of wood a kg, 33 to 67 bundles of 10 kg, which at the production spec's 3 to 5 bundles a unit is 7 to 22 units of cutting. About 19 to 34 units a peak night, 3 to 6 person-days, against a two-adult household's 12 autumn units. A hard cure adds salting (about 8 units) and 83 kg of salt (D2-283), which inland is about 83 more bundles to boil (salt's 1 firewood a salt). wave3_keeping §5 finds the wattle hut never binds for one household with six traps and one weir turn (243 kg over the whole run), but it uses the 60 kg firewood (C21), so its fuel is 6 times light, and it does not count the cutting. wave1 §5.1 prices only 500 fish a year. No document prices a full weir's glut end to end. | number (the nutrition arms) |
| K2 | **Hot smoke is nearly worthless under the floor.** | On wave1's curve fresh fish keeps 1.5 nights, hot smoke 2.4: a hot smoke buys under a night. D2-271's first depth ("eaten soon, sold nearby") then has almost no reason to exist in the engine. Nobody has said whether that is intended. | number |
| K3 | **Real store capacities against compressed shelf lives** (L-154). | A real household's year of grain (1.5 to 2.5 t) is about 11 world years of eating (storage.md §0). Under wave1's curve grain keeps about 221 nights well kept (about 7 world years), longer than today's 138, while smoked fish falls from 462 to 10. So grain becomes free to hoard (capacity never binds, keeping hardly does), and every other food binds on keeping, not on room. storage.md's "a granary of several tonnes becomes a village's or a lord's store, a chokepoint" then has no pull except vermin. L-154 flags the gap "lightly"; the grain reading is not in it. | number |
| K4 | **The year clock against run lengths and the life clock.** | The withy bed gives nothing its first world year, half its second, full from its third (D2-264): 64 to 96 nights. Tanning is 16 to 48 nights (wave1 §2.4). The salmon's return is 32 nights (D2-209) or 96 (D2-273). A lifespan is 64 days, two world years. The live runs that tested this thread were 30 days (02zzy, 02zzy2); the nutrition worlds 64; the peoples worlds 200. In a 30-day run no withy bed yields and a hide laid down on day 1 may not come out, so the withy bed (§4.1's "switch") and every leather use (D2-281's frame, harness, bellows, shoes) can appear only if seeded. | number (what a run can show) |
| K5 | **A net's life decides the flax close.** | building_clock.md §1.2: a gill net's real life is 50 to 450 sets; times 1/7 that is 7 to 65 engine uses. The proposal's 60 to 80 sits at the top, and its "a fishing household needs about 1 to 3 kg of cord a year" holds only there. At the bottom a household needs about 10 times the cord, and "flax is a close, not a field" (§4.2) fails. | number |
| K6 | **Set gear wears by the night, not by the hour.** | building_clock.md §2 argues that "anything done by work happens about 1/7 as often per world year: uses of a tool, sets of a net". A set trap or net fishes per night, and nights run at 1/11.4. With lives times 1/7, set gear lasts about 1.6 times its real span in world years. Same root as wave1's question 4 (lives counted in nights). | number |
| K7 | **The staging is written for one direction only.** | D2-281: "from today's (about 1/40) through about 1/15" to 1/7. That describes the works. Gear, the weir, the oven and the racks are today above the target (a net 30 against 3; a weir 24 against 1 to 3; an oven 12 against 2 to 3). building_clock.md stage 1 writes new gear "on the rule from the start", so during the 1/15 stage gear sits at 1/7 while works sit at 1/15: gear dearer per real hour than buildings, the reverse of the rule's point. | **blocks** W-82's reading |
| K8 | **Households form fast, and each needs a house at the new price.** | building_clock.md (research note) §9: households form about 20 times as often per world year as real; at 1/7 a village of 15 spends 2 to 4% of its labour on cottages. Priced in the note only, at a 20 to 32 unit cottage; wave1's is 19 to 51 (C31); rest days (L-157) would lower the factor and the price. The proposal and D2-276 do not carry it. | number |
| K9 | **Chores from spare units only, on a run night.** | D2-274: chores are done from spare units only. On a glut night a fisher's units go to lifting, the weir crew and setting; hanging that is a chore from spare units would not get done, and fresh fish keeps 1.5 nights. wave3_keeping §5.1 finds 7 to 8 spare units in its walk; K1's weir night needs 19 to 34. Either hanging is an act in the plan, or the chore phase must take priority over the fallback (wave3 W80-Q13). | number |
| K10 | **Vermin's illness.** | D2-279: more vermin "raise the baseline chance of sudden illness". The only hook is the adult risk of 0.001 a night (`life.py:475-491`, D2-149), about 6% over a 64-day life, not scaled with the lifespan. Doubling it would barely register; no magnitude is proposed anywhere. | number |
| K11 | **Wild cord's cost, read in wave 1.** | wave1 §5.1 says the wild-cord household spends only about 12 units more than the flax household, and that the proposal's "an eighth to a third of a year" "was on the old making prices". Cord is a material (day clock, D2-276), so its hours did not change; the difference is wave1's assumed need (about 0.7 kg a year: half a net and a snare bundle) against the proposal's 1 to 3 kg. Which need is right turns on K5. | number |
| K12 | **Salt for a glut.** | At D2-283's 1 to 4, a 333 kg night needs 83 kg of salt; boiled inland at 1 firewood a salt (L-110) on wave1's 10 kg bundle, about 830 kg of wood. Salting a glut inland costs more wood than smoking it. That may be the intended bind ("salt from elsewhere"), but no document says so. | number |

---

## 4. Code against the design

| # | The code | The design | Severity |
|---|---|---|---|
| E1 | `engine/clocks.py:20-24`: `ITEMS.*.spoil`, `RESOURCES.*.r`, `TECHNIQUES.*.set.life`, `TECHNIQUES.*.rack.nights` and `PHYSICS.smokehouse.fire.*` on the **day** clock; `:31` `PHYSICS.labour.fade_rate` and `fade_after` on the **year** clock. | D2-273: how long goods keep, the wild's production, process times on the year clock; learning and practice on the life clock. A nightly share can stay a night's share, but it must be derived from a year-clock value, or a world with another year length departs from the rule. wave3_keeping §7 #4 finds the first half; the fading half is new. | number |
| E2 | `world.py:97`: `season_days` defaults to 6, a 24-day year. | D2-209 and every wave number: a 32-day year. Every current world maker sets 8, so it only bites a world that forgets. | wording |
| E3 | `data.py:1130`: `LIFE["lifespan"]` 32 (D2-153's default); `knowledge.py:75-83` `practice_x` scales only the hunt's practice (`hard(tech)`) by 32 / lifespan; trades and basic work are not scaled at all. `SKILL` tau 50 (`data.py:732`). | D2-267: all practice and learning set at a 64-day lifespan and scaled with the world's. | number |
| E4 | `wild/kinds.py:412`: the expert sign "an eel night: dark, wet and the water rising after the dry weeks; set the traps tonight"; `wild/kinds.py:894`: "{kind} crowding in the pool below the dam at {place}: net them, or draw the hatches and let them up" (found by wave3_taking). | D2-269: never direct an act. | wording |
| E4b | `engine/wild.py:918`: the set result "they will catch by night for about N nights, for whoever comes to them"; `wild/methods.py:66`: "whoever finds it takes the catch". | Q-80's answer (S14): unnamed acts touch only one's own. | wording |
| E5 | No ice term in `wild/gear.py` or `wild/runs.py`; ice only wears the weir faster (`wild.py:2992-3002`) and crowds fowl onto open water (`OPEN_WATER`, `wild.py:1235-1272`, `frozen_run` at `:1207`). | D2-265: a freeze stops fishing (C12). | **blocks** (no design yet: G1) |
| E6 | `verbs.py:142`: `n = int(TECHNIQUES[tech]["units"])`: a cost under 1 truncates to 0 (free); 1.5 to 1. | D2-276's prices: about 40 rows fall below 1 (wave1 §5.3). Dressing a deer (hunt_fish_materials §4.3, "about 0.5 unit") is free today. | **blocks** (the floor and batches) |
| E7 | `night.py:339-352` `spoil_rate`: the item's spoil × `house_spoil` 0.3 (`data.py:776`) × the best fitting's `spoil` (bins 0.5, granary 0.2, cellar 0.25), × 2 for fresh fish in a store (D2-212). | D2-272 and D2-279 remove the house rate and the fittings' multipliers; wave3 §7 #2: the fresh fish × 2 becomes a penalty a store adds, which D2-272 does not allow. | number (known; listed for completeness) |
| E8 | `keeping.py:1-13`, `:39-47`: racks hold the technique's batch of 40 a fitting, for 3 nights; a done batch goes to the store at once. `data.py:624`: smoking costs 1 unit whatever the batch. | D2-284: 250 kg a set, a keeping smoke 1 night, a hard cure 2 to 3; hanging 30 fish a unit; done lots stay up (open, C28). | number |
| E9 | `things.py:637-647` `find`: the most recently known thing matching a place or set words, with no preference for one's own; `farm.py:816-818` `_herd_on`: unnamed, one's household's herd first, then anyone's (`(own or hs)[0]`). `things.py:289-291` `owns_set`: only the setter (`by`) or a weir's crew. | Q-80 and acts_on_owned_things: one's own by default; wave4 §5.3 and acts_on_owned_things open question 1: a household's things count as its members' own, which `owns_set` does not do. | number |
| E10 | `here.py:379-387` `party_container`: work for a household goes to its first-claimed building with a withdrawal right. | store_rules: a fault the book fixes; wave3_keeping §7 #14: a later smoke hut or tub never receives a catch by default. | number (known) |
| E11 | `life.py:475-491`: an adult's "sudden illness" at 0.001 a night, not scaled with the lifespan (only the elder's doubling scales). | D2-279's vermin-raised illness (K10); D2-273 puts ageing on the life clock. | number |
| E12 | `bots_livelihood.py`: no bot issues a `build` act; the only scripted builds are in `specs/peoples_settle_probe.py:81-90`. | W-82: "the building clock's first stage read with bots: ... does building still happen". The bots can price what a build costs, but cannot show whether anyone builds, unless W-82 wrote a build policy (its note was not there to check). | **blocks** W-82's reading |
| E13 | `data.py:105`: the pack has no life; `data.py:812`: carry on foot 10; `data.py:51`: the fishing rod's 30 uses, never worn (`uses` items wear only by ploughing and hoeing, engine_audit §5, `farm.py:1115`). | D2-264 (gear life by material), D2-281 (basket and frame), D2-276 (lives at the factor). | number (known) |
| E14 | `data.py:729-730` `TRY`: aware cannot try; rough uses 1.7 times the inputs and works half the time. | trying_and_learning §2 and wave4 §4.2: aware may try at 0.6, 0.35 or 0.15 by class. | number (open) |
| E15 | `memory.py:135` `KEPT`: 25 words, 5 places a lifespan. | D2-266: about 40 words, a place a stretch. | number |
| E16 | No fouling or pollution state anywhere in `engine/` or `wild/`. | D2-264 (retting fouls the water), D2-281 (retting and tanning now). New work (G3), not a conflict. | **blocks** (no design) |
| E17 | `data.py:254`: the anvil and bellows already take 2 hide; `data.py:108`: harness exists with an 80-day life. | D2-281 lists bellows and harness as leather's uses to come: they would need leather in place of raw hide, a recipe change, not a new item. | wording |
| E18 | `data.py:376-386` `WATER_WORKS["weir"]`: the first section 6 timber and 8 units on top of the wattle section's 6 timber and 16 (12 timber, 24 units in all); timber 10 and 25; footing 10 stone and 15. | hunt_fish_materials §6 cites "the first 4 timber, 2 withies, 8 units for its base, then wattle 12 withies, 1 timber, 16 units" as if built ("built; recosted") without saying which parts are proposed. | wording |

---

## 5. Gaps: mechanics a decision needs that no proposal designs

| # | Decision | What is missing | Severity |
|---|---|---|---|
| G1 | D2-265 (a freeze stops fishing) | Which methods stop (hand fishing, angling, set gear, nets, the weir), on which water (still water and the edge freeze first; a river seldom), after how many frosty nights (`frozen_run` exists), what becomes of salmon running into early winter and of eel spearing through ice, and how D2-210's ice wear sits beside a weir that has stopped. L-150 defers the refining, not the base rule. | **blocks** |
| G2 | D2-281 (tanning in this build) | Lime (no good exists; wave1 assumes wood ash), the tan pits as a work (cost, site by water), peeling bark as an act (late spring, from coppice: which stock does it draw?), leather as a good with a weight, and each use's mechanic: the frame's +20 carry; harness and bellows switched from raw hide to leather; **shoes have no mechanic at all** ("less cost to walking and the cold": there is no walking cost by footwear, and the cold works through shelter). Seeding leather, since tanning outlasts a 30-day run (K4). | **blocks** |
| G3 | D2-264, D2-281 (pollution from retting and tanning) | hunt_fish_materials §7.5 is a sketch: no amount a batch puts in, no fade rate or clock, no rule for how far downstream it carries (by reach, by body: D2-229's waters), no harm in numbers (the share of the shallows and resident stock killed), and "beasts will not drink" assumes a drinking mechanic for herds that I did not find (I don't know whether one exists). | **blocks** |
| G4 | D2-282 (conditional rules) | store_rules has `unless` (starving, winter, full) and no `when`. wave3_keeping §4 now designs it (states latched, knowledge only, a chore phase). Still open there: the chore phase against the fallback (`run.py:1036-1057`, L-142), and whether a rule may do production (W80-Q6). | **blocks** (designed, undecided) |
| G5 | D2-271 (three depths) | Whether a depth is a good or a state. The engine has one `smoked fish` (`data.py:55`); D2-282's "a cure finished" implies a state; wave3 W80-Q7 recommends new goods (hot-smoked, hard-cured); wave1 hands "the hard-cured meat good" to part 3. | number |
| G6 | D2-264 (the shallows by water type) | No proposal gives the shallows' K and r by water type or the generator's rule. fishing_ladder §2 holds the real anchors (a brook 30 to 60 kg a km; production about the standing stock a year, P/B 0.6 to 1.1); hunt_fish_materials §7.8 is qualitative only. | number |
| G7 | D2-276 (builders as a trade) | A builder's skill halving the units and setting a building's soundness (building_clock.md open question 4) is designed nowhere; it was moved to W-76, queued after the wave (S13). | **blocks** the staging |
| G8 | D2-276 (cheaper crop protection) | Herding by children (the order exists), dead hedges, moved folds, fences priced by length: listed in building_clock.md, designed nowhere, no OPEN row. | **blocks** the staging |
| G9 | D2-276 (clearing a plot at a time) | L-153, deferred and open. | **blocks** the staging |
| G10 | D2-279 (barrels, or something that holds brine) | No cooper, no tub. wave3 W80-Q9 proposes a basic tub now. | number |
| G11 | D2-279 (vermin raise sudden illness) | No magnitude, no hook other than the adult death risk (K10). | number |
| G12 | Q-80, wave4 §5.3 (a household's things as its members' own) | `owns_set` knows only the setter; household-held sets and gear need an owner field (the household) and a rule for whose catch it is when a member lifts. | number |
| G13 | W-82 (bots read the 1/15 stage) | A bot policy that decides to build (E12). | **blocks** W-82 |
| G14 | D2-273 for set gear (K6) | A rule for gear whose life is counted in nights (traps, nets, tents, bedrolls) against gear counted in acts. wave1 question 4 asks it. | number |

---

## 6. Questions for Zach, ranked by what they block

Each stands alone. Ids in brackets are the records' where one exists; "(new)" means no ask is recorded yet.

**1. What a unit of the bulk goods weighs** (D2-264; wave1 question 1; new). Every good's weight is now to be in kilograms, but the
bulk goods' units do not survive it: a timber reads as about 240 kg (a figure that came from squeezing a year's fuel into the
engine's year), a stone weighs 3 though 30 of them build a 40 t room, a straw is a fifteenth of a plot's real straw, and the wave's
own notes disagree on firewood (10 kg in wave 1, 60 kg in wave 3, so every fuel cost differs by six). **Options:** (a) a handling
unit for each, with every recipe rewritten in real kilograms: timber and stone a 25 kg load, firewood a 10 kg bundle, straw a 16 kg
truss, hay 10 kg, charcoal 20 kg, withies and bark 10 kg bundles (wave 1's recommendation); (b) keep the units and state their real
weights (timber about 240 kg, a stone over a tonne), so timber can never be carried on foot. **Recommend (a):** it makes three
present rates real with no change of number (straw a plot, fuel cut a unit, salt's fuel), and it is the only option under which a
person can carry a building material. **Blocks:** every recipe, the fuel a night, the smokehouse's fuel, salt's cost, carrying,
the moving rate, and part 2 of the wave.

**2. How "keeps for X" becomes a nightly loss, and the floor's shape** (D2-273; wave1 question 3; wave3 W80-Q1; new). The engine
loses a fixed share a night; a shelf life has to become that share. Wave 1 reads "keeps d days" as half lost by then and puts every
food on one curve (nights = the first two days in full, the rest at 1/11.4); wave 3 recommends reading it as a quarter lost by then.
The difference is about a factor of two on every keeping rate: a household in wave 3's winter walk reaches spring with about 12
food left under the half reading, 29 under the quarter, 41 under a tenth. **Options:** (a) half-life, on wave 1's curve; (b) a
quarter lost by then, on the same curve; (c) a curve by age (whole until its time, then fast), which needs dated lots in stores.
**Recommend (b) now and (c) later with the stores:** it keeps salt and the hard cure worth having over the gap between runs without
making keeping hopeless. Also say whether the curve itself is a fair reading of your "a day or two keeps its real nights" rule
(the literal floor gives every food from 2 days to 3 weeks the same 2 nights). **Blocks:** every shelf life, the stores'
calibration, and whether salt, barrels and the timber smokehouse are worth building.

**3. Whether hot smoke should be worth anything** (D2-271; new). On the compressed shelf lives fresh fish keeps about 1.5 nights and
a hot smoke about 2.4, so the first of your three depths buys under a night. **Options:** (a) accept it: hot smoke is for eating
soon and selling nearby, and the engine has little "soon" to offer; (b) a named departure giving hot smoke 3 to 4 nights; (c)
drop hot smoke as a separate act and keep two depths. **Recommend (a)**, written as a known consequence, since the real keeping
order is still kept. **Blocks:** whether hot smoke is built as its own act and good.

**4. The smoke racks' load and the floor a set takes** (Q-83 and D2-284; wave3 W80-Q5; new). You said yes to both "about 500 fish
on 2 spaces" (Q-83) and "about 250 kg a set" (D2-284) on 22 Nov. A fish unit is about a kilogram, so these differ by two. **Options:**
(a) 250 kg a set on 2 spaces (about 25 kg a m², a real hut of 7 to 10 m²; wave 3); (b) 250 kg a set on 1 space (50 kg a m², the
research's middle; wave 1); (c) 500 kg a set on 2 spaces (Q-83's wording). **Recommend (b)**, with D2-284 standing and Q-83's
record corrected: the 250 is the later decision and wave 1 already prices the smokehouses on it. **Blocks:** the racks' `holds`,
the hut room's size, the smokehouses' costs, hanging and fuel.

**5. Gear whose life is counted in nights against gear counted in acts** (D2-276; wave1 question 4; new). D2-276 says a thing's life
is "its real years as world years, or its real uses times the same factor" (about 1/7). A set trap or net fishes by the night, and
nights run at 1/11.4, not 1/7; a bedroll and a tent are counted in nights too. And a net's real life is 50 to 450 sets, so times 1/7
it lands anywhere from 7 to 65 engine sets, which decides whether a fishing household needs 1 kg of cord a year or 10, and so
whether flax is a garden close or a field. **Options:** (a) lives in nights at 1/11.4, lives in acts of work at 1/7, set gear counted
in nights; (b) everything at 1/7. **Recommend (a)**, with a net's life near the top of the range (about 40 to 60 sets) so the
proposal's cord need and the flax close hold. **Blocks:** the gear-life table (D2-264), cord demand, the flax close's size.

**6. Smoking as a make act or as a processing container** (D2-282; hunt_fish_materials open question 10; wave3 W80-Q2; new).
Wave 4 writes "smoke fish" as a make act, a batch over nights, and its lore lines read a batch size and nights. Wave 3 makes racks,
a salting tub, drying racks, tan pits and retting ponds one kind of container holding lots that change state over nights, with
hanging as work by the kilogram, the cured state firing the rules you asked for, and the smokehouse a store once the lot is done.
**Options:** (a) one processing-container unit for all five (wave 3); (b) smoking stays a make act and the rules read the batch;
(c) five separate mechanisms. **Recommend (a):** it is what D2-282's "move smoked fish to the cellar once cured" needs, and today's
smokehouse code is already most of it. **Blocks:** the racks' rebuild, tanning and retting in this build, and the people part's
craft lines.

**7. Whether gear moves to 1/15 with the works in the first stage, and whether the stage waits for its companions** (D2-276,
D2-281; W-82; L-153; W-76; new). The staging "from today's about 1/40 through about 1/15" describes buildings. Gear, the weir and the
oven are today above the target and get cheaper; written "on the rule from the start" (building_clock.md), gear would sit at 1/7
while buildings sit at 1/15, so gear costs more per real hour than a house. And D2-276 brings the factor in with builders as a trade,
cheaper crop protection and clearing a plot at a time, which building_clock.md puts before any work is raised; but plot clearing is
deferred (L-153), builders are in the timber economy (W-76) after this wave, and crop protection has no row. **Options:** (a) all
capital on one factor at each stage, and the stage waits until a minimal builder skill (units cut with skill, nothing more) and
plot clearing are in; (b) gear at 1/7 at once, works staged, companions later; (c) run W-82's bots now and decide after. **Recommend
(a).** Also note: the livelihood bots never build (`bots_livelihood.py` has no build act), so W-82 can show what building costs but
not whether anyone builds, unless a build policy is written for it. **Blocks:** W-82's reading and every repricing of works.

**8. The lifespan learning is set at** (D2-267, D2-153; new). D2-267 sets practice at a 64-day lifespan; the engine's default
lifespan and the base its hunt practice scales from is 32 (D2-153); trying_and_learning's tables are at 96. Only the hunt's practice
scales with the lifespan today; trades and basic work do not, and skill fading runs on the year clock. **Options:** (a) change the
engine's default lifespan to 64 (the worlds already use 64), re-base the constants once, scale every craft's practice with the
lifespan, and move fading to the life clock; (b) keep 32 as the default and state D2-267's values as 64-based constants converted.
**Recommend (a)**: one basis, and the current worlds read as written. **Blocks:** the learning build (wave 4 §4).

**9. Whether acts on held things default to one's own is now decided, and what "several of one's own" does** (Q-80; S14). Your
21 Nov answer is in Q-80's notes ("yes to the concrete proposal ... unnamed acts touch only one's own (one: that; several: asked;
none: refused ...)"), but Q-80 is still open and has no decision number. Since then the fishing design and both wave 3 (taking) and
wave 4 have a lift (or tend) take the catch from all of one's own sets at a place, against your "several: asked". Separately, the
engine counts only the setter as a set's owner, so a household member lifting the household's traps is taking another's.
**Options:** (a) record your answer as a decision, with one amendment: a lift takes all one's own of that kind at the place (six
traps are one line to a fisher), while an act that uses a thing up (slaughter, a take from a pile) asks, as you said; household
things count as every member's own; (b) record it exactly as you said, every "several" asked. **Recommend (a).** **Blocks:** the
resolver, set and tend, wave 3 (taking) as a whole, and the target rule.

**10. The kept-line budget over a life** (D2-266, D2-268; new). Knowledge in their own words budgets about 20 kept lines (800
words) over a 64-day life. Wave 4 seeds founders with up to 20 lines that do not take the places opening each stretch, so a founder
reaches old age with about 40 lines, 1,600 words, before the rewritten memory. **Options:** (a) seeded lines additive, as wave 4;
(b) seeded lines count against a fixed total of about 20, so founders gain few new places; (c) additive with a cap of about 30 lines.
**Recommend (c)**, measured for cost in the first runs. **Blocks:** the memory build and every prompt's length.

**11. Moving goods inside and between stores** (D2-274's provisional labour; new). The store rules make moving free within a
building, including into containers; hanging fish on racks is real work at about 30 a unit; and the rate between buildings (about
800 kg a unit a parcel step) assumes a 40 kg sack a trip while people carry 10 on foot and 25 with a basket. **Options:** (a) hanging
and taking down are quantity work at real rates wherever they happen; other moves inside a building free; the between-buildings
rate set from the carry limit (about 500 kg a unit a step with a basket); (b) everything inside a building free. **Recommend (a).**
**Blocks:** the rules book's labour, the chore phase.

**12. Barrels, or a tub, in this build** (D2-279; wave3 W80-Q9; new). D2-279 lists barrels in the set of stores and also says
"barrels later". Salt fish keeps its year only in brine; out of it, twice as fast, about 17 nights, which puts it below the hard
cure. **Options:** (a) a basic salting tub now (about a timber and withy hoops, no cooper), barrels and the cooper later; (b) barrels
and a cooper now; (c) nothing, salt fish at half its year. **Recommend (a).** **Blocks:** salt's value in this build and the keeping
order.

**13. Tanning's scope in this build** (D2-281; wave3 W80-Q12; new). Tanning needs lime (no good exists), tan pits, bark peeled in late
spring, and 16 to 48 nights in the pits, longer than the 30-day live runs. Its uses: the frame, harness and bellows (which today take
raw hide), and shoes, which have no mechanic (there is no walking cost by footwear). **Options:** (a) lime from wood ash, lighter
leathers at 16 to 24 nights, the frame, harness and bellows switched to leather, shoes later, tanner households seeded with leather
and hides in the pits; (b) the whole process and shoes now. **Recommend (a).** **Blocks:** the materials part (wave part 2).

**14. What "a freeze stops fishing" means** (D2-265; L-150; new). The engine fishes on under ice (only the weir wears faster and fowl
crowd onto open water), the river's signs say it must not claim otherwise, and in reality eels were speared through ice and rivers
seldom froze. **Options:** (a) still water and the edges freeze after a run of frosty nights (the engine already counts them):
hand fishing, set gear and nets there stop; a flowing river, its runs and the weir go on, the weir wearing as now; (b) wave 3
(taking) §4.5's version: set gear idle, the edge and bank lines refused, the weir icing up and wearing as built, a run's night held
over to the next open night, fowling at its best; (c) every water method stops on any frozen night; (d) nothing stops, and the
signs say so. **Recommend (b)**, which is (a) made specific, with one check: whether a big river's open main stream still lets a
run pass (it did in reality). **Blocks:** the river's ice signs, the fowling rise in a freeze, and a phase-1 engine change.

**15. Whether D2-274's household book replaces 37.4's standing orders and standing rules, and posting it** (D2-274, D4-16; S5,
S12; new). The spec says standing orders bind only the one who sets them; 37.4's standing rules proposal changes them only at the
evening and excludes trips. D2-274 gives a household a book that binds its members, set in any turn, and the travel deferral (L-152)
would put "when to push on or turn back" in it. Several other decisions of the day also land in 37.4's areas (buildings' costs, the
prompt, memory, the archetypes), and nothing has been posted to the board since 19 Nov. **Options:** (a) yes: post to 37.4, mark D4-16,
D4-64, D2-155 and D2-166 amended, keep trips out of the book as 37.4 proposed; (b) wait for 37.4. **Recommend (a).** **Blocks:** any
merge in those areas.

**16. Repricing the network's gear and works to D2-276** (D2-276; new; confirm). hunt_fish_materials still prices a net at 30
units, a trap at 2.5 and the withy bed at 10; wave 1 has them at 3 to 4 plus cord, 0.3 to 0.6 (six for 3 units), and 1.5, at 1/7,
with the 1/15 stage beside them. **Options:** (a) rewrite §4 to §6 and §13 of the proposal to wave 1's prices; (b) keep the
proposal's as a stage. **Recommend (a).** **Blocks:** the craft lines that show units (D2-263).

**17. Accepting the peak-night bind on keeping** (D2-284, D2-283; new). Once fuel is cut at real weights, smoking a weir's 333 kg peak
night costs about 19 to 34 units (hanging, tending and cutting the wood), three to six person-days, and a hard cure adds salting and
83 kg of salt. One household cannot keep a full weir's glut. **Options:** (a) accept: the answer is several households, hired hands
or salt bought in, which is the leverage the design wants; check with the bots that the full-weir arm still feeds; (b) lower fuel
per kilogram as a named departure. **Recommend (a).** **Blocks:** the nutrition arms' calibration.

**18. Whether the core prompt says knowledge dies unless it is passed on** (Q-81; new). Knowledge in their own words puts it in the
core; wave 4 leaves it out so it can be one of the cultural strands you asked to vary. **Options:** (a) a strand, varied (wave 4);
(b) in the core for all. **Recommend (a)**, following your 22 Nov words ("These themselves can be experimental parameters to vary as
different cultures"). **Blocks:** the core's text.

**19. Whether D2-269 covers results and seeded lore as well as signs** (D2-269; new). A live expert sign says "set the traps
tonight"; the river's signs propose "traps set now will stand"; a spent trap's result says "Set again to fish on"; the fisher's
seeded lore in wave 4 says "Dry it at the hearth ... or salt it ... the day it is caught". **Options:** (a) signs and results only
observe; seeded lore, as a person's own memory, may give advice; (b) everything observes. **Recommend (a)**, and fix the live sign
now as a phase-1 mend. **Blocks:** little; the mend-what-misleads phase.

**20. The food's energy basis as a decision** (Q-69; S1; new). Everything in the wave is priced on 1 food = 2,500 kcal, a child 0.6
and an elder 0.8 of it, recorded only as a default taken on Q-69. **Options:** (a) confirm as a decision; (b) change it. **Recommend
(a).** **Blocks:** nothing new, but every food number rests on it.

**21. The salmon's return on the year clock** (D2-209, D2-273; new). D2-209 compressed the salmon's three-year return to one world
year; D2-273 would make it three. **Options:** (a) keep one world year as a named departure (at three, a 64-day run never sees a
return); (b) three world years. **Recommend (a)**, written into clocks.md as a departure. **Blocks:** the runs' calibration, slightly.

**22. Grain under the new shelf lives** (L-154; new as a reading). With real capacities and compressed shelf lives, grain keeps
about 221 nights well kept (about seven world years) while everything else keeps 2 to 40, so grain is free to hoard and a large
granary has no pull except vermin. **Options:** (a) as L-154: read it in the first farm-world run; (b) set grain's well-kept life
to about two real years (about 66 nights). **Recommend (a)**, with (b) ready. **Blocks:** nothing now.

**23. The year clock against short runs** (D2-273, D2-264, D2-281; new). The withy bed takes 64 to 96 nights to come into yield,
tanning 16 to 48; the live runs that test this thread are 30 days. **Options:** (a) seed worlds with beds, pits and leather already
in their state, and run the long-capital questions in long bot runs; (b) a named departure shortening them. **Recommend (a).**
**Blocks:** what a live run can show of the withy bed and leather.

**24. The hearth rack's drying time** (hunt_fish_materials open question 8; wave3 W80-Q10). Its 3 nights are about a month of real
drying, against days to two weeks: 1 night, with the batch raised to 10 to 15. **Recommend yes.** **Blocks:** the hearth rack's
recost only.

---

## 7. The sibling notes, checked

**wave1_physical_basis.md (W-77).** Thorough; its 28 contradictions overlap mine (C1, C2, C21, C22, C26, C30 among them) and I
have not repeated its own list. Against it:
- §7 says "Q-73 is still Zach's": Q-73 was closed by D2-283 on 22 Nov. §5.4 #15 says the open row on the racks (Q-83) "should be
  read against it": Q-83 was closed by D2-284.
- §5.1 says the wild-cord household spends only 12 units more than the flax one because the proposal's figure "was on the old making
  prices". Cord is a material on the day clock, so its hours did not change; the difference is wave 1's assumed need (about 0.7 kg a
  year) against the proposal's 1 to 3 kg (K11). The real question is K5's.
- Its firewood of 10 kg is not carried into wave 3, which uses 60 kg (C21).
- Its half-life reading of shelf lives is not wave 3's (C9).
- Its racks are 1 space a set; wave 3 recommends 2 (C1, question 4).
- Its cottage (19 to 51 units) differs from building_clock.md's (20 to 32, "about 36") (C31).

**wave4_people.md (W-78).** Against it:
- §2.6 "Kept lines and memory open each stretch as now": today about five places open over a life, not one a stretch; the change is
  D2-266's.
- Its seeded lines are additive to the stretch places, doubling knowledge_in_their_own_words' budget (C15, question 10).
- Its lift takes all one's own (C6), resolving Q-80's second question differently from the proposal; its household-as-own needs
  `owns_set` changed (E9).
- It writes smoking as a make act (C27, question 6), against wave 3.
- It drops the "knowledge dies unless passed" line from the core (C18).
- `do` as a free string with the 38-verb enum gone (§5.2) changes 37.4's reply schema while the verb list (Q-27) is still open;
  D2-266 ties this build to W-70, 37.4's, which waits on Q-27.
- Its fisher lore lines FI3 and FI16 give advice and repeat "fresh fish keeps worse in a store than meat", which wave 1 (#18) and
  wave 3 (§7 #2) find inconsistent with D2-272 (question 19).
- Its tau of 7, 17 and 33 units (simple, practised, skilled) at lifespan 64 against the code's single 50 for every trade is a large
  change in how fast simple crafts are learnt; it is labelled calibrate, but nobody has read it against the runs' practice counts.

**wave3_keeping.md (W-80).** Its 15 conflicts (§7) overlap mine (E1, E7, E8, E10, C1, C28). Against it:
- It uses the 60 kg firewood (C21), so its fuel is about six times light on wave 1's unit, and its "the wattle hut never binds"
  should be re-read with fuel cutting counted (K1).
- §5.1 cites "taking down free within the building (D2-274)": D2-274 says the labour rates are provisional; the free move is
  store_rules', and hanging is not free in the same note (C23).
- §5.1 cites "1 food = 2,500 kcal, D2-258": D2-258 does not state it (S1).
- Its walk is one household with six traps and one weir turn (243 kg in a run); the question of who keeps a full weir's glut is not
  in it (K1, question 17).

**wave3_taking.md (W-81)**, read in its §0, §4.5 and §7 only (it landed at 08:29). Its 17 conflicts overlap mine (C4, C5, C6, C12,
C13, E4) and add two I had not found (`kinds.py:894`, the set's "for whoever comes to them"). Against it:
- It chooses "tend" for the second act where wave 4 chose "lift" (C5); the two people notes need one word before either is built.
- It drops a set's life in nights (each night fished is a use of its gear), where wave 1 proposes lives counted in nights at
  1/11.4 (question 5). The two are compatible only if a night's use is counted at the calendar's factor; neither says so.
- It resolves "several of one's own" as "take all" while quoting Zach's "several: asked" (question 9).
- Its §7 #15 reads wave 1 as saying the carry limits bind only on the road; if so, moving goods within a village is limited only by
  the store rules' rate (C24), and that rate is the one to get right.

---

## Report back to 37.2

The five findings that matter most. **First**, the wave's three notes disagree on the basis everything else is priced on: a
firewood is 10 kg in wave 1 and 60 kg in wave 3 (six times on every fuel cost), "keeps a season" is a half-life in wave 1 and a
quarter lost in wave 3 (about twice on every keeping rate), and a set of racks takes 1 space or 2; and Zach said yes both to 500 kg
of racks (Q-83) and to 250 kg a set (D2-284) on the same day (questions 1, 2, 4). **Second**, the rule under every number, 1 food =
2,500 kcal with children 0.6 and elders 0.8, has no decision: it is a default taken on Q-69, which D2-275 closed with the unit's
length only (question 20). **Third**, hunt_fish_materials has not caught up with the day's decisions: its gear and works are priced
at real hours (a net 30 units against D2-276's 3 to 4), tanning is "left out" against D2-281, shelf lives are "open" against D2-273,
and its summary states the replaced wild-clock rule; river_signs fishes under ice against D2-265; trying_and_learning is set at
lifespan 96 against D2-267's 64 and the code's 32; and a live expert sign tells people to "set the traps tonight" against D2-269
(`wild/kinds.py:412`). **Fourth**, the staging of the building factor is only half designed: it is written for things that get
dearer, while gear and the weir get cheaper; its decided companions (builders, plot clearing, cheaper crop protection) sit deferred
or queued; and the livelihood bots never build, so W-82 cannot read "does building still happen" from them as they are (question 7).
**Fifth**, the day's decisions land in 37.4's areas (the standing rules, the buildings' costs, the prompt, memory, the archetypes)
with no board post since 19 Nov, nine of the 23 decisions have no spec home, none fills its Replaces column, and goods.md and
buildings.md still state the store multipliers D2-272 removed (S2 to S7, S12, question 15). Unpriced couplings worth a look before
the build: a full weir's peak night needs 3 to 6 person-days of keeping once wood is cut at real weights (K1), hot smoke is worth
under a night under the floor rule (K2), and the year clock puts the withy bed and tanning beyond a 30-day live run (K4).

## Sources

`docs/cybertron2/proposals/` (hunt_fish_materials.md, building_clock.md, store_rules.md, verb_grammar.md, trying_and_learning.md,
knowledge_in_their_own_words.md, acts_on_owned_things.md, river_signs.md; 37.4's standing_rules.md, livelihood_archetypes.md);
`docs/cybertron2/spec/` (core/clocks.md, economy/goods.md, production.md, buildings.md, README.md, agents/work.md,
standing_orders.md, information/memory.md, process/how_we_work.md); `docs/cybertron2/DECISIONS.md` (D2-153, D2-155, D2-209,
D2-210, D2-258 to D2-285, D4-16, D4-64); `docs/cybertron2/items/` (Q-27, Q-69, Q-73, Q-79 to Q-84, L-133, L-148, L-150, L-154,
L-157, O-2, W-70, W-71, W-76 to W-82); `docs/coord/BOARD.md`; this folder's notes (building_clock, smokehouse_capacity, storage,
store_management, engine_audit, fishing_ladder, learning_times, founders_knowledge, household_skills, wave1_physical_basis,
wave3_keeping, wave3_taking in part, wave4_people); the code at the lines cited (`engine/clocks.py`, `world.py`, `verbs.py`, `night.py`, `keeping.py`,
`things.py`, `farm.py`, `here.py`, `knowledge.py`, `life.py`, `memory.py`, `data.py`, `bots_livelihood.py`, `wild.py`,
`wild/kinds.py`, `wild/gear.py`, `wild/runs.py`; `specs/make_peoples.py`, `make_water_worlds.py`, `peoples_settle_probe.py`).
