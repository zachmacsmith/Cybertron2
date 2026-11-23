# U9 People: the core prompt, what each person is shown, the act shapes, the founders' seeded knowledge, learning as one record

**Status:** discussion (component spec, 22 Nov 2026). Nothing built. The parts decided are cited (D2-263, D2-266 to D2-270,
D2-274, D2-279, D2-282, D2-286, D2-289 to D2-296); everything else is a default or open, marked, with its question in the last
section.
**Owner:** 37.2 (the content: the core's lines, the founders' templates, the crafts' learning data, the worlds); 37.4 owns the
engine's core this unit changes (the prompt, the reply schema, memory, the knowledge record, the verb registry and its resolver) and
is named on any merge (README, owners). **Thread:** the wave's integrated design (W-85), under W-73; the people part was W-78.
**Feature units** (D2-244): three, each with its data, acts, lines and process listed together so the later cut can move it whole:
**the prompt core** (§1, §2), **the act shapes** (§3), **knowing and learning** (§4, §5: the record, its five events, the founders'
templates). Generation and the gate check that place the founders' lines are U11's (`u11_worlds.md`).


> **Decisions since this spec was written (binding over its text; the build reads this table first):**
> - **D2-301:** own rules and standing fallback before every household chore; none at the start, nothing pushing; units left are rest.
> - **D2-304:** unnamed acts on several of one's own: a yield-taking act (tend) takes all; an act that uses up, kills, destroys or gives away needs a named target.
> - **D2-305:** acts on held things take the thing as target; unnamed, only one's own; household things are every member's own.
> - **D2-307:** learning scaled with lifespan in every part; fading on the life clock.
> - **D2-308:** kept lines: founders' seeded lines on top of the places opened each stretch, about 30 in all, for now.
> - **D2-311:** seeded memory of a household's capital is inside the 20-line budget, written with the livelihood it belongs to (not an extra line).
> - **D2-313:** 37.2 owns every engine file this wave changes (read every '37.4' in the code tables as 37.2 for this wave).
> - **D2-314:** the eleven act shapes are the verb list.
> - **D2-318:** fowling postponed to the hunting build-out (no fowling net, no fowling method in this wave).
> - **D2-319:** rules changed any time and in the evening talk; a seeded line on evenings as the time to revisit rules.
> - **D2-320:** crop protection as it is (dead hedge postponed); a rough watch act (units watching over a field, herd or building, by day or night), widening `guard`.
> - **D2-326:** practice alone can reach known (slower); teaching far more efficient; replaces 'the last lesson only from a teacher'.
> - **D2-327:** tanning and leather deferred until the wave is tested (frame, harness and bellows in leather, tanning's pollution with it).

## Extends

Each read in full, not from its summary.

| Earlier | What this spec takes from it |
|---|---|
| proposals/knowledge_in_their_own_words.md (Q-81; accepted in part D2-266, D2-268) | the short purposeful core told to all; knowledge that differs by person; a kept place each stretch, about 40 words; attention as learning; the founders' common sets by practice; cultural variants as a parameter |
| proposals/trying_and_learning.md (Q-82) | three difficulty classes and their parameters; every attempt teaches (cause, else the next lesson, else the hands); awareness easy; skilled crafts need a teacher; teaching toward the teacher's peak; continuous skill with capability points; transfer through underlying skills; inherited aptitude off |
| proposals/verb_grammar.md (exploration) | a verb is a shape, a technique the how; the agent names the technique and its target; the shape only where one technique has two; social acts folded; verbs by knowledge and stage |
| proposals/acts_on_owned_things.md (Q-80; Zach's 21 Nov answer in its notes) | the thing is the target, by tag or a known name; one's own shown with tags; unnamed touches only one's own; another's only when named, and called what it is |
| proposals/livelihood_archetypes.md (37.4's, read, not edited) | the universal core of about 35 acts; archetypes with tiers; two livelihoods a household (Zach, 16 Nov); individuals from another household bring its crafts |
| proposals/verbs.md (37.4's, read, not edited) | verbs as typed handlers whose objects are data; the rules against swelling; refusals that teach; the free reply fields |
| docs/review/37_growth/02zzzh_hunt_fish/wave4_people.md (W-78, all of it) | the main draft: the core's tests and lines, the per-person prompt, crafts under shapes, the rules block, the base, head and livelihood templates, the cap, the record and its events, the shapes and the fold table, sizes |
| docs/review/37_growth/02zzzj_steering/steering.md (W-84) | §2's fixes F1 to F8 and §4's wording table: no horizon word in intent lines; examples replaced by each person's own; the fallback as a standing setting (now D2-296) |
| docs/review/37_growth/02zzzh_hunt_fish/wave_conflicts.md (W-79) | C5, C6, C14, C15, C17, C18, C27 (now settled by D2-295), S6, S14, E3, E14, E15; questions 8, 9, 10, 18, 19 |
| founders_knowledge.md, household_skills.md (with its 22 Nov addendum), learning_times.md (session notes) | the evidence for what to seed and what to leave out (Part 4.1 of founders_knowledge); the bands, depth by age, the line budget; the classes, apprenticeship terms, the failure lines |
| wave3_taking.md §0, §2.0, §6 (W-81) | set and tend; the state rule for a technique named alone (§6.3); where wave 4's shapes fail for taking (§6.4) |
| wave2_making.md §3.4, §3.5 (W-83) | the craft lines rendered at each level; the learning fields on each new craft (class, curve, profile, lessons, points) |
| wave3_keeping.md §2.1, §4 (W-80) | loading a processing container is a `make` act charged by quantity; the rule grammar's `when` and `if` and the chore phase |
| Decisions | D2-263 (recipes shown), D2-266 (kept places, told-knowledge arm, one build), D2-267 (learning at 64), D2-268 (founders' templates), D2-269 (experts' signs observe), D2-270 (household skills, couplings), D2-273 (the clocks), D2-274 and D2-282 (the book and conditional rules), D2-275 (a unit is 2 hours), D2-279 (management seeded to the head), D2-286 (the options list gone), D2-289 (keeping curve), D2-290 (fuel a night), D2-292 (the food unit), D2-294 (tend), D2-295 (depths as goods), D2-296 (fallbacks by the book); earlier D2-153 (lifespan), D4-29 (no aims shown), D4-61 (memory rewritten), D4-64 (kept lines), D4-76 (the fallback), D4-95 (refusals), D4-105 (fading, sowing lore), D4-123 (lesson in the teacher's craft) |
| Zach, 22 Nov (household_skills, quoted there) | "if we give a family a mill that should definitely be related to their seeded memories": the holdings' lines (§5.6), matched to capital by U11 |

## Departures

Every place this spec differs from what it extends, with the reason. Where an overnight note departed from a decision without
saying so, it is named and the decision followed.

| # | From | This spec | Why |
|---|---|---|---|
| 1 | wave4 §5.2: a technique with two shapes, named alone, "takes its first (set)" | named alone, it **tends** if one's own gear of it stands at the place, **sets** if not and the gear is in hand, else is refused naming where one's gear is (basis §6) | wave4's rule brings back the set-for-lift fault (wave3_taking §6.3, §6.4 #1); basis §6 corrects it |
| 2 | wave4 §5.1: one shape "set and lift" | two shapes, **set** and **tend** (D2-294); lift, check, empty, walk and collect resolve to tend | D2-294 decides the word; the two take different arguments (gear in hand and a place; a thing), cost and change different things |
| 3 | wave4 §1.5: `"why": what you mean to do today, and why`; the morning closing "Plan your day."; the evening's "what you mean to do tomorrow" | no horizon word anywhere an intent is asked: "what you mean to do, and why"; "Decide what to do."; "what you make of the day and what you mean to do" (basis §6, default) | steering §1.2, §3: the word asked is the word given (the evening's "tomorrow" in 83 to 100% of whys, 33% without), at no cost in acts |
| 4 | wave4 §1.5's example acts (`"snares"`, `"lift" T12`) and offers (`"2 bread"`, `"work 2 days"`) | the example act is the person's own first craft and a place it is done, and their own tag when they have one; offers in placeholders (`"<n> <good>"`) | steering Q4 and §1.4: an example read as a template steers (firewood in the fallback; "work 1 days" copied 142 times) |
| 5 | wave4 §1.5 keeps `fallback` as a daily reply field "until L-142"; D4-76 the daily field | the fallback is a **standing setting**: one's own first, else the chores the household's book gives (D2-296); sent only to change it; shown each morning with what it did | D2-296 decides it; steering F2. The mechanism (chores against the fallback, U6's G4) is U6's; this spec gives the words |
| 6 | today's reply line describes "the village" alone among attend targets | no special target described | steering §1.3, F5: the one described target was the most chosen, again and again |
| 7 | wave4's core says nothing of settings | core line 7 ends "What you set stays as you set it until you change it." | steering §1.6, F8: doors barred 967 times though a door stays barred; sleep stated in 92% of evenings |
| 8 | wave4 core line 2: units "told each morning", no length | "units of about two hours" | D2-275 is the engine's frame, not lore; it lets a person's own sense of real work (a kilo of salt to four of fish, an hour's hanging) meet the engine's units. 3 words |
| 9 | knowledge_in_their_own_words §5: "The core says plainly that what one knows dies with one unless it is passed on" | not in the core; it is the base line BS8's last clause and the first cultural strand, varied by world | wave4 §1.4 and its question 1, from Zach's 22 Nov words ("These themselves can be experimental parameters to vary as different cultures"); open (Q below) |
| 10 | D4-64 and spec/information/memory.md (25-word lines, about five places over adult life); `memory.py:135` KEPT | 40-word lines, a place each stretch (D2-266), seeded lines additive, with a total of 30 kept lines (default, open) | D2-266 replaces D4-64's schedule (wave_conflicts S6: D4-64 not yet marked amended); the total answers C15 (founders reaching 40 lines) as the audit's question 10 recommends |
| 11 | wave4 §2.2: a rough idea shows "the main input and the place" | a rough idea shows its inputs **as its card does** (all inputs and amounts), the place, and its odds | D2-263 says so in words; wave2 W2-17 found the conflict; the decision is followed |
| 12 | wave4 §5.1, FI16, FI17: smoking as a make act with `smoke_batch` and `smoke_nights` | loading a processing container is a `make` face ("lay a lot": hang, salt down, lay in pits, sink flax) whose lot becomes the next good when its nights are counted (D2-295, U4); FI16 to FI18 read the container's holds and the process's nights | C27, settled by D2-295 and U4's container |
| 13 | wave4 FI16: "Fresh fish keeps worse in a store than meat" | dropped | D2-272: a store never adds a penalty or slows a food below its base (wave_conflicts §7, audit q19) |
| 14 | wave4 FI3, BS3, HU4: "half gone in {d}"; "keeps a season", "keeps for months" | every keeping figure is said in the world's own nights and seasons from the keeping curve read as a quarter lost (D2-289), through one words scale (§5.1, Basis row B9-1) | the half-life reading was replaced (brief rule 3); "months" do not exist in a 32-day year |
| 15 | wave4 SA1, FI3, FI16: "one salt to {salt_in}" fish (engine units) | "a kilo of salt keeps four of fish, or eight of meat" | D2-283 in kg; D2-264 weights in kg |
| 16 | wave4 BS2, HH6 (today's heat: a cold night 4 times) | a cold night about three times the fuel; a bundle a normal night (D2-290, basis §3) | D2-290 |
| 17 | trying_and_learning §2 (lifespan 96); the engine (base 32, `data.py:1130`; only the hunt's practice scaled, `knowledge.py:75-84`; fading on the year clock, `clocks.py:35`) | every learning increment (practice, score, sightings, aptitude, teaching's share) scaled by 64 / lifespan; the 32-based constants doubled once so worlds at 64 read as now; fading on the life clock | D2-267 and D2-273 (learning on the life clock); audit q8 and basis §1 (default) |
| 18 | wave4 §4.2 scales tau to 64 but not the score a try gives | the score is scaled too | D2-267 says practice **and learning**; a world of lifespan 200 has three times the tries |
| 19 | today's rules text: "A day being taught by someone who knows it makes you capable"; the engine's one session (`teach`) | a session moves the learner toward the teacher's peak by class: capable after one in a simple craft, after two in a skilled one; known in a skilled craft only with the taught lesson | trying_and_learning §5, §6; D4-123 itself (the lesson is in the teacher's craft) stands |
| 20 | `data.py:730` TRY: aware cannot try | aware may try at its class's odds and waste | trying_and_learning §4 and q1 (open; default taken) |
| 21 | the `watch` verb (4 units beside someone) | `attend` with `units` (1 to 4); `watch` resolves to attend with 4 units | Q-81 q3, trying_and_learning §4 (open; default taken) |
| 22 | verbs.md's free `look up` of a card; `look_up` in today's reply | dropped: the craft's line is its card (D2-263) | used in 0.1 to 0.8% of replies (wave4 §1.3 row 42); 37.4's field, named on merge |
| 23 | verbs.md's closed list of about 24; the built 38 (`verbs.py` VERB) | eleven shapes, `do` a free string resolved to a technique or an act; old replies still read | Q-27 is open: this is the proposal to it (§3), not a decision; worlds set `acts: shapes` until Zach decides, so old worlds replay |
| 24 | Zach's Q-80 note "several: asked" | a tend takes all one's own of that technique at the place; an act that uses a thing up asks | basis §6 marks it open on the audit's recommendation (q9); U2 owns the resolver; this spec only renders it |
| 25 | trying_and_learning §8: six to eight aptitudes, strength among them | seven, strength left out | the engine's units already carry the body by stage and age (wave4 §4.8); open (wave4 q6) |
| 26 | livelihood_archetypes q5 ("now: from the line at coming of age") | children minded at home become aware of what their household does at home and rough in a simple craft done often | wave4 §4.5; open (wave4 q7) |
| 27 | wave4 §2.6: "Kept lines and memory open each stretch as now" | not as now: today about five places open over a life; one a stretch is D2-266's change | wave_conflicts §7 |
| 28 | steering §4 / memory.py append-mode request ("what happened, what was agreed or promised, who owes what, what you mean to do") | "what you want to remember of them" | steering §4: the content list steers memory toward ledgers (38.36) |
| 29 | wave4 numbers the head's fuel line HH6 in its table but HH7 in §1.3 and §1.6; HH5 "What comes in goes to {house}" | renumbered (§5.4); HH5 rewritten to the book's real defaults | D2-274: there is no default for putting carried goods away at night |
| 30 | wave4 §3.4: seven head lines | eight: HH8, the chores and fallbacks as a lever | D2-296 makes chores a way of managing a household; D2-279 seeds such ways to the head |
| 31 | wave4 seeds holdings' lines to their keeper only | each household also seeds one holdings line, naming every holding and its keeper, to each working founder (§5.6) | Zach, 22 Nov (a family with a mill knows the mill); household_skills §2.1 had the short form and wave4 dropped it |
| 32 | wave4 §6.4: Nichola capable; household_skills §6.1: Nichola an expert | one expert in a household of three working members | D2-270's size rule (U11) |
| 33 | wave4 FI2, HU1, the reply: "lift" | "tend" in the engine's words; a lore line may say it in a person's words ("goes back to every trap") | D2-294 |
| 34 | wave_conflicts q19 (whether D2-269 covers lore) | lore, a person's own memory, may give advice; signs and results only observe (default) | audit q19's recommendation; open |

## Purpose

The people decide; the engine holds the physics and tells the truth about it (README). This unit decides what is told to everyone
(only the engine's frame, what a run needs to measure society rather than confusion, and the facts of the body), what each person is
shown of their own crafts and rules, how they say what they do, what the founders remember on day 0, and how what anyone knows
changes. Everything that is this world's lore (the seasons, keeping, the runs, food values, fuel, wear) is seeded or learnt, never
told, so that knowing, teaching, forgetting and depending on others have work to do (Q-81; scenario_design §1: leverage and
dependence). The test is whether a fisher knows when the eels run and a farmer does not, and whether it is passed on.

---

## 1. The core prompt, told to everyone

### 1.1 The test for a core line

A line is told to all only if it passes one of three tests (wave4 §1.2): **the frame** (the engine's turn, units, memory, what one
sees and when, how to reply: things no one can learn by living, because living happens inside them); **the measurement** (without
it a run measures confusion: an act that silently touches another's thing, a belief read as the live state); **the body** (what any
person of any age and livelihood holds: one eats, a fire cooks and warms, people are born and die). A line of this world's lore
fails all three and is seeded (§5) or learnt (§4). wave4 §1.3's table of 50 candidates and their verdicts stands, with rows 6, 41,
42 and 49 changed by departures 8, 3 to 5, 22 and 2.

### 1.2 The core, in full (391 words)

```
How life goes:
1. Each day you plan in the morning and may talk with those here; then you work. In the evening you are with those under your
   roof: you talk freely and settle the night.
2. Work is counted in units of about two hours, told each morning: fewer in winter, for the young and the old, and when you are
   hungry, hurt or worn out. Any units you do not use are wasted.
3. Everyone eats each night, from what they carry, then from the stores they may use. Without enough you go hungry, then
   starving, and may die. Hard work, cold and nights out make you need more.
4. A house needs a fire at its hearth each night to cook and keep warm, and far more fuel when it is cold.
5. People are born, grow up, pair, have children, grow old and die. A child must be fed and cared for by someone, or it may die.
6. Land, buildings, herds, stores and what someone made or set are held by claims that others know of. You can reach for
   anything, but others may see and remember. Taking what is another's is your choice, and theirs to answer.
7. Your household shares its house and store. Its head keeps its standing rules, which may give you chores for units your plan
   leaves. Your own rules and fallback come before the household's; going against the household's is seen. What you set stays as
   you set it until you change it.
8. You know only what you have learnt, by watching, trying and being taught; others know other things. A failed try shows you
   why, as far as you can see. What goes unpractised fades.
9. Each morning you hear what concerned you and what stood out. Each day you look closely at one thing, free, and may spend units
   to look harder.
10. You remember in your own words: a memory you rewrite every few days, lines you keep for good word for word, and notes.
    Nothing else of past days stays with you. What you cannot see, you know as you last saw it.
11. Places lie apart, and only what is carried goes between them.
12. An act names what it acts on. Unnamed, it touches only your own things; another's you must name.
```

**Variants by world setting** (each deterministic, read from the world spec):
- `evening: false`: line 1 ends at "then you work." (as today's evening line is added only when on, `prompt.py:534-539`).
- `children` off: line 5 keeps "People are born, grow up, grow old and die." and drops pairing and the child clause.
- A world with no households (none today): line 7 is dropped.
- A world with `view` other than beliefs: line 10's last sentence is dropped (it states the view model, `view: beliefs`).

| Line | Test | Why told rather than learnt | Steering check (steering §4) |
|---|---|---|---|
| 1 the day | frame | the turn's shape is the engine's | describes the turn: kept |
| 2 units, two hours, wasted | frame | the scenario rule "Any actions you do not use are wasted" (scenario_design §3); D2-275 | kept |
| 3 eating | body, frame | that it happens is the body's; carried then stored is the engine's order | no number: amounts are lore (BS5) |
| 4 fire | body | known to every person of the time; the figures are lore (BS2, HH6) | |
| 5 birth and death | body | the life cycle frames every aim; care acts exist because a child needs care | |
| 6 what is whose | measurement | a theft must be the agent's choice, knowing it may be seen (Q-80) | |
| 7 the household, chores, settings stand | frame | the book acts every night (D2-274, D2-296); "settings stand" ends re-choosing (F8) | no default named |
| 8 knowing | frame | knowledge differs by person (D2-266); without it the craft lines read as the world's rules for all | "dies unless passed" left to BS8 (departure 9) |
| 9 noticing | frame | attention is a learning channel (§4.5); its free use and its cost are the engine's | |
| 10 memory, beliefs | frame, measurement | what survives a stretch decides what they write; "as you last saw it" is `view: beliefs` | names no horizon: it says what lasts and leaves the horizon to them |
| 11 places apart | frame | goods move only when carried (the graph's physics) | |
| 12 targets | measurement | an act on another's thing made by the engine's default is a bug in the measurement | |

**Deliberately not said:** any season, any food's worth, any fuel figure, that a store keeps food, that the land renews, that
knowledge dies unless taught, any example act or good.

### 1.3 The reply format, in full (202 words)

```
Reply with JSON:
- "why": what you mean to do, and why.
- "actions": the day's acts in order, each {"do": a craft you know or an act, and what it acts on}, as
  {"do": "<example craft>", "at": "<example place>"}<or example tend>. What goes past your units is not done. "for": a person
  or your household, on their behalf.
- "fallback": acts for units your plan leaves, in the order to try them, every day until you change it; [] clears it. Send it
  only to change it.
- "tell": [{"to", "text"}] to one person here, before work; only they hear it. "say": [{"to": "everyone" or a building,
  "text"}] aloud, a unit each.
- "explain": [{"to", "what": a craft}] what you know of a craft (free).
- "offers": [{"to": a person or "anyone", "give", "get"}], as "<n> <good>", "<n> <good> by day <d>" or "work <n> days"; done when
  accepted, both ways or not at all.
- "attend": what or whom you look at closely (free), with "units" to look harder.
- "rule": [a standing rule in your words] to set, change or drop one (free).
- "note": [{"title", "text"}], "pin", "open", "forget": your notes (up to 8).
- "memory", "keep", "drop": only when asked for.
```

**The examples, filled per person** (departure 4; deterministic, so a person's system prompt does not change from day to day unless
what they know changes):
- `<example craft>`: the first technique under the first shape of the person's "What you can do" (§2.3's order: the household's
  livelihood's crafts first) that is not universal and is done at a place they know; else their first universal craft. `<example
  place>`: the first place (parcel or building) they know where it is done (`knowledge.where` over `mind.places`). A youth come of
  age in the run with only universal crafts: `{"do": "firewood", "at": "<the nearest wood they know>"}`.
- `<or example tend>`: `, or {"do": "tend", "thing": "<tag>"}` only when the person has set gear standing at the system prompt's
  build; the tag is their own. Otherwise absent.
- Never the same example for everyone by construction; a household of fishers will share one, which is their own living.

**Fields added, dropped, moved.** Added: `rule` (D2-274), `units` on attend (§4.5). Dropped: `look_up` (departure 22), the offers'
payment-schedule example (`"2 grain every 3 days for 4 times"`: it stays in the agreements' own line where an offer is made, as
wave4 §1.5 has it), the private-message count (said each morning already), the description of "the village" (departure 6).
`overwork` is inserted after `fallback` where the world offers it (as `prompt.py:546-548` now): `- "overwork": 0 to <n>: units to
push on past your day's.` (without "if your plan needs them": the field invites an explicit 0 in 98% of replies, steering §1.6,
and the reason is the agent's).

**The schema.** `actions.items.do` becomes a free string; the enum of 38 verbs (`prompt.py:75`) goes, with the argument union of
§3.1's shapes. `what` stays as an alias of `do` for a shape named first (`{"do": "make", "what": "smoke fish"}`), so old replies and
worlds still run (wave4 §5.2). `fallback` keeps the actions' item schema. `rule` is `{"type": "array", "items": {"type": "string"}}`.
`attend` becomes `{"type": ["string", "object"]}` with `{"what", "units"}`. Validity is the resolver's (D4-95 refusals), not the
schema's.

### 1.4 The fixed lines around the turn

These are the engine's frame too, the same for everyone, in the turn prompt rather than the system prompt.

| Where | Line now | Becomes | Source |
|---|---|---|---|
| morning closing (`view.py:222`, `prompt.py:816`) | "Plan your day. Reply with JSON only." | "Decide what to do. Reply with JSON only." | steering F4 |
| evening (`evening.py:90-91`) | `"why": what you make of the day and what you mean to do tomorrow.` | `"why": what you make of the day and what you mean to do.` | steering F3 |
| evening's night list (`evening.py:85-91`) | the acts of the night listed for choosing | prefixed once: "What you set stands: a door stays as you left it, and you sleep at home unless you say otherwise." | steering F8 |
| memory request, append mode (`prompt.py:1006-1008`) | "what happened, what was agreed or promised, who owes what, what you mean to do" | "what you want to remember of them" | steering §4 |
| memory request, rewrite mode (`memory.py`, `keep_change`) | as now | as now (it names no horizon) | steering §4 |
| kept-lines request (`memory.py:136`) | "(at most 25 words)" | "(at most 40 words)"; "When your places are full" as now | D2-266 |
| the morning's fallback line (new, in "## You") | | §1.5 | D2-296 |

### 1.5 The fallback, as a standing setting (D2-296)

D2-296: the household's book gives chores for spare units; a person's own standing fallback comes first. The mechanism (the chore
phase, its order against the fallback: U6's gap G4) is U6's. What a person reads, each morning, in "## You":

| State | The line |
|---|---|
| own fallback set | `Your fallback: <acts, in order>. Yesterday it took <n> units: <what it did, in the day's words>.` |
| no own fallback; a chore from the book applies | `Your chores, from <the household>'s rules (set by <head>): <chore words>. Yesterday they took <n> units: <what was done>. Your own fallback, if you set one, comes first.` |
| neither | `You rested <n> units yesterday.` (only when n > 0; corrected 23 Nov to D2-301: units left are rest, and the morning does not push for a fallback) |
| a chore missed (D2-274: shown) | `Not done yesterday: <chore> (no one had units left).` |

Beside it, the house line already says how many nights of food and fuel the store holds (`prompt.py:582-587`), so the filler is
seen beside the state it ignores (steering F2). The first state's "yesterday" is omitted on day 0.

**What an unset fallback does** is U6's to decide with Zach (steering Q2; listed under Open questions as a cross-reference). This
spec takes U6's default if U6 gives one; until then it renders the third state, which wastes the units and says so each morning
(steering Q2's (b) then (a)).

---

## 2. What each person is shown

### 2.1 The system prompt, in order

Rebuilt when what one knows, holds or may set changes (as now); otherwise the same text each call, so it caches.

| # | Section | Words (est.) | From |
|---|---|---|---|
| 1 | **Who you are**: name, stage, household, place, head; the livelihood line (§2.2) | 30 to 50 | the person, U11's livelihood row and band |
| 2 | **The place**: its text, without the "its people know" list | 15 to 40 | the node |
| 3 | **Your people**: kin, debts and feuds as now (`_kin_lines`) | 40 to 120 | relations |
| 4 | **How life goes**: the core (§1.2) | 391 | fixed |
| 5 | **The rules** (§2.5) | 70 to 160 | the book (U6) |
| 6 | **What you can do** (§2.3) | 150 to 600 | the shapes (§3) and the person's crafts |
| 7 | **Other places, as you know them** (as now, `prompt.py:535-539`, with the carry and weights phrase moved to §2.6) | 0 to 400 | `mind.places` |
| 8 | **Reply** (§1.3) | 202 | fixed, examples filled |

**Gone from the system prompt:** "How life works here" (`prompt.py:500-534`: the food table, fuel values, the hearth's spaces,
labour's costs, fittings' wear, buildings, ownership's powers, knowing, noticing), "What you know how to do" (`KN.crafts_lines`:
"Everyone knows" and the levels), the 38 verbs with every craft's name (`verb_lines`), and the "By trade" phrase. wave4 §1.6's table
of where each part goes stands, with these changes: the labour costs that a world turns on (`work_food`, `over_units`, `step`) are
told in the reply's `overwork` line and in the result lines where they bite ("walking tires" in the travel result, the work's food in
the night's line), not in a rules block; fittings' wear goes to the keeper's holding lines (§5.6) and BS9.

### 2.2 Who you are

```
You are <name>, <stage words>, of <household> in <place>.<head clause> <livelihood line>
```

| Part | Rule |
|---|---|
| stage words | as now (`prompt.py:492`) |
| head clause | " You are its head." / " Its head is <head>." (as now) |
| livelihood line | from U11's row and the person's band: "You live by <livelihood words>" + for an expert ", and you are best at <specialism words>" + for a keeper ", and you keep <holding> at <place>" + a second living ", and by <second words> beside it". A cottager: "You live by work for others and your garden." A youth: "You are learning your household's living" + if apprenticed " from <expert>, at <specialism words>". A child: no line |

Examples: "You live by fishing, and you are best at the weir and its nets, and you keep the weir on the Isel." / "You live by
boiling salt at the spring, and by fishing beside it." The words are the row's (U11 §1), never a list of crafts (today's "By trade:
sowing a field broadcast and reaping a crop" for six people with no fields, wave4 §6.4).

### 2.3 What you can do: crafts under their shapes

One section replaces the crafts list and the verb list (which today repeat each other). Its head line, then one entry per shape the
person has something to do with (§2.4), each with its grammar line (§3.1) and "Yours:" with the techniques the person knows under it.

```
What you can do. Name the craft or the act in "do", and what it acts on:
- <shape> <its arguments>: <its grammar line>. Yours: <craft line>; <craft line>; ...
```

**A craft line, by level** (D2-263; departure 11; the numbers from the craft's row, which U3 writes, at the capital factor and the
1-unit floor of basis §1):

| Level | Shown | Form |
|---|---|---|
| known | inputs (with "up to" a batch where the row has one, D2-247), what it gives, units, place or fitting; the skill word; capability points held; the next point when within reach | `<name> (known, <skill word>: <inputs>, <units>, <where>; gives <output><; points>)` |
| capable | as known, with the class's odds and extra materials (§4.2) | `<name> (capable: <inputs>, <units>, <where>; gives <output>; works about <k> times in <n>, with <x> more <main input>)` |
| rough | inputs as the card has them (amounts included), the place, the odds, and the lessons had, as their short clauses | `<name> (a rough idea: <inputs>, at <where>; works about <k> times in <n>, and takes more; <lesson clauses>)` |
| aware | the name and its source | `<name> (<source>)`: "you have seen Peter at it", "you know the Tanners do it" |
| universal, no inputs | the name; and a season clause where the yield reads one (wave2 §3.4) | `firewood`; `cut withies (best in winter)` |
| universal, with inputs | as known | `a fire ring (known: ...)` |

- **Odds in words** (from §4.2's chance): 0.95 and up "nearly always"; 0.75 to 0.95 "about 4 times in 5"; 0.6 to 0.75 "about 2 times
  in 3"; 0.45 to 0.6 "about 1 time in 2"; 0.25 to 0.45 "about 1 time in 3"; under 0.25 "seldom". Extra materials as "<x> more"
  where x is the class's multiplier less 1 in words ("a fifth more", "half as much again", "nearly twice").
- **Lessons** as short clauses, each the lesson row's `short` field, the ones had; at rough also the next not had as "you have not
  yet <short form>" (trying_and_learning §3): "soak the rods; you have not yet got the throat right".
- **Skill words** as now (`SKILL_WORDS`: novice, competent, skilled, master), by the share of the craft's own range (§4.2).
- **Capability points**: those held as a clause ("a timber section only you can set"); the next one as "with more practice: <what
  it opens>" only when skill is within a quarter of the range below its threshold (wave4 §2.2), so it reads as within reach, not a
  menu.
- **Modifiers** (the hunt's range, build's how) on the line of the technique they modify, only at rough or above (as `MOD.lines`).
- **Processing** (U4): the loading face shows the container it loads and the process's nights from the container row: `smoke fish
  (capable: fish hung at about 30 kg a unit on smoke racks; a keeping smoke of 1 night gives smoked fish; works about 4 times in 5)`
  (hanging basis §3; nights D2-284).
- **Set gear** (U2) shows what one holds and has standing: `wicker traps (known: up to 6 a set from your hands, 1 unit; you carry
  6; yours stand in the Isel, T7)`.
- **The order inside a shape:** the household's livelihoods' crafts first (core, then second), by level (known, capable, rough,
  aware), then universal ones. A fisher reads traps before firewood, the opposite of today (wave4 §2.2).

**Universal crafts.** A field on the craft's row, `universal: {stages: [youth, adult, elder]}`, replaces `basic` as the mark of
what every person of the time can do (livelihood_archetypes.md's "keep basic" group, about 35: firewood, fell, cut young growth,
gather wild food, fish by hand, care for a child, herd, fence, gates, dung, repair, clear for building, a small room, beds, a camp, a
fire ring, a crude tool, a crude weapon, bury, burn a carcass, a cairn, dry meat at a fire,
boil acorns, slaughter, tallow lights, clappers, a horn, pest work, guard a field, shut the hens, bins, a hearth loaf). The four
livelihood_archetypes left open (slaughter, drying meat, a hearth loaf, fishing by hand) are universal here (wave4's default; 37.4's
question 1 there). A universal craft is shown by name under its shape; it needs no record until first used (as `knowledge.tried`
creates one). `basic` stays on the rows for worlds without `acts: shapes`, so they replay.

### 2.4 Shapes by stage and by what one holds

A shape appears only when the person has something to do with it; a technique only when known at aware or above, or universal for
their stage. Children (infant, child) do not act (`world.agents_acting`) and have no prompt; their learning is §4.5.

| Shape | Youth | Adult | Elder | A head adds |
|---|---|---|---|---|
| go | travel, sleep at, come | + a fire on the road | as adult | |
| gather | universal + known | known | known | |
| set, tend | known gear; tend shown when one's own gear stands | as youth | as youth | |
| make | known (skilled crafts no higher than rough) | known | known | |
| work | universal + known | known | known | |
| build | none unless known (an apprentice builder) | universal rooms and fittings + known | as adult | |
| move | take, give, put | + drive (a herd of one's household) | as adult | |
| change | own rules, own fallback, a thing's name, doors and gaps one may set | + who may use a house one may let people into, claims, leave or found a household, part, release a debt | as adult | the household's rules and chores, the heir, the children's work, admit |
| agree | an offer, a lesson | + partner, join a household, try for a child | as adult | |
| force | guard | attack, guard | attack, guard | |

Office verbs, when institutions come, appear only to office holders (verbs.md).

### 2.5 The rules block

D2-274 and D2-279: each person sees their current rules, how to change them, what they can set, and each time something is moved or
drawn by a rule (the turn's and evening's lines, U6). D2-282: `when` on lasting states. In the system prompt:

```
<Household>'s standing rules (<you set them | set by <head>>):
- <each rule, as the engine reads it back (store_rules: "shown back as the engine reads it")>
Chores: <each chore, with who>.            (only when the book has chores, D2-296)
Your own rules: <each, or "none">. Your fallback: <acts, or "none">.
A standing rule says, in your words: where goods go; where something is kept, or how much is held back; what is taken or eaten
first; what is moved, and by whom; a chore, who does it when their plans leave units; with "when" or "if" (a cure is done, a store
is full or has room, a store is under so much, something is seen) and "unless" (someone is starving, it is winter, it is full).
The most specific rule wins, yours before the household's.
```

The grammar paragraph is 79 words, the same for everyone; the rules above it are the book's. A store built for a kind shows its own
droppable rule ("grain to the granary", D2-274). How to manage a house well is not here: it is the head's seeded lines (§5.4), so it
can be passed on or lost (D2-279). The grammar words follow U6's book exactly; if U6 names its verbs differently, U6's words win and
this paragraph is rewritten from them.

### 2.6 Goods and their uses, by familiarity

The food table leaves the core (wave4 §2.5). A good shows its use where it is shown (the carry line, the house's store line, the
craft lines' inputs and outputs) at the depth one knows it:

| One knows | Shown | Example |
|---|---|---|
| a good one's household's livelihood makes or uses (U11's row: `gives`, `needs`) | its use sentence, its food a unit if a food, and how long it keeps in words (§5.1) | "salt fish (keeps about a year in brine; 0.46 a meal, cooked)" |
| a good whose craft one knows at rough or above | its use sentence | "withies (for traps, baskets and hurdles)" |
| any other good | its name | "leather" |

Each good row carries a `uses` sentence (U3's rows for materials, U0's for foods). Familiarity is read from `Mind.know` and the
household's livelihoods. The night's line (as now) names what was eaten and how far it went, so others' foods are learnt by eating
them. The weights phrase (`weights_text`, `prompt.py:481-487`) moves to the carry line in "## You", where the load is shown: "You
carry: 6 fish (5 kg) of the 10 kg you can carry on foot" (basis §5).

### 2.7 One's own things, with their tags (Q-80)

In "## You", one line for one's own and one's household's placed and held things at this place, each with its tag (acts_on_owned_things
§2; U2 supplies the state):

```
Your things here: wicker traps in the Isel (T7: 6, set 2 nights ago, tended yesterday); the household's herd on the Leaze (H3: 4 cows, 1 ox).
```

Another's things one knows of stay in "Here, as you see it" by owner and tag (`_things_lines`), so naming one is a choice.

### 2.8 A head's prompt, rendered (Peter of the Marshes, the remade Eelmouth)

Between the core and the reply. Numbers: from basis.md where it gives them; [U3], [U4], [U7] where that unit's row sets the value
(shown here at wave2's 1/7 figures, as a placeholder); none invented here.

```
You are Peter, a grown man, of the Marshes in Eelmouth. You are its head. You live by fishing, and you are best at the weir and its
nets, and you keep the weir on the Isel.
Eelmouth: a village of 3 households on a terrace above the river.
Your people: [kin, the feud with Oliver over the pig, the 2 timber Gunnild owes]
[the core]
The Marsh household's standing rules (you set them):
- none yet
Your own rules: none. Your fallback: none.
[the grammar paragraph]
What you can do. Name the craft or the act in "do", and what it acts on:
- go {"to": a place or a way, "when"?: morning | nightfall, "on trouble"?: go round | push on | turn back | wait}: travel; "sleep" at a place;
  "come" to a meeting called here.
- gather {"do", "at": a place here}: take from the land and water into your hands. Yours: angle; fish by hand; cut withies (best in
  winter); firewood; cut young growth; gather wild food.
- set {"do": gear you carry, "at": a place, "qty"?}: lay gear from your hands where it catches by night; it stays, yours, until you
  take it up. Yours: wicker traps (known, master: up to 6 a set, 1 unit; you carry 6); a gill net (known: 1 a set, 1 unit; open
  water, overnight).
- tend {"thing"?: a tag, "at"?: a place, "up"?: true}: go back to your gear: take what it caught and set again what was sprung; "up"
  brings it home. Unnamed, all of yours at the place. 1 unit a place.
- make {"do", "qty"?}: goods into goods, from your hands, then stores here you may use; or a lot laid in a container that becomes the
  next good over nights. Yours: a gill net (known, master: 1 cord and 0.1 stone, 4 units, at a house; gives a net) [U3]; mend gear
  (known: a tenth of its materials, a fifth of its units) [U3]; wicker traps (known: up to 2 from 0.45 withies each, 1 unit; soak the
  rods) [U3]; salt fish (known: up to 40 kg of fish and a kilo of salt to four, a unit, in a salting tub) [U4; D2-283]; smoke fish
  (known: hung at about 30 kg a unit on smoke racks; a keeping smoke of 1 night) [U4; D2-284]; dry fish (known: at a hearth) [U4].
- work {"do", "on"?: a thing or a place}: labour on what stays where it is. Yours: mend a weir section (known) [U7]; repair; care for
  a child; bury.
- build {"do", "at", "structure"?: wattle | timber}: its materials at the start, the work over days. Yours: a weir section (known,
  master: [U7's costs by material]; a timber section only you can set); a small room [U7]; bins; a fire ring.
- move {"do": take | give | put, "item", "qty", "from" | "to"}: goods between your hands, stores, people and places, or left in the
  open ("hidden": buried | under brush). Taking from a store not yours is theft.
- change {"thing", "to"}: what you control: Marsh House's door; the weir's gap (shut: its traps take the run passing; open: the run
  goes by); who may sleep or eat at Marsh House; a name for a thing; as head, the household's rules and chores, your heir, the
  children's work.
- agree {"with", "do"}: what both must choose: an offer accepted, a lesson (teach or learn, the same day, 2 units each), partnering
  or parting, taking someone into your household or asking to join one, trying for a child.
- force {"do": attack | guard, "target"?, "aim"?: rob | hurt, "at"?}: settled tonight.
[the reply, its example {"do": "wicker traps", "at": "the Isel"}]
```

Note the `on trouble` enum: steering §1.5 found "push on", listed first, taken in 80% of travels. Rotating the order per person is
untested and changes the schema per person (steering Q5); this spec lists the choices alphabetically for everyone (go round, push
on, turn back, wait), so the order is the alphabet's and not the old default's, as the cheapest neutral step, and leaves rotation
untried. Whether the order mattered at all is untested (steering §1.5: low to medium).

### 2.9 Sizes (estimates)

Words counted on this spec's texts (core 391, reply 202, grammar paragraph 79, shapes' grammar lines about 230); the rest estimated
from wave4 §2.7's renders adjusted for the longer core and the eleven shapes.

| Person | Header, people, rules | What you can do | Core, grammar, reply | **System prompt** | Today | Opening: kept lines (seeded, §5) |
|---|---|---|---|---|---|---|
| a youth come of age in the run (Haiku) | about 150 | about 180 | about 670 | **about 1,000** | 4,944 (Nigel, today) | 0 to 4 passed lines |
| a broad adult (Haiku) | about 220 | about 290 | about 670 | **about 1,180** | 4,937 | 14 to 18, about 530 to 680 words |
| a capable adult or expert (Sonnet, Opus) | about 210 | about 520 | about 670 | **about 1,400** | 5,042 | 15 to 20, 570 to 800 |
| a head and expert (Opus) | about 280 | about 520 | about 670 | **about 1,470** | 5,100 | 19 to 20, 720 to 800 |

A smith, a builder or a miller runs to about 1,700 (build's costs are long). So the cost moves from text told to all into each
person's own lines, as Q-81's Risks 3 expected; a founder head's first call of a stretch is about 1,470 + 800 + their memory
(450 to 570), against today's 5,100 + 600 to 1,000. Measured in the first runs, not assumed.

---

## 3. Acting: eleven shapes (the proposal to the verb list, Q-27)

### 3.1 The shapes

A shape is what an act takes, what it costs, how long it runs and what kind of change it makes (verb_grammar §1). A new shape only
when an act has one the others cannot express; everything else is a technique, a setting or a target (verbs.md's rules against
swelling, kept).

| Shape | Takes | Cost | Runs | Changes | Its techniques and faces (examples) | Its grammar line |
|---|---|---|---|---|---|---|
| **go** | a place or a way; when; on trouble | the day's travel | a day or more | where one is and sleeps | travel, sleep at, come to a meeting, a fire on the road | travel; "sleep" at a place; "come" to a meeting called here |
| **gather** | a technique; a place here | the technique's units | one act | a stock to hands | firewood, fell, cut, hay, wild food, fish by hand, the edge, a line, angle, hunt, stalk, drive (with a party), den work, fowling, mine, quarry, cut withies, twist cord, peel bark | take from the land and water into your hands |
| **set** | gear in hand (by technique); a place; how many | 1 unit a set act (basis §6: up to about 6 traps) | over nights, until taken up | gear from hands to a placed thing, tagged, one's own | wicker traps, snares, a gill net, a set line, a fowling net set | lay gear from your hands where it catches by night; it stays, yours, until you take it up |
| **tend** | a thing (tag or known name), or a technique and place; up | 1 unit a place | one act | the catch to hands; sprung gear set again; up: gear to hands | tend, lift, check, empty, walk, collect (D2-294); empty the weir's traps | go back to your gear: take what it caught and set again what was sprung; "up" brings it home |
| **make** | a technique; a quantity | the technique's units (the 1-unit floor, basis §1) | one act, or a lot over nights | goods to goods; a lot into a container | every recipe; mend gear; load a container: hang, salt down, lay in pits, sink flax (U4's lots, D2-295) | goods into goods, from your hands, then stores here you may use; or a lot laid in a container that becomes the next good over nights |
| **work** | a technique; a thing or a place that stays put | the technique's units | one act | the state of a fixed or living thing | sow, reap, plough, herd, milk, slaughter, dress a kill, repair, mend a weir section, tend a container's fire (U4), clear the leat, care for a child, bury, guard a field, write and erase on a building | labour on what stays where it is |
| **build** | a technique; a place or building; a structure | materials at the start, work over days | days | a fixed thing at a place | rooms, fittings (racks), works (a weir section, a withy bed, tan pits), upgrades, monuments | its materials at the start, the work over days |
| **move** | goods or a herd; from and to | take 1 unit, the rest free; drive 1 | one act | who or where goods are held | take, give, put, drive; hidden (buried, under brush); take down a done lot (U4) | goods between your hands, stores, people and places |
| **change** | a thing one controls; its setting | free | until changed | a setting | a door, a weir's gap, the mill's hatches, who may use a house (host, grant, revoke), a claim, a name, the heir, the children's work, leaving or founding a household, parting, releasing a debt; one's rules and fallback (the `rule` and `fallback` fields are its free form) | what you control |
| **agree** | a person; what both choose | each side's units (a lesson 2, as now) | today | what only two can do | an offer accepted, a lesson (teach and learn), partnering, joining and admitting, trying for a child | what both must choose |
| **force** | a person or building and an aim; or a place to guard | 3, or 1 to guard (as now) | settled tonight | harm, theft by force, defence | attack (rob, hurt), guard | settled tonight |

Free reply fields stay outside the shapes (they are not acts on the world): speech (`tell`, `say`, `explain`, a meeting called),
attention (`attend`, with units), memory (`note`, `pin`, `open`, `forget`, `keep`, `drop`), `offers`, `rule`, `fallback`.

**Against Q-27's two options** (keep 38, or fold to 22 to 24): this is a third, eleven, folding further than verbs.md's 24 by
treating its `set` (settings), `invoke` (office powers, later), membership and consent acts as faces of change and agree, and by
splitting none of the work verbs. Each shape is a kind of change on a kind of referent (verbs.md: "verbs partition actions by the kind
of change and the kind of thing changed"); set and tend are separate because they take different referents (gear in hand and a place;
a placed thing). verbs.md's `invoke` comes back as a twelfth shape when offices exist, shown only to holders.

### 3.2 Naming the act

- **The agent names the technique and its target;** the engine knows its shape: `{"do": "wicker traps", "at": "the Isel"}`,
  `{"do": "smoke fish", "qty": 40}`, `{"do": "boil salt"}`.
- **The shape is named only where one technique has two:** set and tend (`{"do": "tend", "thing": "T7"}`), build and work on a weir
  (`build` a section, `work` mend it). Named alone, a technique with two shapes resolves **by what stands** (basis §6; wave3_taking
  §6.3):
  1. one's own gear of that technique stands at the place: **tend** it;
  2. none stands, and one holds the gear: **set** it;
  3. neither: refused, saying where one's gear of it stands, or that one has none and how it is made.

  The result always says which was done and how to ask for the other: "You tended your traps in the Isel (T7): 7 fish. To lay the 6
  traps you carry beside them, set wicker traps." For build and work on a weir: named alone at a weir one holds, it is **work**
  (mending); at a place with no weir of one's own, **build**.
- **A shape named with "what"** (`{"do": "make", "what": "smoke fish"}`) is read the same.
- **Resolution** (`knowledge.resolve` widened): a technique by name, alias or label word, **preferring one the person knows**, then
  a shape or face word; refused with the nearest names the person knows if neither ("You know no craft called 'fish'. Your ways of
  fishing: wicker traps, angle, fish by hand."). The aliases "fish" and "fishing" are removed from fish by hand (`data.py:598`):
  a fisher who knows traps writing "fish" should not get the edge (wave3_taking §6.4 #6).
- **The target** (Q-80, basis §6): by tag or a name the person knows; unnamed, only one's own (a household's things count as every
  member's own, basis §6 default); exactly one there: that; several: a tend takes all of one's own of that technique at the place,
  an act that uses a thing up asks, listing the tags (basis §6, open; U2's resolver); none: refused, saying whose are there. Another's,
  named: done, and the result says it is not one's own ("You took 2 hares from Oliver's snares (T14), which are not yours to take
  from. Whether anyone saw, you will learn."). The refusal and result words are U2's (`u2_taking.md`); this spec only requires them.

### 3.3 How the 38 verbs fold

Nothing is lost: every act today has a shape and a face.

| Verb today (`verbs.py` VERB) | Shape | As | | Verb today | Shape | As |
|---|---|---|---|---|---|---|
| gather | gather; set | worked takes; trap in water, snares, nets to set | | sleep | go | sleep at |
| work | work | | | set (door, gap) | change | a door, a gap |
| make | make | | | travel | go | |
| build | build | | | watch | attend | with 4 units (departure 21) |
| move | move | put | | teach, learn | agree | a lesson |
| take | move; tend | take; from one's own set, tend; from another's, a take named | | attack, guard | force | |
| give | move | give (hidden: buried, under brush) | | fire | go | a fire on the road |
| accept | agree | an offer accepted | | partner | agree | |
| withdraw | the offers field | an offer withdrawn | | part | change | |
| release | change | a debt released | | try | agree | trying for a child |
| host, grant, revoke | change | who may use a house | | name | change | a name, the heir |
| join, admit | agree | joining and admitting | | order | change | the children's work |
| leave_household, found | change | one's household | | meet | say | a meeting called |
| claim | change | a claim | | come | go | to a meeting |
| drive | move | drive | | write, erase | work | on a building or monument |
| | | | | rest | none | an empty plan |

**What changes for the engine.** The registry (`verbs.py` VERB) keeps its handlers; a shape is a table above them (`engine/shapes.py`,
§6) that maps a resolved technique or face to a handler and its arguments. So the 38 handlers stay as code, the agent sees eleven,
and a world without `acts: shapes` keeps the 38 (old worlds replay). The schema's argument union is the shapes' (§1.3).

---

## 4. Learning: one record, five events (D2-267, at lifespan 64)

The engine keeps the knowledge of the hands; the agent writes the lore (wave4 §4.9: what the engine keeps can never be false; what
the agent writes can, and is read for errors). One feature unit (D2-244): `engine/learning.py` holds the record's rules, the classes,
the lessons and the events; `knowledge.py` keeps the views (where, ready, shortfall) and calls it.

### 4.1 The record

```
Mind.know[craft] = {
  level:    aware | rough | capable | known     # how much of the craft one knows: its recipe and steps
  score:    toward the next level (successes and a share of failures, scaled, §4.3)
  lessons:  [lesson ids had, in the craft's order]
  practice: units of the craft, scaled (the curve's x; stored, not inverted from skill, so two-part curves invert cleanly)
  skill:    on the craft's own curve (how well: its yield, waste or quality, by the row's `acts_on`)
  peak:     the best skill held
  points:   [capability points held]
  tries:    {ok, failed}                         # counts, for measurement only
  seen, source, since, practised                 # as now
}
Mind.aptitude = {hands, fire, beasts, water, growing, structure, dealing}     # 0 to 1 each (§4.8)
```

Today's record (`knowledge.py`: level, skill, seen, wins, fails, source, since, practised, peak) gains lessons, points, practice and
the aptitudes; `wins` and `fails` become `tries` and `score`. Level and skill stay separate, as now: one can know the recipe and be
clumsy, or be deft at what one half knows.

### 4.2 Classes and curves, at lifespan 64 (calibrate)

trying_and_learning's tables rescaled from 96 to 64 (tau x 64/96; counts unchanged at 64, scaled elsewhere by §4.3):

| | simple | practised | skilled |
|---|---|---|---|
| chance a try works: aware / rough / capable / known | 0.6 / 0.8 / 0.95 / 1 | 0.35 / 0.55 / 0.8 / 1 | 0.15 / 0.35 / 0.65 / 1 |
| materials: aware / rough / capable / known | 1.3 / 1.15 / 1.05 / 1 | 1.8 / 1.5 / 1.2 / 1 | 2.0 / 1.8 / 1.4 / 1 |
| score to rise: aware→rough / rough→capable / capable→known | 1 / 2 / 2 | 2 / 3 / 4 | 3 / 4 / 4 and the taught lesson |
| known also needs | every lesson had | every lesson had | every lesson, the last only from a teacher |
| default curve shape | shallow | steady (or stepped) | deep |
| tau (units of the craft) | 7 | 17 | 33 |
| skill range | 0.8 to 1.3 | 0.6 to 1.6 | 0.5 to 2.0 |
| practice alone reaches | the top | the top | half the range; beyond only taught or beside a master |

A success scores 1, a failure 1 at aware and 0.5 above (scaled, §4.3). The class is a field on the craft's row; any parameter may be
overridden by the row (U3 writes the rows: wave2 §3.5's table for the new crafts). A real seven-year apprenticeship is about 17 to 25
units at the craft at lifespan 64 (learning_times §1 rescaled; estimate): practice reaches capable in a skilled craft in about 9
tries, and the master's lessons do the rest.

**One formula for the curve shapes** (trying_and_learning §7): `skill = lo + (hi - lo) * [s * (1 - e^(-p / t1)) + (1 - s) * (1 -
e^(-p / t2))]`, capped at the untaught ceiling (a skilled craft's half range) unless taught or beside a master.

| Shape | s | t1 | t2 | Crafts (examples; U3 sets each row) |
|---|---|---|---|---|
| shallow | 1 | tau | | snares, the line, the quern, salting, cord, cutting withies, dressing a kill |
| steady | 1 | tau | | netting, hurdles, smoking, oven bread, spinning, leather work |
| stepped | 0.5 | tau / 3 | tau x 2 | wicker traps (quick to a working trap, long to a tight throat), ploughing |
| deep | 0.2 | tau / 2 | tau x 2 | smelting, smithing, tanning, the weir's timber work |

The hunt keeps its own geometric curve (`SKILL.hard`, `knowledge.py:59-62`) until it is refitted; only its base changes (§4.3).

### 4.3 Scaling with the lifespan (D2-267; departures 17, 18)

Let `s = 64 / lifespan` (the world's, `here.life()["lifespan"]`). **Every learning increment is multiplied by s:** the practice a
unit gives, the score a try or a session gives, a sighting's count, the aptitude a unit feeds. **Every learning share** (teaching's
pull f, §4.6) becomes `1 - (1 - f)^s`. **Every learning time** (fading's wait and rate, §4.3 below; the five days a minded child
needs, §4.5) is divided by s. So a world of lifespan 32 learns twice as fast a unit and a try, one of 200 about a third as fast, and
a person's share of a life spent learning is the same.

**The engine's base re-based once** (audit q8; basis §1 default): `LEARN_BASE = 64` replaces the 32 that `practice_x` reads
(`knowledge.py:80`); the hunt's 32-based constants double so worlds at 64 read exactly as now (`SKILL.top_hard` 50 → 100; `practice_x`
for the hunt then 64/64 = 1 at 64 where it was 32/64 = 0.5 against 50). Trades and basic work, unscaled today, take the class taus
above. `LIFE["lifespan"]`'s default (32, D2-153) is not changed by this spec: that is a life-clock setting U0 owns; learning reads
`LEARN_BASE` whatever it is.

**Fading on the life clock** (D2-273; today on the year clock, `clocks.py:35`; D4-105's rule kept): a craft unpractised for
`fade_after` days starts to fade, by `fade_rate` of what can still be lost each `fade_span` days, never below `fade_keep` (0.6) of
one's best gain over the floor, and comes back `relearn` (3) times faster while below one's best. At lifespan 64: `fade_after` 16
days, `fade_span` 32 days, `fade_rate` 0.5 (D4-105's "half a year" and "a year" at today's 32-day year, so worlds at 64 read as now),
each divided by s elsewhere. Lessons are never lost; a capability point is lost only when skill falls below its threshold less a
tenth of the range.

### 4.4 The five events

Every change to the record comes from one of five events, each through the `learn` primitive (D4-35), so the view and the measurement
see it. All increments scaled by s (§4.3).

| Event | level and score | lessons | skill (practice) | points | aptitude |
|---|---|---|---|---|---|
| **Attend** (free, one a day; or with units, §4.5) | aware of the crafts that make or use the thing seen; a simple craft to rough at once; with units, rough at 3 seen | free: the next lesson the worker has that one lacks; with units, one per 2 units, at most 3 | none | none | none |
| **Try** (an act of a craft at aware, rough or capable) | success +1; failure +1 at aware, +0.5 above | a failure: a true cause, else the next lesson (§4.5's failure lines) | the act's units (a failure counts half) | crossing a threshold opens one | + by the craft's profile |
| **Practise** (the craft done at known) | none | none | the act's units; past the untaught ceiling only beside a master or taught | as try | + |
| **Be taught** (`explain`, free; a lesson session, 2 units each, agree) | explain: aware to rough; a session: +2 | explain: one lesson the explainer has; a session: up to two | a session: toward the teacher's peak (§4.6) | as skill crosses; a taught-only point needs a session | the teacher's dealing + |
| **Fade** (unpractised, §4.3) | none | kept | falls, never below its floor | lost below threshold less a tenth | none |

**Rising:** a level rises when its score reaches the class's mark **and** (for known) every lesson of the row is had, the last of a
skilled craft only from a session (wave4 q5; open). Score resets to 0 on rising. **Beside a master:** the learner works the craft at
the same place on the same day as one whose skill is in the craft's top quarter; the engine checks it from the day's acts, as the
hunt's lead lifts a party now (`lead_hard`).

### 4.5 Every attempt teaches; attention spent in units; children minded at home

**Lessons.** Each craft row carries an ordered list of two to five lessons (U3 writes them: wave2 §3.5, learning_times §5), each
`{id, kind: input | step | place | season | tool, line, short, cause?}`: `line` is the failure sentence, `short` the clause for the
craft line, `cause` an optional state test (a predicate the engine can evaluate: the season out, an input short, the wrong cover,
the fire out). The first lesson is always the main input, so having it is what makes rough.

**A failed try** picks its line (trying_and_learning §3; the senses guide's rule that no line claims a cause the state does not hold):
1. the first lesson whose `cause` holds now: its line, and that lesson marked had ("The rods split: withies cut in summer are
   brittle; cut them in winter.", only if the withies' state holds their cutting season);
2. else the next lesson not had: its line, marked had ("The throat was too wide: an eel went in and out again. Close the cone to a
   finger's width.");
3. else: "You did it as you knew how; your hands are not yet sure of it."

A refusal about the act, not the craft ("teach needs a learner the same day"), is the shape's grammar, said in the refusal (D4-95)
and the shape's line, never a lesson to keep.

**Attention** (Q-81 §4; trying_and_learning §4; the reply's `attend` with `units`):

| Attention | Cost | Gives |
|---|---|---|
| a thing (a trap, a net, a smokehouse, a sack of flour) | free, one a day | the thing in detail next morning (as now); aware of the crafts that make or use it; a simple craft to rough |
| a person at work | free | aware of their craft; the next lesson they hold that one lacks, if they are capable or better |
| a person at work, with units (1 to 4) | the units | 3 sightings at once (rough); a lesson each 2 units (3 at most); they see it ("Nigel watched you at the weir all morning"); no consent needed. Today's `watch` is this at 4 units |
| a finished thing, with units | the units | the making craft's input lesson; a practised craft to rough |
| a place, with units | the units | the place's signs at a lower threshold, by U8's rule (the attention factor in `perceive.chance_of`), and the signs a level opens to those who know the craft (U8's "knows" audiences) |

Hearing a craft named makes one aware only by its own name and aliases, never by common words (crafts_evaluation: "wall", "hunt",
"under brush" made hundreds aware).

**Children minded at home** (wave4 §4.5; open): each night, a child at home becomes aware of each craft its household did at home
that day; a simple craft done at home on five days (divided by s) becomes rough. No lore and no lesson beyond the first unless passed
(`pass` in care, `explain` once they act). So a youth comes of age aware of the household's broad band, as one raised in it, and
knowing none of its lore unless it was passed on.

### 4.6 Teaching from the teacher's peak

A lesson session moves the learner's skill toward the **teacher's lifetime peak** (Zach, 22 Nov, trying_and_learning §6):
`gain = f' * (peak_teacher - skill_learner)`, with `f = 0.25`, times 1.3 when the teacher's present skill is within a tenth of the
range of their peak, times (1 + 0.5 x the teacher's dealing aptitude), then `f' = 1 - (1 - f)^s` (§4.3); applied as the practice that
gives it on the learner's curve. A session also gives up to two lessons and +2 score (scaled). The skilled class's last lesson and
the top half of its curve come only this way or beside a master. The learner never passes the teacher's peak by teaching alone.
Calibrate.

| Class | What one session does (from rough) |
|---|---|
| simple | capable at once; known with a little practice |
| practised | usually capable; known after a second with practice |
| skilled | capable after two; known only with the taught lesson and practice |

### 4.7 Capability points

Discrete, on the skill curve, opening what one can do, never how well (trying_and_learning §7). A row lists its points with a
threshold (a share of the range) and what it opens: a technique, a build option, a sign audience (U8), a teaching power. U3 writes the
lists per craft (wave2 §3.5); examples: a timber weir section (0.6), a tight trap throat (0.5), a hard cure (0.5), heavy leather
(0.6), a keeping cheese (0.6), leading a drive (0.6), casting a pan (0.7), a timber frame (0.5) and a hall (0.8), an upper storey
(0.6); and for any skilled craft, teaching the skilled half (0.75). A point that opens a sign opens an observation only (D2-269: "the
river is rising and coloured after the dry days"), never a direction.

### 4.8 Transfer through underlying skills

Seven aptitudes, each 0 to 1 (departure 25): hands, fire and curing, beasts, water, growing, structure, dealing. Each craft row has a
profile of one to three weights summing to 1 (wave4 §4.8's table by livelihood stands; U3 carries the field for the new rows).
Practice feeds them: `d += units * s * w / 60 * (1 - d)` (60 units of a craft at weight 1 go about two thirds of the way at 64). A
new craft's head start is `h = min(1/3, sum(w_i * d_i))`: its starting skill is `lo + h * (hi - lo)`, and its practice counts
`1 + h` times. Founders' aptitudes are set at generation from their seeded crafts' skills (U11, step 6), so they agree with what the
person already does. Inherited aptitude stays an experiment knob, off. Calibrate.

### 4.9 A worked case: Henry learns the wicker trap (re-derived)

Henry of the Marshes is 5 days old at the start; at lifespan 64 a child is 4 to 12 days old (D2-153's shares), so he comes of age on
day 7, with 4 units a day (`PHYSICS.youth_units`). s = 1. The trap's row is U3's (wave2 §3.2, §3.5: 0.45 withies a trap, 1 unit for
up to 2; practised, stepped; lessons: the rods soaked or green (input), butts and tips turn about (step), the throat to a finger's
width (step)).

- **Days 0 to 6, minded at home:** the household made traps at home on two days and dried fish on six. He is aware of wicker traps
  and set traps; drying fish is simple and done on five days or more: rough. His kept places hold two lines Nichola passed in care.
- **Day 8,** he attends Nichola making traps (free): the next lesson she has that he lacks, the first (the main input): rough. His
  line: `wicker traps (a rough idea: 0.45 withies a trap, up to 2, 1 unit, anywhere; works about 1 time in 2, and takes half as
  much again; soak the rods; you have not yet turned the butts and tips about)`.
- **Day 9,** he tries (practised, rough: 0.55; 1.5 times the withies). It fails; no cause the state holds; the next lesson: "The
  base came out lopsided: lay the stakes butt to tip, turn and turn about." Lesson 2; score 0.5; practice 0.5.
- **Day 10,** fails again: lesson 3, "The throat was too wide: an eel went in and out again. Close the cone to a finger's width."
  Score 1.0; practice 1.0. Skill on the stepped curve (lo 0.6, hi 1.6, t1 = 17/3, t2 = 34): 0.6 + 1.0 x [0.5 x (1 - e^(-1/5.67)) +
  0.5 x (1 - e^(-1/34))] = about 0.70.
- **Day 11,** a session with Nichola (2 units each, agree): score +2, to 3.0, the practised mark for capable; he has every lesson, so
  known waits only on score (4 more). Her peak, as a capable member (U11 §3: the middle of the range), about 1.1, and she is at it:
  f = 0.25 x 1.3 x (1 + 0.5 x 0.2, an estimated dealing) = about 0.36; gain about 0.36 x (1.1 - 0.70) = about 0.14: skill about 0.84.
  His line: `wicker traps (capable: 0.45 withies a trap, up to 2, 1 unit, anywhere; gives wicker traps; works about 4 times in 5,
  with a fifth more withies; soak the rods; butts and tips turn about; the throat to a finger's width)`.

He has spent no kept line on any of it. What he keeps when his next place opens is his own reading of the world. (Estimates: the
dealing aptitude, Nichola's peak; the rest follows §4.2.)

---

## 5. The founders' knowledge: templates, sets and the cap (D2-268, D2-279)

Who gets what, and the matching of a holding to its family's lines, is U11's (`u11_worlds.md` §2 to §4). This section is the lines.

### 5.1 How a line is written

- **A template by hand**, at most 40 words once filled (D2-266), in the person's voice, filled from the engine's state at world build
  where it states a fact (D2-268). Slots are `{name}`; each row lists the state it reads.
- **A condition** drops the line (or a clause, where marked) where it would be false or useless: `[big river]`, `[holds a weir]`,
  `[salt within 2 days]`, `[built: withies]` (a line waiting on another unit). A dropped line is never replaced by a generic one.
- **Tested** (D2-268): each template has a test that renders it on a fixture world and checks each stated figure against the state
  it names (the pattern is `lore.sowing_times`).
- **Band:** B (broad: every working member of a household of that livelihood), C (capable: added for the capable share), and one tag
  per specialism (the expert gets their specialism's lines in full; a capable member who helps that expert the first one or two). Age:
  Y (a youth gets it), A (adults only), E (an elder's extra).
- **No line** states a price, a yield a unit, the best number of traps, a run's date (the cue instead), what lies at an unexplored
  place, or a mechanic of an act (founders_knowledge Part 4.1). A line may give a scale ("about ten fish a trap") and a season, and
  may advise (departure 34).
- **Keeping in words** (Basis row B9-1): every keeping figure is rendered from the keeping curve (D2-289, basis §3) in the world's
  nights by one scale: up to 2.5 nights "a night or two"; up to 5 "a few nights"; up to 10 "about a season"; up to 20 "two seasons";
  up to 28 "most of a year"; up to 40 "about a year"; above 40 "more than a year" (a season is 8 days, a year 32, D2-273). On basis
  §3's order: fresh fish 1.5 "a night or two"; hot smoke 2.4 "a night or two" (audit q3's known consequence); keeping smoke 9.7 "about
  a season"; hard cure 25.5 "most of a year"; salt fish 33.8 "about a year"; dried 41.3 "more than a year".
- **Ids:** two letters and a number (BS base, PE people, HH head, HL a holding's household line, FI fisher, FA farmer, HE herder, HU
  hunter, FO fowler, SA salter, SM smith, MI miller and baker, BU builder, WO woodsman, BA basket maker, CO cord and nets, TA tanner,
  TR trader, CT cottager, NB neighbour). Rows marked Δ differ from wave4's; the reason is in the row.

### 5.2 The budget by role and age, the cap and the drop order

| Role | Base | People | Head (§5.4) | Core livelihood | Specialism and holdings | Household holdings line (HL) | Second livelihood | Neighbours | Lines | Words |
|---|---|---|---|---|---|---|---|---|---|---|
| Head, an expert, prime | 9 | 1 to 2 | 6 to 8 | 2 to 3 B | 2 to 4 | 0 to 1 | 0 to 1 | 0 to 1 | up to 20 | up to 800 |
| Head, not an expert | 9 | 1 to 2 | 6 to 8 | 3 B, 2 C | 0 to 1 | 0 to 1 | 0 to 1 | 0 to 1 | up to 20 | up to 800 |
| Expert, prime | 9 | 1 to 2 | 0 to 2 (partner or heir) | 3 B, 2 C | 3 to 5 | 0 to 1 | 0 to 1 | 1 | up to 20 | up to 800 |
| Expert, elder | 9 + PE3 | 1 | 0 to 2 | 3 B, 2 C | 3 to 5 | 0 to 1 | 0 | 0 | up to 20 | up to 800 |
| Capable adult | 9 | 1 to 2 | 0 to 2 | 3 B, 2 C | 1 (and a keeper line if they keep a holding) | 0 to 1 | 0 to 2 | 1 | 15 to 20 | 570 to 800 |
| Broad adult | 9 | 1 to 2 | 0 to 2 | 3 B | 0 | 0 to 1 | 0 to 2 | 1 | 14 to 20 | 530 to 800 |
| Youth (founder) | 5 (BS1, BS2, BS3, BS5, BS8) | 1 | 0 | 2 Y | 1 if apprenticed | 0 to 1 | 0 | 0 to 1 | 8 to 11 | 300 to 420 |
| Child (founder) | 0 | 0 | 0 | 0 to 2, as if passed by a carer | 0 | 0 | 0 | 0 | 0 to 2 | 0 to 80 |
| Born in the run | none seeded | | | | | | | | what was passed | |

**The cap** (Basis row B9-2; open): 20 seeded lines and about 800 words a founder (lines average about 38 words filled). **Never
dropped by the cap** (protected): a keeper's holding line; the household's holdings line (HL, §5.6: Zach, 22 Nov: a family with a
mill knows the mill); for a head HH1, HH3 and HH7, and for the head's partner or named heir HH1 and HH3 whatever their band (D2-279:
to pass to the heir); PE1; a cultural strand's line. **Dropped in this order** until within the cap, each step taken whole before
the next and stopping as soon as the set fits: (1) neighbour lines beyond one; (2) PE2 (its debt or feud is already in "Your
people", `_kin_lines`); (3) HH5 (the rules block shows the book's defaults); (4) HH8 (core line 7 says chores exist); (5)
capable-band lines a specialism line repeats (FI3 when FI16 is held); (6) the lines of a livelihood in which the person holds only
the broad band, beyond its first, when they hold a deeper band in another (Oliver's fishing beside his salt); (7) BS9, then BS7,
then BS6 (the least specific base lines); (8) the last neighbour line. A set still over the cap after (8) is a gate refusal (U11 §5,
P5: the templates are too long). Worked on the remade Eelmouth and Hollinford (U11 §7, §8): every founder fits by step 8; the heads with
two livelihoods and five neighbours reach step 8.

**Kept places beside the seeded lines** (D2-266; departure 10): seeded lines are ordinary kept lines (D2-268: source "family lore",
"a holding" or "a custom", droppable and passable, never `fixed`), and do not take the places that open each stretch; `come_of_age`
already counts places from the lines held plus one (`memory.py:163-167`). One place opens each stretch (3 days) at 40 words, until
the total of kept lines reaches 30 (Basis row B9-2; open): then a new line needs a drop. A founder with 20 seeded lines gains 10
places, about 30 days; a person born in the run reaches about 21 over a 64-day life, under the total. The source is kept for
measurement, never shown: they are the person's own memories. A person may rewrite a kept line at the cost of its place (Q-81 §3).

**The told-knowledge arm** (D2-266: early testing, not for every experiment): every line of every set, for everyone, in the system
text under "What everyone here knows", instead of seeded. **The depth knob** (D2-268's less-seeded arms; U11 §6): full (this
table), half (base, broad core lines, the keeper lines and the household holdings line; no specialism lines), base (the base set,
the keeper lines and the holdings line), none (no seeded lines; the crafts at their bands' levels only). The holdings' lines stay in
half and base because they read the state the family holds (D2-270's coupling of capital with knowledge); none drops them too, and
is reported as a coupling turned off (U11 §5.1).

### 5.3 The base set and the people lines

| Id | Band, age | Template | Reads | Condition |
|---|---|---|---|---|
| BS1 | all, Y | "The year turns in four seasons of {season_days} days: spring, summer, autumn, winter. Summer days are longest for work, winter's shortest. What land and water give changes each season; one season's emptiness says nothing of the next." | `calendar.season_days` (D2-273's year clock); `PHYSICS.units` by season | |
| BS2 Δ | all, Y | "Winter is the hungry time: {the fields give nothing, }the wild little, a cold night burns about three times the fuel{, and wolves come to the herds}. What a house eats and burns through winter must be in by autumn's end." | the cold night's fuel against a normal night's (D2-290: about 3; departure 16); wolf targets | the fields clause [fields in the village]; the wolves clause [wolves in the region] |
| BS3 Δ | all, Y | "Fresh meat, fish and milk go off in {fresh_keep}, fastest in the hand; grain, beans and nuts keep {grain_keep} kept dry. Dried, smoked or salted, food keeps from about a season to more than a year. Raw food feeds about {raw_share} what cooked does." | the keeping curve in words (§5.1; D2-289) for the fresh foods and grain; U5's outside penalties for "fastest in the hand"; the food rows' raw against cooked | "fastest in the hand" [the hand's outside penalty above the store's, U5]; departure 14 |
| BS4 | all | "A wood, a water or a heath gives less the more it is worked, and comes back when it is rested; game grows wary where it is hunted. Young growth cut comes again; dead wood gathered does not." | the stocks' renewal (year clock); wariness; cut and firewood pools | |
| BS5 | all, Y | "A grown person eats about one food a night, more after a hard day or a night in the cold. A household of {n} wants about {m} food to see a winter through, and more if the frost comes early." | D2-292's food unit; the household's members by stage; winter's nights (8); the cold extra | |
| BS6 | all | "Our household eats from one store and keeps one hearth. Other houses hold their own land, beasts and stores and live by other crafts than ours: what we lack, a neighbour may make, and what they lack, we may." | holdings and claims; the village's livelihoods | [another household in the village] |
| BS7 | all | "Heavy rain raises the rivers and a flood carries off what is set in them; a hard frost kills tender crops; the bear and the wolf come to a kill left lying in the open." | trap wreck by spate and flood (U2); frost loss; carcass targets | each clause [its cause in the world] |
| BS8 | all, Y | "What I know of a craft I got by watching, by trying and failing, and by being taught; a day beside one who knows is worth many tries alone. What I do not teach my children dies with me." | the five events (§4.4); the last clause is the first cultural strand's default, replaced by its variant (§5.7) | |
| BS9 | all | "What is made wears: gear with use, fittings with work, houses with the weather. Mended in time it costs a little; left, it costs the whole." | U3's two lives and mending; fittings' and buildings' wear | |

About 360 words. People and history, from the world's `history` and relations, one each (replacing generate.py's four `memories`,
of which 36 of 45 were the same sentence in the river run, wave4 §2.6):

| Id | Who | Template | Reads |
|---|---|---|---|
| PE1 | every founder | "Our line's founders, {a} and {b} {Line}, came to {village} and built the first {Line} house." / "I came to {village} from {origin} when I married {partner}." | history kind founding; the tree's `origin` |
| PE2 | those in a feud or a debt | "{x} and I came to blows {when} over {what}; it was never settled." / "{x} lent me {q} {item} {when}; I have not paid it back." / "I lent {x} {q} {item} {when}; it is still owed." | history kind feud; the relations' debts and the seeded agreements |
| PE3 | elders, E | "I have seen {k} hard winters, the last {when}: the frost came early and the stores ran out." | history kind winter within the person's life, counted (one line) |

### 5.4 The household head's management lines (D2-279, D2-296)

The ways of managing a household, seeded chiefly to the head, to pass to the heir. Facts and the levers the book offers, never the
policy (what to hold back and how much is the head's to decide).

| Id | Template | Reads | Condition |
|---|---|---|---|
| HH1 | "Our store at {house} holds about {nights} nights' food for the {n} of us as it stands; winter is {winter_nights} nights, and the hungry time is its end and the first days of spring." | the household's stores at the start (`prompt.house_food`); rations by stage (D2-292); the season's length | |
| HH2 | "Next year's {plots} plots want about {seed} of seed. A rule can hold it back from the pot, and say what may be eaten first instead." | `plot_seed` by plots held; the book's `hold back` | [holds fields] |
| HH3 | "Fresh fish and meat go first or go off; what is dried, smoked, salted or in grain keeps. In a hungry spring the keeping food is what is left: eat the soft first, by rule if need be." | the keeping order (basis §3); the book's `first` | |
| HH4 | "Grain on a floor or in sacks draws mice; in bins or a granary fewer, and a cat or an owl hole keeps them down. {store}'s {container} holds about {cap}." | U5's containers: capacity, vermin exposure (D2-279) | [U5 built] |
| HH5 Δ | "What we carry home stays in our hands at night unless we put it away or a rule does; a full store takes no more, and what will not go in lies at the door, where anyone may take it." | the book's defaults (D2-274: no default for putting carried goods away; U6) | departure 29; rewritten from U6's defaults if they differ |
| HH6 Δ | "The hearth burns about a bundle of firewood a night and three on a cold one: a winter wants about {winter_fuel} bundles in by autumn's end. Timber burns longer than firewood." | D2-290 (basis §3); winter's nights and its expected cold nights; the last sentence from the fuel rows (D2-290: revisited with W-76) | departure 16 |
| HH7 | "The household's rules and stores pass to whoever heads it after me. I should name an heir, and tell them where things are kept, and why." | succession (`name` heir) | |
| HH8 (new) | "When the others' plans leave units over, our rules can give them chores: who tends the fire, who hangs the catch, who fetches wood. Each of us may set our own fallback instead, and theirs comes first." | D2-296; U6's chore grammar | departure 30 |

About 300 words. HH2 is dropped for a household with no fields; HH4 waits on U5. HH5 is first to go under the cap after the
neighbours (§5.2).

### 5.5 The livelihoods' sets

Each livelihood's row (fits, bands, specialisms, capital, needs and gives) is U11's (`u11_worlds.md` §1); this section is its lines.
★ marks a line waiting on another unit's build (its condition says which); the condition drops it until built. Each fisher's set and
the others' follow wave4 §3.5's role assignment unless a row says otherwise.

#### 5.5.1 The fisher

| Id | Band, age | Template | Reads | Condition |
|---|---|---|---|---|
| FI1 | B, Y | "The eels go down to the sea in {eel_season}, on dark wet nights, most on the first rain after dry days. The {river} can look empty all summer and still run thick then." | `RUNS.eel` (`wild/kinds.py:873`): seasons, cue `rain_after_dry`, night; the household's water | [eels in the reach] |
| FI2 Δ | B, Y | "One wicker trap takes a few eels on a run night and holds no more than about ten. A house that means to eat from the run sets many before the nights come, and tends every one each morning." | a set trap's hold a night (basis §4: 10 units, D2-297) | "lifts" → "tends" (departure 33) |
| FI3 Δ | B, A | "Fresh fish goes off in {fish_keep} in the hand. Dry it at the hearth, up to {rack_batch} at a time, or salt it the day it is caught, a kilo of salt to four of fish." | the keeping curve in words (§5.1); U4's hearth rack batch; D2-283 | departures 14, 15 |
| FI4 | C; traps and runs | "A spate smashes about half the traps in the water, and a flood nearly all; an otter that finds full traps comes back each night. When the water drops, set again: the run is not over." | U2's wreck shares; `ROB_SETS` | |
| FI5 | C; hand and rod | "In summer the fish lie in the warm shallows and pools, where a hand or a rod takes them. A water fished hard thins in days and comes back when it is rested." | U1's shallows stock and its renewal | [U1 built: the shallows] |
| FI6 Δ | traps and runs | "Salmon come up the {river} after a flood, in {salmon_seasons}, leaping at the shallows. Those that get past go up to spawn, and their young come back as a run {return_words}." | `RUNS.salmon`: seasons, cue `spate`, `return` in words (D2-209 against D2-273 is open, audit q21; the words follow whichever stands) | [a big river with salmon] |
| FI7 | traps and runs | "Lampreys come up in spring when the river runs high after rain: a smaller run, but the first fresh fish of the year." | `RUNS.lamprey` | [lampreys in the river] |
| FI8 ★ | traps and runs, Y if apprenticed | "A trap wants willow rods cut in winter and soaked supple; cut in summer they give a third as much. Make and mend the traps before the runs; the nearest willow is at {willow_place}." | U3's withies and their season (wave2 §2.1); the nearest wet parcel or bank with willow | [built: withies] |
| FI9 | weir and nets | "A weir across the river takes a share of every run that passes, more at the first place than below. With its gap shut through the salmon nights it takes the most now, and leaves fewer to come back." | the weir's sections and position (basis §4); the gap (D2-211); `RUNS.salmon.return` | [a river with runs] |
| FI10 ★ | weir and nets | "A wattle section wants about {wattle_withies} bundles of withies a year, and a spate wears it twice as fast; a timber one lasts longer and costs {timber_section} loads of timber." | U7's weir sections by material and their upkeep; wear by flow | [built: withies] |
| FI11 ★ | weir and nets | "A net of {net_cord} kilo of cord, set overnight in open water, takes fish the traps miss. Mend it before it rots, and bark it once a year: it lasts about {net_life} sets." | U3's gill net: cord, life, mending, barking (wave2 §3.3) | [built: cord] |
| FI12 | weir and nets; the keeper | "Our weir stands {position} on the {river}: {sections} sections of {material}, {wear_words}. {below} lies below it." | the weir's state at the start; the next work downstream | [keeps a weir] (protected) |
| FI13 ★ | hand, rod and dressing | "A rod wants a straight withy and a line of cord, and takes more than a hand line. Bone hooks serve; copper hooks from the smith hold better." | U3's rod, line, bone and copper hooks | [built: withies, cord, bone] |
| FI14 ★ | hand, rod and dressing | "A fish gutted and split the day it is caught dries in the rack; one left whole goes soft. The guts bait the traps." | U3's and U4's dressing the catch; offal as bait (L-145) | [built: dressing, bait] |
| FI15 ★ | hand, rod and dressing | "In a run, a net dipped at the edge takes more than any rod; when the runs are done, a line in the deep water under the bank takes fish at dusk and dawn." | U2's edge, line and open water | [built: the edge and lines] |
| FI16 Δ | keeping | "A hearth's rack dries {rack_batch} at a time over {dry_nights}; a set of smoke racks takes about {set_kg} kilos for a night's keeping smoke; a kilo of salt keeps four of fish." | U4's hearth rack and racks (D2-284, D2-291: 250 kg a set); D2-283 | departure 13: the store clause dropped |
| FI17 Δ | keeping; the keeper | "Our smokehouse on {parcel} holds {sets} set{s} of racks, about {cap} kilos of fish; a keeping smoke takes a night{, a hard cure {hard_nights} more after salting}. Its fire wants tending each night it holds fish{, and a wattle hut can catch and burn}." | the house's racks and material (D2-284, D2-291, D2-271); U4's process nights and fire | [keeps a smokehouse] (protected); the hard-cure clause [timber or stone]; the burn clause [wattle] |
| FI18 Δ | keeping | "Hot-smoked at the hearth, fish keeps {hot_keep}; a night's keeping smoke in a hut keeps it {smoke_keep}; salted, then smoked hard {hard_nights} nights in a timber smokehouse, {hard_keep}." | D2-271, D2-295's goods and their shelf lives in words (§5.1) | [U4 built: the depths] |
| FI19 | keeping | "Salt comes from {salt_place}{, {d} days off}; the salter there wants firewood and grain. {Our dried fish is what the farm houses lack by late winter.}" | the nearest salt pan; roads' days; the neighbours' needs | [salt within 2 days, not in the household]; the second sentence [a farming household within reach] |
| NB-FI | neighbours | "The {Line}s live by the {river}: they know when the eels run, and dry and salt the catch; in late autumn they have fish to spare." | the household's livelihood; `RUNS` | |

By role: broad FI1 to FI3; capable adds FI4 and FI5; traps-and-runs expert FI4, FI6, FI7, FI8; weir-and-nets FI9 to FI12;
hand-and-rod FI5, FI13 to FI15; keeping FI16 to FI19 (FI16 replaces FI3); youths FI1, FI2 (and FI8 or FI9 if apprenticed). A
household whose second living is fishing gets FI1 to FI3 and FI5.

#### 5.5.2 The farmer (arable)

| Id | Band, age | Template | Reads | Condition |
|---|---|---|---|---|
| FA1 | B, Y | The sowing lore, barley: "{barley_lore}" (about 30 words) | `lore.sowing_times` (D4-105, D4-114), split so no cap cuts it | [fields] |
| FA2 | B, Y | The sowing lore, rye and beans: "{rye_beans_lore}" | as FA1 | [fields] |
| FA3 | B | "A plot wants about {plot_seed} of seed, and sown from the best ears of the harvest it bears better. Seed eaten in a hungry spring is next year's harvest gone." | `plot_seed`; seed selection | |
| FA4 | C | "Rye wants a winter in the ground and comes up poor without one; barley and beans are tender, and a hard frost takes what is still growing. Sow nothing into frozen ground." | CROPS needs_winter, hardy; frost loss | |
| FA5 | C; seed and harvest | "Ripe corn will not wait: left standing more than {window} days it sheds and rots, and green ears reaped too soon give only green grain." | farming window, rot, green | |
| FA6 | ploughman | "A crude tool reaps and fells; a copper one from the smith does about twice the work. Oxen and a plough break the ground far faster than a hoe." | tool grades; plough against hoe | |
| FA7 | ploughman; the keeper | "Our oxen plough a plot in {plough_units} where a hoe takes {hoe_units}; they want hay through the winter and the byre in a frost." | the ox pair; plough and hoe units (U7's repricing of works where it applies) | [keeps an ox pair] (protected) |
| FA8 | seed and harvest | "Barley sown after barley tires the ground; beans give it back. Rest a field, or put dung on it, and it bears better." | CROPS takes, restores; fallow, manure | |
| FA9 | seed and harvest; the keeper | "The {field} bore {last_crop} last year and lies {state} now; the {field2} {state2}." | the fields' own state | [holds fields] (protected for the keeper) |
| FA10 | seed and harvest | "Grain ground to meal feeds about half as far again, and bread further; the {mill} grinds for those who bring it grain." | the food rows; the mill's node | [a mill within a day] |
| FA11 | hedge and field | "Woodpigeons come down on the sowing in spring and again in autumn; clappers or a night's watch keep them off. Beasts through an open gate trample a crop by night." | woodpigeon targets; gates; guard a field | |
| NB-FA | neighbours | "The {Line}s sow and reap the big field; they have grain after harvest and want hands at reaping." | | |

#### 5.5.3 The herder or dairy

| Id | Band, age | Template | Reads | Condition |
|---|---|---|---|---|
| HE1 | B, Y | "Hay is cut in summer, and only then; cattle on bare winter grass, or under snow, starve within days without it." | hay season; winter grass; `cattle.starve_nights` | |
| HE2 | B, Y | "Cattle stray through an open gate and wander back to the common; a beast left unherded may be lost on the road." | herds stray; road loss | |
| HE3 | C | "The wolves come to the herd in late winter and early spring; bring the beasts in at dusk and bar the byre." | wolf targets | [wolves in the region] |
| HE4 | C; stock | "Pasture and meadow feed beasts best, fen half as well, heath and moor less; a beast with the murrain must be kept off shared grass." | grazing by cover; diseases | |
| HE5 | dairy | "Milk will not keep past the day it is drawn; {milk_in} of milk with a little salt make a cheese in a cellar, and cheese keeps {cheese_keep}." | milk's shelf life; `cheese` inputs; keeping words | [cheese and a cellar or the means] |
| HE6 | stock | "Without the plough oxen there is no ploughing, and without the bull no calves; meat from them is eaten once." | oxen pull, bulls breed | [holds oxen or a bull] |
| HE7 | stock; the keeper | "Our herd is {cows} cows, {oxen} oxen and {bull}, kept on {pasture}; {calving}." | the herd's state | [holds a herd] (protected) |
| HE8 Δ | hay and winter | "A beast eats about a bundle of hay a night in winter: our {beasts} want about {hay_winter} bundles for the {winter_nights} nights." | hay a beast's day (basis §2: 10 kg); the herd; winter's nights | [holds a herd] |
| NB-HE | | "The {Line}s keep the cattle on the common; they have milk in summer and oxen to lend for the plough." | | |

#### 5.5.4 The hunter and trapper

| Id | Band, age | Template | Reads | Condition |
|---|---|---|---|---|
| HU1 Δ | B, Y | "Snares go on the runs in pasture, meadow, heath and field edges, never in deep wood; a hare snared at night must be taken at first light, before it spoils or another takes it." | snare covers (U2); a snare's catch spoiling and scavenged | "lifted" → "taken" (departure 33) |
| HU2 | B | "Game near home grows wary when it is hunted hard; fresh ground a day or two out gives far more, but one carries home only about ten kilos." | wariness; the carry on foot (basis §5) | |
| HU3 | C | "Deer are fattest in autumn, and the stags roar at dusk in the rut; in spring the hinds have calves and the game is thin." | wild kinds' seasons and body | [deer in the region] |
| HU4 Δ | C | "A kill left lying draws the wolf and, in a hungry spring, the bear: dress it and carry it in the same day. Fresh meat goes off in {meat_keep}; dried or salted it keeps far longer." | carcass targets; meat's keeping in words | departure 14 |
| HU5 | stalking and drives | "Stalking is slow work in wood and heath, downwind and close; a drive wants beaters and spears and is dangerous; one alone with a weapon takes what comes." | stalk, drive, hunt notes | |
| HU6 | stalking and drives | "{far_wood}, {d} days out, holds {game} in autumn; a camp there saves the walk home each night." | the nearest unhunted wood known; its kinds | [a wood within 2 days] |
| HU7 ★ Δ | snares and small game | "Snares want a little cord, or a thong of rawhide that rots on a wet night; a bundle of them goes on a run, and moves when the run goes cold." | U3's snares: a bundle of 25 from cord or hide (wave2 §3.2) | [built: cord] |
| HU8 ★ | dressing the kill | "A kill gives more than meat: the hide, the tallow of a fat beast, and bone; a careful hand takes all of it, a careless one wastes meat. The herders and the tanner want hides." | U3's dressing the kill | [built: dressing] |
| NB-HU | | "The {Line}s go to the woods in autumn and come back with deer; they trade hides and meat." | | |

#### 5.5.5 The fowler

| Id | Band, age | Template | Reads | Condition |
|---|---|---|---|---|
| FO1 ★ | B, Y | "The duck and geese come in autumn, are thickest in winter and leave in spring; they flight at dusk and dawn." | U2's fowl seasons | [built: fowl seasons] |
| FO2 | B | "Woodpigeons flock on the sown fields in spring; the eggs and young of the colonies are there for a few weeks only." | woodpigeon targets; gather young | |
| FO3 ★ | C; freeze and flight | "In a hard freeze the fowl crowd onto the open water that is left, and a net there takes many." | the freeze's crowding (`OPEN_WATER`; D2-265, U1) | [built: the freeze] |
| FO4 ★ | nets and decoys | "A clap net takes far more than hands, and wants about {fowl_net_cord} kilo of cord; cord is twisted from nettles in late summer." | U3's fowling net and cord | [built: cord, fowling net] |
| FO5 ★ | freeze and flight | "Fowl flight along the same lines each dusk and dawn; a net laid across a flight line takes most." | U2's flight lines | [built] |
| NB-FO | | "The {Line}s take duck on the fen in winter; when everything else is thin they have fowl." | | |

#### 5.5.6 The salter

| Id | Band, age | Template | Reads | Condition |
|---|---|---|---|---|
| SA1 Δ | B, Y | "A kilo of salt keeps four of fish or eight of meat for about a year. Every house that kills, fishes or makes cheese needs it, and few can make it." | D2-283; salt fish's keeping in words | departure 15 |
| SA2 | C; the pan | "{pan_fuel} bundles of firewood boil {pan_salt} kilos of salt at the pan; the pan wears through after about {pan_life} boilings and must be mended." | `boil salt` (U3/U7 repriced); the brine pan's wear | [a brine pan] |
| SA3 | the pan | "The pan wants copper, which only the smith makes; our fuel is the wood about us, which thins as we cut it." | the pan's materials; the wood's renewal | |
| SA4 | the pan; the keeper | "The pan at {salt_house} has boiled {uses} times since it was mended." | the pan's wear at the start | [keeps a pan] (protected) |
| SA5 | salting for keeping | "Meat salted in a tub keeps {salt_meat_keep}; salt fish keeps its year only in brine; a cheese takes a little salt and a cellar." | U4's salting and brine (W80-Q9's tub); keeping words | [U4 built: the tub] |
| SA6 | carrying salt | "Salt is heavy only in bulk: one carries about ten kilos a day's walk on foot{, more with a pack basket}; {village} has {surplus} and no salt." | basis §5's carry; the neighbours' needs | [a village within 2 days] |
| SA7 | B, saltmarsh | "The pans on the marsh make salt in the sun; in winter they give little." | the saltmarsh pans' season | [holds saltmarsh] |
| NB-SA | | "The {Line}s boil salt at the spring; they want grain and firewood for it." | | |

#### 5.5.7 The smith and miner

| Id | Band, age | Template | Reads | Condition |
|---|---|---|---|---|
| SM1 | B | "Charcoal burns hotter than timber, and it takes {charcoal_in} loads of timber burnt slow to make one sack of it." | the fuel rows' heat (D2-290: revisited with W-76); `charcoal` inputs (basis §2: 20 kg) | the heat clause from W-76's rows once revisited |
| SM2 | C | "A copper tool does about twice a crude one's work; the plough, the salter's pan and the fisher's hooks all want copper." | tool grades | |
| SM3 | smelting and tools | "Smithing is years at the anvil: tries alone get one only so far, and the rest is taught." | the skilled class (§4.2) | |
| SM4 | smelting; the keeper | "Our forge at {house} has an anvil, a hearth and bellows; it wants charcoal by the sack, and holds {charcoal} now." | the forge's fittings and stock | [keeps a forge] (protected) |
| SM5 | mining and charcoal | "Ore is dug where the rock shows it, at {ore_place}, {d} days off; {ore_in} of ore and {charcoal_per} of charcoal smelt to one copper at the anvil." | rock covers with ore; `smelt` inputs | [ore within 2 days] |
| SM6 | fittings | "{salter}'s pan, {farmer}'s plough share and the fishers' hooks are copper work: those who need them come to us." | the households needing copper in reach | |
| NB-SM | | "The {Line}s work copper at their forge; they make tools and want charcoal and grain." | | |

#### 5.5.8 The miller and baker

| Id | Band, age | Template | Reads | Condition |
|---|---|---|---|---|
| MI1 | B, Y | "Grain ground feeds about half as far again as grain boiled, and bread further still; flour keeps as grain does, bread goes off in {bread_keep}." | food rows; keeping words | |
| MI2 | C | "The farmers bring grain after harvest; the mill is busiest then, idle in spring." | the crop calendar | |
| MI3 | the mill; the keeper | "Our mill grinds up to {batch} at a turn; the leat silts and wants clearing once a year, the stones dressing after about {stones_life} grain. {leat_state}." | the mill's fittings, batch (D2-247's "up to") and wear (D4-105) | [keeps a mill] (protected) |
| MI4 | the mill | "Shut, the hatches hold the river and the wheel turns full; drawn, they let the fish by, and the wheel turns at half." | the mill's gap (D2-246) | [a mill on a run river] |
| MI5 | the oven; the keeper | "The oven bakes up to {oven_batch} loaves from as much flour and {oven_fuel} of fuel, and wants relining after about {oven_life} bakings." | the oven's batch and wear | [keeps an oven] (protected) |
| NB-MI | | "The {Line}s keep the mill; bring them grain after harvest and they grind it." | | |

#### 5.5.9 The builder: wright and mason (household_skills addendum)

| Id | Band, age | Template | Reads | Condition |
|---|---|---|---|---|
| BU1 | B, Y | "Wattle cracks on cold nights and every building falls to ruin unmended: keep timber back for repairs as well as for the fire." | building wear; repair | |
| BU2 | B | "Felling with a tool gives far more than gathering dead wood by hand; a crude tool wants a little stone." | `fell`, `firewood`; `crude tool` | |
| BU3 | C | "A full store spills what is brought in out of the door; {store_caps}." | U5's containers' capacities (D2-279: real) | [U5 built] |
| BU4 ★ | C, both | "One who knows the work raises a room in about half the days a neighbour takes, and it stands longer; a room thrown up wears faster." | U7's builders (G7) | [built: builders] |
| BU5 ★ | wright | "Timber felled in winter and seasoned before it is worked splits less and lasts longer; green timber warps in the frame." | W-76's seasoning | [built: seasoning] |
| BU6 | wright | "The mill's wheel, the plough's frame and the handcart are a wright's work; {who} need them." | the households holding or wanting them | |
| BU7 | mason | "Stone lies only where the rock shows, at {rock_place}, {d} days off; quarrying wants a tool." | rock covers; `quarry` | [rock within 2 days] |
| BU8 | mason | "A hearth wants {hearth_stone} stones and an oven {oven_stone}; stone walls outlast wattle many times over, and want their footings on dry ground." | blueprints (U7's costs, basis §2: 25 kg stones) | |
| NB-BU | | "The {Line}s build: a frame, a wheel or a hearth is their work." | | |

#### 5.5.10 The woodsman

| Id | Band, age | Template | Reads | Condition |
|---|---|---|---|---|
| WO1 | B, Y | "Young growth in {wood} cut comes again in a few years; the dead wood once gathered is gone." | forest renewal | |
| WO2 | C; charcoal | "{charcoal_in} loads of timber burnt slow in the wood make a sack of charcoal; the smith and the salter want it, and little else does." | `charcoal`; buyers in reach | |
| WO3 ★ | charcoal | "A burn takes {burn_nights} of watching; left, it flares to ash." | the burn as a process (U4 or W-76) | [built: the burn as a process] |
| WO4 ★ | coppice | "A coppice cut over every {cycle} years gives poles and withies again; the standards left to grow give timber for building." | W-76's coppice | [built: coppice] |
| WO5 | B | "{buyer} at {place} burns more than they cut: they take firewood and charcoal for grain." | the fuel-hungry households in reach | [a buyer within 2 days] |
| NB-WO | | "The {Line}s work the wood; they have charcoal and poles, and firewood in winter." | | |

#### 5.5.11 The basket maker (withies) ★

| Id | Band, age | Template | Reads | Condition |
|---|---|---|---|---|
| BA1 | B, Y | "Willow rods are cut in winter when the sap is down; cut in summer they give a third and harm the stools." | U3's withies by season | [built: withies] |
| BA2 | B | "Hurdles of withies fold beasts and fence a garden, and are lighter to move than posts and rails." | U3's hurdle | [built] |
| BA3 | C; traps and creels | "A creel carries the catch on the back; a pack basket carries about twenty-five kilos where hands carry ten." | basis §5 (creel +5, pack basket 25 in all) | [built] |
| BA4 | the withy bed | "A withy bed takes three years to bear and then gives for thirty, if beasts are kept off it." | the bed's yield by year (D2-264) | [built] |
| BA5 | the withy bed; the keeper | "Our bed by {parcel} is in its {year} year; {fence_words}." | the bed's state | [keeps a bed] (protected) |
| NB-BA | | "The {Line}s cut the willow; they make traps, creels and hurdles for those who need them." | | |

#### 5.5.12 Cord and nets ★

| Id | Band, age | Template | Reads | Condition |
|---|---|---|---|---|
| CO1 Δ | B, Y | "Nettles twisted in late summer make cord enough for snares and lines; it is slow work, a kilo in about {cord_days} days." | U3's twist cord rate (wave2: about 0.04 kg a unit) and season | [built: cord] |
| CO2 | C | "A close of flax gives the cord a whole fishing village needs; it takes ground and dung from the grain." | U3's flax (W2-2 open) | [built: flax] |
| CO3 | flax and linen | "Retted in the river, flax fouls the water {foul_nights} for the fishers below; retted on the grass or in a pit, it fouls nothing." | U10's pollution from retting (G3) | [built: pollution] |
| CO4 | flax and linen | "Retted flax is dressed and spun in winter, when other work is thin; about {flax_in} of it make a kilo of cord." | U3's dress and spin | [built] |
| CO5 | nets | "A net wants about {net_cord} kilo of cord and many evenings' knotting; the fishers and fowlers need one every few years." | U3's nets and their lives | [built] |
| NB-CO | | "The {Line}s grow flax and twist cord; fishers and fowlers get their nets from them." | | |

#### 5.5.13 The tanner (D2-270, D2-281)

| Id | Band, age | Template | Reads | Condition |
|---|---|---|---|---|
| TA1 | B, Y | "Hides come in autumn, from the hunters and the slaughter; a hide left raw and wet rots in {hide_keep}, dried or salted it waits." | U3's hide keeping; slaughter season | |
| TA2 | C | "Oak bark is stripped in spring, when the sap rises, and kept dry; bark left in the rain gives little." | U3's bark (wave2 §2.5) | [built: bark] |
| TA3 Δ | the pits | "A hide lies in the pits {tan_words}, the liquor weak at first and stronger by stages; a pit wants water and about {bark_in} bundles of bark a hide." | U10's tanning nights (basis §1: 16 to 48) in words | [built: tanning] |
| TA4 | the pits | "Leather makes the pack frame's straps, the harness, the smith's bellows and shoes; raw hide does for a season and rots." | U10's leather uses (D2-281) | [built] |
| TA5 | the pits; the keeper | "Our pits by {parcel} foul the water below them{; the {Line}s fish downstream}." | U10's pollution; the downstream holders | [keeps pits] (protected) |
| NB-TA | | "The {Line}s tan hides in pits by the {water}; they take hides and bark and give leather." | | |

#### 5.5.14 The trader or carrier (D2-270: roads and needs, never prices)

| Id | Band, age | Template | Reads | Condition |
|---|---|---|---|---|
| TR1 | B, one a village | "{village} has {surplus} after {season} and lacks {need}." (up to three villages) | the villages in reach: their livelihoods' gives and needs | [within 2 days] |
| TR2 | C | "A pack ox carries about {ox_carry} kilos where one on foot carries ten, but wants grazing on the way; a handcart carries {cart_carry} on a road with a track and is no use off one." | basis §5 (open: 100 kg, 100 to 150 on a track) | |
| TR3 | the road | "The road to {place} is {days} days {track_words}; {landmark} is a place to stop the night." | roads; landmarks known | |
| TR4 | the market | "Salt, copper and stone are made in few places and wanted in all; grain and fish are scarce everywhere by late winter." | the region's chokepoints | |
| NB-TR | | "{name} of the {Line}s carries between {village} and {village2}; ask them for what is not made here." | | |

#### 5.5.15 The cottager

| Id | Band, age | Template | Reads | Condition |
|---|---|---|---|---|
| CT1 | B, Y | "We hold a cottage and a garden and no field; we live by work for others, for food or coin, and by what the common gives." | holdings | |
| CT2 | B | "The {Line}s want hands at {season_work}, the {Line2}s at {season_work2}; a day's work earns a meal or more." | the neighbours' busy seasons | |
| CT3 | C | "A cow or a pig on the common and a garden of beans see us through when the work fails." | the common's grazing; garden crops | |
| CT4 | C | "In winter, when work is thin, we spin and make baskets for those who will take them." | by-crafts; winter's units | [built: spinning, baskets] |
| NB-CT | | "The {Line}s work for whoever needs hands; they spin in winter." | | |

### 5.6 Holdings' lines: the keeper's and the household's

Zach, 22 Nov: a family given capital has seeded memories related to it. Two kinds of line, both protected under the cap (§5.2):

- **The keeper's line**, one per holding, to its keeper: the livelihood's keeper line (FI12, FI17, FA7, FA9, HE7, SA4, SM4, MI3, MI5,
  BA5, TA5), rendered from the holding's state at the start (its batch, its wear so far, its stock). So the mill in the store and the
  mill in the memory are the same mill (household_skills §2.2).
- **The household's holdings line (HL)**, one per household, to every working founder who is not the keeper of all of them: the
  household's holdings, each with its keeper, then one fact clause per holding while the line stays within 40 words; a household with
  more holdings than fit drops fact clauses, never a holding's name. Template: "We hold {holding, with whose keeping it is}{; ...}.
  {fact clause}{ ...}." A child seeded as if passed by a carer may be given it as one of their two.

| Holding | Name in HL | Fact clause (in order of use) | Reads |
|---|---|---|---|
| a weir | "the weir on the {river}, which {keeper} keeps" | "its traps take the run when its gap is shut" | the weir, its gap, its keeper |
| a smokehouse | "the {name} on {parcel}, which {keeper} keeps" | "it holds about {cap} kilos of fish at a time, and its fire wants tending while fish hang" | racks and capacity (D2-284, D2-291) |
| a salt house and pan | "the Salt House at the {spring}, where {keeper} boils salt" | "the pan wants copper when it wears through" | the pan |
| a mill | "the mill at {parcel}, which {keeper} keeps" | "it grinds the grain the farm houses bring; its stones and leat want care" | the mill |
| an oven | "the oven, where {keeper} bakes" | "it wants fuel at each firing and relining in time" | the oven |
| a forge | "the forge, which {keeper} works" | "it eats charcoal" | the forge |
| a herd | "{count} beasts on {pasture}, which {keeper} herds" | "they want hay in winter and the byre in a frost" | the herd |
| fields | "{fields}, which {keeper} sees to" | "seed must be kept for them" | the fields |
| an ox team | "the ox team and plough" | "they break the ground for us{ and for others who borrow them}" | the team |
| a granary or cellar | "the {store}" | "it keeps {what} from the damp{ and the mice}" | U5's container |
| a withy bed ★ | "the withy bed by {parcel}, which {keeper} cuts" | "it gives rods for traps and baskets{ once it bears}" | the bed's year |
| tan pits ★ | "the pits by {parcel}, which {keeper} works" | "they turn hides to leather over many nights, and foul the water below" | U10's pits |
| a flax close ★ | "the flax close by {parcel}" | "it gives the fibre for cord and nets" | the close |

Example (the remade Marsh household, U11 §7): "We hold the weir on the Isel, which Peter keeps, and the Marsh Smokehouse on Clay
Field, which Nichola keeps. Its traps take the run when its gap is shut; it holds about 250 kilos of fish at a time." (37 words.)

Gear held (traps, nets, a handcart) seeds no holding line; the livelihood's lines cover it (FI2, TR2).

### 5.7 Neighbours, marriages and cultural strands

As household_skills §4 and wave4 §3.6, §3.7: in one village, aware of each other household's broad band, rough in one craft whose
product one's own household uses (keyed draw), and one NB line each (two at most before the cap); a village within a day, the
chokepoint crafts only, aware, with the NB line naming household and place; further, nothing. A spouse who married in brings their
natal household's broad band at the level they left with and up to three of its B lines in their own voice ("At home at {origin} we
..."), within the cap, displacing NB lines first; with chance `marriage_expert` (U11) a capable specialism. Whose origin is outside
the world brings only PE1's married form. founders_knowledge Part 3's twelve strands stand; a strand's line replaces or adds one
base line, counts in the cap and is protected. The first pair to run: BS8 (a) against (c).

---

## 6. Code changes

Owner: 37.4 for the core it holds (named on the merge); 37.2 for content (lines, rows' data, worlds). Lines are today's.

| File | Where | Change | Owner |
|---|---|---|---|
| `engine/prompt.py` | `SCHEMA` 15-54; `schema_for` 68-113 | `do` free; argument union of §3.1; `rule`; `attend` with units; `look_up` dropped (99); `fallback` kept as the setting's form (104); `on trouble` enum alphabetical (76) | 37.4 |
| `engine/prompt.py` | `_craft_note` 128-174, `verb_lines` 198-224, `_build_more` 227-254 | replaced by `shape_lines(here, mind)` and `craft_line(here, mind, tech)` (§2.3, §2.4); build's extra lines only for what one can build | 37.4 (the frame), 37.2 (the words) |
| `engine/prompt.py` | `REPLY_LINES` 257-277 | §1.3, with `reply_examples(here, mind)` filling the examples | 37.4 |
| `engine/prompt.py` | `_labour_lines` 280-311; `system_prompt` 490-550 | system prompt rebuilt to §2.1's order; "How life works here" replaced by `CORE` (§1.2) and its variants; `KN.crafts_lines` call (544) removed; the rules block (§2.5) | 37.4 |
| `engine/prompt.py` | `turn_prompt` 729-817 | the options list (787-796) removed (D2-286); closing line (816); "## You" gains §1.5's fallback line and §2.7's own things | 37.4 |
| `engine/prompt.py` | `_memory_sections` 943-960; `memory_prompt` 1001-1009 | kept lines first; the seeded `memories` list no longer generated for new worlds (U11); append-mode wording (§1.4) | 37.4 |
| `engine/view.py` | `turn` 173-223 | at no place (175-176) render the beliefs view's road form, not `PR.turn_prompt` (D2-286); closing line (222); `_self` 94-108 gains the fallback and own-things lines | 37.4 |
| `engine/evening.py` | 85-91 | the why line and the "settings stand" sentence (§1.4) | 37.4 |
| `engine/memory.py` | `KEPT` 135, `KEPT_ASK` 136-138, `places` 170-187 | `words: 40, schedule: every, every: 3`, `most: 30` total (§5.2); `places` caps the total at `most` counted with seeded lines | 37.4 |
| `engine/learning.py` (new) | | the classes (§4.2), the scale (§4.3), the five events (§4.4), lessons and failure lines (§4.5), teaching (§4.6), points (§4.7), aptitudes (§4.8): one feature unit | 37.4 (core), 37.2 (data) |
| `engine/knowledge.py` | `curve` 41-47, `tau` 55-56, `practice_x` 75-84 | read the class and shape from the row; `practice_x` = s for every craft (`LEARN_BASE` 64) | 37.4 |
| `engine/knowledge.py` | `seed` 88-104 | the new record fields; seeded lessons (all at known, the first at rough); aptitudes from U11 | 37.4 |
| `engine/knowledge.py` | `card` 368-386, `crafts_lines` 389-408, `options` 411-432 | `card` becomes `craft_line`'s source; `crafts_lines` and `options` removed (D2-286) where `acts: shapes` | 37.4 |
| `engine/knowledge.py` | `tried` 448-474, `saw` 477-488 | replaced by `learning.try_event` and `learning.attend_event` | 37.4 |
| `engine/knowledge.py` | `resolve` 24-37 | prefer known techniques; shapes and face words; refusal with the person's own nearest names (§3.2) | 37.4 |
| `engine/shapes.py` (new) | | the eleven shapes over the VERB handlers; the state rule for a technique named alone (§3.2); `acts: shapes` world setting | 37.4 |
| `engine/verbs.py` | `VERB` 18-80 | `watch` (62) resolves to attend with 4 units; `teach`/`learn` (63-64) under agree; `set` (53) under change | 37.4 |
| `engine/data.py` | `TRY` 730, `SKILL` 732-739 | `CLASSES` (§4.2) replacing `TRY`; `SKILL.top_hard` 50 → 100; `LEARN_BASE = 64` | 37.2 (values), 37.4 (shape) |
| `engine/data.py` | `TECHNIQUES` rows | `class`, `curve`, `lessons`, `points`, `profile`, `universal`, `acts_on`; aliases "fish", "fishing" off fish by hand (598) | 37.2 (U3 writes the rows) |
| `engine/data.py` | `PHYSICS.labour` 756-759 | `fade_after` 16, `fade_span` 32 (life days at 64) | 37.2 |
| `engine/clocks.py` | 35 | `fade_rate`, `fade_after` on the life clock | 37.4 (U0's file) |
| `engine/perceive.py` | `evening` 375-513 | attention with units (§4.5): sightings, lessons, the watcher seen; children minded at home | 37.4 |
| `engine/lore.py` | whole | widened to `engine/founders.py` (new): the templates of §5, `render(w, name, role)`, the cap and drop order, the tests' fixtures; `lore.sowing_times` kept and called by FA1, FA2 | 37.2 |
| `engine/run.py` | 1036-1056 | the fallback as a standing setting read from the person's and the book's (U6) | 37.4 (with U6) |
| `tests/` | new | §7 | 37.2 |

---

## 7. Tests

**Unit tests** (each with a fixture world; bots test interfaces only, D2-298):

| Test | Checks |
|---|---|
| `test_core_words` | the core renders 12 lines and its variants by setting; no season, food value, fuel figure or horizon word (a word list: today, tomorrow, winter, season, food values) appears in it or the reply |
| `test_reply_examples` | two persons of different livelihoods get different example crafts; a person with set gear gets their own tag; offers carry placeholders only |
| `test_craft_line_levels` | each level renders D2-263's fields; rough shows the card's inputs; odds words match §4.2 |
| `test_shapes_resolve` | every one of the 38 verbs' acts in a recorded journal resolves to a shape and runs as before (replay of a short run under `acts: shapes` and under the old registry gives the same state) |
| `test_named_alone` | wicker traps named alone: tends when one's own stand, sets when in hand and none stand, refuses otherwise with where one's gear is |
| `test_learning_scale` | at lifespan 32, 64 and 200 a person's share of a life to capable in each class is the same within 5% |
| `test_failure_lines` | a failed try reports a holding cause when the state holds it, else the next lesson, else the hands; never a cause the state lacks |
| `test_teaching_peak` | a session never lifts the learner past the teacher's peak; a teacher at peak teaches faster |
| `test_fade_life_clock` | fading starts after 16 days at 64, 8 at 32; never below the floor |
| `test_templates` | every template renders on its fixture and each figure equals the state it names (D2-268); every filled line is 40 words or fewer; a false condition drops the line, never a stand-in |
| `test_cap_order` | a set over 20 lines drops in §5.2's order and keeps every protected line; over the cap after (8) raises the gate refusal |
| `test_kept_places` | a founder with 20 seeded lines reaches 30 kept lines and no more; a youth born in the run gains one place each stretch |
| `test_minded_child` | a child at home five days beside a simple craft is rough at coming of age, aware of the rest of the household's home crafts, with no lessons |

**What live runs should read** (D2-297, D2-298; scenario_design §6; each against the null arm and with a qualitative end-state
reading): the share of units the fallback does and what it holds by store level (steering §3.3); evening and morning whys' horizon
words; how many kept lines are world knowledge, how many mechanics of acts (founders_knowledge Part 1.2: 13% mechanics today; this
design aims at near none); what is passed in care and whether it is practical; lessons taught, by whom to whom; time to the first run
fished well and to the first false belief, by depth arm; the prompt's length per call by role.

---

## Basis rows needed

| Row | Value | Mark |
|---|---|---|
| **B9-1 Keeping in words** | nights → words: ≤2.5 "a night or two"; ≤5 "a few nights"; ≤10 "about a season"; ≤20 "two seasons"; ≤28 "most of a year"; ≤40 "about a year"; >40 "more than a year" (a season 8 days, a year 32) | default |
| **B9-2 Kept lines** | 40 words a line and one place a stretch (D2-266); seeded lines up to 20 and about 800 words a founder; kept lines in all at most 30 | decided (words, places); default (20 seeded; 30 in all: audit q10) |
| **B9-3 The learning scale** | s = 64 / lifespan on every learning increment; shares as 1 - (1 - f)^s; times divided by s; `LEARN_BASE` 64; the hunt's `top_hard` 100 | decided in rule (D2-267); the base and the form default (audit q8) |
| **B9-4 The classes** | §4.2's table (chances, materials, scores, tau 7, 17, 33, ranges, the untaught ceiling) | calibrate |
| **B9-5 Fading** | after 16 life days at 64, half of what can be lost each 32, never below 0.6 of the best gain, relearnt 3 times faster | default (D4-105 kept; D2-273's clock) |
| **B9-6 Teaching** | f 0.25, x1.3 at peak, x(1 + 0.5 dealing); two lessons and +2 score a session | calibrate |
| **B9-7 Aptitudes** | seven; 60 units at weight 1 to two thirds; head start at most a third | calibrate |
| **B9-8 Attention with units** | 1 to 4 units; 3 sightings at once; a lesson per 2 units, at most 3 | default |
| **B9-9 The core's words** | core 391, reply 202, rules grammar 79 | default (to Zach's question on the core's size) |
| **B9-10 Odds in words** | §2.3's bands | default |

## Gaps

| Gap | State |
|---|---|
| The example act per person (steering Q4) | designed (§1.3) |
| The fallback's words as a standing setting (L-142, D2-296) | designed (§1.5); the mechanism and the unset default are U6's (G4) |
| Lessons that read a state cause (withies' cutting season, a net's rot) | designed as a `cause` predicate on the lesson row (§4.5); each predicate needs the state to hold the fact (U3's goods carry it or the lesson has no cause and falls to rule 2) |
| The shapes over the 38 handlers | designed (§3); waits on Q-27 for adoption; built behind `acts: shapes` |
| The holdings' lines | designed (§5.6): one keeper line a holding, one household line a household; matched by U11 |
| HH4, BU3 (containers), HH5 (the book's defaults), FI16 to FI18 (depths), SA5 (the tub) | wait on U5, U6, U4: each line's condition drops it until built |
| The lines for tanning, retting and pollution (CO3, TA3 to TA5, the pits' HL clause) | wait on U10 (G3) |
| SM1's heat clause | waits on the fuel kinds revisited with the timber economy (D2-290, W-76) |
| FI6's return words | wait on whether the salmon's return is one world year or three (audit q21, D2-209 against D2-273) |
| A sign a capability point opens | U8's audiences; this unit names the points only |
| Inherited aptitude | deferred: an experiment knob, off (trying_and_learning §8) |

## Open questions for Zach

1. **Eleven shapes as the verb list** (the verb list, Q-27). go, gather, set, tend, make, work, build, move, change, agree, force;
   the agent names the technique alone (the shape only for set or tend, build or work on a weir), `do` a free string; the 38 handlers
   kept under them; old worlds keep the 38. Options: (a) adopt the eleven; (b) 37.4's lean 24 with techniques as objects; (c) keep
   the 38. Recommend (a): it carries every act today and every act of taking (wave3_taking §6.4), at about 230 words of grammar
   against 2,844. Blocks: the prompt's "What you can do", the schema, the archetypes build (D2-266, W-70).
2. **The core's lines and size** (knowledge in their own words, Q-81, its question 1). Twelve lines, 391 words, with "units of about
   two hours" and "what you set stays as you set it" added to wave 4's 363; the reply 202. Options: (a) as drafted; (b) cut lines 11
   and 12 into the shapes' grammar (to about 360); (c) wave 4's text without the two additions. Recommend (a). Blocks: the prompt
   build.
3. **Whether the core says that knowledge dies unless it is passed on** (Q-81; wave 4 question 1; audit 18). Options: (a) no: it is
   BS8's last clause and the first cultural strand, varied by world; (b) yes, for everyone. Recommend (a), from your 22 Nov words
   ("These themselves can be experimental parameters to vary as different cultures"). Blocks: the core's text and the first strand
   arm.
4. **How many kept lines a life holds** (audit 10; D2-266, D2-268). Founders seeded up to 20 lines; one place a stretch after.
   Options: (a) additive, no total (founders reach about 40 lines, 1,600 words); (b) seeded lines count against about 20, so founders
   gain few places; (c) additive with a total of about 30. Recommend (c), measured for cost in the first runs. Blocks: the memory
   build, every prompt's length.
5. **Known needs every lesson** (trying and learning, Q-82; wave 4 question 5). The lessons are the content of a level: rough needs
   the main input, known all of them, a skilled craft the taught one. Options: (a) yes; (b) score alone, lessons as explanation only.
   Recommend (a). Blocks: the learning record's rising rule.
6. **Learning scaled with the lifespan in every part, and fading on the life clock** (D2-267; audit 8). s = 64 / lifespan on every
   increment, score included; the base re-based from 32 to 64 so today's worlds read as now; fading moved from the year clock.
   Options: (a) as written; (b) scale practice only, as wave 4 did. Recommend (a): D2-267 says practice and learning. Blocks: the
   learning build.
7. **Whether one who only knows of a craft may try it** (Q-82, trying and learning question 1). Options: (a) every craft at aware, at
   its class's odds and waste; (b) only rows marked tryable untaught (10 today). Recommend (a): a skilled craft tried from hearsay
   wastes about 13 times its materials for a good result, so it teaches but does not pay. Blocks: little; the try rule.
8. **Seven aptitudes, strength left out, a third's head start at most, inherited aptitude off** (wave 4 question 6). Options: (a) yes;
   (b) eight with strength; (c) no transfer. Recommend (a). Blocks: the rows' profiles.
9. **Children minded at home learn what their household does** (wave 4 question 7). Aware of the crafts done at home, rough in a
   simple one done often, no lore unless passed. Options: (a) yes; (b) children learn nothing until they act. Recommend (a): a youth
   raised in a fishing house should know a trap when they see one. Blocks: little.
10. **Whether seeded lore may advise** (audit 19; D2-269). Signs and results only observe (D2-269); a founder's own memory may say
    "salt it the day it is caught". Options: (a) lore may advise, signs and results observe; (b) everything observes. Recommend (a).
    Blocks: the wording of about a dozen lines (FI3, FI4, HE3, HH3, HU4).
11. **What units do while no fallback and no chore is set** (cross-reference: U6's gap G4; steering question 2; L-142). Options: (a)
    they go unused, the morning says how many; (b) each morning asks for one until one is set (as §1.5's third line does); (c) an
    engine default. Recommend (b) then (a); (c) is the engine choosing, which D4-76 rejected. Blocks: U6's chore phase and §1.5's
    lines.

## Sources

`docs/review/37_growth/02zzzh_hunt_fish/wave4_people.md` (all), `wave_conflicts.md` (§1 C5, C6, C14, C15, C17, C18, C27; §2 S6, S14;
§4 E3, E14, E15; §6 questions 8, 9, 10, 18, 19; §7), `founders_knowledge.md`, `household_skills.md` (and its addendum),
`learning_times.md`, `wave2_making.md` §3, `wave3_keeping.md` §2.1, §4, `wave3_taking.md` §0, §2.0, §6, `morning_23nov.md`;
`docs/review/37_growth/02zzzj_steering/steering.md`; proposals `knowledge_in_their_own_words.md`, `trying_and_learning.md`,
`verb_grammar.md`, `acts_on_owned_things.md`, `livelihood_archetypes.md` and `verbs.md` (37.4's); `w73_design/README.md`, `basis.md`;
`docs/scenario_design.md`; `docs/cybertron2/guides/senses.md`; DECISIONS D2-153, D2-244, D2-246, D2-247, D2-263 to D2-298, D4-29,
D4-35, D4-36, D4-61, D4-64, D4-76, D4-78, D4-95, D4-105, D4-114, D4-123; items Q-27, Q-80, Q-81, Q-82, L-141, L-142, W-70, W-78,
W-85. Code read: `cybertron2/engine/prompt.py`, `view.py`, `memory.py`, `knowledge.py`, `lore.py`, `perceive.py` (seed_knowledge,
evening), `life.py` (care_gifts), `verbs.py` (VERB), `data.py` (TRY, SKILL, LIFE, PHYSICS, ITEMS), `clocks.py`, `run.py` (the
fallback), `generate.py`; `cybertron2/specs/nutrition/runs_high.yaml`, `cybertron2/specs/make_nutrition_runs.py`.

*Current as of 22 Nov 2026: D2-263 to D2-298.*
