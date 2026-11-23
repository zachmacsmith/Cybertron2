# U6. The household book: where goods go, what is kept, first, eaten and moved; `when` on lasting states; chores and fallbacks

**Status:** discussion (component spec of the integrated design, W-85). The parts decided are cited; nothing built.
**Owner:** the standing rules are **37.4's** (proposals/standing_rules.md, W-37; the book's records, the `rule` act, precedence, the
prompt's rules block, the day loop in `run.py`, the fallback's code, spec agents/standing_orders.md and actions.md). **37.2** owns
what the book reads and does in its areas: the store moments (go, keep, hold back, first), the lasting states of containers and
stores, the keeping chores' work on containers, the fallback as a standing setting (L-142, D2-296), and this spec. Each code row
below names its owner; 37.4 is named on every merge that touches its code (D2-237).
**Thread:** the integrated design (W-85), under the network (W-73); the standing rules thread is W-37 (37.4's).


> **Decisions since this spec was written (binding over its text; the build reads this table first):**
> - **D2-301:** own rules and standing fallback before every household chore; none at the start, nothing pushing; units left are rest.
> - **D2-313:** 37.2 owns every engine file this wave changes (read every '37.4' in the code tables as 37.2 for this wave).
> - **D2-319:** rules changed any time and in the evening talk; a seeded line on evenings as the time to revisit rules.

## Extends

- **standing_rules.md (37.4's; read, not edited):** a household default written as rules; a person's own defaults override the
  household's, an act in a turn overrides both; going against a household rule is recorded and noticed; the head sets the household's
  rules and members propose at the evening; shown and changed at the evening; a road default; later the fire, the door, herds; never
  trade, trips, loans or taking people in. Its open questions 1 to 5 stay 37.4's.
- **store_rules.md** (D2-274, D2-279, D2-282, D2-296): one book per household and per person for eating and stores; the grammar (go,
  keep, hold back, first, eat, move, drop; goods, where, qty, before, who, by, unless); five moments; the defaults; labour; visibility.
- **fallback.md (D4-76)** and **L-142** (`records show L-142`: a fallback as a standing setting, unset at the start, set or changed
  whenever one chooses; waits on W-37).
- **D2-274** (one book; a store built for a kind writes its own droppable rule; no default for putting carried goods away; chores
  from spare units only; a person may override their own defaults; agents see their rules, how to change them, what they can set,
  each move or draw by a rule, and chores a rule would have done but no one did), **D2-279** (the household's book runs its stores;
  the system prompt gives the grammar; the ways of managing seeded as memories, chiefly the head's), **D2-282** (a rule may fire when
  a good, container or place changes state: "move smoked fish to the cellar once cured"), **D2-296** (the head divides the
  household's spare units out as chores; each person can overrule with their own standing fallback, which comes first), **D4-16**
  (routine work on standing orders), **D2-148** (the head's standing order for children), **D4-23** (members use the household's
  store; the head manages it), **D4-35** (beliefs from signs only).
- **store_management.md** (§1 the thought experiments, §2 the grammar, §3 the ten defaults, §4 labour, §5 what is seen), **wave3_keeping.md
  §4** (conditional rules: states latched, knowledge only, the chore phase, worked sentences, visibility), **wave4_people.md §2.4** (the
  rules block) and **§3.4** (the head's management lines), **steering.md** §1.1, §3 F2 and question 2 (the fallback's steer).
- **wave_conflicts.md** G4, C29, S5, S12, K9, E10.
- **The code** (read 22 Nov): `run.py:985-1035` (the plan loop, interleaved), `:1036-1057` (the fallback, D4-76), `:1104`
  (children's work, D2-148), `prompt.py:106` and `:261` (the reply's `fallback` field and its example), `here.py:378-386`
  (`party_container`), `verbs.py:1569-1595` (`_move`), `night.py:116-127` (the night's draw order), `labour.py:42-58` (the walk's
  fraction carried until whole: the precedent for chores), `life.py:236` (`children_work`), `world.py:993`.

## Departures

| # | From | This spec | Why |
|---|---|---|---|
| 1 | wave3_keeping §4.1: `when` (fires on becoming true) and `if` (applies while true) beside `unless` | `when` and `unless` only, both on states: a `when` rule applies while its state holds and is pending from the moment it comes true until done or the state ends; `unless` switches a rule off while its state holds | with the latch, `when` and `if` do the same thing; one word fewer in the prompt |
| 2 | wave3_keeping §4.1: new rule verbs `load` and `take down` | folded: a `go` into a processing container is a load (quantity work, a chore); a `move` out of a container is taking down | store_rules' verbs already say it; fewer verbs |
| 3 | wave3_keeping W80-Q6: rules keep only, never production | keeping rules keep, move and tend; `chore` rules (the fallback, D2-296) name acts a fallback may do, production included; trade, travel and another's things stay refused | D2-296 made fallbacks assignable by the book; a fallback is production (firewood, wild food) |
| 4 | D2-296 read literally (a person's own standing fallback comes first over every household chore) | two tiers in the spare units: **keeping chores** (state-latched: tend, load, take down, move) first; then **fallbacks**, a person's own before the household's. Inside each tier a person's own rule beats the household's (D2-274's precedence) | a keeping chore answers a known need the day brought (a lot to take down, a fire to tend); a fallback is a filler for units nothing else claims. Read so to keep D2-296's precedence without letting a filler (firewood: steering §1.1, L-142) eat every chore. **This is a reading; asked (Q-U6-1); default taken** |
| 5 | store_management §4, store_rules: move chores "in the fallback's place" | in the spare-units phase, before any fallback (Departure 4) | G4; wave3 W80-Q13 |
| 6 | D4-76: a fallback written in every reply | a standing fallback, set or changed by the reply's `fallback` field or a `rule` act, standing until changed; unset at the start (L-142) | L-142; D2-296 ("their own standing fallbacks") |
| 7 | standing_rules.md §5: rules changed by an act at the evening | changed by a free `rule` act at any time; shown at the evening with what they did (wave_conflicts C29) | store_rules ("a free `rule` act", any turn). 37.4's to settle; proposed here |
| 8 | spec agents/standing_orders.md: standing orders bind "only itself" (D4-16) | the household's book binds its members unless they override (D2-274) | D2-274; S5. 37.4's spec to amend |
| 9 | store_management §3 D7 (carried goods put away at night) | no such default | D2-274 |
| 10 | store_rules open question 1: about 12 rules a household and 6 a person | no cap now; the rules block's length is measured in bot tests and live runs | Zach: "idk about the cap"; a cap decides for him |

## Purpose

Routine work is where these models drop things: a fire not tended on the big night, a cured lot left up, seed eaten. The book is the
one place a household sets its routine (where goods go, what is kept and eaten, who does the chores, what each does with units left),
in its own words, shown back as the engine reads it, and it adapts to what the day brought because it runs after everyone's plans.
It is never an oracle: a rule reads only what the household knows.

## The design

### 1. Whose book, who sets it

- **One book a household and one a person** (D2-274). The head sets the household's; a member's household rule is a proposal to the
  head at the evening (standing_rules item 4, 37.4's). Anyone sets their own.
- **A rule is set, changed or dropped by a free `rule` act** at any time, and by the evening's call (Departure 7).
- **A store built for a kind writes its own droppable rule** (D2-274): a granary for grain, a woodshed for fuel, a byre or barn for
  fodder; a smokehouse, a cellar, a tub, a vault write none.

### 2. The record

The agent fills the fields and gives its own sentence; the engine shows it back in its own reading with their words beside it.

```
{"do": "rule",
 "rule": "go" | "keep" | "hold back" | "first" | "eat" | "move" | "tend" | "chore" | "drop",
 "for": "household" | "me",                       # whose book (a household rule from a member who is not head: a proposal)
 "goods"?: an item ("fish") | a kind (grain, dry goods, food, fresh food, keeping food, fish, meat, fuel, fodder, tools, coin) | "everything",
 "to" | "in" | "from"?: a building, a storey, a container by kind ("the chest", "the racks in the Smoke Hut", "the salting tub"), "hands",
 "qty"?: n | "all" | "up to n" | "leave n",
 "before"?: goods (for first, eat),
 "who"?: the household | a person | guests,
 "by"?: a person | "whoever has time",          # for go into a container, move, tend, chore
 "acts"?: [acts],                                # for chore: what to do with units left, in order and again (D4-76)
 "when"?: a state (§3),
 "unless"?: a state (§3),
 "words": "their sentence",
 "n"?: the rule's number (to change or drop it)}
```

`go` into a processing container (racks, a tub, a pit) is a load (U4: hanging, salting, laying in): quantity work done as a chore. A
`move` out of one is taking down (U4: 120 kg a unit, est.). A `tend` is a container's fire (U4), the same verb standing_rules item 7
foresees for the hearth ("keep it lit"). A `chore` is a fallback: for oneself (one's standing fallback) or, set by the head, for a
member (D2-296).

### 3. The states a rule may name

Each is read only from what the household knows (wave3 §4.2): its own containers and stores (known without a roll, brief 4c §6.4),
its members' acts and their results, the calendar, and what its members noticed (D4-35). Never the engine's hidden state (a run's
pulses, `wild/runs.py`): "when the eels run" reads as "when one of us has seen the run".

| State | Of | Lasting? | Read from | Words |
|---|---|---|---|---|
| done | a lot in one of the household's containers | yes, until taken down | U4's lot `done` | "when the eels are smoked" |
| in process | a container with a lot not done | yes | U4's lot | "while anything is smoking" |
| has room / full | a container or a store | yes | U4's `room`; U5's `room_for` | "when the racks have room"; "unless the tub is full" |
| under n / over n | a good in a store or container | yes | U5's portions | "when the bins hold under 20 grain" |
| arrives | goods coming home | the day | the store moment 1 (§4) | "whatever fish comes in" |
| the fire out | a container's fire last night | the night after | U4's lot `out` | "if the hut's fire died" |
| seen | a sign a member noticed and holds: the run, frost, the river rising, rats in the store (each a named set of U8's sign rows) | the day it is noticed | the members' beliefs of that day | "when we have seen the eels running" |
| a season, a day | the calendar | yes | `w.calendar()` | "in winter"; "from the first day of autumn" |
| at home, away | a member at the place | yes | where each is | "when Wat is home" |
| someone is starving | a member | yes | hunger | (as store_rules' `unless`) |

**The latch.** A rule whose state is lasting is pending from the night it comes true until its work is done or the state ends: a cured
lot not taken down today is still cured tomorrow, and the rule fires again; the miss is shown, not lost. A rule on a state of the day
(arrives, the fire out, seen) is pending that day only.

### 4. When the book is read

| Moment | Rules | What it decides | Code (owner) |
|---|---|---|---|
| 1. goods arrive (work output, a gift, a purchase, a catch tended home) | `go` | which store or container they go into; a `go` into a processing container leaves them in that building's store, pending as a load chore | `verbs._out` (37.4) via `book.where_to` (37.4), `party_container` replaced (E10) |
| 2. a store's goods change | `keep`, `hold back` | which portion each good lies in; what is set apart (U5 §4) | `buildings.alloc` (37.4's module; 37.2 writes) |
| 3. drawing (making, building, giving, paying) | `first`, `hold back` | which store and good is used first; what is not touched | `world.takeable`, `verbs._top_up` (37.4) |
| 4. the night's meal | `eat`, `first`, `hold back` | order, rations, who first, guests (standing_rules) | `night._eat` (37.4, W-37) |
| 5. spare units, after every plan | `go` into containers, `move`, `tend`, then `chore` | the keeping chores, then the fallbacks (§5, §6) | `book.spare_units` (37.4), the work by U4 and U5 (37.2) |
| the night | | lots finish, fires die, goods spoil, vermin take: states change and latch | U4, U5 (37.2) |
| the morning | | what fired, what was missed, what waits (§8) | `prompt` (37.4), lines from `book` |

### 5. The spare-units phase

**Where.** After the plan loop (`run.py:995-1035`) and in place of today's fallback loop (`run.py:1036-1057`). After the plans,
because the plan loop interleaves people's acts, so a hand-off by hand ("Agnes hangs what Wat brings") depends on the order and a
refused act is not tried again (`run.py:1007-1009`); a chore after every plan sees what the day brought. That is the plainest value of
rules over hand acts: **they adapt to quantities nobody knew at dawn.** A chore never takes units from a plan (D2-274).

> **Corrected 23 Nov by 37.2 to D2-301** (Zach: "Your own rule should overrun chores ... I choose (b)"): a person's own rules and
> standing fallback come before every household chore, keeping chores included. The phase therefore runs **person by person: first
> what that person's own book says (their own keeping rules, then their own standing fallback), then, with units still spare, the
> household's chores for them** (keeping chores in the order below, then the head's fallback chores). A household chore with
> "whoever has time" goes to members who have spare units after their own rules, most spare first; a member whose own fallback took
> their units is not "going against" the household unless a household rule named them. People start with no personal fallback
> (L-142), and nothing in the defaults pushes them to set one. Units left are rest (D2-301), which has no effect until fatigue.

**The household's keeping chores.** Every pending household `go` into a container, `move` and `tend` whose `when` holds and whose
`unless` does not, in this order (wave3 §4.4):

1. `tend` (a fire dying ruins a lot already worked: U4 §8, one missed tend on a full set about 17 food);
2. `go` into a container, the most perishable goods first (fresh fish and meat before hides and flax), in the book's order among
   rules of the same goods;
3. `move` out of a container whose lot blocks a load pending today;
4. other `move`s;
5. within each, the book's own order; a household may reorder with `first` ("Hob tends before anything").

**Who.** The rule's `by`; or "whoever has time": the household's members at the node of the container or store, with at least 1 spare
unit, the most spare first, then by name. A person's own rule: only that person. A member whose own rule says otherwise for the same
goods or container (D2-274's precedence) is passed over, and that is recorded as going against the household's rule (§7). A member
away does nothing.

**Labour.** Keeping chores are quantity work at U4's and U5's rates (hanging 30 kg a unit, salting 40, taking down 120, tending 1;
moving between buildings basis §5's provisional rate; within a building free). Their real fractions are summed a person a day and
charged as the walk is (`labour.py:42-58`): a fraction carried until whole. A person takes chore work only with at least 1 spare unit,
and only while the whole units charged stay within their spare (Basis rows needed, 1).

**Partial chores.** A load done in part splits the goods: what was hung is hung; the rest falls to the next rule that takes it (the
tub "unless the racks are full"), then stays where it is, and the morning line says so.

**Cascades.** A chore can make another rule pending (taking down frees the racks; "when the racks have room, hang the salted fish").
The states are read again after each chore; each rule fires at most once a day; at most three rounds (Basis rows needed, 2). In sorted,
keyed order: deterministic and replay-safe.

**The head's fallback chores** (§6) come last, for members with units still spare.

**A glut day** (wave_conflicts K9). On a run's peak night the plans may take every unit; hanging by rule then waits, and fresh fish
keeps 1.5 nights. That is real: a household that wants its glut hung by rule leaves units unplanned, plans the hanging as an act, or
pushes on (`overwork`). The morning line shows what waited.

### 6. Fallbacks (D2-296, L-142)

- **A person's standing fallback** is their own `chore` rule: acts for units left over, done in order and again until the units are
  used or none can be done (D4-76's loop, `run.py:1041-1057`, kept). Free acts and travel cannot be one (D4-76). It may carry `when`
  and `unless` ("gather firewood when the woodpile is under 20 bundles"), which lets a filler follow need (steering §1.1: today's
  firewood fallback does not).
- **The household's chores** are the head's `chore` rules for its members (D2-296): "with units left, Hob gathers firewood; Joan mends
  the nets in winter". A member's own standing fallback comes first (D2-296); with none, the household's chore for them runs.
- **Setting it.** The reply's `fallback` field (`prompt.py:106`, `:261`) sets or changes one's standing fallback and it stands until
  changed (Departure 6); a `rule` act does the same. The field's example "(say, gather firewood)" goes (steering question 1).
- **Unset** (the start of a world, L-142): units left over are rest (D2-301), and the morning says so plainly ("You rested 2 units
  yesterday."), without asking for a fallback.
- **Children's standing work** (D2-148, `life.children_work`, `run.py:1104`) stays the head's order as now; it is the same thing as
  a household chore for a child, and folds into the book once the spare-units phase is built (Gaps, 3).

### 7. Precedence and going against

Store_rules' order, highest first: an act in a turn; the person's own rule; the household's rule; the engine's default. The most
specific rule wins: an item over a kind over everything; then a rule with a `when` that holds over the same rule without (wave3 §4.4);
then the newer. Going against a household rule (a person's own rule or act that overrides it, a held-back good eaten) is never hidden:
it is recorded, and shown to the person and the head next morning ("Joan's own fallback took her units; the household's rule 3 had
her tend the fire, and Hob did it"). Who else sees it is standing_rules open question 3 (37.4's).

### 8. Where the book is silent: the defaults

store_rules' list as decided (D2-274): goods come home; inside a building, the best place with room (U5 §4); when full, the
household's next store at the place, then the door, with a line; drawing from hands, home, other household stores, door piles, food
needing no fire first, then the most perishable; full rations; guests fed by the host; nothing held back, and the evening says so; a
store built for a kind writes its own droppable rule; never between households by rule. **No default** puts carried goods away, loads
a container, tends a fire, takes a lot down or sets a fallback: the house lines say what waits (wave3 §4.7).

### 9. What each person sees (D2-274's visibility)

**In the system prompt** (37.4's core; wave4 §2.4 extended by about 60 words), rendered from the records:

```
The Reed household's standing rules (Wat sets them; you may propose):
1. fish that comes in goes to the Smoke Hut's racks when they have room; when they are full, into the salting tub while there is salt
2. take down the smoked fish from the racks into Reed House when a lot is done; whoever has time
3. tend the Smoke Hut's fire while anything is smoking; Hob first, then whoever has time
4. eat the fresh fish first, then the smoked, then the salt
5. with units left over: Hob gathers firewood when the woodpile is under 20 bundles
Your own rules: your fallback: mend the traps (it comes before the household's chores for you).
A standing rule says, in your words: where goods go; where something is kept, or how much is held back; what is taken or eaten first;
what is moved, hung, salted or tended, and by whom; what someone does with units left over. It may say "when" (a lot is done, a store
is full or has room, a store holds under so much, something is seen, a season) or "unless" (someone is starving, it is winter, it is
full). The most specific rule wins, yours before the household's. Setting, changing or dropping a rule costs nothing.
```

**The `rule` act's result** (the engine's reading, their words beside it):

> Rule 2 (the household's): take down smoked fish from the racks in the Smoke Hut into Reed House, when a lot there is done; whoever
> has time (your words: "When the eels are smoked, take them down and put them in the house"). It fires the morning after a lot is
> done and waits until someone with units left has done it.

**The morning's record** (the house lines, one line a chore; facts only):

> By the household's rules yesterday: Agnes hung 126 kg of fish on the Smoke Hut's racks (4.2 units); Hob tended its fire (1 unit);
> Joan salted 24 kg into the salting tub (0.6 units, 6 kg of salt).
> Not done yesterday: 30 kg of fish waited to be hung (no one of the household with units left was at Reed); it lies in Reed House's
> store.
> Waiting today: take down the smoked fish on the racks (rule 2: a lot is done).
> Rule 1's salting stopped: there is no salt in Reed House.
> Your fallback (mend the traps) took 2 units yesterday.

**At the evening:** the book with what each rule did that day, and the place to change it (standing_rules item 5, 37.4's).
**Attending to the store** shows each container's lots, nights left and the rule that put them there (U4 §7, U5 §7).

**Refused when set** (the reason in the result):

| Rule | Result |
|---|---|
| trade, travel, an agreement, taking from another household's store or lot | "Refused: a rule keeps, moves and tends what is your household's, and says what someone does with units left; trade, trips and what is another's are yours to choose each day." |
| a chore of travel or a free act | "Refused: a fallback is work for units left over: travel and free acts cannot be one." |
| a building or container the household does not hold | "Refused: the Granary is not your household's." |
| a household rule from a member who is not head | "Proposed to Wat, who heads the household: [the reading]. It stands once he takes it." (37.4's evening) |
| a hard cure in a wattle hut | U4 §6's refusal |
| a `when` on what nobody can see ("when the run begins") | read as "seen: the run" and shown back so: "(it fires the day one of you has seen the run)" |

### 10. Worked sentences, in the agents' words

1. *"Whatever eels come home, keep enough for tonight and hang the rest in the smoke hut. If the racks are full, salt them."* →
   Hold back: fish, one night's meal, at home, when fish arrives. Go: fish to the Smoke Hut's racks, when they have room (a load,
   whoever has time). Go: fish to the salting tub when the racks are full, while there is salt (a load).
2. *"When the eels are smoked, take them down into the loft."* → Move: smoked fish from the racks in the Smoke Hut to Reed House's
   smoke loft, when a lot is done; whoever has time. (D2-282's own example, to the cellar, reads the same.)
3. *"Keep the hut's fire going while anything hangs. Hob first."* → Tend: the Smoke Hut's fire, while a lot is smoking; Hob, then
   whoever has time.
4. *"Salt the first 60 kg for the end of winter."* → Go: fish to the salting tub, up to 60 in all, when fish arrives, before the racks
   rule (the book's order).
5. *"When the bins get under 20, fill them from the granary."* → Move: grain from the Granary to Holt House's bins, up to full, when
   the bins hold under 20; whoever has time (between buildings: basis §5's rate).
6. *"When the racks free up, hang the salted fish for a hard cure."* (a timber smokehouse) → Go: salt fish to the Fish House's racks
   for a hard cure, when they have room. In a wattle hut: refused (U4 §6).
7. *"Hob: with your spare time, firewood when the pile is low, else mend the traps."* (the head) → Chore: Hob, gather firewood when
   the woodpile is under 20 bundles; else mend the traps. Hob's own fallback, if he sets one, comes first (D2-296).
8. *"When the eels start running, everyone stays at the river."* → Refused: a rule cannot plan the day's work; "when we have seen the
   eels running" can start keeping chores and fallbacks only.

### 11. Where the book meets standing_rules.md, and whose code is whose

| Part | Whose | Notes |
|---|---|---|
| the book's records, the `rule` act in the verb registry, validation and refusals, precedence and matching, proposals to the head | **37.4** | standing_rules items 3 to 5; this spec's §1, §2, §7 propose the shape |
| the eating rules (eat, first and hold back at the meal; rations; guests; the road default) | **37.4** (W-37) | standing_rules items 1, 2, 6; this spec adds nothing but the shared grammar |
| the spare-units phase in `run.py` and the fallback's code (D4-76) | **37.4**, with L-142's design and D2-296 (37.2's) | §5, §6 |
| the rules block in the system prompt, the evening, the morning record lines' rendering | **37.4** (prompt core) | §9 gives the wording |
| the lasting states of containers and stores; the latch's readers | **37.2** (U4 `process.states`, U5 `buildings` fills) | §3 |
| the keeping chores' work (load, tend, take down) and the store moments' readers (go, keep, hold back, first in stores) | **37.2** (U4, U5) | §4, §5 |
| `seen`: matching a member's held beliefs to a named set of sign rows | **37.2** reads beliefs through 37.4's perceive and memory (read only) | §3; the sign sets are U8's |
| the head's seeded management lines (how to keep, what to hold back) | **37.2** (U9, wave4 §3.4) | D2-279: the prompt gives only the grammar |
| spec: agents/standing_orders.md (D4-16 "binding only itself"), agents/actions.md (D4-76) | **37.4** | amended for D2-274, D2-282, D2-296 when the build is decided (S5) |

standing_rules item 7 lists "the fire (keep it lit)" for later; §2's `tend` is that verb for a container's fire, and the hearth's can
use it when 37.4 builds it. Item 7's "not for trade, trips, loans or taking people in" is kept (§9's refusals); D2-296 widens it only
for fallbacks.

## Code changes

| File, line | Change | Owner |
|---|---|---|
| new `engine/book.py` | the records (`s["books"][household or person]`), `rule` (set, change, drop, propose), `reading(rule)` (the shown-back sentence), `match` (precedence, §7), `pending(w)` (the latch, §3), `spare_units(w, today, order, budget, used, results)` (§5, §6), `rec["book"]` (fired, partly, missed, lapsed, gone against) | 37.4 |
| `verbs.py` VERB registry | `rule` (cost 0) | 37.4 |
| `run.py:1036-1057` | replaced by `book.spare_units(...)`; the fallback loop kept inside it for tier 2 | 37.4 |
| `run.py:498`, `:521`, `:926` | the reply's `fallback` sets the standing fallback | 37.4 |
| `prompt.py:106`, `:261` | the `fallback` field's text: "acts for units left over, in order; they stand until you change them"; the example dropped | 37.4 |
| `prompt.py` system text; `evening.py` | the rules block (§9); the book with what each rule did at the evening | 37.4 |
| `prompt.py:652-700` `_house_lines` | the morning's record lines (§9) from `rec["book"]` | 37.4 |
| `here.py:378-386` `party_container`; `verbs.py:326` `_out` | goods arriving go by the book's `go`, then home (E10) | 37.4 |
| `verbs.py:1569-1595` `_move` | `from` and `to` as buildings and containers; taking down at U4's rate; between buildings at basis §5's | 37.4 (verb), rates 37.2 |
| `night.py:116-127` | the draw order by `first`, `eat`, `hold back` | 37.4 (W-37) |
| `process.py` (U4) | `states(w, household)`: done, in process, has room, full, fire out by container; `load`, `tend`, `take_down` callable from a chore at a real fraction | 37.2 |
| `buildings.py` (U5) | `fill(b)`: has room, full, under n, by portion; `alloc` reading `keep` and `hold back` | 37.2 writes in 37.4's module |
| `perceive.py` / memory (read only) | `seen(w, household, set)`: a member noticed a sign of the set that day | 37.2 reads 37.4's |
| `life.py:236` `children_work` | unchanged now (Gaps, 3) | 37.2 |
| `bots_livelihood.py` | a bot policy that sets a book (go to racks, take down when done, tend, a fallback) to exercise the interfaces | 37.2 |
| spec agents/standing_orders.md, actions.md | amended when decided (S5) | 37.4 |

## Tests

Interface tests with bots (D2-298: interfaces, not behaviour):

1. A `rule` act is read back in the engine's words; refusals of §9 fire with their reasons; a member's household rule becomes a
   proposal.
2. The latch: a done lot with "take down when done" and no one with spare units stays pending, is shown as not done, and fires the
   next day.
3. Order: the spare-units phase runs after every plan: Wat's tend at midday brings 150 kg home; Agnes, who planned 2 units of 6, hangs
   it by rule in her 4 spare units.
4. Tiers: a person with a standing fallback of firewood and a household tend pending tends first, then gathers; with two rules for
   the same goods, the person's own wins and the record says she went against the household's.
5. Fallbacks: the person's own before the head's chore for them; unset, units unused and the line says how many.
6. Labour: chores' fractions carried until whole; never more units charged than spare; none taken from a plan.
7. Cascades stop at three rounds; each rule fires once a day.
8. `seen`: a rule "when we have seen the run" fires only on a day a member noticed a run sign; never from the run's hidden pulse.
9. Store moments: a catch with a `go` rule to the Smoke Hut arrives in its store, not in the first-claimed building (E10).
10. Replay: the same book and journal give the same chores and lines.

**What live runs should read** (against a null arm with no book, only today's hand acts and fallback): the rules people set and drop;
missed tends and lots left up; the share of the day the fallback fills (steering's 33 to 60%), and whether it follows need with
`when`; whether heads assign chores and members go against them; the qualitative end state (who runs the household's routine).

## Basis rows needed

| # | Row | Value | Mark |
|---|---|---|---|
| 1 | A chore's work charged | real fractions summed a person a day, carried until whole as the walk (`labour.step`); at least 1 spare unit to start | default |
| 2 | Cascades | at most three rounds a day; each rule once a day | default |
| 3 | "Whoever has time" | members at the node with at least 1 spare unit, the most spare first, then by name | default |
| 4 | A cap on rules | none now; measured | default (store_rules open question 1) |

Moving between buildings uses basis §5's provisional rate (D2-274); taking down, hanging and salting use U4's.

## Gaps

1. **The chore phase against the fallback (G4): designed** (§5, §6), on a reading of D2-296 asked of Zach (Q-U6-1).
2. **What a rule may do (W80-Q6): designed** with D2-296 (Departure 3; Q-U6-2).
3. **Children's standing work as a household chore:** the same thing as the head's `chore` for a child; folded into the book after the
   spare-units phase runs in live runs (it waits on them, so that D2-148's dial is not disturbed before it can be compared).
4. **A household as a shared book people subscribe to, a village smokehouse by rota, constitutions: deferred** (L-151).
5. **Travel in the book: deferred** (L-152).
6. **Rules passed to a household founded by a member, and who may change the household's rules:** standing_rules open questions 1
   and 5 (37.4's).

## Open questions for Zach

1. **Keeping chores before fallbacks** (Q-U6-1; G4; W80-Q13; D2-296). D2-296 says a person's own standing fallback comes first over
   the head's chores. Options: (a) two tiers: keeping chores the book sets off by a state (tend the fire, hang what came in, take down
   a done lot, move) first, then fallbacks, a person's own before the household's; inside each tier a person's own rule beats the
   household's; (b) a person's own fallback before everything, the household's keeping chores after it; (c) every household chore
   before any personal fallback. Recommend (a): it keeps D2-296's precedence for what is done "when nothing else is planned" without a
   filler (today's firewood fallback fills 33 to 60% of the day) taking the units a fire needed; a person can still opt out of a
   household chore with their own rule, and it is seen. Default taken: (a). Blocks: the spare-units phase.
2. **What a chore may be** (Q-U6-2; W80-Q6 with D2-296). (a) A fallback's acts, production included, with `when` and `unless`;
   trade, travel, another's things refused; (b) keeping only. Recommend (a): D2-296 made fallbacks the book's, and a `when` lets a
   filler follow need. Default taken: (a). Blocks: the grammar.
3. **A fallback left unset** (Q-U6-3; L-142; steering question 2). (a) Unset at the start; units left over go unused and the morning
   says how many; the reply's field sets it and it stands; (b) the morning asks for one until it is set; (c) an engine default (D4-76
   rejected it). Recommend (a): it is a fact, not an ask, and the reply's field stays in the format. Default taken: (a). Blocks: L-142.
4. **When rules are changed** (C29; 37.4's to decide). (a) By a free act at any time, shown at the evening; (b) only at the evening.
   Recommend (a). Blocks: the `rule` act.

## Sources

store_rules.md; standing_rules.md (37.4's, read only); fallback.md; L-142, L-151, L-152 (records); store_management.md §1 to §7;
wave3_keeping.md §4, §6, §7 items 6, 17, 18; wave4_people.md §2.4, §3.4; steering.md §1.1, §3, §5; wave_conflicts.md G4, C29, S5, S12,
K9, E10; DECISIONS D2-274, D2-279, D2-282, D2-296, D4-16, D4-23, D4-35, D4-76, D2-148; the code under Extends; U4 and U5 of this
folder.

## History

- **22 Nov 2026:** written by a 37.2 design subagent for W-85 from the sources above.

*Current as of 22 Nov 2026: D2-263 to D2-298.*
