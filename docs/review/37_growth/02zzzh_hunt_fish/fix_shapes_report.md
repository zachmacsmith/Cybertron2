# The act shapes' interface faults from live run 1 (W-102)

Session 37.2, 23 Nov 2026, branch `w85-fix-shapes`. Live run 1's rebuilt arm (`prompt: core`: the core prompt and the eleven act
shapes, `engine/core.py`, `engine/shapes.py`; u9_people.md §1 to §3) was stopped at day 10 for its refusals: 213 in days 0 to 9,
against 96 on the engine before the rebuild and 69 on the rebuilt engine with the old prompt. Each fault below is the
interface's, not the world's: an act the prompt invites, written the way the prompt invites it, that a handler could not read.
Line numbers are the code before this branch (`1b2c01cb`).

## The count: the run's refused acts, replayed

Of the 213 refusals, 25 are not acts (`tell` over the day's three messages 12, `explain` 8, `offer` 4, `pin` 1): the world's or
the agents', left as they are. The other 188 are acts.

Every act in the turns file (615: each day's final plan, and each evening and evening-answer reply's acts) was replayed one agent
at a time on the run's own checkpoint before its phase (the work on `d<n>.talk.0`, the evening on `d<n>.work`), through the same
path the run takes (`shapes.quiet`, `verbs.cost`, the units, `verbs.do`; the evening through `evening.apply`), once on the code
before this branch and once after. The replay on the old code refuses 195 acts (the run's 188, give or take what other agents did
first that day: one agent alone finds the willow uncut more often, and so on).

| The old refusal | Refused before | Go through now |
|---|---:|---:|
| 1. a rule (`a rule is one of: ...`) | 23 | 0: all 23 would now be refused with a field-precise message (no kind in `rule`; D2-337, D2-339: rules are records in their own field, read by their fields, not their words) |
| 2. a free act at the evening (`the day's work is done`) | 29 | 14 (of the 15 left: 3 are rules, refused as above; 11 are a member barring a door only the head manages, the world's; 1 a tend, which is work) |
| 3. `go` to a parcel or a building at one's own place | 31 | 31 |
| 4. arguments dropped (`called None`; a lesson's craft in `what`) | 24 | 23 (the one left is a rule, `{"do": "change", "thing": "rule", "what": "eat roots first"}`, refused as above) |
| 4 and 6. `say what to ... in "what"` | 7 | 3 (of the 4 left, two name nothing to read, `{"do": "gather", "at": "the Isel"}` and `{"do": "agree", "with": "Peter"}`, and two now reach their handler and are refused by the world: pest work at a house, a craft only heard of) |
| 5. a verb word inside `do` | 7 | 7 |
| 6. `move` from a store or racks by its words; `move` to a building; `set` with no gear named; `accept` with `what` | 18 | 17 (the one left is a heap named by its tag that holds none of the good) |
| refused under a world message (fuel for a fire, no willow, no line, a sound house, fished out, nothing smoking) | 56 | 7 (four were fault 6 under the world's words: a set craft named at a house is its making, 2; goods carried from one's own store, 2; two follow from an earlier act of the day now done; one is now "Not done" for want of units) |
| **all** | **195** | **102** |

After the fixes 93 acts are refused: 27 rules, each refused naming the field it lacks (`"rule"`), its kinds and an example; and 66
by the world (no fuel, no willow, no line in hand, nothing on the racks, a door the person does not manage, a craft only heard
of). No act that went through before is refused now. Three acts that went through before now do what they named: `{"do": "move",
"what": "put", "item": "salt", "to": "the Salt House"}` (twice) and a `put` of firewood `to` the smokehouse had put the goods into
the house instead (fault 6).

The first pass on this branch, which read rules from their words (before D2-337), let all 23 rules and the 4 evening and dropped-
argument rules through (129 in all, 66 refused).

## The faults

### 1. No rule was ever set (23 refused)

**Cause.** `book.act` (`book.py:251-253`) read the kind only from a `rule` field, which the core schema did not carry
(`prompt.py` SCHEMA), while the core's rules paragraph asked for a rule "in your words" and named no fields (`core.py` GRAMMAR,
u9 §2.5). The agents wrote `{"do": "rule", "text": "Eat fresh fish and meat first, before roots, ..."}`, `{"do": "rule", "what":
"first", "item": "fish"}`, `{"do": "rule", "as": "first", ...}`, `{"do": "change", "thing": "rule", "to": "..."}`, `{"do":
"change", "what": "eat", "item": "egg", "line": "first"}`, `{"do": "rule", "thing": "fallback", "to": "angle the Isel; ..."}`:
not one carried its kind in `rule`.

**Fix: the rules grammar of D2-337, D2-338 and D2-339 (Zach, 23 Nov).** A first pass on this branch read the kind, goods,
order, places and states from the agents' sentences; D2-337 took that out (the engine reads the fields, never the words), and
D2-339 set the final grammar, built here (`book.py`, rewritten as one feature unit):

- **Form.** Rules are records in the reply's own field `"rules": [...]`, not in "actions" (`book.apply_rules`, called on the
  morning reply and its talk waves in `run.py`, and on the evening reply in `evening.apply`); free, at any time or in the evening.
  Shared fields: `"for"`: household | me, `"words"` (their own sentence, shown beside the engine's reading), `"n"` to change one.
  The old `{"do": "rule", ...}` act is still read the same way (the bots and old replies use it). The reply schema carries the
  field and its records (`prompt.SCHEMA`); the core's reply format names it.
- **Kinds.** `set {"name", "people"?, "goods"?, "places"?}` (D2-338: a named set, sets may hold sets; built in: everyone, adults,
  children, elders, the head, whoever has time, and the engine's kinds of goods); `keep {"goods", "in"?, "at least"?}` (where a
  good lives: goods arriving go to that store and the sort puts them there; and a floor not eaten, drawn or used, what "hold back"
  was); `first {"goods": [ordered]}` (at the meal and in drawing); `share {"order"?, "who"?, "qty"?, "goods"?}` (in place of
  `eat`: the night's meal goes in its order, fed first when short, `book.meal_order` read by `night.py`; its rations by who; goods
  kept for whom it names, the others' meal skipping them, `night._eat(skip=...)`); `do {"who"?, "act", "when"?, "unless"?}` (in
  place of go, move, tend and chore: an ordinary act, read as the actions are, done with units left over in the spare-units phase,
  again while the units allow, it can be done and its condition holds; with no condition it is a fallback, and the reply's
  `fallback` field sets one's own); `drop {"n"}`.
- **Conditions** are objects only (`book.cond`, `book.cond_holds`): an amount `{"goods"?, "in"?, "under" | "over": n | "full" |
  "room": true}`, a process `{"in", "state": done | in process | fire out}`, `{"arrives": goods}`, `{"season"}`, `{"seen": the run
  | frost | the river rising | rats}`, `{"starving": a person, a set or anyone}`, `{"home": a person}`; lasting states hold until
  they end, read only from what the household knows.
- **Precedence.** One's own before the household's (the spare units: each person's own `do` rules, conditions first, then their
  fallback; then the household's conditional rules by whom they name, whoever has time most spare first, in up to three rounds so
  one rule's work can make another's hold; then its fallbacks); a rule naming one person or one good before one naming a set;
  newer before older (`book._ranked`).
- **Refusals.** A rule missing a field its kind needs (set: name and one of people, goods, places; keep: goods and in or at least;
  first: goods; do: act; drop: n), or with a value it cannot read (goods that name no good or set, a place that is not the
  household's or not here, a condition that is not one of the forms, a qty that is not full, half or a fraction, an act that is
  travel or free), is refused naming the field, its form and what was written: `Refused: rule: 'first' needs "goods" (an item, a
  kind (...) or a set you named); you wrote {...}`. A rule with no kind in `rule` is refused with the six kinds and an example.
- **The prompt.** The rules block (`book.GRAMMAR`, the core's the same) states the form, the five kinds and drop with their
  fields, the condition forms and the precedence in 119 words, with two examples (a set, and a do with a when).
- **Old records** on a book (go, keep, hold back, first with before, eat, move, tend, chore; conditions as sentences or u6 §3's
  state dicts) are converted as they are read (`book.convert`): a go into racks, a tub or a hearth is a `do` of the loading act; a
  go into a store, a keep and a hold back a `keep`; a tend and a move a `do` of that act with its condition; an eat a `share`; a
  chore a `do`; first with before one ordered list. One that names nowhere it can be read as is dropped.
- **The bots** (`bots_livelihood.book_rules`) set the keeper's five rules in the new kinds (`do` hang fish when fish comes in
  unless the racks are full; tend while anything is smoking; take down when a lot is done; carry firewood when the smokehouse holds
  under 15; salt when fish comes in unless the racks have room).
- `move` from a store now reads in every world, not only the shapes' (a rule's act moves goods between stores with it); its line
  is "You moved ...".

**In the count** the run's 23 rule attempts would all now be refused with a field-precise message: none carried its kind in
`rule` (they wrote it in `what`, `as`, `thing` or the sentence), so each reads `Refused: rule: a rule names its kind in "rule":
set | keep | first | share | do | drop; you wrote {...}. As {"rule": "first", ...}`. With the 3 evening rules and the 1 dropped-
argument rule above, 27 refusals of the 93 left are rules. Each attempt, and what it now reads:

| Day | Who | When | What they wrote | Reads now |
|---|---|---|---|---|
| 0 | Gunnild | evening | `{"do": "rule", "thing": "fresh fish goes first: eat it or dry it at the hearth the same day; keep dried or salted fish for the hungry time"}` | refused, naming `rule`: its kind was only in the sentence |
| 0 | Hamon | evening | `{"do": "rule", "text": "Eat fresh fish and meat first, before roots, dried meat or anything that keeps."}` | refused, naming `rule`: its kind was only in the sentence |
| 0 | Hamon | evening | `{"do": "rule", "text": "Fresh fish beyond a night's eating goes to the Shepherd Smokehouse racks to be smoked."}` | refused, naming `rule`: its kind was only in the sentence |
| 0 | Nigel | evening | `{"do": "rule", "thing": "Fish and wild food I take go into the Marsh House store, to be eaten first by the household's children."}` | refused, naming `rule`: its kind was only in the sentence |
| 0 | Oliver | evening | `{"do": "rule", "text": "Eat fresh fish and meat first, then roots, and keep the dried meat and salt fish for winter and the hungry spring, unless s..."}` | refused, naming `rule`: its kind was only in the sentence |
| 0 | Oliver | evening | `{"do": "rule", "text": "Fish brought home goes into the Brook House store. When the store holds 8 or more fresh fish, whoever has units left salts ..."}` | refused, naming `rule`: its kind was only in the sentence |
| 0 | Peter | evening | `{"do": "rule", "text": "Fresh fish and fresh meat are eaten first, then roots, and dried meat last."}` | refused, naming `rule`: its kind was only in the sentence |
| 0 | Peter | evening | `{"do": "rule", "text": "Any fresh fish brought home is hung to dry at the Marsh House hearth the same day."}` | refused, naming `rule`: its kind was only in the sentence |
| 1 | Gunnild | evening | `{"do": "rule", "thing": "first", "to": "Eat fresh fish and roots before dried meat and smoked fish; keep the dried and smoked food back for the win..."}` | refused, naming `rule`: its kind was in `thing` ("first") |
| 1 | Hamon | evening | `{"do": "rule", "what": "first", "item": "fish"}` | refused, naming `rule`: its kind was in `what` ("first") |
| 1 | Oliver | work | `{"do": "change", "what": "rule", "thing": "first", "item": "fish"}` | refused, naming `rule`: its kind was in `what` ("rule") |
| 1 | Oliver | evening | `{"do": "rule", "what": "first", "item": "fish"}` | refused, naming `rule`: its kind was in `what` ("first") |
| 1 | Peter | evening | `{"do": "rule", "what": "first", "item": "fish", "text": "eat fresh fish first"}` | refused, naming `rule`: its kind was in `what` ("first") |
| 2 | Hamon | evening | `{"do": "rule", "as": "first", "item": "fish"}` | refused, naming `rule`: its kind was in `as` ("first") |
| 2 | Katherine | evening | `{"do": "rule", "thing": "fallback", "to": "angle the Isel; firewood the Spinney only when the house store runs short"}` | refused, naming `rule`: its kind was in `thing` ("fallback") |
| 3 | Oliver | evening | `{"do": "rule", "text": "first fish"}` | refused, naming `rule`: its kind was only in the sentence |
| 4 | Oliver | work | `{"do": "change", "what": "rule", "line": "first: roots, then egg, then salt fish; keep dried meat for winter"}` | refused, naming `rule`: its kind was in `what` ("rule") |
| 4 | Oliver | evening | `{"do": "rule", "what": "first", "item": "roots", "at": "Brook House"}` | refused, naming `rule`: its kind was in `what` ("first") |
| 5 | Gunnild | evening | `{"do": "rule", "thing": "eat first", "to": "soft wild food first; keep dried meat and roots for the hungry time"}` | refused, naming `rule`: its kind was in `thing` ("eat first") |
| 6 | Katherine | evening | `{"do": "rule", "thing": "Eat the fresh fish first; when the keeping food is under three nights, kill a hen before touching the dried or salted stor..."}` | refused, naming `rule`: its kind was only in the sentence |
| 7 | Oliver | evening | `{"do": "rule", "text": "Eat fresh fish first, then eggs, then a hen when no fresh fish is left; eat the dried meat last, unless someone is starving."}` | refused, naming `rule`: its kind was only in the sentence |
| 8 | Oliver | evening | `{"do": "rule", "as": "first", "item": "fish", "at": "Brook House"}` | refused, naming `rule`: its kind was in `as` ("first") |
| 8 | Peter | evening | `{"do": "rule", "text": "Nichola keeps at least 6 firewood in the Marsh Smokehouse store, carried from Marsh House, whenever fish is on the racks."}` | refused, naming `rule`: its kind was only in the sentence |

Written in D2-339's fields, the same aims set and run (the tests): Hamon's of day 0 is `{"rule": "first", "goods": ["fish", "meat"]}`
and `{"rule": "do", "act": {"do": "smoke fish", "at": "the Shepherd Smokehouse"}, "when": {"arrives": "fish"}}`; Katherine's
fallback `{"rule": "do", "act": {"do": "angle", "at": "the Isel"}}`; Peter's of day 8 a `do` moving firewood to the smokehouse
`"when": {"goods": "firewood", "in": "the Marsh Smokehouse", "under": 6}`.

**Tests** (`tests/test_cybertron2_w102_live1_acts.py`): `test_the_runs_rule_attempts_are_refused_naming_the_field`,
`test_each_kind_set_in_the_rules_field_with_its_words_beside_the_reading` (set, first through a set, keep with a floor, do with a
when and an unless, share, drop), `test_the_meal_goes_by_the_shares_order_its_rations_and_its_goods`,
`test_a_rule_missing_a_field_or_with_an_unreadable_value_says_which`, `test_a_do_rule_runs_in_the_spare_units_own_first_and_while_its_condition_holds`,
`test_old_records_on_the_book_are_converted_or_dropped`, `test_the_rules_block_gives_the_grammar_and_two_examples`; and the
stage 3 book tests and the bots' tests rewritten to the new kinds (`tests/test_cybertron2_stage3_keeping.py`,
`tests/test_bots_livelihood.py`).

### 2. Free acts refused at the evening (19 `change`, 5 `put`, 2 `go`, 1 `first`, 1 `set the door`)

**Cause.** `evening.apply` (`evening.py:143`) judged an act by its raw `do` against `NIGHT_VERBS` before the shapes read it, so
`change` (a door, a rule, a claim, a name), `put` (the move shape), `go` (travel) and `first` were refused as work; the work phase
was not at fault (a free act costs 0 there).

**Fix.** The evening reads each act through `shapes.normalize` first, then lets through every night verb and every free verb
(`verbs.FREE`), whatever the units left. Work still waits for tomorrow.

**Test.** `test_free_acts_run_at_the_evening_whatever_their_shape_word` (Hamon's door, Nigel's put, Hamon's rule; a craft is still
refused).

### 3. `go` to a place at one's own node (31 refused)

**Cause.** `verbs._travel` (`verbs.py:2468-2471`) refused a parcel at one's own place ("not a road away"), and a building there
fell to "there is no way from here to 'Marsh House'".

**Fix** (the coordinator's correction: `go` is travel between places along roads, and parts of here are reached by naming them
in "at", the walk charged from the route). With the shapes on, `go` to a parcel or a building at one's own place is harmless: no
refusal, no units, no move; the result says the day's acts take one where they name with "at". `go` to a building here at
nightfall is sleeping there (the go shape's `sleep` face; Petronel's `{"do": "go", "to": "Brook House", "when": "nightfall"}`). The
go shape's line now says it is travel to another place along a road and that a part of this place is named as "at" in the act.

**Tests.** `test_go_to_a_parcel_here_is_no_move_no_refusal_and_no_units`, `test_go_to_ones_house_at_nightfall_is_where_one_sleeps`.

### 4. Arguments the handlers dropped (6 `sleep`, 11 `learn` and `teach`, 7 `agree`)

**Cause.** `shapes.normalize` (`shapes.py:134`) passed a face's other fields on untouched; `verbs._sleep` (`verbs.py:2380`) reads
only `at`, `_teach` and `_learn` (`verbs.py:2517`, `2530`) only `to` / `from` and `what`. So `{"do": "agree", "with": "Hamon",
"what": "learn", "line": "wicker trap"}` reached `_learn` with no teacher and no craft, and `{"do": "sleep", "to": "Shepherd
House"}` with no building. A craft after the face in `what` ("teach cut withies") was looked for as a craft whole.

**Fix.** `shapes._lesson`: the other person from `with`, `person`, `to`, `from` or `target`; the craft from `what`, `line`,
`craft`, `thing` or the words (`craft_in`: the words as a craft, without a leading verb word, else the longest craft name inside
them); a face read from "teach me" or "learn" in the words; a craft with no face is taught if one knows it, else learnt.
`shapes._sleep` reads `at`, `to`, `thing` or `where`. Hamon's `{"do": "change", "thing": "heir", "heir": ...}` reads as `name`.

**Test.** `test_sleep_reads_to_and_a_lesson_reads_with_what_and_line` (Gunnild and Hamon's lesson of day 7 meet in
`today["learn"]`; Petronel's craft by its label; Gunnild's lesson described in words).

### 5. A verb word inside `do` (4 `learn boil salt`, `make wicker trap`, `set wicker trap`, `cut firewood`)

**Cause.** `shapes.normalize` (`shapes.py:171`) looked the whole of `do` up as a craft.

**Fix.** A leading shape, face or verb word is read as the shape with the rest as what it acts on ("set the door" a door, "go X"
a place only when X is one); else a leading word of one's own is dropped when the rest is a craft ("cut firewood").

**Test.** `test_a_shape_or_verb_word_first_in_do_is_read_as_the_shape`.

### 6. The rest of the list: the same kind of fault

- **`move` from** (`verbs.py:1886-1887`): every `from` was read as racks to take a done lot down, so `{"do": "move", "item":
  "salt", "from": "the Salt House"}` and firewood `from` Marsh House to the smokehouse were refused (14). Now `verbs.move_from`
  reads `from` as a store (taken from as `take` is, 1 unit; into another building named in `to`, or the hands), a thing by its
  tag, or racks by their words ("rack", "the rack by the hearth", "the hearth": one's own here); a done lot of that good is still
  taken down.
- **`move` to** (`verbs.py:1890`): the store put into was `at`, never `to`, so goods went into the house when another building was
  named (three acts that "went through" put salt and firewood in the wrong store); now `to` names it, and goods not in hand but in
  one's own store here are carried across.
- **`set` with no gear named** at a place: the one kind of set gear in hand. **`accept`** reads the offer from `what`. **A key with
  a space after it** (`{"do": "gather", "do ": "angle"}`, three times) is read, the second `do` as what the shape acts on.
  **A set craft named at a house** (`{"do": "wicker trap", "at": "Shepherd House"}`) is the making of it.
- Left as the world's: a fire with too little fuel, `tell` over three messages, a member barring a door only its head manages,
  no willow, no line in hand, nothing on the racks, a heap to take named by tag.

**Tests.** `test_the_move_shape_reads_from_and_to_a_store_and_a_rack_by_its_words`, `test_other_arguments_read_where_the_reply_put_them`.

## Also on this branch

### The hearth rack's meat test (`test_meat_hung_on_a_rack_dries_in_three_nights_and_salt_meat_needs_salt`)

It pinned the old fresh-meat rate: a cold-hearth night spoils a drying lot at its input's base and the season (`process.decay`),
0.13 x 1.5 = 0.195, inside its 20% bound; since D2-336 fresh meat goes off at 0.28 a night, 0.42 with summer's warmth, so 8 kg
leaves 4.61. The code follows the decided rates; the test is re-pinned to the engine's own `spoil_rate`.

### The river's run signs (the coordinator's added fault)

The premise did not hold in the comparison arm (`/home/user/live1/live1_A_old`): `perception.jsonl` holds fact ids, not texts, so
a text search there finds nothing. Replaying day 9 (`d9.work`) gives the same fact ids as the run's notices, and the run rows were
offered and noticed: Nichola and Petronel noticed F9.Eelmouth.44, "dark eels moving in the slack water under the banks of the Isel,
all one way, downstream". The arm's turns show the run rows in prompts: "dark eels" 28 times, "eels against your legs" 16, "thick
with eels" 11, "an eel run in" 10, "silver eels" 30. The record writes `band` (day 9's checkpoint: eel thick, salmon glut, for
night 8); the evening reads today's pulses against the station's year (`year_basis`): day 7's 146 eels and day 9's 169 read
"running" (about 3.5% of a year of 4,200 to 4,500), day 11's 246 eels and 155 salmon "thick". The bands land as u8 §1 means them.

Two rows never fired, and one was a fault:
- **the catch carried home** (`river.carried`, `river.py:472`): it needs a day worked at the water, and tending set gear or a weir
  did not mark the water. Peter emptied the weir on day 9 (197 kg) and carried 167 kg home unseen. Tending now records the parcel
  in `today["tended"]` (`placed.tended`; kept apart from `worked` so the day's act draws are unchanged), read by the carried catch
  and by the doers' touch row, with a building worked in read as its parcel.
- **the herons**: the world has no heronry (`wild.sites`), so the heron rows cannot fire there; that is the world's.

**Test.** `test_day_9s_run_offers_the_run_rows_and_the_weirs_catch_is_seen_carried_home`: day 9's record from the `d9.evening`
checkpoint, the run rows offered at the Isel, and Peter's weir emptied on `d9.talk.0` then seen carried home by the others.

## The suite

The full suite in six parallel shards (69 files, each shard `timeout 1700 python3 -m pytest -q <files>`), at `9e6a3d3f` (all of
this branch's code): **849 passed, 2 skipped, 0 failed** (shards: 104, 151, 127, 215 and 2 skipped, 111, 141; the longest 10
minutes). On the way: the first full run, on the first pass's code, failed two tests that the branch then fixed
(`test_agent_facing_modules_never_read_the_world`: the move's store check read the world, now through `Here.done_lots`;
`test_a_go_rule_sends_goods_arriving_to_its_store`: the first pass's word reader took a "to" as words); at `bd923195` (D2-337) the
suite passed whole (847, 2 skipped); after D2-339's rebuild, `test_a_40_meat_glut_loses_far_more_with_only_the_hearth_rack` failed
once (a `move` from a house whose hearth rack had emptied took the dried meat into the hands, where before it was refused), fixed
by reading a done lot of that good by its output as well as its goods. The stage 3 book tests, the bots' book tests and the shapes'
resolver test (`"go eeling"` now reads as the eel traps, a shape word first and the rest a craft) were rewritten to the new
behaviour; no other test changed.

The replay of the run's acts (above) was run on the final code: 615 acts, 93 refused (27 rules, 66 the world's), 102 of the 195
the old code refused now go through, none newly refused.

## Defaults taken (no decision asked)

- `go` to a building here at nightfall is sleeping there; otherwise `go` to a part of here does nothing and says so.
- A craft named under `agree` with no "teach" or "learn" is taught if the person knows it, else learnt.
- In D2-339's rules: a `share` with "goods" needs "who" gets them; a `keep` needs "in" or "at least"; the household's conditional
  `do` rules run in up to three rounds a day (cascades); a `do`'s act is repeated while it can be done; an old record that names
  nowhere it can be read as is dropped, not refused.
- Moving goods out of a store costs what `take` costs (1 unit).
