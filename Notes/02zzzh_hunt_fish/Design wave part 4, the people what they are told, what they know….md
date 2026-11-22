---
id: docs/review/37_growth/02zzzh_hunt_fish/wave4_people.md
kind: note
updated: "2026-11-22"
---
# Design wave part 4, the people: what they are told, what they know, how they learn, how they act

*note · `docs/review/37_growth/02zzzh_hunt_fish/wave4_people.md`*


22 Nov 2026, 37.2 (subagent). A session note for design wave part 4 ([[W-78 Design wave part 4, the people|W-78]]), under the fishing, hunting and materials thread
([[W-73 Fishing, hunting and their materials developed together|W-73]]), designed in full before it is built ([[D2-278 The next wave of the fishing, hunting and materials network|D2-278]]). No code changed; nothing decided. Parts 1 to 3 (the physical basis [[W-77 Design wave part 1, the physical basis|W-77]],
materials and making, taking and keeping) run beside it: this note names their goods, crafts and holdings and leaves their numbers
to them. Where a number appears in a rendered example it is today's engine value or the network's proposal
(proposals/hunt_fish_materials.md), marked as such, to be replaced by theirs.

**Builds on:** knowledge in their own words ([[Q-81 Knowledge in their own words|Q-81]], proposals/knowledge_in_their_own_words.md; answered in part [[D2-266 Knowledge in their own words|D2-266]], [[D2-268 The founders' starting knowledge|D2-268]]),
trying and learning ([[Q-82 Trying and learning|Q-82]], proposals/trying_and_learning.md), the verb grammar (exploration, proposals/verb_grammar.md), acts on
owned things take the thing as their target ([[Q-80 Whether acts on owned things default to one's own|Q-80]], proposals/acts_on_owned_things.md), stores in the book of standing rules
([[D2-274 One book of standing rules per household and per person covers both…|D2-274]], [[D2-279 Stores, as answered|D2-279]], proposals/store_rules.md), the livelihood archetypes and standing rules ([[W-70 Verbs and livelihood archetypes, before the engine rework|W-70]], 37.4's: proposals/livelihood_archetypes.md,
standing_rules.md); decisions [[D2-263 A craft a person knows at capable or known shows, where they look|D2-263]], [[D2-266 Knowledge in their own words|D2-266]] to [[D2-270 Household skills|D2-270]], [[D2-273 Three clocks, each system on one|D2-273]], [[D2-277 Every idea explored in conversation is written down before moving on|D2-277]] to [[D2-279 Stores, as answered|D2-279]]; the research notes founders_knowledge.md,
household_skills.md (with its 22 Nov addendum), crafts_evaluation.md and learning_times.md in this folder. **Code read:**
`cybertron2/engine/prompt.py` (system_prompt, verb_lines, turn_prompt, REPLY_LINES), `knowledge.py` (the record, levels, cards,
crafts_lines, tried, saw), `memory.py` (KEPT, places, seed_line), `perceive.py` (seed_knowledge, customs), `life.py` (care_gifts,
stages), `verbs.py` (VERB: 38 verbs), `data.py` (TECHNIQUES: 132 rows, 94 basic; TRY, SKILL), `world.py` (agents_acting),
`landgen/write.py` (FARMING, TRADES), and the runs world `specs/nutrition/runs_high.yaml`, whose system prompt was rendered for all
eight acting people (scratchpad script; 4,831 to 5,100 words each).

**Ownership:** the prompt, memory, knowledge and verb cores are 37.4's and are named on any merge; the content (lines, livelihoods,
crafts' learning data, worlds) is 37.2's. Under the engine's seams ([[D2-244 The engine's reworking into feature packages|D2-244]]): learning is one feature unit (its record, events,
lines), livelihoods another (rows, templates, the generator's steps), the shapes a third (the registry and resolver).

## The short answer

- **The core told to everyone is twelve lines, 363 words** (§1.4), against 961 words of rules today; with the reply format (192
  words) about 555. Each line passes one of three tests: it is the engine's frame, not the world (the day, units, memory, what one
  sees); without it a run measures confusion rather than society (own by default, stale beliefs); or it is a bodily fact no person
  of any age or livelihood lacks (eating, fire, birth and death). **Everything that is this world's lore, true but learnable or
  losable, is seeded or learnt, not told:** the seasons, keeping, the runs, food values, fuel, wear. That is the experiment.
- **What each person is shown** (§2) is one section, "What you can do", with each of ten shapes followed by the crafts that person
  knows under it at their level (inputs and batch at capable and known, [[D2-263 A craft a person knows at capable or known shows, where they look|D2-263]]; the main input at rough; the name at aware; the
  lessons a try has taught). The crafts list and the verb list, which today repeat each other, become one. Then their household's
  rules and their own, with the rules' grammar ([[D2-274 One book of standing rules per household and per person covers both…|D2-274]], [[D2-279 Stores, as answered|D2-279]]). Kept lines and memory open each stretch as now.
- **Sizes:** a youth come of age in the run about 860 words of system prompt; a broad adult about 1,020; an expert about 1,250; a head who is
  an expert about 1,300 (today 4,830 to 5,100 for every one of them). The opening's kept lines grow instead: a founder expert or
  head starts with 19 or 20 seeded lines (720 to 800 words), a broad founder 14 to 18 (530 to 680), a youth come of age in the run only
  what was passed to them (0 to 4).
- **The founders' knowledge** (§3): a base set of nine lines, the household head's seven management lines ([[D2-279 Stores, as answered|D2-279]]), people and
  history lines from the world's own history, and a set for each of fifteen livelihoods, split by band (broad, capable, each
  specialism) and age, every line a hand-written template with the state it reads and the condition that drops it ([[D2-268 The founders' starting knowledge|D2-268]]). A
  hard cap of 20 seeded lines and about 800 words a founder, with a set drop order. The fisher's set is §3.5.1 in full.
- **Learning is one record and five events** (§4): `Mind.know[craft]` holds level (how much of the craft one knows), lessons
  (which of its steps), skill (how well, continuous, on the craft's own curve), peak, and capability points (what it lets one do);
  `Mind.aptitude` holds seven underlying skills. Attending, trying, practising, being taught and fading each change named fields.
  Failures report a true cause or the next lesson; known needs every lesson; skilled crafts stop halfway up without a teacher or a
  master beside one; teaching pulls the learner toward the teacher's lifetime peak; transfer gives a head start of at most a third.
  Parameters at lifespan 64 ([[D2-267 Practice and learning are set at a 64-day lifespan and scaled with a…|D2-267]]).
- **Acting is ten shapes** (§5): go, gather, set and lift, work, make, build, move (take, give, put, drive), change, agree, force.
  The 38 verbs fold into them; the social acts go into agree (both must choose) and change (what one controls). The agent names
  the technique alone ("snares", "smoke fish"), the shape only where one technique has two (set and lift). The thing is the target;
  unnamed, an act touches only one's own ([[Q-80 Whether acts on owned things default to one's own|Q-80]]).
- **Generation** (§6): fifteen livelihood rows, pin and fill in eleven keyed steps, capital and knowledge filled both ways, the gate
  check extended. Two villages worked end to end: the runs world's Eelmouth remade (three households, three chokepoints, one expert
  each by [[D2-270 Household skills|D2-270]]'s size rule) and Hollinford, a six-household mixed village.
- **Couplings** (§7): 38 goods, crafts and holdings part 4 reads from parts 1 to 3, with the field each template or craft line needs.
- **Open questions** (§8): seven.

---

## 1. The core prompt

### 1.1 What is there now

Rendered for Gunnild of the Shepherds (runs world, high arm, day 0), the system prompt is 4,937 words; the river run's Osric was
5,744 (crafts_evaluation Part 5).

| Section | Gunnild (words) | Osric, river run | Same for everyone? |
|---|---|---|---|
| Who you are, the place | 73 | 383 (with people) | no |
| Your people | 112 | | no |
| How life works here | 961 | 961 | yes, with the food table and fuel numbers read from the engine |
| What you know how to do (73 crafts "Everyone knows", then by level) | 522 | 581 | the first line yes |
| What you can do (38 verbs, their arguments, every known craft's name, build's costs) | 2,844 | 2,890 | mostly |
| Places (Osric only) | | 376 | no |
| Reply format | 425 | 425 | yes |

The 961 words of rules carry a table of 37 foods' values, the fuel values, the hearth's spaces, labour's food cost, four fittings'
wear, and the household's powers. The crafts appear twice: by level in one section, by name under their verb in the next. Things
that matter most to the runs (the seasons, keeping, the runs, what goods are for) are not in it at all ([[Q-81 Knowledge in their own words|Q-81]]).

### 1.2 The test for a core line

A line is told to everyone only if it passes one of three tests:

1. **The frame:** it describes the engine's turn, not the world: when one plans and speaks, what a unit is, what memory one has,
   what one sees and when, how to reply. No one can learn these by living, because living happens inside them.
2. **The measurement:** without it a run measures confusion, not society: an act that silently touches another's things, or a
   belief read as the live state of things.
3. **The body:** a fact every person of any age and livelihood holds and could not forget: one eats, a fire cooks and warms, people
   are born and die. A child grows up seeing it every night.

A line that is **this world's lore** (the seasons, keeping, the runs, food values, fuel, wear, the land renewing) fails all three:
it is true, a person of the time would know it, and it can be learnt or lost. It is seeded to the founders and passed on, or not.
That is the experiment the core must leave open, and the told-knowledge arm ([[D2-266 Knowledge in their own words|D2-266]]) is where it is told instead.

### 1.3 The brainstorm: every candidate line

| # | Candidate | Today | Verdict | Goes to | Why |
|---|---|---|---|---|---|
| 1 | Who you are: name, stage, household, head | system | per person | header | differs by person |
| 2 | Trade ("By trade: sowing ... reaping" for all) | system | per person | header, from the livelihood and specialism | today false for most (02zzy: sowers with no fields) |
| 3 | The place, with "its people know ..." | system | per person | header, the list dropped | the crafts list was where nobody looked for a teacher; neighbour lines replace it (§3.6) |
| 4 | Your people, debts, feuds | system | per person | header | |
| 5 | The day: morning plan, talk, work, evening | rules | **core 1** | | frame |
| 6 | Units by season (7, 6, 5), youth 4, elder 5 | rules | core 2, qualitative | the turn prompt gives today's units | frame; the numbers are told daily |
| 7 | Unused units are wasted | rules | **core 2** | | frame; the scenario rule ("Any actions you do not use are wasted") |
| 8 | Everyone eats each night; the order of drawing | rules | **core 3**; the order to the rules block | rules block | body; the order is the book's default ([[D2-274 One book of standing rules per household and per person covers both…|D2-274]]) and shown there |
| 9 | Hunger, starving, death | rules | **core 3** | | body |
| 10 | Work, cold and nights out raise the need | rules (numbers) | core 3, qualitative | numbers: dropped | body; the night's line shows the cost |
| 11 | The food table, 37 foods' values | rules | out | uses of goods by familiarity (§2.5); base BS3 (raw feeds half); the evening's store in nights | lore; one's own goods' worth is known, others' learnt |
| 12 | What spoils fastest in the hand; a store keeps 3 times better | rules | out | base BS3; the keeping lines; the signs of spoiling | lore, the core of the keeping experiment |
| 13 | Fuel values (firewood, timber, charcoal) | rules | out | base BS2 (cold burns more), the woodsman's and smith's lines, the head's HH7 | lore |
| 14 | A hearth needs fire to cook and warm, more on a cold night | rules (numbers) | **core 4**, qualitative | numbers: HH7 | body |
| 15 | Camp and open fires, sharing a fire | rules | out | the road default in the book (standing_rules §6); the `go` shape's fire | told when one travels |
| 16 | Overwork | rules | reply format, where the world offers it | | frame |
| 17 | Walking tires | rules | out | the travel result says it | learnt on the road |
| 18 | Fittings wear and their mending crafts | rules | out | the keeper's holding lines (§3.5), base BS9, the signs | lore, by who keeps what |
| 19 | Skill fades unpractised | rules | core 8 | | frame of knowing |
| 20 | Buildings are what is in them; a hearth or anvil takes a trade | rules | out | the build shape and the builder's set | lore by livelihood |
| 21 | Repair takes timber | rules | out | base BS9, builder BU1 | lore |
| 22 | What is whose: claims, being seen, theft | rules | **core 6** | | measurement: theft must be a choice the agent knows it makes |
| 23 | The household: members, head, store | rules | **core 7** | | frame of the book of rules ([[D2-274 One book of standing rules per household and per person covers both…|D2-274]]) |
| 24 | Host, grant, join, leave, found, claim | rules | out | the shapes change and agree | grammar, not lore |
| 25 | Knowing how: levels, watching, explained, trying, taught | rules | **core 8**, short | each craft line shows its level | frame |
| 26 | What you notice: the morning, one thing closely | rules | **core 9** | | frame |
| 27 | Attention may be spent in units | new | core 9 | | frame (trying_and_learning §4) |
| 28 | The evening at the hearth | rules | core 1 | | frame |
| 29 | Memory: rewritten, kept for good, notes | reply | **core 10** | | frame: what survives a stretch |
| 30 | What you cannot see is as you last saw it (`view: beliefs`) | turn prompt only | **core 10** | | measurement: "fished out" was a stale belief read as the state |
| 31 | Places lie apart; only what is carried goes between | places line | **core 11** | | frame: no goods move by themselves |
| 32 | Night out costs, carrying limits, weights | places line | out | the turn prompt's carry line and road line | told when it applies |
| 33 | An act names its target; unnamed, only one's own | new | **core 12** | | measurement ([[Q-80 Whether acts on owned things default to one's own|Q-80]]) |
| 34 | Birth, growing up, ageing, death; children need care | life lines | **core 5** | | body |
| 35 | Everyone knows (73 crafts) | crafts | out | universal crafts under their shapes, names only (§2.2) | flattens specialists; 16 never used in nine runs |
| 36 | Crafts by level | crafts | per person | under their shapes with inputs ([[D2-263 A craft a person knows at capable or known shows, where they look|D2-263]]) | |
| 37 | Species one knows | crafts | per person | the hunter's and fowler's sets | |
| 38 | 38 verbs with arguments and notes | verbs | ten shapes, grammar per person | §2, §5 | 2,844 words; 18 to 29 used |
| 39 | Build's rooms, storeys, upgrades, every building's costs | verbs | per person | the builder's build line; others see their known builds | lore of the builder |
| 40 | Modifiers ("ways") | verbs | per person | on the technique line they modify, when known | |
| 41 | Reply format | reply | trimmed (§1.5) | | frame |
| 42 | `look_up` of a craft's card | reply | dropped | the craft line carries the card ([[D2-263 A craft a person knows at capable or known shows, where they look|D2-263]]) | used in 0.1 to 0.8% of replies |
| 43 | The seasons and what they bring | absent | **not core** | base BS1, the livelihoods' lines | lore; the first thing the less-seeded arms test |
| 44 | The land gives less when worked and comes back when rested | absent | not core | base BS4 | lore; "fished out" is what its loss looks like |
| 45 | Children are born knowing nothing; what is not passed on dies | absent | **not core** | base BS8, the first cultural strand | Zach framed it as a starting memory that varies by culture ([[Q-81 Knowledge in their own words|Q-81]] §6); the core says only that one knows what one has learnt (core 8), which is the fact |
| 46 | A scored goal | river run's seeded goal | never | | scenario_design §3; 171 of 481 river kept lines |
| 47 | Aims | generated, not shown ([[D4-29 No aims for now|D4-29]]) | stays unshown | | |
| 48 | Prices, yields, the best plan | absent | never told | | the decisions themselves (founders_knowledge Part 4) |
| 49 | How a set and a lift differ, teach needs learn the same day | refusals | the shapes' grammar (§5) | | frame of acting, not lore |
| 50 | Standing rules' grammar | absent | per person block, same for all | §2.4 | [[D2-279 Stores, as answered|D2-279]]: the system prompt gives the grammar it needs |

### 1.4 The proposed core (363 words)

```
How life goes:
1. Each day you plan in the morning and may talk with those here; then you work. In the evening you are with those under your
   roof: you talk freely and settle the night.
2. Work is counted in units, told each morning: fewer in winter, for the young and the old, and when you are hungry, hurt or worn
   out. Any units you do not use are wasted.
3. Everyone eats each night, from what they carry, then from the stores they may use. Without enough you go hungry, then starving,
   and may die. Hard work, cold and nights out make you need more.
4. A house needs a fire at its hearth each night to cook and keep warm, and far more fuel when it is cold.
5. People are born, grow up, pair, have children, grow old and die. A child must be fed and cared for by someone, or it may die.
6. Land, buildings, herds, stores and what someone made or set are held by claims that others know of. You can reach for anything,
   but others may see and remember. Taking what is another's is your choice, and theirs to answer.
7. Your household shares its house and store; its head sets its standing rules. Your own rules come before the household's, and
   going against the household's is seen.
8. You know only what you have learnt, by watching, trying and being taught; others know other things. A failed try shows you why,
   as far as you can see. What goes unpractised fades.
9. Each morning you hear what concerned you and what stood out. Each day you look closely at one thing, free, and may spend units
   to look harder.
10. You remember in your own words: a memory you rewrite every few days, lines you keep for good word for word, and notes. Nothing
    else of past days stays with you. What you cannot see, you know as you last saw it.
11. Places lie apart, and only what is carried goes between them.
12. An act names what it acts on. Unnamed, it touches only your own things; another's you must name.
```

Line 1 drops its evening clause in a world without the evening (`evening: false`), as today's line is added only when it is on.

| Line | Test | Why told rather than learnt |
|---|---|---|
| 1 the day | frame | the turn's shape is the engine's; it cannot be discovered from inside a turn |
| 2 units, wasted | frame | the scenario rule; without it agents bank units that do not bank |
| 3 eating | body, frame | the night eats by the engine's order; that it happens at all is the body's, that it is from carried then stored goods is the frame |
| 4 fire | body | every person of the time knows it; the numbers are lore (HH7, BS2) |
| 5 birth and death | body | the life cycle frames every aim; that a child needs care is what care acts are for |
| 6 what is whose | measurement | a theft must be the agent's choice (acts_on_owned_things), and knowing one may be seen is what makes it a choice |
| 7 the household | frame | the book of rules acts every night ([[D2-274 One book of standing rules per household and per person covers both…|D2-274]]); people must know it exists and that theirs comes first |
| 8 knowing | frame | knowledge differs by person ([[D2-266 Knowledge in their own words|D2-266]]); without this line the craft lines read as the world's rules for all |
| 9 noticing | frame | attention is the learning channel (§4.5); its cost and its one free use are the engine's |
| 10 memory, beliefs | frame, measurement | what survives a stretch decides what they write; "as you last saw it" is the view model (`view: beliefs`) |
| 11 places apart | frame | no goods move between places unless carried: the graph's physics |
| 12 targets | measurement | [[Q-80 Whether acts on owned things default to one's own|Q-80]]: an act on another's thing made by the engine's default is a bug in the measurement |

What the core deliberately does not say: any season, any food's worth, any fuel figure, that a store keeps food, that the land
renews, that knowledge dies unless taught. Those are seeded (§3) or learnt (§4), and the less-seeded arms ([[D2-268 The founders' starting knowledge|D2-268]]) and the
told-knowledge arm ([[D2-266 Knowledge in their own words|D2-266]]) measure the difference.

### 1.5 The fixed frame around the core

Three more pieces are the same for everyone but sit in the per-person prompt, because they frame what follows them.

**The reply format (192 words):**

```
Reply with JSON:
- "why": what you mean to do today, and why.
- "actions": today's plan in order, each {"do": a craft or an act, and what it acts on}, as {"do": "snares", "at": "the Common"}
  or {"do": "lift", "thing": "T12"}. What goes past your units is not done. "for": a person or your household, on their behalf.
- "fallback": acts for units left over, done in order until your units are used.
- "tell": [{"to", "text"}] to one person here, before work; only they hear it. "say": [{"to": "everyone" or a building, "text"}]
  aloud, a unit each.
- "explain": [{"to", "what": a craft}] what you know of a craft (free).
- "offers": [{"to": a person or "anyone", "give", "get"}], as "2 bread", "1 copper tool by day 10" or "work 2 days"; done when
  accepted, both ways or not at all.
- "attend": what or whom you look at closely (free), with "units" to look harder.
- "rule": [a standing rule in your words] to set, change or drop one (free).
- "note": [{"title", "text"}], "pin", "open", "forget": your notes (up to 8).
- "memory", "keep", "drop": only when asked for.
```

Out of today's 425: `look_up` (the craft line is the card), `open` for crafts, the offers' payment schedule wording (kept in
the agreements' own line where an offer is made), the private message count (told each morning already). In: `rule` ([[D2-274 One book of standing rules per household and per person covers both…|D2-274]]),
`units` on attend (§4.5). The fallback stays a reply field until fallbacks become a standing setting ([[L-142 Fallbacks as a person's standing setting|L-142]]).

**The rules' grammar (about 60 words; §2.4).** **The shapes' grammar** (about 200 words; each shape's one-line description, §2.2),
filled per person with their crafts.

So everyone is told about 820 words the same (core 363, reply 192, rules grammar 60, shapes about 200), against about 1,400 today
(rules 961, reply 425) plus the 73-craft line (about 500) plus the verbs' fixed text.

### 1.6 What leaves today's system prompt, and where it goes

| Today's part (words, Gunnild) | Goes to |
|---|---|
| Rules: the food table (about 350) | goods' uses known by familiarity (§2.5); BS3; the evening's "the store holds about n nights" |
| Rules: fuel and the hearth's numbers (about 130) | core 4 qualitative; BS2; HH7; the woodsman's and smith's lines |
| Rules: work's cost, overwork, walking (about 90) | core 3 qualitative; overwork in the reply where offered; the travel result |
| Rules: fittings' wear (about 70) | the keeper's holding lines; BS9; the fitting's state in the house lines |
| Rules: buildings, what is whose, household powers (about 160) | core 6 and 7; the shapes change and agree |
| Rules: knowing how, noticing, the evening (about 170) | core 1, 8, 9 |
| Crafts: Everyone knows, 73 (about 500) | the universal crafts under their shapes, names only; the rest by livelihood (§3) |
| Crafts: by level (about 100) | under their shapes, with inputs, lessons and points (§2.2) |
| Verbs: 38, with every craft's name and notes (2,844) | ten shapes; each person's crafts under them; modifiers on the crafts they modify; build's costs only for what one can build |
| Reply (425) | the trimmed reply (192) |
| Not there at all: seasons, keeping, runs, renewal, goods' uses | the founders' seeded lines (§3) and the engine-kept lessons (§4) |

---

## 2. What each person is shown

### 2.1 The shape of the per-person prompt

The system prompt, rebuilt when what one knows or holds changes (as now):

1. **Who you are** (about 40 words): name, stage, household and place; the head; the livelihood and specialism ("You live by
   fishing; you are best at the weir and its nets, and you keep the weir on the Isel"), read from the livelihood row and the
   member's band (§3, §6). A cottager: "You live by work for others and your garden."
2. **The place** (about 25): its text, without the "its people know" list.
3. **Your people** (40 to 120): kin, debts and feuds as now.
4. **How life goes:** the core (§1.4).
5. **The rules** (60 to 150): the household's standing rules as they stand, who sets them, one's own, and the grammar (§2.4).
6. **What you can do** (150 to 550): the ten shapes, each with one's crafts under it at one's level (§2.2).
7. **Reply** (§1.5).

The opening of each stretch (the turn prompt, as `_memory_sections` now): **kept for good** (the seeded lines first, then one's
own, word for word), **your memory** (rewritten, or appended for Haiku, [[D4-61 An agent rewrites its one memory each stretch, within a length that…|D4-61]]), the notes' titles. The rest of the turn prompt (now,
yesterday, here, you, offers, agreements, beliefs) is as built, less the options list where a world drops it ([[D4-78 The morning message built from beliefs|D4-78]]).

### 2.2 Crafts under their shapes

One section replaces the crafts list and the verb list. Each shape has its one-line grammar, then "Yours:" and the techniques the
person knows under it. A technique's entry follows [[D2-263 A craft a person knows at capable or known shows, where they look|D2-263]] and its record (§4.1):

| Level | Shown | Example |
|---|---|---|
| known | inputs (with "up to" a batch), what it gives, units, place or fitting, a skill word, capability points held and the next one | dry fish (known, a master's hand: up to 8 fish at a hearth or a fire ring, 1 unit; 3 nights to dried fish) |
| capable | as known, with "works about 4 times in 5" and the extra materials of the class (§4.2) | salt fish (capable: 4 fish and 1 salt, 1 unit, gives 4 salt fish; works about 4 times in 5) |
| rough | the main input and the place, and the lessons had | smoke fish (a rough idea: fish and firewood at smoke racks; you have not yet kept the fire low) |
| aware | the name and where one saw it | a weir section (you have seen Peter at it) |
| universal, no inputs | the name only | firewood; fish by hand; repair |

Numbers in the examples are today's engine rows (`dry fish`, `salt fish`), to be replaced by part 2's.

- **Lessons** show as short clauses: "soaked; you have not yet got the throat right" (trying_and_learning §3). The clause is the
  lesson's own short form, a field of the lesson row.
- **Capability points** show as "a timber section only you can set" when held; the next one as "with more practice: ..." only when
  the person is within a quarter of its threshold, so it reads as something within reach, not a menu.
- **Modifiers** (the hunt's range, build's fine and grand) show on the line of the technique they modify, and only when one knows
  that technique at rough or above.
- **Universal crafts** (about 35, livelihood_archetypes.md): the acts any adult of the time can do (firewood, fell, cut, gather wild
  food, fish by hand, care, bury, repair, a small room, beds, bins, a fire ring, a camp, a pack, a crude tool, slaughter, dry meat at
  a fire, a hearth loaf). Shown as names under their shapes, never as a separate line, and only those the place allows to the
  person's stage. A craft becomes universal by a field on its row, not by being `basic` (the flag that grew from 55 to 94 rows).
- **The order inside a shape:** the household's livelihood's crafts first, then by level, then universal ones. This puts the
  fisher's traps before firewood, the opposite of today.

### 2.3 Shapes by knowledge and stage

A shape appears only when the person has something to do with it; a technique appears under it only when they know it at aware or
above (or it is universal for their stage).

| Shape | Youth | Adult | Elder | Head adds |
|---|---|---|---|---|
| go | travel, sleep at | + come to a meeting, a fire on the road | as adult | |
| gather | universal (firewood, wild food, fish by hand, herd) + known | all known | all known (units fewer) | |
| set and lift | known sets | known sets | known sets | |
| make | known (no skilled crafts above rough) | all known | all known | |
| work | universal + known | all known | all known | |
| build | none unless known (an apprentice builder) | universal rooms and fittings + known | as adult | |
| move | take, give, put | + drive (a herd of one's household) | as adult | |
| change | own rules, a thing's name | + doors and gaps one manages, who may use a house one may let people into, claims, leave or found a household, part | as adult | the household's rules, the heir, the children's work, admit |
| agree | offers, a lesson (as learner or teacher) | + partner, join a household, try for a child | as adult, less trying | |
| force | guard | attack, guard | attack, guard | |

Children (infant and child stages) do not act (`world.agents_acting`), so they have no prompt; what they learn while minded is in
§4.5. Office verbs, when institutions come, appear only to office holders (verbs.md).

### 2.4 The rules block

[[D2-274 One book of standing rules per household and per person covers both…|D2-274]] and [[D2-279 Stores, as answered|D2-279]]: each person sees their current rules, how to change them, what they can set, and each time something is moved
or drawn by a rule (in the turn and evening lines). In the system prompt:

```
The Marsh household's standing rules (you set them):
- what comes in goes to Marsh House; fish to the Marsh Smokehouse
- eat the fresh fish first, then the grain; keep back 20 dried fish for the road
Your own rules: none.
A standing rule says, in your words: where goods go; where something is kept, or how much is held back; what is taken or eaten
first; what is moved, and by whom; with "unless" (someone is starving, it is winter, it is full). The most specific rule wins,
yours before the household's.
```

The rules listed are the book's, rendered from the engine's records as the engine reads them (store_rules: "shown back as the
engine reads it"); a store built for a kind shows its own droppable rule ([[D2-274 One book of standing rules per household and per person covers both…|D2-274]]). How to manage the house is not here: it is the
head's seeded lines (§3.4), so it can be passed on or lost.

### 2.5 Goods and their uses

A good shows its uses where it is shown (the carry line, the house's store line) at the depth one knows it (crafts_evaluation
choice 8): one's own livelihood's goods with their uses and food value ("salt fish, keeps months; 0.46 a meal at a fire"); a good
whose craft one knows at rough or above with its use; any other good by name only. Each good row carries a `uses` sentence and its
crafts (part 1 and 2's rows); familiarity is read from `Mind.know`. This is where the food table goes: a fisher knows what fish is
worth, a farmer what grain is, each learns the other's by eating it (the night's line names what was eaten and how far it went).

### 2.6 Kept lines and memory

- Kept lines ([[D2-266 Knowledge in their own words|D2-266]]): about 40 words, one place opening each stretch (3 days). In `memory.KEPT` terms: `words: 40, schedule:
  every, every: 3, per_lifespan: 3` (about 21 places over a 64-day life). The places opened by care in childhood stay four.
- Seeded lines are ordinary kept lines ([[D2-268 The founders' starting knowledge|D2-268]]): `seed_line` with source "family lore", "a custom" or "a holding", droppable and
  passable, never `fixed`. They do not take the places that open each stretch: `come_of_age` counts places from the seeded lines
  (it already does: start is the lines held plus one). A founder who drops one frees its place.
- The source is kept for measurement and never shown: they are the person's own memories.
- Today's generated memories (founders, hard winters, a feud, a debt) become people and history lines (§3.3): one each, from the
  world's `history` and relations, instead of four lines of which 36 of 45 were the same sentence (river run).
- A person may rewrite a kept line at the cost of its place ([[Q-81 Knowledge in their own words|Q-81]] §3).

### 2.7 Four people, and the sizes

The head's system prompt, Peter of the Marshes in the remade Eelmouth (§6.4), between the core and the reply (numbers: today's
rows or the network's proposal):

```
You are Peter, a grown man of the Marshes in Eelmouth, and its head. You live by fishing; you are best at the weir and its nets,
and you keep the weir on the Isel.
Eelmouth: three houses on a terrace above the Isel; woodland, pasture, meadow, scrub and the fen, where the brine spring is.
Your people: [kin, the feud with Oliver, the 2 timber Gunnild owes him]
[the core]
[the rules block, §2.4]
What you can do (name the craft or the act, and what it acts on):
- go {"to": a place or a way, "when"?: morning | nightfall, "on trouble"?: push on | wait | turn back}: travel (a night out on a
  one-day road unless you go in the morning); also {"do": "sleep", "at"} and {"do": "come"} to a meeting called this morning.
- gather {"what", "at"?}: take from the land. Yours: firewood; cut young growth (a tool helps); cut withies (best in winter); fish by
  hand; angle; gather wild food.
- set {"what", "at"} and lift {"thing"}: gear left where it works by night; lift takes the catch from all your own of it at a place
  and sets it again (1 unit a place). Yours: wicker traps in the water (known; up to 6 a set, about 10 a trap a night at most); a
  fish net (known; open water, overnight); snares (a rough idea).
- make {"what", "qty"?}: inputs into goods, from your hands, then stores here you may use. Yours: a fish net (known, a master's
  hand: 1 cord; 30 units over days; lasts about 70 sets); twist cord (known: nettle in late summer; about 25 units a cord); mend gear
  (known: a tenth of its materials); a wicker trap (capable: 0.4 withies, soaked; 2.5 units; works about 4 times in 5); dry fish
  (known: up to 8 fish at a hearth, 1 unit; 3 nights); salt fish (known: 4 fish and 1 salt, 1 unit); smoke fish (a rough idea: fish
  and firewood at the racks; you have not yet kept the fire low).
- work {"what", "on"?: a thing or a place}: labour on what stays where it is. Yours: mend a weir section (known: about 6 withies a
  section); repair; tend the smoke (capable); care for a child; bury.
- build {"what", "at", "structure"?: wattle | timber}: its materials at the start, then the work over days. Yours: a weir section
  (known, a master's hand: base 4 timber, 2 withies, 8 units; wattle 12 withies, 1 timber, 16 units; timber 10 timber, 25 units; a
  timber section only you can set); a small room (wattle 8 timber, 6 units); bins; smoke racks; a fire ring.
- move: take or give {"item", "qty", "from" | "to"}: goods between your hands, stores, people and places, or left in the open
  ("hidden": buried | under brush). Taking from a store not yours is theft.
- change {"thing", "to"}: what you control: Marsh House's door; the weir's gap (shut: its traps take the run passing; open: the run
  goes by); who may sleep or eat at Marsh House; a name for a thing; as head, your heir and the children's work.
- agree {"with", ...}: what both must choose: an offer accepted, a lesson (teach or learn, the same day, 2 units each), partnering
  or parting, taking someone into your household or asking to join one, trying for a child.
- force {"target", "aim": rob | hurt} or guard {"at"?}: settled tonight.
[the reply]
```

Gunnild (a broad adult, fisher with fowling as the household's second living), Nichola (capable, traps and the runs at rough), and
Henry (a child at the start who comes of age on day 7, standing for those born in the run: no seeded lore, only
what was passed in care) were rendered the same way in the scratchpad and counted:

| Person | Header, people, rules | What you can do | Core and reply | **System prompt** | Today | Opening: kept lines | Opening: own memory (budget) |
|---|---|---|---|---|---|---|---|
| Henry, youth come of age in the run (Haiku) | about 150 | about 150 | 555 | **about 860** | 4,944 (Nigel) | 0 to 4 passed lines, up to 160 words | about 110 words (append mode) |
| Gunnild, broad adult (Haiku) | about 210 | about 260 | 555 | **about 1,020** | 4,937 | 18 seeded, about 680 words | about 110 (append) |
| Nichola, capable (Sonnet); an expert alike | about 200 | about 500 | 555 | **about 1,250** | 5,042 | 19 seeded, about 720 | about 360 to 450 |
| Peter, head and expert (Opus) | about 260 | about 480 | 555 | **about 1,300** | 5,100 | 19 seeded, about 720 | about 450 to 570 |

A smith, a builder or a miller with many fittings runs to about 1,500 (build's costs are long). Per call, a founder head's first
call of a stretch is about 1,300 + 750 + 500 = 2,550 words against today's 5,100 + 600 to 1,000: the cost moves from text told to
all into each person's own lines, as [[Q-81 Knowledge in their own words|Q-81]] §Risks 3 expected. Over a life the own kept lines add up to about 800 more words.

---

## 3. The founders' knowledge

### 3.1 How a line is written

- **A template by hand,** at most 40 words once filled, in the person's voice, filled from the engine's state at world build where
  it states a fact ([[D2-268 The founders' starting knowledge|D2-268]]). Slots are `{name}`; each line lists the state it reads.
- **A condition** drops the line where it would be false or useless: `[big river]`, `[holds a weir]`, `[salt within 2 days]`,
  `[built: withies]` (a line waiting on parts 1 to 3). A dropped line is not replaced by a generic one.
- **Tested:** every template has a test that renders it on a fixture world and checks each stated figure against the state it names
  (the sowing lore's test is the pattern: `lore.sowing_times`).
- **Band:** B (broad: every working member of a household of that livelihood), C (capable: added for the capable share), and one
  tag per specialism (the expert gets their specialism's lines in full; a capable member helping that expert gets the first one or
  two). **Age:** Y (a youth gets it), A (adults only), E (an elder's extra).
- **No line** states a price, a yield a unit, the best number of traps, a run's date (the cue instead), what lies at an unexplored
  place, or a mechanic of an act (founders_knowledge Part 4.1). A line may give a scale (about ten a trap) and a season.
- **The ids** are two letters and a number (BS base, HH head, PE people, FI fisher, FA farmer, HE herder, HU hunter, FO fowler, SA
  salter, SM smith, MI miller and baker, BU builder, WO woodsman, BA basket maker, CO cord and nets, TA tanner, TR trader, CT
  cottager, NB neighbour); the founders_knowledge id each comes from is given.

### 3.2 The budget by role and age

| Role | Base | People and history | Head | Core livelihood | Specialism | Holdings | Second livelihood | Neighbours | Lines | Words |
|---|---|---|---|---|---|---|---|---|---|---|
| Head, an expert, prime | 9 | 1 to 2 | 4 to 5 | 2 to 3 B | 2 to 3 | (in the specialism) | 0 to 1 | 0 to 1 | 19 to 20 | 720 to 800 |
| Head, not an expert | 9 | 1 to 2 | 5 to 7 | 3 B, 2 C | 0 | 0 to 1 | 0 to 1 | 0 to 1 | 19 to 20 | 720 to 800 |
| Expert, prime | 9 | 1 to 2 | 0 to 2 (the head's partner or heir) | 3 B, 2 C | 3 to 4 | (in the specialism) | 0 to 1 | 1 | 19 to 20 | 720 to 800 |
| Expert, elder | 9 + PE3 | 1 | 0 to 2 | 3 B, 2 C | 3 to 4 | (in the specialism) | 0 | 0 | 19 to 20 | 720 to 800 |
| Capable adult | 9 | 1 to 2 | 0 to 2 | 3 B, 2 C | 1 | 0 | 0 to 2 | 1 | 15 to 20 | 570 to 760 |
| Broad adult | 9 | 1 to 2 | 0 to 2 | 3 B | 0 | 0 | 0 to 1 | 1 | 14 to 18 | 530 to 680 |
| Youth (founder) | 5 (BS1, BS2, BS3, BS5, BS8) | 1 | 0 | 2 (Y lines) | 1 if apprenticed | 0 | 0 | 0 to 1 | 8 to 10 | 300 to 380 |
| Child (founder) | 0 | 0 | 0 | 0 to 2, as if passed by a carer | 0 | 0 | 0 | 0 | 0 to 2 | 0 to 80 |
| Born in the run | none seeded | | | | | | | | what was passed | |

**The cap:** 20 seeded lines and about 800 words a founder (lines average about 38 words filled). Over it, drop in this order:
neighbour lines beyond one; HH5 (the book's defaults, which the rules block shows anyway); capable-band lines a specialism repeats;
a second livelihood's lines beyond one; the second people line; the last neighbour line. The head's partner, or the named heir, gets
HH1 and HH3 whatever their band ([[D2-279 Stores, as answered|D2-279]]: to pass to the heir). The told-knowledge arm ([[D2-266 Knowledge in their own words|D2-266]]) gives the same lines, all of them, in the system text for everyone
instead; the depth knob (household_skills §7: full, half, base, none) cuts within this table.

### 3.3 The base set, people and history

| Id | Band, age | Template | Reads | From |
|---|---|---|---|---|
| BS1 | all, Y | "The year turns in four seasons of {season_days} days: spring, summer, autumn, winter. Summer days are longest for work, winter's shortest. What land and water give changes each season; one season's emptiness says nothing of the next." | the calendar's season length ([[D2-273 Three clocks, each system on one|D2-273]]'s year clock); PHYSICS units by season | B1 |
| BS2 | all, Y | "Winter is the hungry time: the fields give nothing, the wild little, a cold night burns {cold_x} times the fuel, and wolves come to the herds. What a house eats and burns through winter must be in by autumn's end." | PHYSICS heat cold against normal; wolf targets; renewal in winter | B2 |
| BS3 | all, Y | "Fresh meat, fish, milk and greens go off within days, fastest in the hand; grain, beans and nuts keep a season in a store. Dried, smoked or salted, they keep for months. Raw food feeds about half what cooked does." | part 1's shelf-life table on the year clock; the stores' keeping ([[D2-279 Stores, as answered|D2-279]]); the food rows' raw values | B3 |
| BS4 | all | "A wood, a water or a heath gives less the more it is worked, and comes back when it is rested; game grows wary where it is hunted. Young growth cut comes again; dead wood gathered does not." | the stocks' renewal; wild wariness; the cut and firewood pools | B4 |
| BS5 | all, Y | "A grown person eats about one food a night, more after a hard day or a night in the cold. A household of {n} wants about {m} meals to see a winter through, and more if the frost comes early." | PHYSICS ration and labour; the household's size; the winter's nights | B5 |
| BS6 | all | "Our household eats from one store and keeps one hearth. Other houses hold their own land, beasts and stores and live by other crafts than ours: what we lack, a neighbour may make, and what they lack, we may." | holdings and claims; the village's livelihoods | B6 |
| BS7 | all | "Heavy rain raises the rivers and a flood carries off what is set in them; a hard frost kills tender crops; the bear and the wolf come to a kill left lying in the open." [drop each clause whose cause the world lacks] | trap wreck by spate and flood; frost loss; carcass targets | B7 |
| BS8 | all, Y | "What I know of a craft I got by watching, by trying and failing, and by being taught; a day beside one who knows is worth many tries alone. What I do not teach my children dies with me." | the knowledge paths; the last clause is the first cultural strand's default (founders_knowledge Part 3), replaced by its variant | B8 |
| BS9 | all | "What is made wears: gear with use, fittings with work, houses with the weather. Mended in time it costs a little; left, it costs the whole." | part 1's gear lives; fittings' wear; buildings' wear; mend gear | new (from the rules' wear line) |

About 350 words. People and history, from the world's `history` and the relations, one each:

| Id | Who | Template | Reads |
|---|---|---|---|
| PE1 | every founder | "Our line's founders, {a} and {b} {Line}, came to {village} and built the first {Line} house." (or "I came to {village} from {origin} when I married {partner}") | history kind founding; the tree's origin |
| PE2 | those in a feud or a debt | "{x} and I came to blows last winter over {what}; it was never settled." / "{x} lent me {q} {item} last winter; I have not paid it back." | history kind feud; the relations' debts |
| PE3 | elders, E | "I have seen {k} hard winters, the last {when}: the frost came early and the stores ran out." | history kind winter, counted (one line, not one a winter) |

### 3.4 The household head's management lines ([[D2-279 Stores, as answered|D2-279]])

The ways of managing a household, seeded chiefly to the head, to pass to the heir. They give facts and the levers the book of rules
offers, never the policy (what to hold back and how much is the head's decision). The head's partner, or the named heir, gets HH1
and HH3.

| Id | Template | Reads |
|---|---|---|
| HH1 | "Our store at {house} holds about {nights} nights' food for the {n} of us as it stands; the winter is {winter_nights} nights, and the hungry time is its end and the first days of spring." | the household's stores and goods at the start (house_food); rations; season length |
| HH2 | "Next year's {plots} plots want about {seed} {crop} of seed. A rule can hold it back from the pot, and say what may be eaten first instead." [holds fields] | plot_seed by plots held; the book's `hold back` |
| HH3 | "Fresh fish and meat go first or go off; what is dried, smoked, salted or in grain keeps. In a hungry spring, the keeping food is what is left: eat the soft first, by rule if need be." | the shelf-life order (part 1); the book's `first` |
| HH4 | "Grain on a floor or in sacks draws mice; in bins or the granary fewer; a cat or an owl hole keeps them down. {store}'s {container} holds about {cap}." | part 3's stores and containers, their capacities and vermin exposure ([[D2-279 Stores, as answered|D2-279]]) |
| HH5 | "What comes in goes to {house} unless a rule sends it elsewhere; when a store is full the rest lies at the door, where anyone may take it." | the book's defaults (store_rules) |
| HH6 | "The hearth burns about {fuel_night} a night and {fuel_cold} on a cold one: a winter wants about {winter_fuel} firewood, or timber to match, in by autumn's end." | heat normal and cold; the winter's nights and its expected cold nights |
| HH7 | "The household's rules and stores pass to whoever heads it after me. I should name an heir, and tell them where things are kept, and why." | succession (`name` heir); [[D2-279 Stores, as answered|D2-279]]'s "to pass to the heir" |

About 270 words. HH2 is dropped for a household with no fields; HH4 waits on part 3's containers (it renders the store the
household actually has).

### 3.5 The livelihoods

Each subsection gives the row (fits, broad, capable, specialisms, capital), then the lines. Crafts marked ★ are the network's
([[W-73 Fishing, hunting and their materials developed together|W-73]], parts 2 and 3; not built), † later. Classes: s simple, p practised, k skilled.

#### 3.5.1 The fisher (in full)

**Row.** Fits: water, best a river with runs. Broad: fish by hand (s), angle (s), set wicker traps (p), dry fish (s), a fishing rod
(s). Capable: salt fish (s), smoke fish (p), tend the smoke (p), a wicker trap★ (p), a creel★ (s). Specialisms: **traps and the
runs** (set traps, wicker traps★, cut withies★); **weir and nets** (the weir's sections (p, a crew's), a fish net★ (p), twist cord★
(s), mend gear★); **hand, rod and dressing** (the edge, the line, the rod, bone hooks★, dressing the catch★); **keeping** (smoke
racks, the smokehouse, salt and dry). Capital likely: about six traps, smoke racks; sometimes: a weir, a smokehouse, a withy bed★,
creels★. Needs salt, withies, cord; gives fish, dried and smoked fish.

| Id | Band, age | Template | Reads | Condition | From |
|---|---|---|---|---|---|
| FI1 | B, Y | "The eels go down to the sea in autumn, on dark wet nights, most on the first rain after dry days. The {river} can look empty all summer and still run thick then." | `RUNS.eel`: window, cue `rain_after_dry`, night; the household's water | eels in the reach | F1 |
| FI2 | B, Y | "One wicker trap takes a few eels on a run night and holds no more than about {trap_hold}. A house that means to eat from the run sets many before the nights come, and lifts every one each morning." | the trap's hold; the run's take a trap a night | | F4 |
| FI3 | B, A | "Fresh fish is half gone in {fish_half} in the hand. Dry it at the hearth, up to {rack_batch} at a time, or salt it, {salt_in} fish to a salt, the day it is caught." | part 1's shelf life of fish; `dry fish` batch; `salt fish` inputs | | F6, short |
| FI4 | C; traps and runs | "A spate smashes about half the traps in the water, and a flood nearly all; an otter that finds full traps comes back each night. When the water drops, set again: the run is not over." | trap wreck by spate and flood (words from the shares); `ROB_SETS` | | F5 |
| FI5 | C; hand and rod | "In summer the fish lie in the warm shallows and pools, where a hand or a rod takes them. A water fished hard thins in days and comes back when it is rested." | the shallows and resident stocks and their renewal | | F7 |
| FI6 | traps and runs | "Salmon come up the {river} after a flood, in autumn and on into early winter, leaping at the shallows. Those that get past go up to spawn, and their young come back as the run after." | `RUNS.salmon`: seasons, cue `spate`, `return` | a big river | F2 |
| FI7 | traps and runs | "Lampreys come up in spring when the river runs high after rain: a smaller run, but the first fresh fish of the year." | `RUNS.lamprey` | lampreys in the river | F3 |
| FI8 | traps and runs, Y if apprenticed | "A trap wants willow rods cut in winter and soaked supple. Make and mend the traps in late summer, before the runs; the nearest willow is at {willow_place}." | part 2's withies and their season; the nearest wet parcel with willow | built: withies | F8 |
| FI9 | weir and nets | "A weir across the river takes a share of every run that passes, more at the first place than below. With its gap shut through the salmon nights it takes the most now, and leaves fewer to come back." | the weir's position shares; the gap ([[D2-211 Fresh fish keep as meat in hand, and alive in a trap or a weir until…|D2-211]]); `RUNS.salmon.return` | a river with runs | F9 |
| FI10 | weir and nets | "A wattle section wants about {wattle_withies} bundles of withies a year, and a spate wears it twice as fast; a timber one lasts longer and costs {timber_section} timber." | part 2's weir sections by material; wear by flow | built: withies | W1 (household_skills) |
| FI11 | weir and nets | "A net of {net_cord} of cord, set overnight in open water, takes fish the traps miss. Mend it before it rots: mended, it lasts about {net_life} sets." | part 2's fish net: cord, life, mend | built: cord | N1 (new) |
| FI12 | weir and nets; the keeper | "Our weir stands {position} on the {river}: {sections} sections of {material}, {wear_words}. {below} lies below it." | the weir work's state at the start; the next work downstream | holds a weir | holding line |
| FI13 | hand, rod and dressing | "A rod wants a straight withy and a line of cord, and takes about half as much again as a hand line. Bone hooks serve; copper hooks from the smith hold better." | part 2's rod, line, bone and copper hooks | built: withies, cord, bone | F8 (rod) |
| FI14 | hand, rod and dressing | "A fish gutted and split the day it is caught dries in the rack; one left whole goes soft. The guts bait the traps." | part 2 and 3's dressing the catch; offal as bait ([[L-145 Offal's uses bait for set lines and traps, dog food|L-145]]) | built: dressing fish, bait | D1 (household_skills) |
| FI15 | hand, rod and dressing | "In a run, a net dipped at the edge takes more than any rod; when the runs are done, a line in the deep water under the bank takes fish at dusk and dawn." | part 3's methods: the edge, the line, the open water | built: the fish net | new |
| FI16 | keeping | "Fresh fish keeps worse in a store than meat. A hearth's rack dries {rack_batch} at a time over {dry_nights} nights; smoke racks take {smoke_batch}; one salt keeps {salt_in} fish." | shelf life by store (part 1); `dry fish`, `smoke fish`, `salt fish` | | F6 |
| FI17 | keeping; the keeper | "The smokehouse takes {smoke_batch} at a time for {smoke_nights} nights. Tend its fire once a day or it dies, and a wattle smokehouse can catch and burn." | the smoke racks' fitting; tend; fire risk | holds a smokehouse | K1 |
| FI18 | keeping | "A light smoke of a night keeps fish {light_keep}; a hard smoke of {hard_nights} nights keeps them {hard_keep}, and takes the wood to match." | part 3's three depths of smoking (hunt_fish_materials §7.3) | built: smoking depths | new |
| FI19 | keeping | "Salt comes from {salt_place}{, d days off}; the salter there wants firewood and grain. Our dried fish is what the farm houses lack by late winter." (the second sentence only where a farming household is in reach) | the nearest brine pan or saltmarsh; roads' days; the neighbours' needs | salt within 2 days, not in the household | F10 |
| NB-FI | neighbours | "The {Line}s live by the {river}: they know when the eels run, and dry and salt the catch; in late autumn they have fish to spare." | the household's livelihood; `RUNS` | | |

Each fisher's set, by role (all within the cap): broad FI1 to FI3; capable adds FI4 and FI5; the traps-and-runs expert FI4, FI6,
FI7, FI8; the weir-and-nets expert FI9 to FI12; the hand-and-rod expert FI5, FI13 to FI15; the keeping expert FI16 to FI19 (FI16
replaces FI3); youths FI1, FI2 (and FI8 or FI9 if apprenticed). A household whose second living is fishing (a farmer who fishes)
gets FI1 to FI3 and FI5. A traps-and-runs expert in prime: 9 base, 2 people, FI1 to FI5, FI6 to FI8, 2 neighbours: 21 lines;
cut by the drop order to 20 (one neighbour line), about 790 words.

#### 3.5.2 The farmer (arable)

**Row.** Fits: fields by soil. Broad: sow, hoe, weed, reap, manure, dung, clear, burn the stubble, pest work, guard the field, bins
(s). Capable: plough (p), select seed, dry fodder, a hearth loaf. Specialisms: **ploughman and oxen**; **seed and harvest**; **hedge
and field**. Capital: fields held, a granary floor, bins; sometimes an ox pair, a plough and harness, a byre. Needs the smith (share,
tools), the miller; gives grain.

| Id | Band, age | Template | Reads | Condition | From |
|---|---|---|---|---|---|
| FA1 | B, Y | The sowing lore, barley: "{barley_lore}" (about 30 words) | `lore.sowing_times` ([[D4-114 What is physically there can be used|D4-114]]), split so no cap cuts it | | A1 |
| FA2 | B, Y | The sowing lore, rye and beans: "{rye_beans_lore}" | as FA1 | | A1 |
| FA3 | B | "A plot wants about {plot_seed} of seed, and sown from the best ears of the harvest it bears better. Seed eaten in a hungry spring is next year's harvest gone." | `plot_seed`; seed selection | | A4, as a reason (the taboo form is a cultural strand) |
| FA4 | C | "Rye wants a winter in the ground and comes up poor without one; barley and beans are tender, and a hard frost takes what is still growing. Sow nothing into frozen ground." | CROPS needs_winter, hardy; frost loss | | A2 |
| FA5 | C; seed and harvest | "Ripe corn will not wait: left standing more than {window} days it sheds and rots, and green ears reaped too soon give only green grain." | farming window, rot, green | | A5 |
| FA6 | ploughman | "A crude tool reaps and fells; a copper one from the smith does about twice the work. Oxen and a plough break the ground far faster than a hoe." | tool grades; plough against hoe | | A7 |
| FA7 | ploughman; the keeper | "Our oxen plough a plot in {plough_units} where a hoe takes {hoe_units}; they want hay through the winter and the byre in a frost." | the ox pair held; plough and hoe units; fodder | holds an ox pair | new |
| FA8 | seed and harvest | "Barley sown after barley tires the ground; beans give it back. Rest a field, or put dung on it, and it bears better." | CROPS takes, restores; fallow, manure | | A3 |
| FA9 | seed and harvest; the keeper | "The {field} bore {last_crop} last year and lies {state} now; the {field2} {state2}." | the fields' own state | holds fields | household_skills §2.1 |
| FA10 | seed and harvest | "Grain ground to meal feeds about half as far again, and bread further; the {mill} grinds for those who bring it grain." | food rows; the mill's node | a mill within a day | A8 |
| FA11 | hedge and field | "Woodpigeons come down on the sowing in spring and again in autumn; clappers or a night's watch keep them off. Beasts through an open gate trample a crop by night." | woodpigeon targets; gates; guard the field | | A6 |
| NB-FA | neighbours | "The {Line}s sow and reap the big field; they have grain after harvest and want hands at reaping." | | | |

#### 3.5.3 The herder or dairy

**Row.** Fits: pasture, meadow, fen. Broad: herd, milk (s), fence, gates, hay, dung, stalls. Capable: slaughter (s), dry fodder,
a hurdle★. Specialisms: **dairy** (cheese (p), the cellar); **stock and breeding**; **hay and winter**. Capital: a herd, pasture
and meadow held, a byre; sometimes a cellar, hay in store. Needs salt (cheese), hay land; gives milk, cheese, oxen, dung.

| Id | Band, age | Template | Reads | Condition | From |
|---|---|---|---|---|---|
| HE1 | B, Y | "Hay is cut in summer, and only then; cattle on bare winter grass, or under snow, starve within days without it." | hay season; winter grass; cattle starve nights | | H2 |
| HE2 | B, Y | "Cattle stray through an open gate and wander back to the common; a beast left unherded may be lost on the road." | herds stray; road loss | | H4 |
| HE3 | C | "The wolves come to the herd in late winter and early spring; bring the beasts in at dusk and bar the byre." | wolf targets | wolves in the region | H3 |
| HE4 | C; stock | "Pasture and meadow feed beasts best, fen half as well, heath and moor less; a beast with the murrain must be kept off shared grass." | cattle grazing by cover; diseases | | H6 |
| HE5 | dairy | "Milk will not keep past the day it is drawn; {milk_in} of milk with a little salt make a cheese in a cellar, and cheese keeps through the winter." | milk shelf life; `cheese` inputs | built: cheese; a cellar or the means | H1 |
| HE6 | stock | "Without the plough oxen there is no ploughing, and without the bull no calves; meat from them is eaten once." | herds: oxen pull, bulls breed | holds oxen or a bull | H5, as a reason (the taboo form is a strand) |
| HE7 | stock; the keeper | "Our herd is {cows} cows, {oxen} oxen and {bull}, kept on {pasture}; {calving}." | the herd's state | holds a herd | new |
| HE8 | hay and winter | "A beast eats about {hay_night} hay a night in winter: our {beasts} want about {hay_winter} for the {winter_nights} nights." | fodder rate; the herd; the winter | holds a herd | new |
| NB-HE | | "The {Line}s keep the cattle on the common; they have milk in summer and oxen to lend for the plough." | | | |

#### 3.5.4 The hunter and trapper

**Row.** Fits: wood, scrub, heath, the wild. Broad: hunt the wild, snare (s), dry meat, a crude weapon, a camp, a pack. Capable:
stalk (p), den work, salt meat, a tent, a bedroll. Specialisms: **stalking and drives**; **snares and small game**; **dressing the
kill**★. Capital: a weapon, snares, a camp at a far wood; sometimes a tent, hides in store. Needs points (the smith), salt; gives
meat, hides, tallow, bone.

| Id | Band, age | Template | Reads | Condition | From |
|---|---|---|---|---|---|
| HU1 | B, Y | "Snares go on the runs in pasture, meadow, heath and field edges, never in deep wood; a hare snared at night must be lifted at first light, before it spoils or another lifts it." | snare covers; set and lift | | T2 |
| HU2 | B | "Game near home grows wary when it is hunted hard; fresh ground a day or two out gives far more, but one carries home only about {carry_foot}." | wariness; the carry (part 1's weights) | | T4 |
| HU3 | C | "Deer are fattest in autumn, and the stags roar at dusk in the rut; in spring the hinds have calves and the game is thin." | wild kinds' seasons and body | deer in the region | T1 |
| HU4 | C | "A kill left lying draws the wolf and, in a hungry spring, the bear: dress it and carry it in the same day. Fresh meat rots in {meat_days}; dried or salted it keeps." | carcass targets; meat's shelf life | | T5 |
| HU5 | stalking and drives | "Stalking is slow work in wood and heath, downwind and close; a drive wants beaters and spears and is dangerous; one alone with a weapon takes what comes." | stalk, drive, hunt notes | | T3 |
| HU6 | stalking and drives | "{far_wood}, {d} days out, holds {game} in autumn; a camp there saves the walk home each night." | the nearest unhunted wood; its kinds | a wood within 2 days | new |
| HU7 | snares and small game | "Snares want a little cord, or a thong of rawhide, which rots on a wet night; move a line when the runs go cold." | part 2's snares from cord or rawhide | built: cord | new |
| HU8 | dressing the kill | "A kill gives more than meat: the hide, the tallow of a fat beast, and bone; a careful hand takes all of it, a careless one wastes meat. The herders and the carriers want hides." | part 2's dressing the kill; hide, tallow, bone | built: dressing | T6 |
| NB-HU | | "The {Line}s go to the woods in autumn and come back with deer; they trade hides and meat." | | | |

#### 3.5.5 The fowler

**Row.** Fits: fen, flooded meadow, open water. Broad: fowling★ (from today's `net`, p), snare, gather young and eggs. Capable: a
fowling net★ (p), twist cord★, dry meat. Specialisms: **nets and decoys**; **the freeze and the flight**. Capital: a fowling net★.
Needs cord; gives fowl in winter.

| Id | Band, age | Template | Reads | Condition | From |
|---|---|---|---|---|---|
| FO1 | B, Y | "The duck and geese come in autumn, are thickest in winter and leave in spring; they flight at dusk and dawn." | part 3's fowl seasons | built: fowl seasons | W1 |
| FO2 | B | "Woodpigeons flock on the sown fields in spring; the eggs and young of the colonies are there for a few weeks only." | woodpigeon targets; gather young season | | W3 |
| FO3 | C; freeze and flight | "In a hard freeze the fowl crowd onto the open water that is left, and a net there takes many." | the freeze's crowding (part 3) | built | W2 |
| FO4 | nets and decoys | "A net takes about four times what hands do and wants about {fowl_net_cord} of cord; cord is twisted from nettles in late summer." | part 2's fowling net, cord | built: cord | W4 |
| FO5 | freeze and flight | "Fowl flight along the same lines each dusk and dawn; a net laid across a flight line takes most." | part 3's flight lines | built | new |
| NB-FO | | "The {Line}s take duck on the fen in winter; when everything else is thin they have fowl." | | | |

#### 3.5.6 The salter

**Row.** Fits: a brine spring or saltmarsh. Broad: boil salt (s), salt meat, salt fish, firewood, cut. Capable: mend the brine pan,
the saltmarsh pans. Specialisms: **the pan**; **salting for keeping**; **carrying salt**. Capital: a brine pan in a salt house at a
spring; or saltmarsh pans held. Needs copper (the pan), fuel; gives salt.

| Id | Band, age | Template | Reads | Condition | From |
|---|---|---|---|---|---|
| SA1 | B, Y | "Salt keeps meat and fish for months: one salt to {salt_in}. Every house that kills, fishes or makes cheese needs it, and few can make it." | `salt meat`, `salt fish`, `cheese` inputs | | S2 |
| SA2 | C; the pan | "{pan_fuel} firewood boils {pan_salt} salt at the pan in a unit; the pan wears through after about {pan_life} boilings and must be mended." | `boil salt`; the brine pan's wear | a brine pan | S1 |
| SA3 | the pan | "The pan wants copper, which only the smith makes; our fuel is the wood about us, which thins as we cut it." | the pan's materials; the wood's renewal | | S3 |
| SA4 | the pan; the keeper | "The pan at {salt_house} has boiled {uses} times since it was mended." | the pan's wear at the start | holds a pan | holding line |
| SA5 | salting for keeping | "Meat salted in a tub keeps {salt_meat_keep}; fish salted wet must be kept cool; a cheese takes a little salt and a cellar." | part 3's salting and stores | | new |
| SA6 | carrying salt | "Salt is heavy only in bulk: a load of {load} goes a day's walk; {village} has {surplus} and no salt." | carry by weight (part 1); the neighbours' needs | a village within 2 days | S4 |
| SA7 | B, saltmarsh | "The pans on the marsh make salt in the sun; in winter they give little." | the saltmarsh pans' season | holds saltmarsh | household_skills §2.1 |
| NB-SA | | "The {Line}s boil salt at the spring; they want grain and firewood for it." | | | |

#### 3.5.7 The smith and miner

**Row.** Fits: rock with ore within a day, an anvil. Broad: charcoal (p), fetching ore, firewood. Capable: mine (with a tool), a
copper tool (k) at rough. Specialisms: **smelting and tools** (smelt (k), copper tool, coin, the anvil); **mining and charcoal**;
**fittings** (the brine pan, the plough share, copper hooks★). Capital: a forge (hearth, anvil, bellows), charcoal; sometimes a
claim on the ore. Needs charcoal, ore; gives copper.

| Id | Band, age | Template | Reads | Condition | From |
|---|---|---|---|---|---|
| SM1 | B | "Charcoal burns {heat_x} times hotter than its weight in timber; {charcoal_in} timber burnt slow make one." | the fuel rows; `charcoal` inputs | | M2 |
| SM2 | C | "A copper tool does about twice a crude one's work; the plough, the salter's pan and the fisher's hooks all want copper." | tool grades; the pan; copper hooks | | M3 |
| SM3 | smelting and tools | "Smithing is years at the anvil: tries alone get one only so far, and the rest is taught." | the skilled class (§4.2) | | M4 |
| SM4 | smelting; the keeper | "Our forge at {house} has an anvil, a hearth and bellows; it wants charcoal by the load, and holds {charcoal} now." | the forge's fittings and stock | holds a forge | household_skills §6.4 |
| SM5 | mining and charcoal | "Ore is dug where the rock shows it, at {ore_place}, {d} days off; {ore_in} of ore and {charcoal_per} of charcoal smelt to one copper at the anvil." | rock covers with ore; `smelt` inputs | ore within 2 days | M1 |
| SM6 | fittings | "{salter}'s pan, {farmer}'s plough share and the fishers' hooks are copper work: those who need them come to us." | the households needing copper in reach | | new |
| NB-SM | | "The {Line}s work copper at their forge; they make tools and want charcoal and grain." | | | |

#### 3.5.8 The miller and baker

**Row.** Fits: a mill site, grain within a day. Broad: grind (s), a hearth loaf, bins. Capable: mill at millstones, oven bread (p),
dress millstones. Specialisms: **the mill** (water mill, the leat, the stones, the wheel's hatches); **the oven**. Capital: a mill
(millstones, wheel and leat); sometimes an oven, a hand mill. Needs grain, the mason (stones), the wright (wheel); gives meal,
bread.

| Id | Band, age | Template | Reads | Condition | From |
|---|---|---|---|---|---|
| MI1 | B, Y | "Grain ground feeds about half as far again as grain boiled, and bread further still; flour keeps as grain does, bread goes off {bread_x} times as fast." | food rows; shelf life | | G1 |
| MI2 | C | "The farmers bring grain after harvest; the mill is busiest then, idle in spring." | the crop calendar | | G4 |
| MI3 | the mill; the keeper | "Our mill grinds up to {batch} grain at a turn; the leat silts and wants clearing once a year, the stones dressing after about {stones_life} grain. {leat_state}." | the mill's fittings, batch ([[D2-247 A process of bulk goods has a most it takes at once, not a least|D2-247]]'s "up to") and wear | holds a mill | M-mill (household_skills) |
| MI4 | the mill | "Shut, the hatches hold the river and the wheel turns full; drawn, they let the fish by, and the wheel turns slow." | the mill's gap ([[D2-246 With a mill's gap open|D2-246]]) | a mill on a run river | G3, M-gap |
| MI5 | the oven; the keeper | "The oven bakes up to {oven_batch} loaves from as much flour and {oven_fuel} timber, and wants relining after about {oven_life} bakings." | the oven's batch and wear | holds an oven | household_skills §2.1 |
| NB-MI | | "The {Line}s keep the mill; bring them grain after harvest and they grind it." | | | |

#### 3.5.9 The builder: wright and mason (household_skills addendum)

**Row.** Fits: managed wood (wright), rock within a day (mason). Broad: fell, a small room, beds, bins, repair, clear for building,
a woodshed. Capable: a medium room, a granary, a hearth, smoke racks. Specialisms: **the wright** (timber framing, the hall, the
water wheel, the plough frame, the handcart); **the mason** (quarry, wall, hearth, oven, cellar, millstones, vault). Usually with
farming as the second living. Capital: timber or stone in store, a woodshed; sometimes a quarry claim, a managed wood's claim.
Faster and sounder (building_clock.md: about half the units at master; craftsmanship sets wear).

| Id | Band, age | Template | Reads | Condition | From |
|---|---|---|---|---|---|
| BU1 | B, Y | "Wattle cracks on cold nights and every building falls to ruin unmended: keep timber back for repairs as well as for the fire." | building wear; repair | | C2 |
| BU2 | B | "Felling with a tool gives far more than gathering dead wood by hand; a crude tool wants {tool_stone} stone." | `fell`, `firewood`; `crude tool` | | C4 |
| BU3 | C | "A full floor spills what is brought in out of the door; a granary floor holds {granary_cap} grain, bins {bins_cap}." | SPACE; part 3's stores | | C3 |
| BU4 | C, both | "One who knows the work raises a room in about half the days a neighbour takes, and it stands longer; a room thrown up wears faster." | part 2's build rates by skill; wear by craftsmanship | built: building_clock | new |
| BU5 | wright | "Timber felled in winter and seasoned before it is worked splits less and lasts longer; green timber warps in the frame." | the timber economy's seasoning ([[W-76 The timber economy|W-76]]) | built: seasoning | new |
| BU6 | wright | "The mill's wheel, the plough's frame and the handcart are a wright's work; {who} need them." | the households holding or wanting them | | new |
| BU7 | mason | "Stone lies only where the rock shows, at {rock_place}, {d} days off; quarrying wants a tool." | rock covers; `quarry` | rock within 2 days | C1 |
| BU8 | mason | "A hearth wants {hearth_stone} stone and an oven {oven_stone}; stone walls outlast wattle many times over, and want their footings on dry ground." | blueprints; wear by structure; the cellar's ground rule | | new |
| NB-BU | | "The {Line}s build: a frame, a wheel or a hearth is their work." | | | |

#### 3.5.10 The woodsman (household_skills addendum)

**Row.** Fits: managed wood. Broad: fell, cut young growth, firewood. Capable: charcoal (p), a camp, cut withies★. Specialisms:
**charcoal**; **coppice**† ([[W-76 The timber economy|W-76]]). A full living only where a smith or a salter buys fuel. Capital: a managed wood's claim.

| Id | Band, age | Template | Reads | Condition | From |
|---|---|---|---|---|---|
| WO1 | B, Y | "Young growth in {wood} cut comes again in a few years; the dead wood once gathered is gone." | forest renewal by pool | | charcoal burner |
| WO2 | C; charcoal | "{charcoal_in} timber burnt slow in the wood make one charcoal; the smith and the salter want it, and little else does." | `charcoal` inputs; buyers in reach | | charcoal burner |
| WO3 | charcoal | "A burn takes {burn_nights} nights of watching; left, it flares to ash." | the burn as a process (part 2) | built: the burn as a process | charcoal burner (held back until true) |
| WO4 | coppice | "A coppice cut over every {cycle} years gives poles and withies again; the standards left to grow give timber for building." | the timber economy's coppice and standards ([[W-76 The timber economy|W-76]]) | built: coppice | new |
| WO5 | B | "{buyer} at {place} burns more than they cut: they take firewood and charcoal for grain." | the fuel-hungry households in reach (smith, salter, baker) | a buyer within 2 days | new (needs, never prices: [[D2-270 Household skills|D2-270]]'s rule kept for all) |
| NB-WO | | "The {Line}s work the wood; they have charcoal and poles, and firewood in winter." | | | |

#### 3.5.11 The basket maker (withies)

**Row.** Fits: wet ground with willow. Broad: cut withies★ (s), hurdles★ (p). Capable: wicker traps★, creels★, pack baskets★.
Specialisms: **traps and creels**; **the withy bed**. Capital: a withy bed★. Gives traps, baskets, hurdles to fishers, herders,
carriers.

| Id | Band, age | Template | Reads | Condition | From |
|---|---|---|---|---|---|
| BA1 | B, Y | "Willow rods are cut in winter when the sap is down; cut in summer they give a third and harm the stools." | part 2's withies by season | built: withies | founders_knowledge basket maker |
| BA2 | B | "Hurdles of withies fold beasts and fence a garden, and are lighter to move than posts and rails." | part 2's hurdle | built | new |
| BA3 | C; traps and creels | "A creel carries the catch on the back; a pack basket with a hide strap carries about {pack_carry} where hands carry {carry_foot}." | part 1's carrying; part 2's creel and pack basket | built | new |
| BA4 | the withy bed | "A withy bed takes three years to bear and then gives for thirty, if beasts are kept off it." | the bed's yield by year | built | founders_knowledge |
| BA5 | the withy bed; the keeper | "Our bed by {parcel} is in its {year} year; {fence_words}." | the bed's state | holds a bed | new |
| NB-BA | | "The {Line}s cut the willow; they make traps, creels and hurdles for those who need them." | | | |

#### 3.5.12 Cord and nets

**Row.** Fits: a close of good soil; still water or a pit. Broad: twist cord★ (s). Capable: sow and pull flax★, ret flax★.
Specialisms: **flax and linen** (ret, dress and spin★, the retting pit★); **nets** (fish and fowling nets★). Capital: a flax close★;
sometimes a retting pit★. Gives cord and nets.

| Id | Band, age | Template | Reads | Condition | From |
|---|---|---|---|---|---|
| CO1 | B, Y | "Nettles twisted in late summer make cord enough for snares and lines; it is slow work, a kilo in many days." | part 2's twist cord, rate, season | built: cord | founders_knowledge |
| CO2 | C | "A close of flax gives the cord a whole fishing village needs; it takes ground and dung from the grain." | part 2's flax crop | built: flax | new |
| CO3 | flax and linen | "Retted in the river, flax fouls the water three nights for the fishers below; retted on the grass or in a pit, it fouls nothing." | part 3's pollution from retting (§7.5) | built | household_skills §2.1 |
| CO4 | flax and linen | "Retted flax is dressed and spun in winter, when other work is thin; about {flax_in} of it make a cord." | part 2's dress and spin | built | new |
| CO5 | nets | "A net wants about {net_cord} of cord and many evenings' knotting; the fishers and fowlers need one every few years." | part 2's nets, their life | built | new |
| NB-CO | | "The {Line}s grow flax and twist cord; fishers and fowlers get their nets from them." | | | |

#### 3.5.13 The tanner ([[D2-270 Household skills|D2-270]]: the row now)

**Row.** Fits: water, an oak wood, hides from herders or hunters within a day. Broad: dress hides. Capable: harness, a pack, a
bedroll from leather†. Specialisms: **the pits** (tanning (k)). Capital: tan pits† by water, bark from an oak wood. Usually beside
farming or herding. Gives leather: the pack frame's straps, harness, the smith's bellows, shoes (hunt_fish_materials §7.6).

| Id | Band, age | Template | Reads | Condition | From |
|---|---|---|---|---|---|
| TA1 | B, Y | "Hides come in autumn, from the hunters and the slaughter; a hide left raw and wet rots in {hide_days}, dried or salted it waits." | part 1's shelf life of hides; slaughter season | | new |
| TA2 | C | "Oak bark is stripped in spring, when the sap rises, and kept dry; bark left in the rain gives little." | part 2's bark | built: tanning | learning_times tanning lesson, as lore |
| TA3 | the pits | "A hide lies in the pits {tan_time}, the liquor weak at first and stronger week by week; a pit wants water and about {bark_in} of bark a hide." | part 2's tanning (a process on the year clock, [[D2-273 Three clocks, each system on one|D2-273]]) | built | new |
| TA4 | the pits | "Leather makes the pack's straps, the harness, the smith's bellows and shoes; raw hide does for a season and rots." | part 2's leather uses | built | new |
| TA5 | the pits; the keeper | "Our pits by {parcel} foul the water below them; the {Line}s fish downstream." | part 3's pollution; the downstream holders | holds pits | new |
| NB-TA | | "The {Line}s tan hides in pits by the {water}; they take hides and bark and give leather." | | | |

#### 3.5.14 The trader or carrier ([[D2-270 Household skills|D2-270]]: roads and needs, never prices)

**Row.** Fits: a road with a track, villages a day or two apart. Broad: carry, travel, offers. Capable: a handcart, a pack ox.
Specialisms: **the road**; **the market** (who makes what, who lacks what). Always a second living beside another. Capital: a handcart
or pack ox, coin, a pack.

| Id | Band, age | Template | Reads | Condition | From |
|---|---|---|---|---|---|
| TR1 | B, one a village | "{village} has {surplus} after {season} and lacks {need}." (up to three villages) | the villages in reach: their livelihoods' gives and needs | within 2 days | household_skills §1.3 |
| TR2 | C | "A pack ox carries {ox_carry} where one on foot carries {carry_foot}, but wants grazing on the way; a handcart carries {cart_carry} on a road with a track and is no use off one." | part 1's carrying; the pack ox; tracks | | household_skills §1.3 |
| TR3 | the road | "The road to {place} is {days} days {track_words}; {landmark} is a place to stop the night." | roads; landmarks known | | new |
| TR4 | the market | "Salt, copper and stone are made in few places and wanted in all; grain and fish are scarce everywhere by late winter." | the region's chokepoints; the year's lean time | | new (needs, not prices) |
| NB-TR | | "{name} of the {Line}s carries between {village} and {village2}; ask them for what is not made here." | | | |

#### 3.5.15 The cottager (household_skills addendum)

**Row.** Fits: a cottage and garden, little or no land; a village with work to hire. Broad: gather, a garden, the common's beasts,
work for pay. Capable: spinning, baskets (by-crafts). Specialisms: none (by-crafts at capable at most). Capital: a cottage, a garden
lot, perhaps a cow or pigs on the common. A village's labour supply and a test of labour markets.

| Id | Band, age | Template | Reads | Condition | From |
|---|---|---|---|---|---|
| CT1 | B, Y | "We hold a cottage and a garden and no field; we live by work for others, for food or coin, and by what the common gives." | holdings | | new |
| CT2 | B | "The {Line}s want hands at {season_work}, the {Line2}s at {season_work2}; a day's work earns a meal or more." | the neighbours' busy seasons; work-for-pay offers | | new |
| CT3 | C | "A cow or a pig on the common and a garden of beans see us through when the work fails." | the common's grazing; garden crops | | new |
| CT4 | C | "In winter, when work is thin, we spin and make baskets for those who will take them." | by-crafts; the winter's units | built: spinning, baskets | new |
| NB-CT | | "The {Line}s work for whoever needs hands; they spin in winter." | | | |

### 3.6 Neighbours and marriages

As household_skills §4: in one village, aware of each other household's broad band, rough in one craft whose product one's own
household uses (keyed draw), and one NB line each (two at most in a founder's set by the cap); a village within a day, the
chokepoint crafts only, aware, and the NB line naming household and place; further, nothing. A spouse who married in brings their
natal household's broad band at the level they left with and up to three of its B lines in their own voice ("At home at {origin} we
..."), within the cap, displacing NB lines first; with chance `marriage_expert` (0.15) a capable specialism.

### 3.7 Cultural strands

founders_knowledge Part 3's twelve dimensions stand. Each replaces one base line or adds one: passing on replaces BS8's last
clause; a taboo replaces the reason form of FA3, HE6 or FI9 with the custom ("We never shut the weir through the salmon nights");
exploring, sharing crafts, hospitality and the rest add one line to every founder of the people. A strand's line counts in the cap
and is dropped last. The first pair to run: BS8 (a) against (c).

---

## 4. Learning: one mechanism

### 4.1 The record

```
Mind.know[craft] = {
  level:   aware | rough | capable | known      # how much of the craft one knows (the recipe and its steps)
  score:   wins + a share of fails toward the next level
  lessons: [lesson ids had, in the craft's order]
  skill:   a number on the craft's curve (how well: yield, waste or quality, by the craft's `acts_on`)
  practice: units of the craft (the curve's x), peak: the best skill held
  points:  [capability points held]
  seen, source, since, practised                # as now
}
Mind.aptitude = {hands, fire, beasts, water, growing, structure, dealing}   # 0 to 1 each (§4.8)
```

Today's record has level, skill, seen, wins, fails, source, since, practised, peak (`knowledge.py`). Added: lessons, points,
practice (stored rather than inverted from skill, so curve shapes with two parts invert cleanly), and the aptitude. Level and skill
stay separate, as now: one can know a recipe (known) and be clumsy at it (skill low), or be deft at what one half knows.

### 4.2 Classes and curves (at lifespan 64, [[D2-267 Practice and learning are set at a 64-day lifespan and scaled with a…|D2-267]]; calibrate)

The trying_and_learning tables, rescaled from lifespan 96 to 64 (a life of 64 days holds about two thirds of the units; tau scales
with it):

| | simple | practised | skilled |
|---|---|---|---|
| chance a try works, aware / rough / capable / known | 0.6 / 0.8 / 0.95 / 1 | 0.35 / 0.55 / 0.8 / 1 | 0.15 / 0.35 / 0.65 / 1 |
| materials, aware / rough / capable / known | 1.3 / 1.15 / 1.05 / 1 | 1.8 / 1.5 / 1.2 / 1 | 2.0 / 1.8 / 1.4 / 1 |
| score to rise, aware→rough / rough→capable / capable→known | 1 / 2 / 2 | 2 / 3 / 4 | 3 / 4 / and the taught lesson |
| known also needs | every lesson had | every lesson had | every lesson, the last only from a teacher |
| default curve | shallow | steady or stepped | deep |
| tau (units of the craft) | 7 | 17 | 33 |
| skill range | 0.8 to 1.3 | 0.6 to 1.6 | 0.5 to 2.0 |
| practice alone reaches | the top | the top | half the range; beyond it only taught or beside a master |

A success scores 1; a failure 1 at aware and a half above. The class is a field on the craft's row; any parameter may be overridden
by the row. A real seven-year apprenticeship is about 8 life-days at lifespan 64, about 17 to 25 units at the craft (learning_times
§1 rescaled): practice reaches capable in a skilled craft in about 9 tries, and the master's lessons do the rest.

**The curve shapes** (trying_and_learning §7), one formula:
`skill = lo + (hi - lo) * [s * (1 - e^(-p / t1)) + (1 - s) * (1 - e^(-p / t2))]`, capped at the untaught ceiling unless taught.

| Shape | s (shoulder) | t1 | t2 | Crafts |
|---|---|---|---|---|
| shallow | 1 | tau | | snares, line fishing, the quern, salting, cord |
| steady | 1 | tau | | netting, hurdles, smoking, oven bread |
| stepped | 0.5 | tau / 3 | tau x 2 | wicker traps (quick to a working trap, long to a tight throat), ploughing, the hunt (today's own geometric curve is kept for the hunt until it is refitted) |
| deep | 0.2 | tau / 2 | tau x 2 | smelting, smithing, tanning, the weir's timber work |

### 4.3 The five events

Every change to the record comes from one of five events, each through the `learn` primitive ([[D4-35 Everything happens in a place|D4-35]]) so the view and the
measurement see it.

| Event | level and score | lessons | skill | points | aptitude |
|---|---|---|---|---|---|
| **Attend** (free, one a day; or with units, §4.5) | aware of the crafts that make or use the thing seen; a simple craft to rough at once; with units, rough at 3 seen | free: the next lesson the worker has that one lacks; with units, one per 2 units, at most 3 | none | none | none |
| **Try** (any act of a craft at aware, rough or capable) | success +1; failure +1 at aware, +0.5 above | a failure: a true cause, else the next lesson (§4.4) | the act's units as practice (a failure counts half) | crossing a threshold unlocks | +, by the craft's profile |
| **Practise** (the craft done at known) | none | none | units as practice; past the untaught ceiling only beside a master or taught | as try | + |
| **Be taught** (`explain`, free; a lesson session, 2 units each) | explain: aware to rough; a session: score +2 | explain: one lesson the explainer has; a session: up to two | a session: toward the teacher's peak (§4.6) | as skill crosses; a taught-only point needs a session | the teacher's dealing + |
| **Fade** (unpractised, [[D4-105 Sowing windows are lore, not rules|D4-105]]) | none | kept | falls, never below 60% of its best gain; relearnt faster | a point is lost only when skill falls below its threshold less a tenth | none |

"Beside a master": the learner works the craft at the same place on the same day as one whose skill is in the craft's top
quarter. The engine can check it from the day's acts; it is how the hunt's lead already lifts a party (`lead_hard`).

### 4.4 Every attempt teaches

Each craft row carries an ordered list of lessons (two to five; learning_times §5 drafts three for each of eighteen crafts), each
with a kind (input, step, place, season, tool), a failure line, and a short form for the craft line. The first lesson is always
the main input (so a lesson had at aware is what makes rough). A failed try:

1. reports a cause the state holds, if one does (the season out, wet wood, an input short, the wrong place): "The rods split:
   withies cut in summer are brittle; cut them in winter." It marks that lesson had if it is one;
2. otherwise gives the next lesson not had: "The throat was too wide: an eel went in and out again. Close the cone to a finger's
   width.";
3. once every lesson is had, says the shortfall is the hands: "You did it as you knew how; your hands are not yet sure of it."

No line claims a cause the state does not hold (the senses guide). A refusal that is about the act, not the craft ("teach needs a
learner the same day"), is the shape's grammar, given in the refusal and in the shape's line, never a lesson to keep.

### 4.5 Attention, spent in units

One mechanism, its depth set by what one spends ([[Q-81 Knowledge in their own words|Q-81]] §4; trying_and_learning §4):

| Attention | Cost | Gives |
|---|---|---|
| `attend` a thing (a trap, a net, a smokehouse, a sack of flour) | free, one a day | the thing in detail next morning (as now); aware of the crafts that make or use it; a simple craft at rough |
| `attend` a person at work | free | aware of their craft; the next lesson they hold that one lacks, if they are capable or better |
| `attend` with `units` (1 to 4) a person at work | the units | 3 seen at once (rough); a lesson each 2 units (3 at most); seen by them ("Nigel watched you at the weir all morning"), consent not needed. Today's `watch` is this at 4 units |
| `attend` with units a finished thing | the units | the making craft's input lesson; a practised craft to rough |
| `attend` with units a place | the units | its signs at a lower threshold (chance x (1 + units / 4), calibrate) and the signs of crafts one knows at rough (normally capable and up); couples with the senses guide (37.4's `perceive.py`) |
| A child minded at home (not acting) | none | each night, aware of the crafts its household did at home that day; a simple one done often (five days) to rough. So a youth comes of age aware of the household's broad band, as one raised in it would, and knowing none of its lore unless passed |

Hearing a craft named makes one aware only by its own name and aliases, not by common words (crafts_evaluation: "wall", "hunt",
"under brush").

### 4.6 Teaching from the teacher's peak

A lesson session moves the learner's skill part of the way toward the teacher's lifetime peak, not their present skill (Zach, 22
Nov, trying_and_learning §6):

`skill_learner += f * (peak_teacher - skill_learner)`, applied as the practice that would give it on the learner's curve, where
`f = 0.25`, times 1.3 when the teacher's present skill is within a tenth of their peak (their hands show what their words say),
times (1 + 0.5 x the teacher's dealing aptitude). Calibrate. A session also gives up to two lessons and +2 score. The skilled
class's last lesson and the top half of its curve come only this way or beside a master. So an elder past their best still teaches
what they knew, a teacher at their peak teaches fastest, and the learner never passes the teacher's peak by teaching alone.

What one session does, by class: simple, rough or aware to capable; practised, usually capable after one and known after two with
practice; skilled, capable after two, and known only with the taught lesson and practice. Today one session makes anyone capable of
anything ([[D4-123 A lesson is in the teacher's craft|D4-123]]).

### 4.7 Capability points

Discrete, on the skill curve, unlocking what one can do, never how well (trying_and_learning §7). A row lists its points with their
threshold (a share of the range) and what they open: a technique, a build option, a sign audience, a teaching power. Examples by
livelihood (the full lists are part 2's per-craft field):

| Livelihood | Point | Opens |
|---|---|---|
| fisher, traps and runs | reads the run's weather (0.5) | the "knows" sign the evening before a cue night: "the river is rising and coloured after the dry days" (an observation, [[D2-269 Experts' signs are observations of what is happening now, which may…|D2-269]]) |
| fisher, weir and nets | a timber section (0.6) | the weir's timber build option |
| fisher, keeping | a hard smoke (0.5) | part 3's long-keeping smoke |
| farmer, ploughman | heavy ground (0.5) | ploughing clay |
| herder, dairy | a keeping cheese (0.6) | cheese that keeps a year |
| hunter, stalking | leads a drive (0.6) | the drive's lead |
| smith | casts a pan (0.7) | building a brine pan |
| builder, wright | a frame (0.5); a hall (0.8) | the medium room in timber; the hall |
| builder, mason | an upper storey (0.6); a vault (0.8) | storeys; the vault |
| any skilled craft | teaches the skilled half (0.75) | lessons that lift past the untaught ceiling |

### 4.8 Transfer through underlying skills

Seven aptitudes, each 0 to 1 (trying_and_learning §8 lists eight; strength is left out because the engine's units already carry
the body by stage and age, and a strength aptitude would count it twice):

| Aptitude | What it is | Fed by |
|---|---|---|
| hands (H) | weaving, knotting, spinning, fine work | baskets, traps, nets, cord, spinning, leather |
| fire and curing (F) | heat and keeping: smoke, charcoal, smelting, baking, salting | smoking, salting, drying, charcoal, smelting, baking, tanning |
| beasts (B) | reading animals | hunting, herding, fowling, snaring, milking |
| water (W) | reading water and the runs | fishing, trapping, the weir's siting, the leat |
| growing (G) | plants and soil | sowing, reaping, hay, withy beds, flax, coppice |
| structure (S) | building in timber and stone | rooms, fittings, the weir, frames, quarrying |
| dealing (D) | people: trade, carrying, teaching | trading, teaching sessions, the drive's lead |

**Each craft's profile** (weights summing to 1, one to three of them; part 2 carries the field on each row):

| Livelihood | Profiles |
|---|---|
| fisher | fish by hand W.8 B.2; angle W.7 H.3; set traps W.8 B.2; a wicker trap H.8 W.2; a rod H1; a fish net H1; set a net W.8 H.2; a weir section S.6 W.4; mend gear H1; dry fish F1; salt fish F.7 H.3; smoke fish F1; tend the smoke F1; dress the catch H.7 B.3 |
| farmer | sow, hoe, weed, manure, select seed G1; reap G.8 H.2; plough G.6 B.4; clear G.5 S.5; pest work G.6 B.4; guard the field B.6 G.4; clappers H1; bins, granary S1; grind H1; a hearth loaf F1 |
| herder | herd B1; milk B.7 H.3; fence S.7 G.3; hay G1; dry fodder G.7 F.3; slaughter B.5 H.5; cheese F.7 H.3; stalls S1; a hurdle H.8 S.2 |
| hunter | hunt the wild, stalk B1; snare B.7 H.3; drive B.6 D.4; den work B.8 S.2; dress the kill H.6 B.4; dry meat F1; salt meat F.7 H.3; make snares H1; a crude weapon H.7 S.3; a camp S1 |
| fowler | fowling B.6 W.4; a fowling net H1; gather young and eggs B1 |
| salter | boil salt F1; mend the pan F.5 S.5; the saltmarsh pans W.5 F.5; salt meat and fish F.7 H.3 |
| smith | smelt F1; a copper tool F.6 H.4; coin H.6 F.4; mine S1; charcoal F1; copper hooks H.6 F.4 |
| miller and baker | grind H1; mill at millstones S.7 B.3; the water mill W.5 S.5; dress millstones S.6 H.4; clear the leat W.6 S.4; oven bread F1; reline the oven S.6 F.4 |
| builder | fell S.6 G.4; rooms, repair, quarry, wall, cellar S1; a hearth S.7 F.3; an oven S.6 F.4; the handcart, plough frame S.6 H.4; the water wheel S.6 W.4; millstones S.6 H.4 |
| woodsman | fell S.6 G.4; cut young growth G1; charcoal F1; coppice G1 |
| basket maker | cut withies G.6 H.4; plant a bed G1; traps H.8 W.2; creels, pack baskets H1; hurdles H.8 S.2 |
| cord and nets | twist cord H1; sow and pull flax G1; ret flax W.6 G.4; dress and spin H1; nets H1; a retting pit S.6 W.4 |
| tanner | dress hides H.6 B.4; tanning F.8 H.2; strip bark G.6 H.4; leather work H1 |
| trader | trade D1; lead a pack ox B.6 D.4; a handcart S.6 D.4 |
| cottager | spinning H1; baskets H.8 G.2; garden G1 |

**The rule:** practice raises the craft first and its aptitudes a little: `d += units * w / 60 * (1 - d)` (60 units of a craft at
weight 1 to go about two thirds of the way; calibrate at lifespan 64). A new craft's head start is `h = min(1/3, sum(w_i * d_i))`:
its starting skill is `lo + h * (hi - lo)` and its practice counts `1 + h` times. So a basket maker takes to netting (hands), a hunter
to fowling (beasts), a charcoal burner to smoking (fire). Founders' aptitudes are set at generation from their seeded crafts'
skills, so they agree with what the person already does. **Inherited aptitude** (from the parents with chance) stays an experiment
knob, off by default.

### 4.9 What the engine keeps, what the agent writes

| | The engine keeps (`Mind.know`, `Mind.aptitude`) | The agent writes (kept lines, memory, notes) |
|---|---|---|
| What | knowledge of the hands: level, lessons, skill, points, aptitudes | lore, places, seasons, people, prices, plans, beliefs |
| Shown | on the craft's line, every prompt | in the opening of each stretch, as written |
| Lost | only by fading (skill), never lessons | by dropping, by rewriting badly, by dying unpassed |
| Passed | by explain, lessons, attention | by `pass` in care, by telling, by notes on a building |
| Can be false | no (it is the state) | yes ("fished out"), and is read for errors ([[Q-81 Knowledge in their own words|Q-81]] Risks 1) |

So no agent spends a kept line on "the throat wants a finger's width", and every kept line is the world as they understood it. A
founder's seeded lore is in the right-hand column; a founder's seeded crafts and their lessons (all lessons had at known, the first
at rough) are in the left.

### 4.10 A worked case: Henry learns the wicker trap

Henry of the Marshes is a child at the start (5 days old) and comes of age on day 7 (youth from 12 days at lifespan 64). Minded at
home, he has become aware of setting traps and making them (the household did both at home), and rough at drying fish (simple, done
most nights). He has no seeded lines; his kept places hold two lines Nichola passed in care ("the eels come on the first rain after
dry days"; "lift the traps every morning of the run").

- Day 8, he attends Nichola making a trap (free): the next lesson she has, the first (the main input: "withies, soaked"). Having the
  first lesson makes him rough. Craft line: "a wicker trap (a rough idea: withies, soaked)".
- Day 9, he tries (practised, rough: 0.55; materials 1.5 times). It fails, and the state holds a cause: his withies were cut in
  summer. "The rods split: withies cut in summer are brittle; cut them in winter." Lesson 2, score 0.5, half the units as practice.
- Day 10, he tries with winter rods from the store. It fails again, with no state cause: the next lesson, "The throat was too wide:
  an eel went in and out again. Close the cone to a finger's width." Lesson 3, score 1.0.
- Day 11, a lesson session with Nichola (2 units each): score +2, to 3.0, the practised class's mark for capable. His skill moves
  toward her peak (1.15): f = 0.25, times 1.3 because she is at her peak, about 0.33, so from 0.6 to about 0.78.
- His craft line: "a wicker trap (capable: 0.4 withies, soaked; 2.5 units; gives a trap; works about 4 times in 5; the throat to a
  finger's width)". He has every lesson the row holds, so known waits only on score (4 more) and practice.

He has spent no kept line on any of it. What he keeps when his next place opens is his own reading of the world: perhaps where the
willow grows, or that the Isel looked empty in summer. (Numbers: today's TRY table replaced by §4.2's; the trap's inputs are the
network's proposal.)

---

## 5. Acting: ten shapes

### 5.1 The shapes

A shape is what an act takes, what it costs, how long it runs and what kind of change it makes (verb_grammar §1). A new shape only
when an act has one the others cannot express; everything else is a technique, a setting or a target.

| Shape | Takes | Cost | Runs | Changes | Its techniques and faces |
|---|---|---|---|---|---|
| **go** | a place or a way; when; what to do on trouble | free (the day's travel) | a day or more | where one is; where one sleeps | travel, sleep at, come to a meeting, a fire on the road |
| **gather** | a technique, a place here | the technique's units | one act | land's stock to hands | firewood, fell, cut, hay, wild food, fish by hand, angle, hunt, stalk, den work, fowling, mine, quarry, cut withies, twist cord |
| **set and lift** | set: a technique and its gear in hand, a place; lift: the thing (or the technique and place) | set: units by the gear; lift: 1 a place | over nights | gear to a place; the catch to hands | snares, wicker traps, lines, fish nets, ret flax; lift re-sets unless told |
| **work** | a technique, a thing or place that stays put | the technique's units | one act | the state of a fixed or living thing | sow, reap, plough, herd, milk, slaughter, dress a kill, repair, mend a weir section, tend the smoke, clear the leat, care for a child, bury, guard the field, write and erase on a building |
| **make** | a technique, a quantity | the technique's units | one act, or a batch over nights | goods to goods | every recipe: salt, dry, smoke, grind, bake, a trap, a net, cord, mend gear, tools |
| **build** | a technique, a place or building, a structure | materials at the start, work over days | days | a fixed thing at a place | rooms, fittings, works (a weir section, a withy bed, pits), upgrades, monuments |
| **move** | goods or a herd, from and to | take 1 unit, others free; drive 1 | one act | who or where goods are held | take, give, put (between one's hands and stores), drive (beasts); hidden (buried, under brush) |
| **change** | a thing one controls, a setting | free | until changed | a setting | a door, a weir's gap, the mill's hatches, who may use a house (host, grant, revoke), a claim, a name, the heir, the children's work, leaving or founding a household, parting, releasing a debt; the `rule` reply field is its free form |
| **agree** | a person, what both choose | each side's units (a lesson 2) | today | something only two can do | an offer accepted, a lesson (teach and learn), partnering, joining and admitting, trying for a child |
| **force** | a person or building, an aim; or a place to guard | 3, or 1 to guard | settled tonight | harm, theft by force, defence | attack (rob, hurt), guard |

Free reply fields stay outside the shapes: speech (`tell`, `say`, `explain`, a meeting called), attention (`attend`, with units),
memory (`note`, `keep`, `drop`), `offers` and `rule`.

### 5.2 The technique named alone

- **The agent names the technique and its target;** the engine knows its shape: `{"do": "smoke fish", "qty": 2}`,
  `{"do": "snares", "at": "the Common"}`, `{"do": "boil salt"}`.
- **The shape is named only where one technique has two:** set and lift (`{"do": "lift", "thing": "T12"}`), build and work on a
  weir (`build` a section, `work` mend it). Named alone, a technique with two shapes takes its first (set, build); the result says
  so when one's own already stand there ("You set 6 more traps in the Isel beside your 6 there (T7); to take their catch, lift T7").
- **A shape named with "what"** (`{"do": "make", "what": "smoke fish"}`) is read the same, so old replies and worlds still run.
- **Resolution** (`knowledge.resolve` widened): a technique by name, alias or label word, preferring one the person knows; then a
  shape; refused with the nearest names the person knows if neither.
- **The schema:** `do` becomes a free string (the enum of 38 verbs goes); the arguments are the union of the shapes'. A reply's
  validity is checked by the resolver, which already refuses with a reason ([[D4-95 What a refusal says|D4-95]]).

### 5.3 The thing as target, own by default ([[Q-80 Whether acts on owned things default to one's own|Q-80]])

1. Every act on a held thing names the thing, by tag (T12, H3) or a name the person knows; one's own things are shown with their
   tags where one is ("your traps in the Isel (T7, 6, set 2 nights ago)").
2. **Unnamed,** an act touches only one's own, a household's things counting as one's own for its members (proposed answer to
   [[Q-80 Whether acts on owned things default to one's own|Q-80]]'s first question):
   - exactly one of one's own at the place: that one;
   - several: a lift takes all of one's own of that technique at the place (the shape is per place); an act that consumes a thing
     (slaughter a beast, take from a pile) is refused, listing the tags;
   - none: refused, saying whose are there ("you have no snares on the Common; T14 there is Oliver's").
3. **Another's, named:** done; the result says it is not one's own ("You took 2 hares from Oliver's snares (T14), which are not
   yours to take from. Whether anyone saw, you will learn.").
4. One's own: what one set or made; one's household's herds, stores, plots and gear; a weir's traps for its crew; what one has been
   given the use of by an agreement.

### 5.4 How the 38 verbs fold

| Verb today | Shape | As | | Verb today | Shape | As |
|---|---|---|---|---|---|---|
| gather | gather, set | snare, trap in water and nets to set | | sleep | go | sleep at |
| work | work | | | set (door, gap) | change | |
| make | make | | | travel | go | |
| build | build | | | watch | attend | with 4 units |
| move | move | put | | teach, learn | agree | a lesson |
| take | move, lift | take; from a set, lift | | attack, guard | force | |
| give | move | give (hidden: buried, under brush) | | fire | go | a fire on the road; and the road's rule |
| accept | agree | an offer accepted | | partner | agree | |
| withdraw | offers field | | | part | change | |
| release | change | a debt released | | try | agree | trying for a child |
| host, grant, revoke | change | who may use a house | | name | change | a name, the heir |
| join, admit | agree | joining and admitting | | order | change | the children's work |
| leave_household, found | change | one's household | | meet | say | a meeting called |
| claim | change | a claim | | come | go | to a meeting |
| drive | move | drive | | write, erase | work | on a building or monument |
| | | | | rest | none | an empty plan |

Nothing is lost: every act today has a shape and a face. Against 37.4's lean list of 24 (proposals/verbs.md), the ten shapes keep
its kinds of change and fold further its membership, settings and consent acts; the verb list itself is still Zach's ([[Q-27 Keep the 38 built verbs, or fold them back to about 22 to 24|Q-27]]).

---

## 6. Generation

### 6.1 The rows

Fifteen livelihoods, as data in one feature unit (`engine/livelihoods.py` with their templates, household_skills Q8):

| Livelihood | Fits | Capital likely / sometimes | Needs / gives | Status |
|---|---|---|---|---|
| farmer | fields by soil | fields, granary floor, bins / ox pair, plough, byre | smith, miller / grain | built |
| herder or dairy | pasture, meadow, fen | herd, grazing held, byre / cellar, hay | salt, hay land / milk, cheese, oxen | built |
| fisher | water, best a river with runs | traps, smoke racks / weir, smokehouse, withy bed★ | salt, withies, cord / fish | built; gear ★ |
| hunter and trapper | wood, scrub, heath, the wild | weapon, snares, far camp / tent, hides | points, salt / meat, hides | built; dressing ★ |
| fowler | fen, flooded meadow, open water | fowling net★ | cord / fowl | as `net`; ★ |
| salter | brine spring or saltmarsh | brine pan in a salt house / saltmarsh pans | copper, fuel / salt | built |
| smith and miner | ore within a day | forge, charcoal / ore claim | charcoal, ore / copper | built |
| miller and baker | a mill site, grain within a day | mill / oven, hand mill | grain, mason, wright / meal, bread | built |
| builder (wright, mason) | managed wood; rock within a day | timber or stone, woodshed / quarry or wood claim | timber, stone / rooms, wheels, hearths | built; building_clock ★ |
| woodsman | managed wood | a wood's claim | buyers / charcoal, poles, firewood | built; coppice † |
| basket maker | wet ground with willow | withy bed★ | / traps, creels, hurdles | ★ |
| cord and nets | a close of good soil; still water or a pit | flax close★ / retting pit★ | / cord, nets | ★ |
| tanner | water, oak wood, hides within a day | tan pits† | hides, bark / leather | † (row now, [[D2-270 Household skills|D2-270]]) |
| trader or carrier | a road with a track; villages 1 to 2 days apart | handcart or pack ox, coin | / carrying | built (always secondary) |
| cottager | a cottage and garden; work to hire | cottage, garden lot / a beast on the common | work / labour | built (work for pay exists) |

### 6.2 Pin and fill

The eleven keyed steps of household_skills §5.2 stand: land; pinned households; unpinned livelihoods by `village_mix` over rows
whose fits hold; capital from livelihoods and livelihoods from capital; the family tree; bands and specialisms; what spouses carry;
neighbours; **the seeded lines rendered from the templates** (§3, against the state of step 4 to 8); the gate check; the cast and
the trade line. Changes from that note:

- **Experts follow household size** ([[D2-270 Household skills|D2-270]]): one for 2 to 4 working members, two for 5 or more, a world may set it; never two in one
  specialism unless set.
- **Apprenticed youths are tried** ([[D2-270 Household skills|D2-270]]): a youth in the older half of youth (about 18 days old or more at lifespan 64) in a house with an expert is apprenticed to that
  specialism by a keyed draw (default 0.5): rough in it, the specialism's first line, and the aim "learn {craft} from {expert}" (the
  aim stays unshown, [[D4-29 No aims for now|D4-29]], but drives the bots and the measurement).
- **Two chokepoints in one household only when the world asks** ([[D2-270 Household skills|D2-270]]); the default draw does not make it.
- **The village rule:** two to five livelihoods that hold capital, cottagers apart (they hold none), at least one chokepoint inside
  and one dependence outside.
- **The head's lines** (§3.4) are rendered in step 9 for each head, against the household's stores at the start.
- **The cast** (scenario_design): the heads and the chokepoints' experts Opus, capable adults Sonnet, broad members and youths Haiku.
- **Couplings off only by explicit setting** ([[D2-270 Household skills|D2-270]]): `skills.couple: {capital_knowledge, livelihood_land, crafts_capital, gates}`,
  each true by default.

### 6.3 Capital and knowledge both ways; the gate check

As household_skills §2: a livelihood fills its capital where the land allows, pinned capital fills its keeper (the expert in the
specialism that works it, or capable in a small house), and holdings seed their lines from their state at the start. The gate check
(household_skills §2.3) gains four rows for part 4:

| Check | Level |
|---|---|
| A seeded line whose condition is false here | the template is skipped (never a generic stand-in) |
| A founder's set over the cap after the drop order | refuse (the templates are too long) |
| A craft known at capable or above with no lesson rows | warn (its failures will only say "your hands") |
| A youth apprenticed to a specialism no one in the household holds at expert | refuse |

### 6.4 Eelmouth remade (the runs world)

**Now** (`runs_high.yaml`): three households on the Isel (a big river reach) with Eelmouth Fen and its brine spring; all six adults
know the same eight crafts at skill 1.6 in the high arm (boil salt, net, salt fish, smoke fish, tend the smoke, trap in water, weir,
and a medium room or the hunt); every adult is "By trade: sowing a field broadcast and reaping a crop" with no fields; each house
has a smokehouse; the Marshes hold the weir, the Fen and the Salt House; the households' system prompts run 4,831 to 5,100 words.

**The fill, step by step:**

1. Land as generated (seed 5).
2. Pinned: the weir to the Marshes (the high arm's chokepoint); nothing else.
3. Livelihoods by fit: the water and the river's runs fit fishers; the spring fits a salter; the fen fits fowling as a second
   living. No fields: no farmer, no sowing lore. `village_mix` draws the Brooks as salters; to keep the default rule against two
   chokepoints in one house, **the Salt House and the Fen's claim go to the Brooks** (in the old world they were the Marshes', which
   with the weir made two).
4. Capital: the Brooks' salt house and pan; the Shepherds' smokehouse kept as the keeping specialism's capital; the Marsh and Brook
   smokehouses kept as `sometimes` capital (both households also smoke).
5. to 6. Members (three working members in each house: one expert each, [[D2-270 Household skills|D2-270]]):

| Household | Livelihoods | Head | Members: band, specialism | Cast | Seeded lines |
|---|---|---|---|---|---|
| **Marsh** | fisher | Peter | Peter: expert, **weir and nets**, keeper of the weir; Nichola: capable, traps and the runs at rough; Nigel (youth, 18 days): broad, apprenticed to the weir; Henry (child), Denise (infant) | Peter Opus, Nichola Sonnet, Nigel Haiku | Peter 19 (BS1 to BS9, PE1, PE2 the pig, HH1, HH3, HH6, HH7, FI1, FI2, FI9, FI12; FI10 when withies are built, displacing PE1; FI3 goes, the keeping being Hamon's); Nichola 19 (BS, PE1, HH1, HH3, FI1 to FI5, FI6, NB-SA); Nigel 9 (five BS, PE1, FI1, FI2, FI9); Henry 0 to 2 |
| **Shepherd** | fisher; second living fowling | Hamon | Hamon: expert, **keeping**, keeper of the smokehouse; Gunnild: broad fisher, broad fowler | Hamon Opus, Gunnild Haiku | Hamon 19 (BS, PE1, HH1, HH3, HH6, HH7, FI1, FI2, FI16, FI17, FI19; FO1 when built makes 20); Gunnild 18 (BS, PE1, PE2 the debt, HH1, HH3, FI1 to FI3, FO2, NB-SA) |
| **Brook** | salter; second living fishing | Oliver | Oliver: expert, **the pan**, keeper of the salt house; Katherine: capable fisher (FI1 to FI3, FI5); Petronel (youth, 14): broad salter; Margery (child), Basilia (infant) | Oliver Opus, Katherine Sonnet, Petronel Haiku | Oliver 20 (BS, PE1, PE2 the pig, HH1, HH3, HH6, HH7, SA1 to SA4, NB-FI; SA6 dropped, no village within reach); Katherine 18 (BS, PE1, HH1, HH3, SA1, FI1 to FI3, FI5, NB-FO); Petronel 7 (five BS, PE1, SA1) |

7. to 8. Katherine married in from Ashby (the tree's origin): her natal broad band and up to three lines would come with her, but
   Ashby is outside the world, so only the people line ("I came to Eelmouth from Ashby when I married Oliver"). Neighbours: each
   house aware of the others' broad bands; the Shepherds rough at salting (they use the Brooks' salt); one NB line each.
9. Rendered: FI1 reads the eel window and the cue; FI6 is kept (the Isel's reach is a big river: salmon); FI7 is dropped unless the
   Isel has lampreys; FI19 renders for Hamon with no road ("Salt comes from the Brooks' Salt House on the Fen; the salter there wants
   firewood and grain"), its second sentence dropped (no farm house in reach); HH2 is dropped everywhere (no fields).
10. Gate check: the weir has a keeper (Peter) and crew (Nichola, Nigel), the smokehouse Hamon, the pan Oliver; every fisher's craft
    has water; no livelihood's fits fail. Pass. The old world fails "a livelihood whose fits fail" for all six adults.
11. Trade lines: "You live by fishing; you are best at the weir and its nets"; "You live by boiling salt at the spring, and fish
    beside it".

**Dependence:** the Marshes take the run at the weir; the Brooks have the salt every keeper needs; the Shepherds keep best and
have the fen's fowl in winter. Each lacks what another holds, where today each house holds everything. **Arms:** today's low,
medium and high become seeded depth (none, half, full) on the same people and holdings, with the weir pinned in or out; the
told-knowledge arm gives every line to everyone in the system text; the less-seeded arms ([[D2-268 The founders' starting knowledge|D2-268]]) are the depth knob.

### 6.5 Hollinford, a mixed village, end to end

A configuration: a middle river with runs (eels, no salmon), clay and loam fields, an oak wood, a wet fen edge with willow, a mill
site; Highpool (the smith) a day up the hill road with a track; Saltwell (the salter) a day downstream.

1. Land: twelve parcels (four fields, two pastures, a meadow, the oak wood, the fen edge, the river, the green, a garden lot).
2. Pinned: none; `village_mix: {farmer: 1.0, miller: 0.4, fisher: 0.5, builder: 0.3, tanner: 0.2, cottager: 0.3}`, `region:
   {smith: 1, salter: 1}`.
3. Livelihoods drawn (keyed): six households.
4. Capital from livelihoods: the mill at the site (the miller's likely), a weir on the river (the fisher's sometimes, drawn), tan
   pits by the ditch below the mill (the tanner's), a withy bed on the fen edge (the basket maker's), a granary floor and an ox pair
   (the farmer's). Pinned none, so nothing fills a keeper backwards.
5. to 8. Members, bands, marriages, neighbours:

| Household | Livelihoods | Holdings | Expert (specialism) | Capable / broad / youth | Cast |
|---|---|---|---|---|---|
| **Field** (7; 5 working) | farmer; herder | four plots, granary floor, ox pair, plough, byre, three cows | Osric (ploughman and oxen), Orabel (seed and harvest) | Baldwin capable herder; Drew, Hawise broad; Hob youth, apprenticed to the plough | Osric Opus (head, the largest land) |
| **Fletcher** (5; 4 working) | miller and baker; farmer | the water mill, an oven, a plot | Hamo (the mill: leat, stones, hatches) | Annora capable (the oven at rough); Alard broad; Piers youth | Hamo Opus (head, chokepoint) |
| **Fenn** (6; 4 working) | fisher; basket maker | the weir upstream of the mill, smoke racks, eight traps, the withy bed | Aldric (weir and nets) | Lucy capable (keeping at rough); Matthew broad, cuts withies; Wilmot youth | Aldric Opus (head, chokepoint) |
| **Mason** (5; 3 working) | builder (mason and wright); farmer | stone and timber in store, a woodshed, a plot | Ralf (the mason) | Emma capable (the wright at rough); Simon youth | Ralf Sonnet (head; no chokepoint inside, but every hearth and the mill's stones need him) |
| **Tanner** (4; 3 working) | tanner; farmer | tan pits below the mill, a plot, hides in store | Godric, an elder (the pits: deepest lines, skill faded toward its floor) | Agnes capable tanner (his apprentice of long standing); Walter broad | Godric Opus (head, the leather everyone's packs and harness need) |
| **Cotter** (4; 3 working) | cottager | a cottage, the garden lot, a cow on the common | none | Tobin, Rose broad (spinning capable); Joan youth | Tobin Haiku |

Rose Cotter married in from the Fenns (`line_born`): she carries the fisher's broad band at rough and FI1 and FI3 in her own voice
("At home with the Fenns we lifted the traps every morning of the run"). Neighbours: each household aware of the others' broad
bands, rough in one (the Fields at grinding, the Fenns at hurdles, the Cotters at reaping); one NB line each, two at most.

9. Rendered lines, from the state at the start:
   - Hamo (head, the mill): BS1 to BS9, PE1, HH1 ("Our store at Fletcher House holds about 14 nights' food for the 5 of us as it
     stands; the winter is 8 nights ..."), HH2 (one plot), HH3, HH6, HH7, MI1, MI3 ("Our mill grinds up to 200 grain at a turn;
     the leat silts and wants clearing once a year, the stones dressing after about 2,000 grain. The leat was cleared last autumn."),
     MI4, NB-FA: 19 lines (numbers today's engine rows).
   - Aldric (head, the weir): BS, PE1, HH1, HH3, HH6, HH7, FI1 to FI3, FI9, FI10 (when withies are built), FI12 ("Our weir stands
     first on the Holl: 2 sections of wattle, sound; Fletcher Mill lies below it."): 20, HH5 dropped by the cap.
   - Godric (elder head, the pits): BS, PE1, PE3 ("I have seen 3 hard winters ..."), HH1, HH3, HH6, HH7, TA1 to TA5 (when tanning is
     built): 20; the farm's lines go to Agnes and Walter, his NB line by the cap.
   - Osric (head, ploughman): BS, PE1, HH1, HH2, HH3, HH6, HH7, FA1 to FA3, FA6, FA7 ("Our oxen plough a plot in 2 units where a hoe
     takes 6 ..."): 20; FA9 and NB-MI dropped by the cap.
   - Tobin (head of a cottage): BS, PE1, HH1, HH3, HH6, HH7, CT1, CT2 ("The Fields want hands at reaping, the Fenns at the runs
     ..."), CT3, NB-FA: 18.
   - The village's 22 working members carry about 340 lines, about 13,000 words, against today's text of about 5,000 told to each.
10. Gate check:
   - Every holding has a keeper (the mill Hamo, the weir Aldric, the pits Godric, the bed Matthew at broad: warn, a withy bed wants
     capable; the fill raises him to capable in cutting withies).
   - The mill's batch passes only with "up to" ([[D2-247 A process of bulk goods has a most it takes at once, not a least|D2-247]]): the Fields' granary holds about 150 at harvest.
   - The pits below the mill foul the water below them: the Fenns' weir is upstream, so no harm to the fishery; TA5 renders "the
     Fenns fish upstream of us; downstream there is no one".
   - Salt and copper are a day off (Saltwell, Highpool): warn, a designed dependence.
   - The tanner's hides: the Fields' slaughter and no hunter within a day: warn (hides only from the herd).
   - Pass, with three warnings.
11. Cast and trade lines as the table.

**Dependence and leverage:** the mill needs the Fields' grain and the Fields need the mill to make grain go further; the weir above
the mill shares the eels with the mill's hatches (MI4, FI9); the tanner needs the Fields' hides and the oak wood's bark, and gives
the leather for packs and the smith's bellows; the Masons are needed by every hearth, the oven and the mill's stones; the Cotters
are the hands at reaping and the runs. Inside, three chokepoints (the mill, the weir, the pits), one each; outside, salt and
copper.

### 6.6 The arms this generation makes

The same seed with: seeded depth full, half, base, none ([[D2-268 The founders' starting knowledge|D2-268]]'s less-seeded arms); the told-knowledge arm (every line to all, in
the system text; [[D2-266 Knowledge in their own words|D2-266]], early testing only); experts differ on or off; marriage carries on or off; one cultural strand at a time
(BS8's passing on first); a coupling turned off by explicit setting ([[D2-270 Household skills|D2-270]]), run once as a fault arm. Each read against the null
arm and a qualitative end-state reading (scenario_design).

---

## 7. Couplings to parts 1 to 3

What part 4 reads, from whom, and for what. "Part 1" is the physical basis ([[W-77 Design wave part 1, the physical basis|W-77]]); "part 2" materials and making; "part 3" taking
and keeping.

| Thing | Kind | From | Part 4 reads | Used in |
|---|---|---|---|---|
| shelf life of each food on the year clock, in hand and by store | table | 1 | days to half, by store kind | BS3, FI3, FI16, HU4, MI1, TA1, HH3 |
| weights in kg; the carry by foot, pack basket, pack ox, cart | table | 1 | the carry figures | HU2, SA6, TR2, BA3 |
| each recipe and work in hours and units, by clock | table | 1 | units for the craft lines | §2.2 craft lines; FA7 |
| gear lives by material | table | 1 | uses a piece lasts | BS9, FI11, the craft lines |
| withies | good, crafts (cut withies, plant a bed) | 2 | season yields, the bed's years | FI8, FI10, BA1, BA4, BA5; the fisher's and basket maker's crafts |
| cord, flax, retted flax | goods, crafts (twist, sow, pull, ret, dress and spin) | 2 | rates, seasons, cord per net | FI11, CO1 to CO5, FO4, HU7 |
| bone, hide, tallow, offal | goods; dressing the kill | 2 | what a careful hand takes | HU8, FI14, TA1 |
| wicker trap, snares, line, rod, bone and copper hooks, fish net, fowling net, creel, pack basket, hurdle | gear | 2 | inputs, units, life, mend | the craft lines; FI13, BA2, BA3 |
| mend gear | craft | 2 | its share of materials | the craft lines; BS9 |
| a weir section by material; its wear by flow | work | 2 | materials, units, wear | FI10, FI12; the build line |
| leather and tanning | goods, craft (k) | 2 | the pits' time, bark, uses | TA2 to TA5 |
| the builder's rates and craftsmanship's wear | building_clock | 2 | units by skill; wear by skill | BU4; the build lines |
| seasoning, coppice and standards | the timber economy ([[W-76 The timber economy|W-76]]) | 2 | seasons, cycle | BU5, WO4 |
| the charcoal burn as a process | craft | 2 | nights, watching | WO3 |
| every craft row's learning fields | per row | 2 | class or curve, lessons (lines and short forms), points, profile, `acts_on`, `uses` | §4 entire; §2.2 |
| the universal flag | per row | 2 | which crafts any adult has | §2.2 |
| set and lift as two faces | methods | 3 | per place lift, re-set | the set-and-lift shape; FI2, HU1 |
| the runs, the shallows, the resident stock | stocks | 3 (and today's `RUNS`) | windows, cues, renewal | FI1, FI5 to FI7, FI15 |
| fowl seasons, the freeze, flight lines | methods | 3 | seasons, crowding | FO1, FO3, FO5 |
| smoking in three depths; salting rate ([[Q-73 Whether salting fish and meat stays at 4 kg a unit of work|Q-73]]) | keeping | 3 | nights, keeping times | FI16 to FI18, SA5 |
| stores and containers (sacks, baskets, bins, chests, granary, cellar, sealed pit, smoke loft, woodshed) | holdings ([[D2-279 Stores, as answered|D2-279]]) | 3 | capacity, what each protects, vermin exposure | HH4, HH5, BU3; the rules block |
| vermin and their signs | process ([[D2-279 Stores, as answered|D2-279]]) | 3 | exposure by container | HH4 |
| the book of standing rules' records | rules ([[D2-274 One book of standing rules per household and per person covers both…|D2-274]]) | 3 and 37.4 | the rules as the engine reads them | §2.4; HH2, HH3, HH5 |
| pollution from retting, tanning | process (§7.5) | 3 | which water, how long, downstream | CO3, TA5; the gate check |
| the withy bed, flax close, retting pit, tan pits | works | 2 and 3 | state at the start | BA5, CO2, CO3, TA5 |
| experts' signs (the "knows" audience) | senses | 3 and 37.4 | which signs a point or level opens | §4.7; attention with units |

Part 4 asks part 2 to put the learning fields on every craft row it writes (one row, one feature unit, [[D2-244 The engine's reworking into feature packages|D2-244]]), and part 3 to give
each holding a state a template can read at the start (its wear, its fill, its last tending).

---

## 8. Open questions

1. **The core's knowledge line** (core 8): it says only that one knows what one has learnt; that knowledge dies unless passed is
   BS8's line and the first cultural strand, so the strand can be run against its absence. Agreed, or should the core state it as a
   fact for all?
2. **The core's size:** 363 words of core and 192 of reply, about 555, slightly over the 500 named ([[Q-81 Knowledge in their own words|Q-81]]). Keep as drafted, or cut
   lines 11 and 12 into the shapes' grammar to reach 500?
3. **Ten shapes as the verb list** ([[Q-27 Keep the 38 built verbs, or fold them back to about 22 to 24|Q-27]]): go, gather, set and lift, work, make, build, move, change, agree, force, with the technique
   named alone and `do` a free string. Adopt, or keep 37.4's 24 with techniques as objects?
4. **The founders' cap:** 20 seeded lines and about 800 words, with the head's lines inside it and the drop order of §3.2. Or let
   heads run to 24?
5. **Known needs every lesson** (§4.2): the lessons become the content of a level (rough needs the main input, known all of them,
   skilled the taught one), beside the score. Or keep score alone and lessons as explanation only?
6. **Seven aptitudes, strength left out** (§4.8), at most a third's head start; inherited aptitude off. Agreed?
7. **Children minded at home** (§4.5): aware of what their household did at home each night, rough in a simple craft done often,
   no lore unless passed. Or children learn nothing until they act?

## Sources

`cybertron2/engine/prompt.py` (system_prompt, verb_lines, REPLY_LINES, turn_prompt, _memory_sections), `knowledge.py` (seed, curve,
card, crafts_lines, tried, saw), `memory.py` (KEPT, places, seed_line, come_of_age), `perceive.py` (seed_knowledge), `life.py`
(care_gifts, STAGES), `verbs.py` (VERB), `data.py` (TECHNIQUES, TRY, SKILL, FITTINGS, LIFE), `world.py` (agents_acting),
`wild/kinds.py` (RUNS, ROB_SETS, RUN_SIGNS), `landgen/write.py` (FARMING, TRADES), `specs/nutrition/runs_high.yaml` (agents,
buildings, history, tree), its system prompts rendered for all eight acting people (4,831 to 5,100 words); proposals
knowledge_in_their_own_words.md, trying_and_learning.md, verb_grammar.md, acts_on_owned_things.md, store_rules.md,
livelihood_archetypes.md, standing_rules.md, verbs.md, hunt_fish_materials.md; this folder's founders_knowledge.md,
household_skills.md (and addendum), crafts_evaluation.md, learning_times.md, building_clock.md; DECISIONS [[D2-263 A craft a person knows at capable or known shows, where they look|D2-263]], [[D2-266 Knowledge in their own words|D2-266]] to [[D2-270 Household skills|D2-270]],
[[D2-273 Three clocks, each system on one|D2-273]], [[D2-274 One book of standing rules per household and per person covers both…|D2-274]], [[D2-277 Every idea explored in conversation is written down before moving on|D2-277]] to [[D2-279 Stores, as answered|D2-279]]; OPEN [[Q-27 Keep the 38 built verbs, or fold them back to about 22 to 24|Q-27]], [[Q-73 Whether salting fish and meat stays at 4 kg a unit of work|Q-73]], [[Q-80 Whether acts on owned things default to one's own|Q-80]] to [[Q-82 Trying and learning|Q-82]], [[L-133 The engine as feature packages postponed, kept in mind|L-133]], [[L-141 How much seeded memory each livelihood starts with|L-141]], [[L-142 Fallbacks as a person's standing setting|L-142]], [[L-145 Offal's uses bait for set lines and traps, dog food|L-145]], [[L-151 A household as a shared book of standing rules people subscribe to|L-151]], [[L-156 The locked chest and its key|L-156]].

*Current as of 22 Nov 2026.*
