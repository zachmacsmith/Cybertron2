# How a household manages its stores: one book of standing rules, a few defaults, labour only where real

22 Nov 2026, 37.2 (subagent). This is a design note. No code was changed and nothing was committed.

**Zach (22 Nov):**
- "dig deeper into how the automanagement of stores should actually work. Think about different scenarios of where should the
  decision making land: between multiple rooms? Knowing which things they have? Moving between stores? etc. Should it follow
  automatic fully, or maybe something more like the standing rules? ... Ideally the principle should be balanced automatically unless
  something would realistically provide a labour burden, but transparent and more manageable if looked into."
- "they should be able to move things around their store if they want, and attend to their store to see where everything is, the
  state of everything, and know how much of what they have so if they want to build more of things."
- His steer: "as little as possible is decided by us unless super obvious defaults exist, and the automatic management should be
  reroutable in an understandable way by the agents, ideally in the same standing rule system we might later use for which food is
  eaten when: I guess where to put things, where to keep them, and what to take when all seem like everyday standing rule sorts of
  things?"

**Read with:**
- [storage.md](storage.md), the stores, containers and the locked chest;
- `proposals/standing_rules.md` (OPEN W-37: how a household eats and what it keeps back);
- OPEN L-142 (fallbacks as a standing setting);
- `proposals/acts_on_owned_things.md` (Q-80, the thing as the target);
- the decisions: D4-23 (a household's members use its store, the head manages it), D4-76 (the fallback), D4-89 (goods at the door
  stay the house's), D4-96 (acts draw on the stores here), D4-105 (a leg's walk).

---

## 0. In brief

**The principle.** One *book of standing rules* per household, and one per person, says four everyday things:
- where incoming goods go;
- where things are kept, and what is held back;
- what is taken or eaten first;
- what is moved, by whom.

The engine applies its own small set of defaults (§3) only where the book says nothing. A rule is the agent's sentence mapped onto a
small grammar (§2), shown back to them in their words and in the engine's reading, and changed by an act at any time (free) or at
the evening. Eating rules (standing_rules.md) are the same book, read at a different moment.

**Where labour lands.** Moving is free within a building (rooms, storeys, a cellar, its containers) and on arrival: the harvest goes
straight to the store a rule names, since it is being carried anyway. Moving goods that are already stored, from one building to
another, costs work by weight and distance. It is done by an act, or by a standing chore that a named person, or whoever has units
left (the fallback, L-142), does out of their units. Moving between households is always an act: give, trade, an agreement.

**What they see.**
- Each store's line by default: what it holds, where it lies, room left, and what is outside.
- *Attending to the store* (the reply's existing `attend` field) shows everything:
  - each container and space by tag, with fill, room and state;
  - what spoiled where last night, and what vermin took;
  - what is held back, and the locked chests;
  - the rules in force, and what they did.

That is enough to know what to build more of.

**Two findings in the code:**
1. Work done for a household goes into `here.party_container` (here.py:379). That is the *first building in the world's insertion
   order* with a withdrawal claim, usually the house, so a granary built later never receives a harvest. In pw1 the Reed Granary held
   10 grain on day 15 while 96 lay outside the Reed House door.
2. The agents already sort by hand. pw1 shows 292 `store` events (moves into and out of stores), about 33 of them into the granary
   and 38 into byres; wild_region_s7 shows 326. `move` costs nothing, wherever the store is at the node, and eating, making and
   giving draw from every household store at the node for free (D4-96).

---

## 1. Where the decisions should land: the thought experiments

Each scenario first asks what a real household would do, then what must be decided, and by whom.

**1. Two rooms in one building** (a hall and an upper chamber over it, a cellar under).
- **Real:** the grain goes up to the dry chamber, the cheese and salt meat down to the cellar, and the roots in baskets by the cold
  wall. These are carries of a few metres.
- **Decision:** none needed. Where each good keeps best, with room, is obvious (storage.md's sort), and costs no work.
- **The rule:** a rule can say otherwise ("the seed barley in the ark"), and that wins.
- **Engine:** the building's one `stock`, sorted into its spaces and containers. Rooms by storey give their climate: a ground floor is
  damp; an upper storey is boarded and dry, like a granary floor.

**2. A harvest of 800 grain for Holt** (a hall with bins and a granary floor in it, and a byre on the same parcel).
- **No rule:** the grain goes home, which is obvious. Inside, the sort puts it in the bins (300) and on the granary floor (up to
  1,200).
- **If the house fills:** the overflow goes to the household's next store at the place with room, here the byre. Only when every
  store is full does it lie at the house's door. The morning line says so: "800 grain came in: 300 in the bins, 500 on the granary
  floor".
- **A rule** "grain goes to the Granary" (a separate building by the mill) sends it there instead.
- **Labour:** none extra. The harvest is carted from the field either way (reaping already carries it).

**3. A new granary is built.**
- **Real:** a granary is built *for* grain. Building one is the household saying where its grain goes.
- **Default:** the build writes the rule into the book: "grain goes to the Granary (set when the Granary was built)". It is shown at
  that evening and dropped by a word.
- **Why:** this is the one default that fixes finding 1 while staying visible. It is the same for a woodshed (fuel) and a barn or byre
  (fodder). A smokehouse, a cellar and a vault get none: what goes there is a choice.

**4. A glut of fish** (a peak weir night: 100 kg of eels lifted into hands).
- **Real:** fresh fish must be gutted, then smoked, salted or eaten within a day or two. That is work and a choice.
- **Default:** what one carries home is put away at night (§3 D7), into the house, where it spoils at fresh fish's rate (D2-212).
- **Rule:** "fresh fish go to the smokehouse" puts them in the smokehouse's store, where the `smoke fish` act finds them.
- **What stays an act:** hanging them and salting them (real labour, and the smoke-or-salt-or-eat choice). A standing chore can't do
  it: production belongs to the fallback (L-142), not to the store's rules.
- **The morning line:** "100 fresh fish in the smokehouse; the racks have room for 500; fresh fish lose about 18% a night in a
  store".

**5. Seed kept apart.**
- **Real:** the seed barley sits in its own sack or the ark, and nobody eats it unless the house is starving.
- **Default:** nothing is held back (standing_rules.md rejects keeping seed back automatically, as that is the very thing a run
  tests). The evening's rules always show "nothing is kept back" until a rule is set.
- **Rule:** "keep back 40 grain as seed, in the ark, unless someone is starving". The sort puts the 40 in the ark; eating, making and
  giving skip it; sowing draws it first.
- **Going against it:** taking from it is recorded and noticed (standing_rules.md item 3).

**6. A hungry spring** (the store at 5 nights' food, the seed held back, the salt fish for the winter).
- **Rules:** the eating rules say the order ("the roots and acorns first, the salt fish last") and the rations ("half rations when
  under 10 nights"). The held-back seed opens only by its `unless`.
- **Default:** eat what spoils first, food that needs no fire first, full rations (standing_rules.md's default, the engine's present
  policy).
- **No labour:** drawing from the household's granary at the place is free (a day's grain is a light carry).

**7. A locked chest** (storage.md §9).
- **Real:** the master's coin and the good knives are in the chest, and he has the key.
- **Rules:** no household rule reaches inside it. The key holders' own rules do ("keep my coin in my chest"). The sort never places
  goods in it or takes them out.
- **What one sees:** "your locked chest (C3): 24 coin, 2 copper tools"; another's: "Anna's locked chest (C5): you hold no key".

**8. A household's buildings on different parcels** (the house on the Street, the granary two parcels away by the mill).
- **Real:** carrying 300 grain two parcels (about 300 m) is six or seven trips with a sack. That is an hour or two, real work.
- **On arrival:** free, by the rule (the cart goes to the granary instead of home).
- **Afterwards:** moving it costs work. An act ("carry 300 grain from Holt House to the Granary") or a chore rule ("keep the
  house's bins full from the Granary; Joan does it"), charged by weight and steps (§4).
- **Drawing for a meal** stays free (D4-96).

**9. A household splits** (a son founds his own house).
- **Real:** the goods are shared out by agreement, and the new house starts its own ways.
- **Rules:** the new household's book starts at the defaults. Whether customs carry over is standing_rules.md's open question 5. A
  rule in the old book that names a building the household no longer holds lapses, and is shown as lapsed.
- **Goods:** divided only by acts (give, an agreement). Never by a rule.

**10. Between households** (a lord's barn taking rent in kind, a village granary).
- **Always an act:** give, pay, an agreement's leg. A rule may not route goods into another's store. That is a gift or an
  obligation, which is a decision whose trade-offs change, and is what a run measures (standing_rules.md excludes trade).
  Agreements may later automate their own legs.
- **Taking** from a store one has no right to is theft, as now.

**11. Knowing what they have, and what to build.**
- **Real:** the goodwife knows the ark is two-thirds full, the sacks are gnawed, and the cellar is damp.
- **Engine:** the morning line per store (default), and attending for the full account (§5). The default is a fact, never advice.
  "335 grain lie outside the door; the Granary has room for 300" tells them what to build or move without telling them to.

---

## 2. The general mechanism: the book of standing rules

**Whose book.** One book for each household, set by its head; members propose at the evening, as in standing_rules.md item 4. One for
each person.

**Precedence** (standing_rules.md item 3), highest first:
1. what the person does in a turn;
2. their own rule;
3. the household's rule;
4. the engine's default.

Going against the household's rule is never hidden: it is recorded and noticed, so it can be answered.

**When the book is read** (one mechanism, read at five moments):

| Moment | Rules read | What it decides |
|---|---|---|
| goods arrive (work output, a gift, a purchase, what one carries home at night) | **go** | which building's store they go into |
| inside a building, every time its goods change | **keep**, **hold back** | which container or space each good lies in, and what is set aside |
| drawing (the night's eating, making, building, giving, paying) | **first**, **hold back**, **eat** | which store and which good is used first; what is not touched |
| the night's meal | **eat** (order, rations, who first, guests: standing_rules.md) | how the household eats |
| a person's spare units (the fallback) | **move** (chores) | stored goods carried between buildings, by whom |

**The grammar.** A rule is a small record. The agent writes it as an act (`rule`, 0 units) with fields and its own sentence, and the
engine shows it back as a sentence of its own reading, with their words in brackets.

```
{"rule": "go" | "keep" | "hold back" | "first" | "eat" | "move" | "drop",
 "goods": an item ("barley") | a kind (below) | "everything",
 "to" | "in": a building, a room or storey, a container (tag or kind: "the ark", "sacks"), or "hands",
 "from"?: a building or container (for "move", "first"),
 "qty"?: n | "all" | "up to n" | "leave n",
 "before"?: goods or a place (for "first", "eat"),
 "who"?: the household | a person | guests | key holders,
 "by"?: a person | "whoever has time" (for "move"),
 "unless"?: "someone is starving" | "winter" | "it is full",
 "words": "their sentence"}
```

**The kinds** are only the engine's existing groupings:
- grain (STORES kinds: grain, rye, beans), and dry goods (DRY_STORES, with meal and flour);
- food (EDIBLE), split into fresh food (spoils in days) and keeping food (dried, salted, smoked, cheese);
- fish, meat;
- fuel (the heat order: firewood, timber, charcoal);
- fodder (hay, straw);
- tools and weapons, coin;
- everything.

**Matching.** The most specific rule wins: an item over a kind over "everything"; a person's over the household's; then the newer.
The matches are shown at the evening when two rules meet. A rule that cannot be followed (the Granary full, a building gone) falls to
the defaults for that good, and the line says so: "the Granary was full: 200 grain went home".

**How a rule is shown back:**

> Grain goes to the Granary (your words: "all the barley into the granary by the mill").
> Keep back 40 grain as seed, in the ark C3, unless someone is starving.
> Joan keeps the bins of Holt House full from the Granary, with her spare time (about 1 unit a day when it runs).

**Limits** (for legibility): about 12 rules a household and 6 a person (est.). A rule naming a place one no longer holds lapses.

**Eating and stores in one book.** standing_rules.md's eating rules are the `eat` and `hold back` rows: order, rations, who first,
guests, what is kept back. `first` is the same rule for drawing at any act ("make with the old timber first"). One parser, one evening
block, one precedence, one "going against it is noticed".

---

## 3. The engine's defaults (where the book is silent)

The smallest set I can justify. Each is obvious, or the engine's current behaviour made visible.

| | Default | Why it is obvious |
|---|---|---|
| D1 | **Goods come home**: work output, gifts and purchases go into the store of the building one lives in at the place (for an act `for` the household, its home there) | a person brings things home; fixes the insertion-order finding |
| D2 | **Inside a building, the best keeping place with room**: each good into the container or space that protects it best (storage.md's sort: grain in the granary on staddles, the chest, bins, the granary floor, sacks, then loose) | nobody tips grain on the floor while the ark is empty |
| D3 | **Full, the next store, then the door**: the household's other stores at the place with room, nearest first; then outside the home's door (D4-89), with its line | the cart goes on to the next door; nothing is lost without being said |
| D4 | **Drawing**: hands, then home, then the household's other stores here, then its door piles; food that needs no fire first, then the most perishable; full rations; guests fed by the host | the engine's present policy (night.py `_eat`, D4-96; standing_rules.md item 1) |
| D5 | **Nothing is held back** (and the evening says so) | standing_rules.md: keeping seed is what a run tests |
| D6 | **A store built for a kind writes that kind's go rule**: a granary for grain, a woodshed for fuel, a barn or byre for fodder; shown that evening, dropped by a word | the one place the purpose is plain; a rule, not hidden behaviour |
| D7 | **What one carries home is put away at night** (D1, then D2), except tools, weapons, gear in use, and what a rule keeps "in hands" (road food) | one sets down one's load at home; today it spoils at the in-hand rate |
| D8 | **Labour only where moving is real** (§4) | Zach's principle |
| D9 | **Never between households by rule** | it is a decision |
| D10 | **A locked chest is outside every rule but its key holders'** | storage.md §9 |

---

## 4. Labour: what moving costs, and who pays

Real moving, all estimates: a sack of about 40 kg on the back, and a parcel's step about 150 m (2 ha cells, about 141 m across).
- One trip one step and back, about 300 m at a loaded walk, takes about 5 to 6 minutes with loading. That is about 20 trips, 800 kg,
  in a unit of 2 hours.
- Within one parcel (a farmyard, 30 to 60 m) it is about a quarter of that.
- Within a building it is a few metres: nothing to count.

| Move | Cost |
|---|---|
| within a building (any rooms, storeys, cellar, containers) | free |
| on arrival, by a go rule or the defaults, to any household store at the place | free (it is being carried anyway) |
| drawing for an act or a meal from any household store at the place | free (D4-96) |
| stored goods from one building to another, same parcel | about 1 unit a 3,200 kg (a quarter step), carried as fractions until whole (as `labour.step`, D4-105) |
| stored goods from one building to another, n parcels apart | about 1 unit a 800 kg a step; a handcart x3 the load, a pack ox x6 (est., from the carry table) |
| between places (nodes) | travel, as now (D4-9) |

**Who pays:**
- An act's mover pays at once: "You carried 300 grain from Holt House to the Granary, two parcels: about 1 unit."
- A `move` chore rule is done by its `by` person out of their *spare* units, the fallback's place (D4-76, L-142). If it says
  "whoever has time", it falls to the first member with units left.
- What was done shows at the evening ("Joan carried 200 grain into the house's bins from the Granary: 1 unit"). What was not done
  shows too ("nobody had time to fill the bins").
- A chore never takes units from someone's plan.

---

## 5. What a person sees

**By default** (the morning's house lines, prompt.py `_house_lines`, which already lists each home's full store):

> Holt House's store: 735 grain (400 in the ark C3, 300 in 6 sacks, 35 loose on the floor), 9 beans in a basket; room for about 600
> more dry goods; 335 grain lie outside its door.
> The Granary (by the mill): 1,200 grain on its floor, full.

The line is per building, by portion, with room left and what is outside, and nothing more.

**Attending to the store** (the reply's `attend` naming one's store or a building of one's household; THINGS attention "subject"):
- each space and container by tag: its fill, room left, state and life ("6 sacks, 2 gnawed through, a world year left in them"; "the
  ark C3, sound"), and the room's own condition (a gappy roof lets the damp in);
- last night's spoiling by where ("35 grain loose on the floor lost about 0.3; nothing in the ark");
- vermin: what was taken and where, the signs (storage.md §6), the cat or owl if any;
- what is held back, and by which rule; locked chests (one's own contents; another's: locked);
- the rules in force for these goods, and what they did last night or today ("by your rule the barley went to the Granary; it was
  full, 200 went home").

**Managing by hand:**
- `move` with `from` and `to` as buildings or container tags, to re-sort (free within a building, charged between them).
- `keep {hold: C3}` holds a container back from the sort (storage.md §9).
- `rule` sets, changes or drops a rule at any time, at no cost. The evening shows all rules with what they did.

---

## 6. How it sits with the engine now

**`world.takeable` and D4-96 (`verbs._top_up`).** Drawing from every household store at the node stays (D4 above). Hold-back
portions and locked chests are left out of it.

**`here.party_container` (here.py:379).** It picks the first building with a withdrawal claim in insertion order. It is replaced by
the go rules, then D1 (home), then D3. Its callers are `verbs._out`, which carries work output into a store, and the agreements'
payments (agreements.py 125, 196, 249, 345). The payment callers keep "the payer's home" as their source, under D4.

**`verbs._move` (verbs.py:1569).** Today it moves between hands and a store, at 0 units. It gains `from` and `to` buildings and
container tags, and the labour of §4 between buildings.

**`verbs._into_store` and `buildings.overflow` (418).** Overflow tries the household's next store at the node (D3) before the door.

**`night._eat` (night.py 118-120).** The store order (hands, home, others) becomes D4, under the `first`, `eat` and `hold back` rules.

**`keeping.done_into_store`.** A smokehouse's finished batch goes into the store of the building it hangs in, for its household. This
is kept; a go rule can send dried goods home.

**The night.** D7 (putting away what one carries) runs before eating and spoiling, for those sleeping at home.

**The evening (standing_rules.md item 5).** It shows the book, and what the rules did.

**The thing as the target (acts_on_owned_things.md).**
- Stores and containers are named by building and tag.
- An act with no target touches one's own and one's household's.
- A rule may name only one's household's buildings and containers, and a person's rule only what they may use.
- A `move` from another household's store is a take, and theft without the right. A `move` into it is a give.

**Household access (D4-23).** Members may use the household's stores. The head sets the household's rules, and members their own. A
member's rule or act against a household rule is recorded and noticed (standing_rules.md item 3).

**The fallback (D4-76, L-142).** Chores sit in the fallback's place. A person whose fallback is unset still does a chore named for
them. This is one more reason to make the fallback a standing setting (L-142).

**Engine cost (est.):**
- the book (records, the `rule` act, the parser of the grammar, matching): about 200 lines;
- the five reading moments (go, keep, draw, eat, move): about 150, over storage.md's fit-out;
- the evening block and the attending view: about 120;
- tests.

The eating rules (W-37) share the book, so building one builds most of the other.

---

## 7. The recommendation

Make store management part of one general standing-rules mechanism:
- one book per household and per person;
- the grammar of §2;
- read at five moments (goods arriving, a store's goods changing, drawing, the night's meal, spare units);
- the engine's ten defaults of §3 only where the book is silent;
- labour charged only for stored goods carried between buildings (§4), done by an act or by a chore out of spare units;
- between households always an act;
- the store's default line, and the full account on attending (§5).

Build it with the eating rules (W-37) as one piece: the book, the parser and the evening block are shared, and L-142's standing
fallback carries the chores.

**Asks for Zach:**
1. **One book for eating and stores.** The grammar and its kinds as in §2.
2. **D6.** A store built for a kind writes its go rule, shown and droppable. Or no default at all, and the build result says nothing
   goes there until a rule does?
3. **D7.** What one carries home is put away at night.
4. **The labour of §4.** Free within a building and on arrival; about 1 unit a 800 kg a step between buildings (est.).
5. **Chores** out of spare units (the fallback's place), and the limit of about 12 rules a household.
6. **standing_rules.md's open questions** carry over, especially whether a member may change the household's rules, and whether
   rules pass to a household founded by a member.
