---
id: docs/review/37_growth/02zzzh_hunt_fish/prompt_compare.md
kind: note
updated: "2026-11-24"
---
# The new prompt against the old, act by act (37.2, 24 Nov 2026)

*note · `docs/review/37_growth/02zzzh_hunt_fish/prompt_compare.md`*


At Zach's ask, after session bench's audit (docs/review/39_monoculture/prompt_audit.md on its branch; D5-2, "interface is not
world"). Read in full: Osric's day-0 system prompt under the rebuilt core (2,016 words) and under the old prompt (7,174), copied to
`iface_ref/`; every handler in `engine/verbs.VERBS` (40) and its `args`; `engine/shapes.py` (SHAPES, FACE, `crafts_by_shape`,
`lines`); checked against the code where an act refuses without an argument.

## 1. Acts the new prompt never names

| Act | What it does (old prompt) | New prompt | Note |
|---|---|---|---|
| watch | a day beside someone: you see how they do things (4 units) | not named; the core says knowledge comes "by watching" | the main way to get a rough idea of a craft |
| meet | call a meeting for tomorrow's start; all who come hear and witness | not named; `go` says "come" to one | nobody can call one |
| write, erase | lines on a building or monument | not named (mapped under `work`'s faces only) | |
| withdraw | take back an offer | not named (in FACE only) | |
| rest | | not named | harmless: units left are rest ([[D2-301 A person's own rules and standing fallback come before every…|D2-301]]) |
| set (gear) | lay traps, snares, a net or a line | shown only while one holds gear (`shapes.py:449`) | a person who could make snares is not told they can set them |
| look_up (reply) | a craft's card before work | gone from the reply format | the only way to read what a craft does |

## 2. Acts reduced to a word, without the arguments they need

| Act | Needs | New prompt |
|---|---|---|
| try for a child | "with", "units" (more units, better chance); both sleep in one place | "trying for a child", last phrase of `agree` |
| partner, part | "with" | "partnering"; "a partnership (part)" |
| teach, learn | the craft | `agree {"do", "with"?}`: the craft's key is not shown (the shapes read it from the words, `shapes.py:170-186`) |
| join, admit | the household, the person | phrases in `agree` |
| care for a child | "at" the child, "item" and "qty" of food, "pass" a sentence | shown only to someone already caring, in the family lines |

## 3. Options and arguments gone

- **work:** "item": which seed to sow (sowing **refuses** without it: `farm.py:931` "say which seed to sow"), which beast to slaughter,
  food for a child; "on" (whose plots in a shared field), "plots" (how many to sow), "pass".
- **gather (hunting):** "range" near | the wood around | far; "alone", "only", "with" (parties); "looking for" one kind; "lead" a
  pack ox; "for" a party.
- **build:** "qty" (how many beds or stalls), "storey" 2 or 3, "how" fine | rich | grand (seen from next door, the road, by all),
  "name", "describe", "upgrade" to timber or stone; a room added costs a quarter less; what each build costs.
- **travel:** "days", "stop at", "gather" on the way, "meeting" stop | pass by, "searching" a lost herd or person, "lead" a pack ox.
- **force:** guard's "units" by day; attack's cost (3 units).
- **move:** `drive` needs "thing" (a herd) and "to" (a place here), not the item, qty, from, to the shape shows; "for" giving from the
  household's store; take's and drive's 1 unit.
- **change:** claim's "plots" and "for"; host's "feed"; grant's "what" and "days"; name's "as" (naming a beast or a thing); order's
  "what" (forage | herd | hay | nothing); burial "method" cairn | shallow.
- **offers:** "lots", "for", payments over time ("2 grain every 3 days for 4 times"), what is owed and arrears.
- **say:** to a building; **tell:** the day's number of private messages (in the morning's header only).

## 4. Techniques: names, not what they do

- Under each shape the person's crafts are names with level, units and covers; nothing says what a craft does (the old: snare
  "catches by night for a few nights: come back ... or it rots there"; drive "dangerous alone"; smoke fish "done after 1 night of a
  tended fire, half the weight, keeping about a season"; ret flax; hard cure).
- **Tools:** the old showed what a tool does to each craft (fell bare hands x0.25, a copper tool x2; cut bare hands cannot); gone.
- **Recipes everyone knows show no inputs** (bedroll, snares, hand line, salt fish, dry fish, fishing rod, tent, crude tool, the
  smoking and curing), though [[D2-263 A craft a person knows at capable or known shows, where they look|D2-263]] says known recipes show their inputs; only the person's own levelled crafts do (bread, dry
  fodder).
- **Crafts only known of are listed under "Yours"** beside doable ones ("mine (you have seen the Brooks at it all your life)" in
  gather; boil salt, coin, smelt in make), where the old kept "You know of, but not how" apart.

## 5. Wording faults in the new

- `go` crams four acts into one line ("sleep" at a building; "come" to a meeting; a "fire" on the road), and a fire needs timber in
  hand and saying it before setting off, which is not said.
- `change` offers "a standing rule (rule)", the old rule act with the older kinds, beside the "rules" reply field and [[D2-339 The household book's grammar|D2-339]]'s
  grammar: two ways, one stale.
- The core's "settle the night" no longer says what is settled (where you sleep, whom you let in, trying for a child, setting off
  at nightfall), which the old core said.

## 6. What the new does better, and what the old put in that is world

- Better: the core's twelve lines (how life goes) are clearer than the old's; the rules grammar; one's crafts by level, one's own
  first; no option list ([[D2-286 The list of what one could do today|D2-286]]).
- Rightly left to memory (world, D5-2): the food table, fuel heat, fittings' wear counts, the weights table, units by season.

## 7. What the restoration should do (D5-2, within the shapes' grammar)

Every act in `VERBS` reachable by a shape is named in its shape's line with its own arguments and options and their costs; the
family acts (try, partner, care, watch, teach, learn) on their own lines; meet, write, erase, withdraw named; set shown whenever
the person knows a gear craft; look_up back in the reply; each technique with a phrase of what it does and what a tool does to it;
every known recipe with its inputs; crafts only known of kept apart; `go`, `change` and the core's evening line put right; a test
that every handler's args keys appear in the rendered prompt for someone who can use it.
