# W-109: the interface from one registry: report (24 Nov 2026, session 37.2, build subagent)

Brief: `iface_brief.md` (with its Amendment D2-351, Correction D2-352 and Resume, which bind). Branch `w109-interface` in the
worktree `/home/user/c2-iface`, not pushed or merged. Rules built to: D2-350, D2-351 (as corrected by D2-352), D2-352, D2-353,
D2-355, D2-356, D5-2; D2-314, D2-263, D2-286, D2-339 kept. Renders beside this report: `iface_renders/` (Osric of World 0b and
Peter of Eelmouth: `*_before.txt` the rebuilt core on `main` before W-109, `*_after.txt` the core now, `*_old_prompt_after.txt`
the same people under the old prompt now).

## What was done, by item

| Item | What was built | Where | Commits |
|---|---|---|---|
| 1. One registry, read by the renderer | Every act's interface as data on its row: `verbs.VERB[v]["iface"]`, one or more faces each with its shape, the word said in "do" (or the "what" it is said with), its arguments (key, required, what it is, every option with what it does, who sees the argument), what it does, what it needs, its cost where the row's is not a number, and who is shown it (conditions named in `iface.WHO`). The crafts' fields stay on `data.TECHNIQUES` (`does`, `args`, `who`, the recipe fields D2-263 shows); the ways' on their modifier rows (`key`, `value`/`values`/`takes`, `does`, `changes.units`). The loader check `iface.check()` raises `RegistryError` naming the first act, craft, way or shape face without its fields (run at load and in the tests). | `verbs.py`, `data.py`, `iface.py` | 767c3ccc, 67d1e777, 1df4f0da |
| Amendment and Correction (D2-351, D2-352) | Shown only once familiar (aware or above); the set everyone knows as data (`verbs.EVERYONE`, and the basic crafts); aware is the name and who does it, apart ("known of, not how"); a rough idea gives how it is said with its required arguments, what it needs and a rough recipe, no cost; known or capable, and everyone's set, the full line (every argument and option, cost, recipe and batch, tool effects, the ways learnt). | `iface.familiar`, `iface.craft_line`, `iface.lines` | 767c3ccc, df12559b |
| 2. World out of the interface | Each craft's `does` written in interface words (54 rows); the season, "anywhere" and the labels' kinds left out of the interface (D5-2); the techniques' `manual` and `note` (yields, keeping times, "best when things run", "in their season") are no longer read by the interface, only by the old prompt. D2-356's `world` field holds the labels' world words (below). | `data.py`, `wild/methods.py`, `process.py`, `iface.py` | df12559b, 6973f2d3 |
| 3. The renderer | `iface.lines` replaces `shapes.lines`: the eleven shapes with their grammar lines; under each, every act's face and every craft of the person's on a line of its own at their familiarity's detail; the family and social acts listed like any other; go's four acts each on their own line; crafts only known of apart; `rules` the only way to write a rule (the old rule act's face retired, D2-339); `look_up` back in the reply format and schema; ways stated once per key across shapes ("as under gather"). | `iface.py`, `core.py`, `shapes.py`, `prompt.py` | 67d1e777, 3762cbbd, 1df4f0da, df12559b |
| 4. Who sees what | The conditions are the registry's (`who` on a face, an argument or a craft, read from `iface.WHO`: grown, not youth, head, household, children, roads, herds, evening, tags, gap, sets), never ad hoc in the renderer. | `iface.WHO`, `iface.allowed` | 767c3ccc, 1df4f0da |
| 5. Tests | `tests/test_cybertron2_w109_interface.py`, 23 tests: coverage of every handler, argument, option and way in some fixture person's prompt; the loader check; familiarity (aware a name, rough the minimum interface, known the full line); only what one is familiar with shown; every required argument shown without "?"; who sees what; D2-356's fields; each World 0b fault; live run 1's lessons. Fixtures: World 0b (`tests/fixtures/world0b_sonnet55.yaml`, session bench's spec: Osric, Orabel, Jocelin, Alice, Hawise, and Alice again as a lone grown person after leaving her household) and Eelmouth (Peter, Nigel, Nichola, Gunnild, Oliver). | tests | b4fb5cd3, later |
| The wave's regressions 2, 3, 10, 11 | The gear line in the beliefs view from one source; crafts keep their hint and source; waiting today each morning; the old rule act's kinds retired from the old prompt. | `here.py`, `knowledge.py`, `view.py`, `prompt.py` | a75c97b2 |
| D2-356 | Every bracketed label split into its name and a field (table below); rendered together by `knowledge.titled` (the old prompt and its cards), `knowledge.named` (the interface's cards by level) and the interface's craft lines; every split on " (" of a label retired (`knowledge.label`, `knowledge._place_words`, `iface.known_of`, `generate.py` twice, `make_wild_region.py`, `verbs._order`); the slicing of composed lines by length replaced by their parts (`knowledge.craft_parts`, `prompt.craft_bits`, `prompt.craft_note_words`); the loader check refuses a label with a bracket. | `data.py`, `gear.py`, `process.py`, `stores.py`, `wild/methods.py`, `knowledge.py`, `iface.py`, `prompt.py`, `modifiers.py`, `shapes.py` | 6973f2d3 |
| World 0b's faults (L-189) | Each below, with a test. | below | 6973f2d3, 7b373edd |
| 6. Replay | Live run 1's 2,509 acts replayed through the shapes' parser and the handlers, before and after. | below | 63894fa7 |
| 7. Suite and bot run | The six shards once at the end; a 4-day bot run of Eelmouth. | below | |

## The registry's fields and where each lives

| Field | Acts (`verbs.VERB[v]["iface"]`, per face) | Crafts (`data.TECHNIQUES[t]`) | Ways (modifier rows of `TECHNIQUES`) |
|---|---|---|---|
| shape | `shape` (one of the eleven) | from `verb` and `set` (`shapes.shape_of`) | the shape of what it `modifies` |
| how it is said | `word` (or `what` for a face said with it, the build's upgrade) | its key or its set noun (`placed.NOUN`) | `key`: `value`, `values` or `takes` |
| name | the face's word | `label`: the name only (D2-356) | `label` |
| what it does | `does` | `does`, else the name | `does`, else the label |
| arguments and options | `args`: `{key, req, is, opts: {option: what it does}, who}` | `args` where it takes more than its shape's | the value or values |
| cost | the row's `cost`, or the face's `cost` where the row's is not a number | `units` (or `hours` and the world's clock) | `changes.units` |
| what it needs | `needs` | `requires` (D2-356) and, derived, a tool (`tools` without bare), others with you (`crew`), the place (`at`), the materials (`inputs`) | `requires` (lead, lead on the hunt) |
| know-how | | `hint` (D2-356: known and capable), `tools`/`gear`/`gear_x` (what a tool does: known and capable), batch | `untaught` |
| world | (none) | `world` (D2-356: the old prompt only), `manual`, `note` | |
| who is shown it | `who` (names in `iface.WHO`); `verbs.EVERYONE` the set everyone knows | familiarity (`mind.know`), `basic`, `who` | familiarity, `untaught: tryable`, `shown_in` |
| things built | | from the blueprint, fitting or monument | |
| fittings, rooms, monuments | | | `about` (D2-356: what it is) |
| the shapes | `shapes.SHAPES[s]`: `args`, `line`, `faces` (each must name an act or an alias: checked), `techs`, `recipe`, `ways` | | |

The set everyone knows (D2-351, `verbs.EVERYONE`, 36 acts): accept, admit, attack, build, claim, come, drive, erase, fire, found,
give, grant, guard, host, join, learn, leave household, meet, move, name, order, part, partner, release, rest, revoke, set, sleep,
take, teach, tend, travel (go), try, watch, withdraw, write; and every basic craft (`basic: True`) of the world's packs. Each is
still shown only where its `who` holds (admit and order for a head; try, partner, found, attack, host for the grown; drive where
there are herds; tend where one has set gear; meet and come in a world with evenings).

## What lacked a field, and what was written

- **Every act** (40 rows of `verbs.VERB`): none had an interface; each got its faces (commit 767c3ccc); `verbs.VERB[v]["doc"]` and
  `args` stay for the old prompt.
- **`does` written for 54 crafts and ways**: forage, ditch, terrace, gather wild food, range: near, range: the wood around, range:
  far, hunt with, hunt alone, hunt only with, looking for, wall, boil salt, salt fish, salt meat, hidden: under brush, hidden: buried,
  method: dibble, method: cairn, how: fine, how: rich, how: grand, method: shallow, on trouble, stop at, meeting, gather on the way,
  lead, lead on the hunt, searching, mend gear, smoke fish, smoke meat, hard cure fish, hard cure meat, hot smoke fish, hot smoke
  meat, dry meat, dry fish, ret flax, hunt the wild, stalk, drive, snare, net, trap in water, gill net, set line, den work, gather
  young, pest work, break a dam, guard the field, shut.
- **`args`** (11): sow (item, always said: its seed; plots; on), care (at, item, qty, pass), slaughter (item), bury (at), burn (at),
  weir (with: the crew), mend gear (item), snare, trap in water, gill net, set line (qty, from the set shape).
- **`who`** (1): care (where there is a child). **`takes`** (9): hunt with, hunt alone, hunt only with, looking for, stop at, gather
  on the way, lead, lead on the hunt, searching.
- **D2-356's fields** (62 rows, the table below).

## World facts moved out of the interface

- The season a craft is best in (`by_season`: "best in winter"): left out of the interface's craft lines; kept in the old prompt.
- "anywhere" as a place: left out.
- The labels' world words, into `world` (shown by the old prompt only): forage (greens, roots, berries, nuts), gather wild food
  (what is in season where you are: greens, berries, nuts, fungi, roots), looking for (boar, deer, hares, fowl, small game), salt pan
  (dried by the sun; the seeded line SA7 already tells the pans' season), hard cure meat (bacon, ham).
- The techniques' `manual` (yields and keeping: "10 kg a unit gives 6.7 kg ... keeping about a week", "about 1 firewood a salt, in
  any season") and `note` ("best when things run", "in their season", "a herd or sounder"): no longer read by the interface, whose
  `does` says what doing it does; the old prompt keeps them. What a craft gives reaches a person as the engine's own report when it
  is done, and through the seeded lines where a founder's template covers it.

## D2-356: each technique's bracket, and the field it went to

The choice per row (a default taken; see the questions): `requires` where the act cannot be done without it (interface, shown from
a rough idea up), `hint` where it says how it is done well (know-how, shown at known and capable; always in the old prompt), `world`
where it is what lives or grows or what the world gives (out of the interface), `about` for what a fitting, room or monument is
(shown as the build's hint; in the old prompt beside the fitting's name).

| row | name (label) | field | words | kind |
|---|---|---|---|---|
| forage | foraging | `world` | greens, roots, berries, nuts | world: out of the interface; the old prompt keeps it |
| firewood | gathering firewood | `hint` | dead wood, by hand | know-how (known and capable; the old prompt always) |
| clear | clearing new ground for a field | `hint` | turf, roots and stones out | know-how (known and capable; the old prompt always) |
| cut withies | cutting withies | `hint` | green rods for wattle and wicker | know-how (known and capable; the old prompt always) |
| sow | sowing a field broadcast | `hint` | seed thrown | know-how (known and capable; the old prompt always) |
| herd | herding | `hint` | watching the beasts | know-how (known and capable; the old prompt always) |
| care | caring for a child | `hint` | feeding, minding, keeping it warm | know-how (known and capable; the old prompt always) |
| gather wild food | gathering wild food | `world` | what is in season where you are: greens, berries, nuts, fungi, roots | world: out of the interface; the old prompt keeps it |
| make clappers | making clappers for scaring beasts off a field | `hint` | two boards on a cord | know-how (known and capable; the old prompt always) |
| range: the wood around | hunting out through the woods and wastes around | `hint` | about 2.5 km | know-how (known and capable; the old prompt always) |
| range: far | hunting far out into the wild land beyond | `hint` | a long day | know-how (known and capable; the old prompt always) |
| hunt alone | hunting alone: no one joins your hunt | `hint` | others may join it unless you say so | know-how (known and capable; the old prompt always) |
| looking for | looking for one thing in particular: name it, a kind or a sort | `world` | boar, deer, hares, fowl, small game | world: out of the interface; the old prompt keeps it |
| fence | fencing a parcel round | `hint` | wattle or post and rail | know-how (known and capable; the old prompt always) |
| wall | walling a parcel round | `hint` | a dry-stone wall | know-how (known and capable; the old prompt always) |
| milk | milking | `requires` | a cow in milk | interface: what it needs (from rough up) |
| dress millstones | dressing worn millstones | `hint` | recutting their furrows | know-how (known and capable; the old prompt always) |
| clear for building | clearing ground for building | `hint` | turf, roots and stones out | know-how (known and capable; the old prompt always) |
| fish by hand | fishing at the edge | `hint` | by hand, with a spear or a hand net | know-how (known and capable; the old prompt always) |
| angle | fishing with a line | `requires` | a hand line, or a rod and line | interface: what it needs (from rough up) |
| salt pan | making salt in the saltmarsh pans | `world` | dried by the sun | world: out of the interface; the old prompt keeps it |
| mend the brine pan | mending a burnt-through brine pan | `hint` | patching and resetting it | know-how (known and capable; the old prompt always) |
| for | doing it for someone | `hint` | into their store, from it by right or agreement | know-how (known and capable; the old prompt always) |
| method: dibble | dibbling seed | `hint` | set by hand, seed by seed | know-how (known and capable; the old prompt always) |
| how: fine | building it finely | `hint` | materials x1.5, work x2; seen from next door | know-how (known and capable; the old prompt always) |
| how: rich | building it richly | `hint` | materials x2.5, work x4; named to all who come | know-how (known and capable; the old prompt always) |
| how: grand | building it grandly | `hint` | materials x4, work x8; seen from the road coming in | know-how (known and capable; the old prompt always) |
| method: shallow | burying it shallow | `hint` | half the digging; beasts may dig it up | know-how (known and capable; the old prompt always) |
| burn | burning a carcass | `requires` | firewood and work by its size | interface: what it needs (from rough up) |
| lead | leading a pack ox | `requires` | an ox of your household's, with a harness | interface: what it needs (from rough up) |
| lead on the hunt | leading a pack ox on the hunt, to carry the kill home | `requires` | an ox here, a harness in hand | interface: what it needs (from rough up) |
| creel | making a creel | `hint` | a fish basket on the back | know-how (known and capable; the old prompt always) |
| keep box | making a keep box | `hint` | a wicker box to hold fish alive in the water | know-how (known and capable; the old prompt always) |
| hurdle | making hurdles | `hint` | woven wattle panels | know-how (known and capable; the old prompt always) |
| set lines | making a set line | `hint` | a line of about 30 hooks | know-how (known and capable; the old prompt always) |
| snares | making snares | `hint` | a noose and tether of cord | know-how (known and capable; the old prompt always) |
| gill nets | making a gill net | `hint` | netting twine, with sinkers | know-how (known and capable; the old prompt always) |
| dip net | making a dip net | `hint` | a hoop net on a pole | know-how (known and capable; the old prompt always) |
| sack | making a sack | `hint` | woven of cord | know-how (known and capable; the old prompt always) |
| salting tub | making a salting tub | `hint` | a hollowed log or boards, hooped | know-how (known and capable; the old prompt always) |
| barrel | making a barrel | `hint` | staves and hoops | know-how (known and capable; the old prompt always) |
| mend gear | mending gear | `hint` | traps, nets, lines | know-how (known and capable; the old prompt always) |
| hard cure meat | hanging salt meat for a hard cure in a timber or stone smokehouse | `world` | bacon, ham | world: out of the interface; the old prompt keeps it |
| hot smoke fish | hot-smoking fish over a fire | `hint` | cooked, to eat cold or carry | know-how (known and capable; the old prompt always) |
| hot smoke meat | hot-smoking meat over a fire | `hint` | cooked, to eat cold or carry | know-how (known and capable; the old prompt always) |
| tend the smoke | tending a smokehouse fire | `hint` | feeding and banking it for the night | know-how (known and capable; the old prompt always) |
| ret flax | retting flax | `hint` | laid in still water, or spread on the grass | know-how (known and capable; the old prompt always) |
| chest | making a chest | `hint` | an ark of boards | know-how (known and capable; the old prompt always) |
| stalk | stalking a beast that keeps to its paths | `hint` | slow, downwind, close in for the shot | know-how (known and capable; the old prompt always) |
| drive | a drive | `requires` | others with you | interface: what it needs (from rough up) |
| drive | a drive | `hint` | beaters and spears; dangerous | know-how (known and capable; the old prompt always) |
| den work | digging out a den or trapping at a lodge | `hint` | spades and a dog help | know-how (known and capable; the old prompt always) |
| pest work | working the pests off a crop | `hint` | picking them off, pinching out the tops | know-how (known and capable; the old prompt always) |
| shut | shutting the hens and the store up for the night | `hint` | the doors wedged, the gaps stopped | know-how (known and capable; the old prompt always) |
| owl hole (fitting) | an owl hole | `about` | a gap left high in a barn's gable | what the thing is (the build's hint; the old prompt's fitting name) |
| smoke racks (fitting) | smoke racks | `about` | hurdles over a smouldering fire | what the thing is (the build's hint; the old prompt's fitting name) |
| brine pan (fitting) | a brine pan | `about` | a shallow pan over a furnace, for boiling salt | what the thing is (the build's hint; the old prompt's fitting name) |
| smoke loft (fitting) | a smoke loft | `about` | hooks in the roof over the hearth | what the thing is (the build's hint; the old prompt's fitting name) |
| small room (room) | a small room | `about` | wattle, timber or stone | what the thing is (the build's hint; the old prompt's fitting name) |
| medium room (room) | a medium room | `about` | timber on stone, or stone | what the thing is (the build's hint; the old prompt's fitting name) |
| hall (room) | a hall | `about` | timber on stone, or stone | what the thing is (the build's hint; the old prompt's fitting name) |
| camp (room) | a camp | `about` | a lean-to and a fire ring | what the thing is (the build's hint; the old prompt's fitting name) |
| weir (monument) | a fish weir | `about` | stakes and wattle across the river, wicker traps in its gap | what the thing is (the build's hint; the old prompt's fitting name) |

## World 0b's faults (session bench's refusals, L-189)

| Fault | Kind | What was wrong | Fix | Test |
|---|---|---|---|---|
| "sleep: there is no building called None here" with no sleep in the reply | parse | a sleep act with no building ({"do": "sleep"}, {"do": "go", "what": "sleep"}) was handed to the handler as `at: None`, while the line says "you sleep at home unless you say otherwise" | sleep's "at" is optional in the registry ("a building here (else your home here)"); with none named, one's home here; with no home, "say where" | `test_sleep_with_no_building_named_is_sleep_at_home_and_home_is_ones_house` |
| "home", "my house" not a building | resolver | `here.building` knew only names | `data.SELF_NAMES` (one table: one's own hands, home, store, self), read by `here.own_word` and `here.building`; "X store" is X's store | same; replay |
| move "to": "my hands" or "me" read as racks | resolver | five tuples of hand words in `verbs.py` and `book.py`, none with "my hands" | the tuples replaced by `SELF_NAMES["hands"]` | `test_goods_moved_to_my_hands_or_me_go_to_the_hands_never_racks` |
| foraged greens and mushrooms refused when stored as "wild food" | resolver | `verbs.item_of` mapped "greens" to the old worlds' good "wild food", and "wild food" named no kind | a good of the world is itself (the alias map only for words that are not goods); "wild food" a kind in `book.KIND_GOODS` (the plants' goods, `wild/plants.py`, with the old good); `move` and `give` with a kind put each good of it held (`verbs._of_kind`) | `test_foraged_greens_and_mushrooms_are_stored_as_wild_food` |
| a rule's "for": "my household" not read | parse | `book.read` took only "household" or "me" | `book._whose`: one's own words (`SELF_NAMES`), the household's name, one's own name | `test_a_rules_for_my_household_or_the_households_name_is_read` |
| burial not shown; "bury" not an act | interface | the move shape's face "bury" named no act, so "bury" never reached the craft of burying the dead (shown under work: `- bury {"at": the body}`) | the face removed; "bury" with goods named is hiding them buried (`verbs.ALIASES`, an alias now names the field it needs); the loader check refuses a shape face that names no act ("put down" also named none: now an alias of give) | `test_bury_is_the_craft_of_burying_the_dead_and_every_face_names_an_act` |
| "say" put among the actions | parse | a reply field written as an act was refused | `shapes.reply_fields`: an act whose "do" names a field of the reply schema (say, tell, explain, offers, attend, look up, note, pin, open, forget, rules; never an act, an alias or a face, nor the stretch's memory fields) is moved to that field, its item read from the schema's properties, with a note telling the person; in the day and the evening | `test_say_and_other_reply_fields_put_among_the_actions_are_read_as_those_fields` |
| a lesson without its fields ("say the lesson") | interface | the refusal named a grammar the prompt does not show ({"do": "agree", "what": "teach" or "learn", "line": ...}); a teach or learn with no craft refused as "None is not something you can teach" | the refusal gives the two faces as the prompt says them, from the registry; an act refused because a required argument was read as None is told which, from its face (`verbs._missing`: 'say a craft you know in "what"') | `test_a_lesson_or_an_act_without_its_fields_is_told_them_from_the_registry` |

Bench's own fix (an unnamed slaughter fell to a neighbour's herd, `farm._herd_on`, W-202) is on bench's branch and was not reviewed
here (Not done).


## Prompt sizes, per section and person (words)

Before: the rebuilt core on `main` when W-109 branched (a217daab); after: this branch. The old prompt for the same people: Osric
7,357 words, Peter 7,260 (about 7,200 as the brief said). "What you can do" splits into the acts' lines, the crafts' lines, the
ways' lines and the "known of" lines.

| person | who and people | core and rules | what you can do: before / after | of it: acts / crafts / ways / known of | other places | reply | total: before / after |
|---|---|---|---|---|---|---|---|
| w0b: Osric | 244 | 551 | 890 / 4980 | 1613 / 2559 / 360 / 113 | 114 | 227 | 2006 / 6116 |
| w0b: Orabel | 234 | 554 | 906 / 4882 | 1558 / 2522 / 354 / 113 | 114 | 227 | 2015 / 6011 |
| w0b: Jocelin | 203 | 551 | 951 / 5017 | 1523 / 2693 / 364 / 102 | 126 | 228 | 2039 / 6125 |
| w0b: Alice | 193 | 554 | 759 / 4779 | 1468 / 2511 / 363 / 102 | 126 | 228 | 1840 / 5880 |
| w0b: Hawise | 228 | 554 | 786 / 4195 | 1162 / 2231 / 354 / 113 | 114 | 227 | 1889 / 5318 |
| eel: Peter | 170 | 551 | 924 / 5009 | 1578 / 2686 / 364 / 46 | 44 | 228 | 1897 / 6002 |
| eel: Nigel | 136 | 554 | 732 / 4099 | 1127 / 2271 / 320 / 46 | 44 | 228 | 1674 / 5061 |
| eel: Nichola | 127 | 554 | 865 / 4838 | 1523 / 2576 / 358 / 46 | 44 | 228 | 1798 / 5791 |
| eel: Gunnild | 152 | 554 | 707 / 4659 | 1523 / 2386 / 345 / 70 | 0 | 228 | 1621 / 5593 |
| eel: Oliver | 167 | 551 | 820 / 4888 | 1578 / 2609 / 342 / 24 | 0 | 229 | 1747 / 5835 |

| person | go | gather | set | tend | make | work | build | move | change | agree | force |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Osric | 380 | 630 | 128 | 93 | 1138 | 924 | 521 | 316 | 481 | 249 | 97 |
| Orabel | 380 | 575 | 128 | 93 | 1138 | 936 | 521 | 316 | 444 | 231 | 97 |
| Jocelin | 380 | 644 | 191 | 93 | 1212 | 884 | 537 | 281 | 426 | 249 | 97 |
| Alice | 380 | 587 | 165 | 93 | 1138 | 891 | 504 | 281 | 389 | 231 | 97 |
| Hawise | 380 | 573 | 128 | 93 | 1134 | 944 | 167 | 316 | 214 | 158 | 65 |
| Peter | 380 | 611 | 191 | 93 | 1178 | 888 | 537 | 281 | 481 | 249 | 97 |
| Nigel | 380 | 540 | 215 | 93 | 1140 | 833 | 157 | 281 | 214 | 158 | 65 |
| Nichola | 380 | 526 | 205 | 93 | 1179 | 835 | 544 | 281 | 444 | 231 | 97 |
| Gunnild | 380 | 495 | 165 | 93 | 1104 | 842 | 504 | 281 | 444 | 231 | 97 |
| Oliver | 380 | 586 | 165 | 93 | 1124 | 888 | 521 | 281 | 481 | 249 | 97 |

Where the words go: the crafts everyone knows, shown in full as D2-351 asks, are most of it: Osric is shown 71 of them in 1,898
words, against 22 of his own crafts in 661; Hawise 63 in 1,725 against 16 in 506. The make shape (about 1,100 words for everyone)
is mostly everyone's makings. The acts' lines (about 1,100 to 1,600 words) carry every argument and option. The rebuilt core's
2,000 words were small because it showed little (prompt_compare.md); the interface now is about 6,000, under the old prompt's 7,300
and without its world. A leaner rendering of everyone's crafts is a question below.

## The coverage test

`test_every_handler_with_every_argument_and_option_reaches_someone_who_can_use_it` and
`test_every_way_and_its_values_reach_someone_who_knows_it`: every act's face, with every argument and option, is in the prompt of a
fixture person its conditions allow; every way with its values in the prompt of one who knows it. The table (made by the test's own
logic over the eleven fixture people; "first fixture" is the first in order whose prompt carries the whole line, then how many do):

| act | said as | shape | shown to (who) | first fixture shown it | arguments (options) |
|---|---|---|---|---|---|
| gather | (its crafts) | gather | by familiarity | every fixture | crafts' own |
| work | (its crafts) | work | by familiarity | every fixture | crafts' own |
| make | (its crafts) | make | by familiarity | every fixture | crafts' own |
| build | (its crafts) | build | by familiarity | every fixture | crafts' own |
| build | upgrade | build | not youth | w0b:Osric (9 of 11) | at, to? (2) |
| move | move | move | everyone | w0b:Osric (11 of 11) | item, qty, to? (3), from?, at? |
| take | take | move | everyone | w0b:Osric (11 of 11) | item, qty, from |
| give | give | move | everyone | w0b:Osric (11 of 11) | to, item, qty, for? |
| accept | accept | agree | everyone | w0b:Osric (11 of 11) | offer, lots?, for? |
| withdraw | withdraw | change | everyone | w0b:Osric (11 of 11) | offer |
| release | release | change | everyone | w0b:Osric (11 of 11) | agreement |
| host | host | change | grown | w0b:Osric (9 of 11) | person, at?, feed? (1) |
| grant | grant | change | grown | w0b:Osric (9 of 11) | to, at, what (2), days? |
| revoke | revoke | change | grown | w0b:Osric (9 of 11) | to, at |
| join | join | agree | everyone | w0b:Osric (11 of 11) | household |
| admit | admit | agree | head | w0b:Osric (4 of 11) | person |
| leave_household | leave household | change | household, grown | w0b:Osric (8 of 11) |  |
| found | found | change | grown | w0b:Osric (9 of 11) | name |
| claim | claim | change | grown | w0b:Osric (9 of 11) | thing, plots?, for? |
| drive | drive | move | herds | w0b:Osric (3 of 11) | thing, item? (5), qty?, to |
| sleep | sleep | go | everyone | w0b:Osric (11 of 11) | at? |
| set | (its crafts) | set | by familiarity | every fixture | crafts' own |
| set | set | change | everyone | w0b:Osric (11 of 11) | thing (1), to (2), at? |
| set | set | change | gap | w0b:Osric (8 of 11) | thing (1), to (2), at? |
| tend | tend | tend | sets | w0b:Osric (11 of 11) | thing?, what?, at?, up? (1), to? |
| travel | go | go | roads | w0b:Osric (11 of 11) | to, when? (2), days? |
| watch | watch | agree | everyone | w0b:Osric (11 of 11) | person |
| teach | teach | agree | everyone | w0b:Osric (11 of 11) | to, what |
| learn | learn | agree | everyone | w0b:Osric (11 of 11) | from, what |
| attack | attack | force | grown | w0b:Osric (9 of 11) | target, aim (2) |
| guard | guard | force | everyone | w0b:Osric (11 of 11) | at?, when? (2), units? |
| fire | fire | go | everyone | w0b:Osric (11 of 11) |  |
| partner | partner | agree | grown | w0b:Osric (9 of 11) | with |
| part | part | change | grown | w0b:Osric (9 of 11) |  |
| try | try | agree | grown, children | w0b:Osric (9 of 11) | with, units |
| name | name | change | household, grown | w0b:Osric (8 of 11) | heir?, head? |
| name | name | change | tags | w0b:Osric (11 of 11) | thing, as |
| order | order | change | head, children | w0b:Osric (4 of 11) | what (5), at? |
| meet | meet | go | evening | w0b:Osric (11 of 11) | at, about? |
| come | come | go | evening | w0b:Osric (11 of 11) | to? |
| write | write | work | everyone | w0b:Osric (11 of 11) | at, text, line?, how? (2), description? |
| erase | erase | work | everyone | w0b:Osric (11 of 11) | at, line |
| rest | rest | work | everyone | w0b:Osric (11 of 11) |  |
| rule | (retired: rules in "rules") | change | | all | |

| way | key: value | first fixture shown it |
|---|---|---|
| for | for | in the reply's format |
| gather on the way | gather: true | w0b:Osric (11) |
| hidden: buried | hidden: buried | w0b:Osric (11) |
| hidden: under brush | hidden: under brush | w0b:Osric (11) |
| how: fine | how: fine | w0b:Osric (10) |
| how: grand | how: grand | w0b:Osric (10) |
| how: rich | how: rich | w0b:Osric (10) |
| hunt alone | alone: true | w0b:Osric (11) |
| hunt only with | only: [the people you take] | w0b:Osric (11) |
| hunt with | with: who leads | w0b:Osric (11) |
| lead | lead: a herd of yours here with an ox | w0b:Osric (11) |
| lead on the hunt | lead: the ox | w0b:Osric (11) |
| looking for | looking for: a kind or a sort | w0b:Osric (11) |
| meeting | meeting: stop \| pass by | w0b:Osric (11) |
| method: cairn | method: cairn | w0b:Osric (11) |
| method: dibble | method: dibble | w0b:Alice (3) |
| method: shallow | method: shallow | w0b:Osric (11) |
| on trouble | on trouble: push on \| wait \| turn back \| go round | w0b:Osric (11) |
| range: far | range: far | w0b:Osric (11) |
| range: near | range: near | w0b:Osric (11) |
| range: the wood around | range: the wood around | w0b:Osric (11) |
| searching | searching: a herd or a person lost on that road | w0b:Osric (11) |
| stop at | stop at: a good place you know on the way | w0b:Osric (11) |

## The replay of live run 1 (Build 6)

Every reply of `live1_A_new` (179 turns) and `live1_B_new` (344 turns), 2,509 acts in "actions" and "fallback", read through the
shapes' parser (`shapes.normalize`) and done by the handlers (`verbs.do`), under the engine before W-109 (a217daab) and after
(63894fa7). Each turn is replayed on a copy of the world as built from the run's own spec at day 0 (the run's state on each day is
not rebuilt: an act that needed that day's goods or a dead person is refused by both alike), so the comparison is of reading, not
of outcomes. Scripts: the session's scratchpad (`replay.py`, `replay_cmp.py`).

| | before | after |
|---|---|---|
| acts refused (parser or handler) | 1,008 | 987 |
| refused after, accepted before | | **0** |
| accepted after, refused before | | 21 |
| read differently by the parser | | 19 |
| refused both times, with another reason | | 34 |
| accepted both times, with another result | | 1 |

**Read differently (19), every one explained:**
- 13 lessons under "agree": 9 now read (the craft and the face written in "agreement" or "name": "learn the weir from Peter at the
  Isel, 2 units" is a learn of the weir from Peter; "teach" with the craft in "how"; "learn" in "agreement" with the craft in
  "line", read as teach before, now learn, as written); 3 offers under agree now accepts (refused since, there being no such open
  offer at day 0); 4 still unreadable (no craft named, or "try for a child" under agree) and told the two faces as the prompt says
  them. One reading is doubtful: "learn the weir from Peter ..., while we empty the weir and traps" reads as wicker traps, the
  longest craft name in the words (`shapes.craft_in` takes the longest), where the weir was meant; it was refused before.
- 3 `bury` acts: before, an unknown verb; now the craft of burying the dead (refused at day 0: nobody lies unburied then).
- 3 lesson acts whose "how" was carried along into the act; now dropped from it.

**Accepted now, refused before (21):** 9 lessons as above; 11 "wild food" or "greens" moved or given from the hands (the greens,
mushrooms and berries foraged; "greens" had been read as the old good "wild food"); 3 gifts "to": "Marsh House store" (that
building's store; at day 0 left at its door, as giving to a building one may not use).

**Refused both times, the reason changed (34):** 13 lesson refusals now in the prompt's grammar; 11 teach, learn or move acts with
a required argument read as None now told which argument (`say a craft you know in "what"`); 8 acts naming "X store" or "the
rack by the hearth" now reach the store or the racks and are refused for what is not there at day 0; 3 `bury` acts as above; and
a gift of greens and roots refused for what the hands hold.

**Accepted both times, the result changed (1):** the lesson written `"agreement": "learn", "line": "fish by hand"`, a teach before
and a learn now, as its words say.

No reply field was found put among the actions in live run 1 (the World 0b fault is Haiku 4.5's); the test covers it.

## The bot run

A 4-day bot run of Eelmouth (`run cybertron2/specs/nutrition/eelmouth.yaml --days 4 --bots`), before and after: both ran the four
days, 11 alive, no errors. Of 593 results, refusals 370 before and 354 after: the 16 fewer are the bots' "move wild food to store"
now putting the gathered greens away; every other refusal is the same, by count and by words.

## The suite

Once, at the end (D2-355), on 63894fa7 with the renders: the 68 test files in six shards (`ls tests/test_cybertron2_*.py | split
-n r/6`): 116, 148, 161, 113, 204 (2 skipped) and 139 passed: **881 passed, 2 skipped, none failed**. One test outside this
thread's file was changed: `test_cybertron2_stage2_taking.py::test_a_craft_line_renders_at_each_level` expected the gill net's
old-prompt line without its hint, which the wave's regression fix 3 (a75c97b2) had restored; it now expects the hint, from its
field.

## Not done, and why

- **The size the interface reached** (about 6,000 words a person, against the rebuilt core's 2,000): not reduced. Most of it is
  everyone's crafts in full, which D2-351 asks for; a leaner form is Zach's choice (question 1).
- **World facts to seeded lines:** the labels' world words are kept in `world` for the old prompt; no new founders' templates were
  written for them (forage's and looking for's kinds, the hard cure's bacon and ham). The salt pans' season is already a seeded
  line (SA7); what a gathering finds is reported when it is done. Writing seeded lines for the rest is founders' work (question 2).
- **The one name resolver from rows' aliases** (L-189 waits on it): not built. `data.SELF_NAMES` is one table for a person's own
  words (hands, home, store, self) in place of the tuples each act kept; `verbs.HOME_WORDS`, `RACK_WORDS` and `book.GOOD_SYNONYMS`
  remain word tables, and `here.building`, `here.person`, `verbs.item_of` and `knowledge.resolve` are still separate resolvers.
- **Bench's fix to the herd lookup** (`farm._herd_on`, an unnamed slaughter fell to a neighbour's herd; W-202 on bench's branch):
  not reviewed; it is on another branch and outside this brief's list.
- **The longest-name rule of `shapes.craft_in`** reads one replayed lesson as the wrong craft (the replay, above): left; changing it
  touches every craft named in free words.
- **Articles stripped from fitting labels** (`knowledge._place_words`, `knowledge.shortfall`: `removeprefix("a ")`): string work
  on a label left; a noun field on fittings would retire it. Not a bracket split, so outside D2-356; noted.
- **`roads.py:819`** splits a result line of one's own offers on " (open": a composed line, not a label; left.
- **The old prompt** shows fittings by their name now where it showed "name (what it is)" in two places (the wear line, the
  building's fittings): its notes on crafts keep `about` (`knowledge.thing_titled`). Small, left.
- **A glitch seen in the build view, not of this thread:** a smokehouse's "upgrade to timber: , 0 units" (an empty cost) in both
  prompts. Not fixed.
- **The replay is of reading, not outcomes:** each reply is done on the world at day 0, not on its day's state.
- **Records:** no rows written to WORK.md or OPEN.md and no hygiene run: the coordinator's (this was a subagent's brief).

## Questions for Zach, with the defaults taken

1. **Everyone's crafts in full make the interface about 6,000 words** (Osric: 71 of everyone's crafts in 1,898 words, his own 22 in
   661). Keep them in full as D2-351 says, or show everyone's crafts that are not of one's livelihood by name with their call
   and how it is said, with the full line on `look_up`? *Default taken: in full, as decided.*
2. **The world words taken out of the labels** (forage's greens, roots, berries, nuts; looking for's boar, deer, hares; the hard
   cure's bacon and ham): kept for the old prompt in `world`, and in the interface left to the engine's reports and the seeded lines
   that exist. Write seeded lines for them? *Default taken: none written.*
3. **Each label's bracket, sorted by hand into `requires`, `hint`, `world` or `about`** (the table above): for instance "a cow in
   milk" and "a hand line, or a rod and line" as what it needs; "spades and a dog help", "slow, downwind, close in for the shot",
   "beaters and spears; dangerous", "about 2.5 km" and the build's "materials x1.5, work x2" as hints; "dried by the sun" as world.
   *Default taken: as in the table; hints shown at known and capable, not at a rough idea.*
4. **A sleep with no building named is a sleep at home** (the line said so; the engine refused it). *Default taken: yes; with no
   home here, "say where".*
5. **"bury" with goods named is hiding them buried; without, the craft of burying the dead.** *Default taken: yes.*
6. **A reply field written among the actions** ("say", "tell", "look up") is moved to its field with a note to the person, not
   refused. *Default taken: moved, with the note.*
7. **"wild food" is the kind of what gathering wild food gives** (the plants' goods, and the old worlds' good of that name), so
   storing or giving "wild food" puts away each of them held. *Default taken: yes, for move and give.*
8. **An act refused because a required argument was missing** is told the argument from its face only where the handler read the
   gap as None (a refusal for a real shortage keeps its own words). *Default taken: as said.*

Current as of 24 Nov 2026 (63894fa7 and the report's commit).
