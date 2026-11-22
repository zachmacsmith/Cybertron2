---
id: docs/review/37_growth/02zzzh_hunt_fish/wave3_taking.md
kind: note
updated: "2026-11-22"
---
# Design wave part 3b, taking: set and tend, snares, the weir, nets, lines, the edge and the hunt as acts on things

*note · `docs/review/37_growth/02zzzh_hunt_fish/wave3_taking.md`*


22 to 23 Nov 2026, 37.2 (overnight subagent). Thread [[W-81 Design wave part 3b, taking|W-81]], under fishing, hunting and their materials developed together ([[W-73 Fishing, hunting and their materials developed together|W-73]]),
designed in full before it is built ([[D2-278 The next wave of the fishing, hunting and materials network|D2-278]]). No code, proposal, spec or record changed; nothing decided. Bot probes ran in the
scratchpad on a copy of the runs world (`specs/nutrition/runs_medium.yaml`, seed 5); no model calls.

**Builds on:** the network (proposals/hunt_fish_materials.md, §5 gear, §7.1 and §7.2 methods, §7.7 snares and edges, §7.8 the shallows
and the fen's traps), river_signs.md, acts_on_owned_things.md, verb_grammar.md (exploration), trying_and_learning.md, spec/core/clocks.md;
decisions [[D2-263 A craft a person knows at capable or known shows, where they look|D2-263]] to [[D2-285 The records brief is run by hand after each compaction for now, since…|D2-285]]; the notes fishing_ladder.md, hunting_ladder.md, engine_audit.md, crafts_evaluation.md in this folder, and
02zzy2 (the live runs). **Prices** come from part 1, now final (wave1_physical_basis.md: weights §1, the keeping curve §2, gear §3.2,
carrying §4). **Shapes** are part 4's (wave4_people.md §5: go, gather, set and lift, work, make, build, move, change, agree, force); §6
says where they fail for taking. **Making and mending** gear is part 2's (wave2_making.md, started): this note names what wears and
when, never how it is made or mended.

**Code read** (main, 22 Nov): `engine/verbs.py` (VERB, `_technique`, `_take`, `_lift`), `engine/wild.py` (`set_work`, `_set_night`,
`hunt`, `run_take`, `_runs_night`, `_robbers`), `engine/knowledge.py` (`ready`, `options`), `engine/things.py` (`find`, `set_line`,
`look_text`, `owns_set`), `engine/here.py` (`building`, `parcel`), `engine/tags.py`, `engine/prompt.py`, `wild/methods.py`,
`wild/kinds.py` (TRAITS, RUNS, RUN_SIGNS, WARY), `wild/gear.py` (`share_run`), `engine/data.py` (TECHNIQUES, MONUMENTS weir,
WATER_WORKS, THINGS.set, NOTICING). 37.4 owns verbs.md, the verb registry, the prompt and the senses core: read, not edited.

Marks: **[m]** measured in the engine or a probe; **[d]** a decision; **[w1]** part 1's figure; **[e]** my estimate, to calibrate.

---

> **Correction by 37.2, 22 Nov ([[D2-286 The list of what one could do today|D2-286]], [[D2-287 Reviewing past runs|D2-287]]):** the "Today you could" list (fault 9, question 14) is not shown in any current
> world: the beliefs view (`view: beliefs`, every current world) has no options list (`engine/view.py:7`). The probe that found it
> rendered the old prompt (`prompt.turn_prompt`). It survives in one path: the beliefs view falls back to the old prompt when a person
> is at no place (`view.py:175-176`), so a traveller can still see it. Zach (22 Nov): the list is removed from the code entirely in the
> crafts, archetypes and beliefs rebuild ([[D2-286 The list of what one could do today|D2-286]]); "sort by one's livelihood first" is withdrawn. It is not a cause of "agents rarely
> fished" in current-view runs; any past run read for it is checked against its view setting first ([[D2-287 Reviewing past runs|D2-287]]).

## The short answer

- **One model for every take.** An act of taking is a shape (set, tend, gather, work), a technique (the how: wicker traps, snares, a
  gill net, a hand line, the edge, the hunt), the gear it uses (held, worn by use) and a target. The target is a **stock** for a
  worked take (the shallows, the open water, a run, the game of an area) and a **thing** for every act on placed gear (a line of
  traps, a snare line, a set net, the weir's traps). Placed gear is one's own thing, with a tag, standing until it is taken up.
- **Set and tend are two acts on gear one holds.** Set lays gear from one's hands; with none in hand it is refused and the refusal
  names one's gear already standing and how to tend it. Tend goes to one's own placed gear at a place: takes the catch, sets again
  what was sprung, and with `up` brings the gear home. Named alone, a technique whose own gear already stands at the place tends it;
  with none standing it sets. That one rule ends the set-for-lift confusion (about 40% of trap acts in the live runs), because the
  mistake can only happen when gear is free and the default is set; it is neither here.
- **Fifteen faults, four of them named in no earlier note** (§3). The five [[Q-79 Whether to fix the fishing bugs the live runs exposed|Q-79]] bugs are traced to file and line, and the net
  puzzle now has a cause in the code: a run's salmon taken by a net adds 30 to the salmon's learned wariness, because the run has no
  resident heads to divide by (wild.py:2436). In the probe one act took learned wariness to about 6 of a ceiling of 8, cutting
  meetings about tenfold and raising flight from 0.4 to about 0.7. The other new ones: a take from another's set carries no theft
  wording; the tags given to sets are never shown in the "Lying about" line; and **the "Today you could" list is the first ten
  crafts in table order, so a fisher in the runs world is offered felling, firewood, clearing, sowing, hay, wild food, clappers,
  fencing and walling, and no fishing at all** (knowledge.py:411 to 432), a cause of "agents rarely fished" no earlier note named.
  The probe also confirmed [[Q-80 Whether acts on owned things default to one's own|Q-80]]'s finding: Peter's take from "my snares" emptied Hamon's T2 and told him nothing.
- **The river's signs lead the act** (§4). Today a run is sensed in the evening at the water, after the day's acts: zero lead. A
  trap is set by day for the night. The design gives each run four leads: the remembered year (lore, days ahead), the cue at dawn
  (the river rising after the first heavy rain, the same day), the run itself at dawn and by day, readable at the water and, through
  the herons, the roar and the catch carried home, from the village; and the night's result told on two axes (what one took, what
  the water held). Two existing rows direct an act and break [[D2-269 Experts' signs are observations of what is happening now, which may…|D2-269]]; they are reworded.
- **Worked nights** (§5). A trap household of three adults through the first autumn run of the runs world, on the river as the bot
  run drew it (about 5,900 eels past Eelmouth in ten nights, five of them in flood or spate): twelve traps feed the house through the
  run and bank about 15 kg of smoked eel and 16 kg of salt fish, about five nights of food, of which about two are left by
  midwinter on part 1's keeping curve. The gear, not the fish, binds: to bank a winter they need thirty to forty traps and about
  45 kg of salt, or a share of a weir. A hunter's winter shows
  the snare line's own clock (a catch lives, dies, is scavenged and spoils by the night), the carry binding the deer, and the
  shy-or-thin reading that decides a trip out.
- **Shapes against bespoke verbs** (§6). Shapes with techniques need about 90 words of prompt for all of taking against about 420
  for bespoke verbs, and they put the confusion where it can be refused with a reason. Part 4's shapes fail for taking in five
  places, the worst its rule that a technique named alone takes its first shape (set).
- **Questions for Zach** (§8): fourteen, each standing alone. The five that matter most are at the end of this note's summary.

---

## 0. What this note takes as decided, and what it found in conflict

### 0.1 Decided and used here

| Decision | What it fixes for taking |
|---|---|
| [[D2-264 The fishing, hunting and materials network|D2-264]] | gear lives by material; weights in kg; one set lays up to about 6 traps; a shallows stock in every water, the three stocks varying by water type; fowling split from fish nets; the snare redesign and edges in the design |
| [[D2-265 The river's signs|D2-265]] | herons at a run where a heronry is; the river's flow class for signs now; dawn signs for the river; **a freeze stops fishing**; fishers' lore with the founders' sets |
| [[D2-269 Experts' signs are observations of what is happening now, which may…|D2-269]] | experts' signs are observations of now; they may imply an act, never direct one |
| [[D2-273 Three clocks, each system on one|D2-273]], [[D2-275 A unit of work is 2 hours|D2-275]], [[D2-276 Making durable things runs on the year clock|D2-276]] | a unit is 2 hours (6 a day in autumn, 5 in winter); the act and the night's catch on the day clock; the runs, the wild's renewal and gear lives on the year clock; gear made at real hours times about 1/7 |
| [[D2-283 Salting fish runs at about 20 kg an hour with gutting, at 1 kg of…|D2-283]], [[D2-284 A smokehouse's capacity comes from the racks fitted, about 250 kg of…|D2-284]] | salting 20 kg an hour with gutting at 1 salt to 4 fish; a set of racks holds about 250 kg, a keeping smoke 1 night |
| [[Q-80 Whether acts on owned things default to one's own|Q-80]]'s answer in its notes (Zach, 21 Nov) | "the target is the thing (by tag or a known name, said in each verb), one's own things shown with tags, unnamed acts touch only one's own (one: that; several: asked; none: refused, saying whose are there), another thing only when named and called what it is". **[[Q-80 Whether acts on owned things default to one's own|Q-80]] is still open in the records and has no D2 number** (§7, conflict 1) |

### 0.2 Conflicts found while reading (each also in §7)

| # | Between | The conflict | Proposed here |
|---|---|---|---|
| 1 | [[Q-80 Whether acts on owned things default to one's own|Q-80]] notes, acts_on_owned_things.md, wave4 §5.3 | Zach said "several: asked"; wave4 says "several: a lift takes all"; the proposal leaves it open | tend takes all of one's own of the technique at the place; acts that consume (slaughter, take from a pile) ask (question 2) |
| 2 | hunt_fish §5 against §7.7 | snares as "a line of 5 nooses, 0.02 cord, about 10 sets" against "a bundle of about 25, 0.15 cord, each used up when torn or rotten" | §7.7, as [[D2-264 The fishing, hunting and materials network|D2-264]] wrote the redesign in; part 1 prices the bundle of 25 at 2 units, 0.1 to 0.15 cord, on the day clock |
| 3 | hunt_fish §5 ("lift"), §7.7 ("tend"), verb_grammar ("tend"), wave4 ("set and lift") | one act, three words | **tend**, with lift, check, empty, walk and collect as its words (question 1) |
| 4 | VERB `set` (verbs.py:53: a door, a weir's gap) against a set shape | the word set already means a setting | wave4 moves doors and gaps to `change`; if gear's set comes first, the gap keeps `set {"thing": gap}` and gear's set takes `what` |
| 5 | river_signs open question 6 (reword the frozen signs) against [[D2-265 The river's signs|D2-265]] | Zach decided a freeze stops fishing; the signs must now say set gear stands idle, not an open lane fishing on | §4.5 |
| 6 | [[D2-269 Experts' signs are observations of what is happening now, which may…|D2-269]] against kinds.py:412 and kinds.py:894 | "an eel night ...; set the traps tonight" and "net them, or draw the hatches and let them up" direct acts | reworded, §4.4 |
| 7 | river_signs §4.4 and the trap's note ("lift it with take, from its tag") | lifting by `take` is the path that confused agents | tend; the take of another's catch stays a `take` from a named thing |
| 8 | wave4 §5.1 puts ret flax under set and lift | retting is a processing container (part 3a's keeping) | leave retting to 3a; it is not a take |
| 9 | `_set_night` (wild.py:932) springs a set after its life in nights (snares 4, traps 8) | under [[D2-264 The fishing, hunting and materials network|D2-264]] and [[D2-276 Making durable things runs on the year clock|D2-276]] gear wears by uses, and a set stands until taken up | a set has no life in nights; each night it fishes is a use of its gear |
| 10 | methods.py:62 comment "whoever finds it takes the catch"; the set result "for whoever comes to them" (wild.py:918) | against [[Q-80 Whether acts on owned things default to one's own|Q-80]] | the result names it as one's own, tagged |

---

## 1. The model: what every take names

### 1.1 Four parts

| Part | What it is | Where it lives now | In this design |
|---|---|---|---|
| **shape** | what the act takes, what it costs, how long it runs, what it changes (verb_grammar §1) | the verb (`gather` for nearly all of it) | set, tend, gather, work (part 4's shapes; §6) |
| **technique** | the how: its rates, what it reaches, its lessons | a TECHNIQUES row; the wild methods generated from traits (methods.py:181) | as now, with each row naming the gear it needs and the stocks its gear reaches |
| **gear** | an item held, with a life in uses by material | absent for every set and net; the rod's 30 uses never worn (engine_audit §3) | in hand to set; in the placed thing while set; worn a use a night fished or a hunt made; back in hand when taken up |
| **target** | a stock (worked takes) or a thing (acts on placed gear, a carcass, the weir's traps) | a place, resolved loosely (things.py:622) | the stock by the gear's reach and the place; the thing by tag or known name, unnamed only one's own |

### 1.2 The stocks a take can reach

| Stock | Where | Renews (year clock, [[D2-273 Three clocks, each system on one|D2-273]]) | Reached by |
|---|---|---|---|
| **the shallows** ([[D2-264 The fishing, hunting and materials network|D2-264]]) | every water's edge, richest in brooks and fens, thin on a big river | fast in summer, near nil in winter | hands at the edge, a dip net, a spear, wicker traps at the edge |
| **the open water** ([[D2-229 One fish stock per water body|D2-229]]'s resident fish) | river reaches, lakes | slow, all year | a hand line, a rod, a set line, a set gill net |
| **a run** (eel down, salmon and lamprey up) | the river's stretches, on its nights | from the spawners that got through, and the sea | wicker traps (eels, lampreys), a set gill net (salmon), a dip net at a pinch, the weir, the race |
| **game of an area** | the wild areas about a village (`wild.state.pop`) | the wild's rule | the hunt, stalk, drive, den work; snares on the runs and edges |
| **fowl** | wet ground, fen, flooded meadow, open water; pigeons on fields | migrants in autumn and winter | fowling with a clap net (worked), hands in a great freeze, gather young and eggs at a colony |

What reaches what is decided by the gear, not by a trait match (engine_audit finding 5): each gear row carries `reaches: {stock:
weight}` and `meshes: {size, flies}`, so a fowling net meets what flies and a gill net what swims at its mesh. Today the trait
match (`social: flock`) puts salmon in the fowling net's table at 3.0 [m: `TECHNIQUES["net"]["yield"]["takes"]`].

### 1.3 A placed thing

A set is a container (`kind: set`, as now) with these fields; the new ones are starred.

| Field | Meaning |
|---|---|
| `by`, ★`household` | who set it; whose it is (one's household counts as one's own: §2.0) |
| `tag` | T-number, given at setting (as now: tags.py) and **shown** wherever one's own things are listed |
| `set.method` | the technique |
| ★`gear` | `{item: n}` laid: 6 wicker traps, 25 snares, 1 gill net, 1 set line |
| ★`uses_left` | the gear's life in uses, as a list (one entry a piece), so a mixed line wears piece by piece |
| `set_day`, ★`tended` | when set; the last night it was tended |
| `holds`, `caught`, `catch`, goods | as now: kg for traps and nets, heads for snares |
| ★`sprung` | for snares: how many nooses are sprung or torn and catch nothing until tended |
| `robbed`, `robbed_by`, ★`scavenged` | another person; an otter (as now); a fox or crows at a snare's catch |
| ★`state` | `fishing`, `full`, `idle` (frozen, or the water too low), `wrecked`, `rotten` |

It never springs by age (conflict 9). It stands, wearing a use each night it fishes, until taken up, wrecked, or every piece is worn
out. Gear left in the water through a frost is idle ([[D2-265 The river's signs|D2-265]]) and wears by time.

---

## 2. Every act of taking

Each entry: what it targets; its default target; the gear and units; the night's process; refusals in their words; what the person
sees before (the prompt's lines) and after (the result, on two axes where the water or the wood has a state of its own); what
others sense. Units at part 1's prices [w1]; take rates are the network's targets (§13 of the proposal) and marked [e] where I set
a number to calibrate.

### 2.0 The rules every act on placed gear keeps

1. **One's own** is what one set, what one's household set (a member may tend it, proposed answer to acts_on_owned_things question
   1; household gear is household capital), a weir's traps for its crew (`owns_set`, things.py:289), and what an agreement lends.
2. **Unnamed, an act touches only one's own** at the place: one thing, that one; several of the same technique, **tend takes all of
   them** (a place's worth of gear is one walk); none, refused with whose are there.
3. **Named** (a tag or a name one knows), it is that thing. Another's thing, tended or taken from, is done and named for what it is.
4. **Each result names the tags** of what it touched and what still stands.
5. **Theft from a set** is an event like the store's (verbs.py:1680): the result says so, and the setter's next look shows it (as
   `robbed` does now, things.py:363).

### 2.1 Wicker traps (set gear in water)

| | |
|---|---|
| **Targets** | the shallows at the edge (yellow eels, small fish, crayfish) and a run passing (eels, lampreys); in a fen dyke, the fen's eels and a run where the fen joins the river ([[D2-264 The fishing, hunting and materials network|D2-264]] §7.8) |
| **Default target** | set: the water parcel named, else the only water one knows here; tend: one's own trap lines at the place |
| **Gear** | wicker traps, 2.5 kg each [w1 §1.7], 0.45 withies each, made a line of 6 for 3 units at 1/7 [w1 §3.2]; life 30 to 45 sets [w1]; a creel to carry the catch (+5 kg for fish, [w1 §4.1]) |
| **Set** | up to 6 traps an act [d [[D2-264 The fishing, hunting and materials network|D2-264]]], **1 unit**; refused with fewer than one trap in hand |
| **Tend** | 1 unit for all of one's own traps at a place; takes the catch into hand (or the creel), sets again each trap still sound, and reports each line by tag; `up: true` brings the traps home instead |
| **The night** | each trap takes from the shallows at the setter's skill (as `_set_night` does now, wild.py:921) and, on a run night, `passing × reach × flow` capped by its 10 kg hold [m WATER_WORKS.trap]. **reach**: about 0.006 of the eels passing a trap's place on a big river's edge, more on a small river, half that in a fen dyke [e; to give 2 to 5 kg a trap on a good run night, fishing_ladder §4]. Fish stay alive in it ([[D2-211 Fresh fish keep as meat in hand, and alive in a trap or a weir until…|D2-211]]). A spate wrecks a river trap at 0.5, a flood at 0.85 [m]; in a fen dyke 0.02 and 0.05 [e; [[D2-264 The fishing, hunting and materials network|D2-264]] §7.8 asks a lower rate: the code today never wrecks a fen trap, wild.py:3160]. An otter robs a full trap left unwatched (wild.py:3185, as now). A night it fishes is a use. **A frozen night it is idle** ([[D2-265 The river's signs|D2-265]]): takes nothing, is not wrecked, wears by time |
| **Refusals** | set, no traps in hand: "You have no wicker traps in hand: your 6 are in the Isel (T7, set autumn day 2). To take what they hold, tend T7." With none anywhere: "You have no wicker traps; they are made from withies (make wicker traps)." Set on land: "Wicker traps are set in water: here that is the Isel or Eelmouth Fen." Tend with none of one's own there: "You have no traps in the Isel. T9 there is Oliver's." The river frozen: "The Isel is frozen at its edges and the dykes are ice: a trap set now would take nothing until the thaw." |
| **Before** (the prompt) | under set and tend: "wicker traps (known, a master's hand: up to 6 an act, 1 unit; you hold 6, and 6 are in the Isel (T7))"; in "Here": "your traps in the Isel (T7: 6, set 2 nights ago, last tended this morning)"; the craft's line by familiarity (river_signs §4.4); the lore lines FI1, FI2, FI4 (wave4 §3.5.1) |
| **After, set** | "You set 6 wicker traps in the Isel (T12). Your 6 there of autumn day 2 (T7) still stand." With a run passing, for one who fishes: "...; eels are running: they will fill as fast as they come." Spate tonight: "...; the Isel is in spate: traps in the main stream may not stand the night." |
| **After, tend** | catch axis and water axis apart (river_signs §3): "You tended your traps in the Isel (T7, 6 traps): 11 eels, about 6 kg, about three meals. Two were full by morning, and eels were still going down past them. You set them again." Robbed: "...; an otter had been at T7 first: scales on the withies, three gone." Wrecked: "Of T7, two traps are gone, torn from their stakes in the night with what was in them; four stand, and you set them again." Nothing, no run: "Nothing in T7: nothing ran last night." Nothing, a run passed: "Nothing in T7, though eels went down past them in the night" (one who fishes) |
| **Others sense** | the set thing as now (`THINGS.set` own 0.12); the tend as a work event at the water; **the catch carried home** (§4.3) |

**The fen as a choice.** A fen dyke takes half the river's share and is almost never wrecked. On a flood night that makes it the
better place, by a lot (§5.1, night 6). The signs say so only as observations: "traps in the fen's dykes stand when the river tears
the rest away" (one who fishes; river_signs §2.10).

### 2.2 Snares (a line on the runs and edges)

| | |
|---|---|
| **Targets** | small game on its runs: hares on open ground, rabbits at field edges once added; woodcock on woodland paths in winter, roe in a strong noose (hunt_fish §7.7); grouse on heath. Not otters at the water: today's snare covers include water and take otters at 2.0 [m methods.py:57 to 60]; an otter snare at a holt is den work |
| **Default target** | set: the parcel named; tend: one's own line(s) there, walked as one |
| **Gear** | a bundle of 25 snares, 0.2 kg, 0.1 to 0.15 cord, 2 units, **on the day clock** (each snare lasts 3 to 10 settings, under a handful at 1/7) [w1 §3.1, [[D2-276 Making durable things runs on the year clock|D2-276]] names "a snare line"]; rawhide nooses as the stand-in, rotting on a wet night |
| **Set** | up to 25 an act, 1 unit, **on good places only**: a parcel holds as many good snare places as its edges give (hedges, gaps, the wood's edge band, field margins, tracks; hunt_fish §7.7), say 10 to 20 for a pasture with a hedge [e]. Fewer on ground one does not know (a stranger sets at half the good places) |
| **Tend** | walk the line: 1 unit for a line of 25 [e; 10 to 15 minutes a snare real, but most are passed, not reset]; take the catch, reset the sprung, drop the torn; may move the line (`to`: another parcel) at no extra cost |
| **The night** | each sound snare on a good place meets the game of the area by its density (as `_set_night`), at about 5 to 15 catches per 100 snare-nights for a practised snarer on known runs [hunting_ladder §1.2]. A catch is **dead by morning about 4 times in 5**; a live one breaks free by the next night 1 time in 3, tearing the snare [e]. **Scavengers:** each night a catch hangs unlifted, a fox, crows or a stoat take it at about 1 in 4 (1 in 3 in a hard frost, when they are hungrier) [e]. **Spoils** as fresh meat in the open on part 1's curve (2.1 nights half-life, faster in the warm), and a catch left two nights draws birds (the existing `birds_after`). **Heavy snaring makes the game shy there** (learned wariness, as hunting). In worlds with lords, snaring their game is poaching |
| **Refusals** | set with no snares: "You have no snares: a bundle is made from a little cord or rawhide (make snares)." No good places left: "The runs on the Leaze are all taken by snares already (yours T4, Agnes's T6); the heath's edge has room." Deep wood: "Snares go on the runs in the open and at the edges, not in deep wood." |
| **Before** | "snares (capable: a line of up to 25, 1 unit; you hold a bundle of 25; your line on the Leaze (T4, 22 standing, 3 sprung))"; lore HU1, HU7 (wave4 §3.5.4) |
| **After, tend** | "You walked your snares on the Leaze (T4, 25): two hares, one dead in the noose and one still alive, which you killed; a third had been taken by something in the night, fur and a torn noose left. Three were sprung empty and you set them again; one is torn past use." A cold line: "...; nothing for two nights, and the runs have no fresh tracks on them." (game thin) against "...; the runs are fresh with tracks, but nothing came to the nooses." (game shy: learned wariness high) |
| **Others sense** | the existing snare signs (crows and magpies over a catch, a stranger's look), tracks to a line in snow (conditional) |

### 2.3 The weir and its sections

| | |
|---|---|
| **Targets** | a run passing, by each section's position (the first 30%, each added 7%, [[D2-210 The weir in sections, capped, with upkeep by the river|D2-210]] as recosted [[W-69 Nutrition worlds|W-69]]) up to its hold (100 kg the first, 70 each added [m WATER_WORKS]) |
| **Default target** | tend: the weir's traps one works at this water (`owns_set` for the crew); its gap: `change` (wave4) or today's `set {"thing": "gap"}` |
| **Gear and capital** | the weir is a work (building_clock, part 1 §3.7: an added wattle section 1.5 units at 1/7, 12 withies and 7 timber; the first section 2.6 to 3.6 units at the research note's size, 11 to 36 if sized to take 30% of a large river's run: part 1 contradiction 26). Its traps are set things of the crew, made with the section (no gear in hand needed) |
| **Tend** | 1 unit for all its traps, as now (one lift empties them); the crew shares the catch as the weir's holders set (an agreement, or by default into the holder's store) |
| **The night** | as built: the gap shut takes, open takes 0.1 of the share; worn by flow, the gap shut in high water and ice ([[D2-210 The weir in sections, capped, with upkeep by the river|D2-210]]); turns away what it cannot hold (record it: river_signs §1). **A freeze** ([[D2-265 The river's signs|D2-265]]): the traps in the gap ice up and take nothing; the run of that night waits (the eels do not run under a hard frost: §4.5); the thaw wears it x2 (as now) |
| **Refusals** | tend by one not of the crew, unnamed: "The weir's traps at the Isel are the Marshs' (T3); you are not of its crew." Named: done, and theft (§2.0). Build by one who does not know the weir: refused with the trying rule (trying_and_learning; question 9) |
| **Before** | for the crew: "the weir in the Isel (T3: 3 sections, the gap shut since autumn day 4; its traps last tended this morning)"; the craft's line; lore FI9, FI10, FI12 |
| **After, tend** | "You emptied the weir's traps at the Isel (T3): about 150 kg of fish, about two hundred eels and a dozen salmon, about 70 meals. They were crammed: as much again went past the gap." (river_signs §3, from `turned`) |
| **Others sense** | the gap shut or open (as built); fish milling at the wattle when full (to anyone at the water, river_signs §2.9); the crew carrying the catch up (§4.3) |

### 2.4 Nets: fish and fowling split ([[D2-264 The fishing, hunting and materials network|D2-264]])

| Net | Shape | Targets | Gear [w1] | Units | The take | Results |
|---|---|---|---|---|---|---|
| **gill net, set** | set and tend | the open water's fish at its mesh; salmon in a run; not eels (they wriggle through) | 4 kg with floats and sinkers, 1 cord; 3 to 4 units at 1/7; 30 to 65 sets | set 1, tend 1 | saturates near 6 kg a night in open water (EN 14 757, fishing_ladder §2d) [e]; in a salmon run, the salmon passing its place x reach (about 0.01 on a big river [e]) up to 15 kg [e]; a spate fouls it with weed (takes nothing that night, a use lost), a flood tears it at 0.3 [e] | "You lifted your net in the Isel (T8): two salmon and a trout, about 10 kg; weed in the upper mesh. You set it again." |
| **dip or hoop net** | gather (worked, at the edge) | a run at a pinch point (below a shut dam, a weir's gap, the shallows a run crosses); the shallows | 1 kg; 1 unit for 2 at 1/7; 15 to 45 uses | 1 a unit of dipping | hands at the edge x3 in a run at a pinch (hunt_fish §7.1) | as the edge (§2.6), "with the net" |
| **fowling (clap) net** | gather (worked; dusk and dawn) | wildfowl on wet ground and the last open water; pigeons on sown fields | 2 kg, 0.8 cord, 4 to 5 units; 30 to 60 uses | 2 | the fowling method x4 over hands (hunt_fish §7.2); in a freeze the fowl crowd onto the last open water (kinds.PUSHED, as built) | **its own words, never "You hunted"** (wild.py:2573, 2585): "You spread your nets on the flooded meadow at dusk: four duck and a teal came down to the decoys and you took them." Nothing: "You lay by your nets at the meadow's edge at dusk; the duck flighted high over and none came down." |

**Refusals:** set a gill net on land, or a fowling net in a river: named by what each does ("a gill net is set in open water; a
fowling net is spread where fowl come down"). Fowling at noon is not refused; it takes less (fowl flight at dusk and dawn).

### 2.5 Lines

| | Hand line or rod (worked) | Set line (placed) |
|---|---|---|
| **Targets** | the open water's fish | the open water; eels in a run at night, baited |
| **Gear** [w1 §3.2] | a hand line 0.05 kg, 1 unit for 5, 4 to 14 uses; a rod 0.8 kg, 0.1 withies, 1 for 5, 20 to 45 uses (the rod's hide goes: Q-57b); hooks of bone (day clock) or copper (a smith's, 4 to 14 uses) | 0.5 kg, 0.3 cord and 30 hooks, 1 unit at the floor, 7 to 14 sets |
| **Units** | 1 a unit of fishing | set 1, tend 1 |
| **Take** | 0.1 to 0.5 food a unit (the network's target; today's angling at 1.5 fish a unit is 1.5 to 3 times real, fishing_ladder §4) | 1.5 to 3 kg a night [fishing_ladder §4]; bait x1.5 and used up (offal, [[L-145 Offal's uses bait for set lines and traps, dog food|L-145]]) |
| **Refusal** | no line: "You have no line to fish with: a hand line is a little cord and hooks." **No resident fish** (the runs world): never "there is no fish at the Isel"; for one who fishes: "The Isel holds few fish of its own; its fish come in the runs, which a line seldom takes." Frozen: "The Isel is frozen at the edges: there is no open water to fish from the bank." |
| **After** | "Your line took two roach and a perch at the Isel, about 1 kg." In a run with none taken: "Your line took nothing of the Isel's own; salmon were going up past it all day." | as traps |

### 2.6 The edge (hand fishing, on the shallows stock)

| | |
|---|---|
| **Targets** | the shallows stock ([[D2-264 The fishing, hunting and materials network|D2-264]]), and a run where it passes a shallows or a pinch point |
| **Default target** | the water parcel named; "fish" alone is not this act (§6.4) |
| **Gear** | none; a dip net x3 in a run at a pinch; a leister or glaive x1.5 to x2 [w1 §3.2: 2 kg, copper tines] |
| **Units, take** | 1 a unit; 0.1 to 0.3 food a unit at the edge (fishing_ladder §4: hands 0.1 to 0.28); in a run at a pinch a few times that; **in a run on open shallows a few heads at best**: the hand is not the tool, and the result says so on the water's axis |
| **The shallows stock by water** ([[D2-264 The fishing, hunting and materials network|D2-264]], §7.8) | a brook: rich shallows, little open water; a big river (the Isel): thin shallows, deep water, the runs; a lake: open water and its rim; a fen: eels and shallows. Strippable in days, back in days in summer, near nil in winter [e] |
| **Refusals** | only when the shallows are at their refuge and no run passes: "The shallows of the Isel are fished out for now; nothing is running." Frozen: "The edges of the Isel are ice." Never "there is no fish" while a run passes ([[Q-79 Whether to fix the fishing bugs the live runs exposed|Q-79]] bug 1) |
| **After** | "The shallows of the Isel are thick with eels slipping past; your hands closed on two." / "The Isel is full of running eels tonight, but they slid through your fingers: you took none." / "You took a few minnows and a crayfish from the shallows, a handful." (river_signs §3) |

### 2.7 The hunt: alone, in a party, the drive, the stalk, den work

The hunt is built (wild.hunt, brief 4b and 4c) and its shape is right: a worked take of a stock, with `with`, `alone`, `only`,
`looking for` and `range` as modifiers. What taking needs of it:

| Need | Now | Design |
|---|---|---|
| **The weapon wears** ([[D2-46 Weapons wear|D2-46]]) | never in the wild hunts (verbs.py:685 applies no wear) | a use a hunt for the leader's weapon; a crude weapon 7 to 21 uses, a copper spear 30 to 70, a bow 40 to 70 and its string every 7 to 14 [w1 §3.2] |
| **The kill is a thing** | dressed where it fell at no work; what cannot be carried is left as a carcass or carrion | the kill is a carcass thing at the spot, tagged, the hunter's; taking it home is the carry (on foot 10 kg, a pack basket 25, a frame 30, a pack ox 100 [w1 §4.1]; a red deer is about 40 kg of venison [w1 §4.2]); what is left is cached, the hunter's, and draws wolves and ravens by the night (as built). Dressing it is a work on the thing (hunt_fish §4.3; part 2 prices it) |
| **A party shares** | the party's catch to each one's carry (wild.py:2245, parties.py) | as built; the drive's crew; a party's carry is the sum, so a party brings a deer home whole |
| **Thin against shy** | "came on nothing" whatever the cause (wild.py:2573); "hunted too often here" fires the day of the first kill, usually (engine_audit §1h) | the result says which: "you came on nothing: few slots and no fresh droppings in the rides" (thin) against "you came on deer twice, and both times they were away before you were near: they are wary here" (shy, learned wariness); the wary sign fires on wariness against the area's heads, not one kill against a small count |
| **Range** | near, the wood around (+1), far (+3); [[D2-255 A very skilled hunter brings in a disproportionate amount of food…|D2-255]]'s master far 3 to 6 food a unit, capped by the carry | as built, with the carry in kg |

---

## 3. The fishing bugs ([[Q-79 Whether to fix the fishing bugs the live runs exposed|Q-79]]), and the faults found beside them

Each: the cause in code, what the probe showed [m], the fix in this design, and the bot test. Probes ran on copies of the runs world's
medium arm (scripts in the scratchpad, `w3/probe2.py` to `probe5.py`). The tests are written in the style of
tests/test_cybertron2_water5_river.py (its `fresh`, `pulse`, `do`, `refused` helpers, on the runs world).

### 3.1 The five of [[Q-79 Whether to fix the fishing bugs the live runs exposed|Q-79]]

**Bug 1. Hand fishing and angling refused at a run where no resident fish live.**
- **Cause:** `knowledge.ready` refuses any technique whose `draws` stock is missing from the parcel (knowledge.py:206: `if d in
  RESOURCES and d not in p["res"]`), before `_technique` reaches `run_take` (verbs.py:610 to 611). The runs world stocks no
  resident fish, so the Isel's `res` is empty.
- **Probe [m]:** with a pulse of 400 eels at Eelmouth (run density about 1,667 a km²), Peter's `fish by hand` and `angle` at the Isel
  both returned "Refused: gather: there is no fish at the Isel".
- **Fix:** the shallows stock in every water ([[D2-264 The fishing, hunting and materials network|D2-264]]) gives the edge a stock to draw everywhere; `ready` refuses the edge only when
  the shallows are at their refuge **and** no run passes; angling refuses with the water's own reason (§2.5). Until the shallows
  stock is built, a phase-1 patch: a technique with `run: True` on a river parcel where a run passes tonight is not refused for a
  missing resident stock.
- **Test:** `test_the_edge_reaches_a_run_where_the_water_holds_no_resident_fish`: a pulse of 400 eels, a person with no fishing
  craft; the edge is not refused and its line names the run; with no pulse and the shallows at refuge, the refusal says "fished
  out for now; nothing is running" and never "there is no fish".

**Bug 2. Setting a trap mistaken for lifting it.**
- **Cause:** `gather trap in water` always lays a new set (verbs.py:678 to 681 into `wild.set_work`, wild.py:909 to 918); a set costs
  nothing and needs nothing in hand; its result says "for whoever comes to them" and never names one's traps standing; the method's
  note "come back to your traps and take what is in them" (methods.py:111 to 114) reads as "gather again" (Jory's thinking, 02zzy2 §3);
  the lift is a `take` by place (verbs.py:1625 to 1635).
- **Probe [m]:** Katherine set twice, the second time with `why: "lift my traps"`: both returned "You set traps in the water at the
  Isel; they will catch by night for about 8 nights, for whoever comes to them", and two sets stood.
- **Fix:** gear in hand to set (§2.1); tend as its own act; named alone, a technique whose own gear stands at the place tends it
  (§6.3); the set result names what stands (§2.1).
- **Test:** `test_a_second_set_with_no_traps_in_hand_is_refused_and_points_to_the_tend`: give 6 traps, set, set again: refused with
  the tag; `test_the_technique_named_alone_tends_what_stands`: with T7 standing and 6 more in hand, `{"do": "wicker traps", "at":
  "the Isel"}` tends T7; `{"do": "set", "what": "wicker traps"}` lays 6 more and names T7.

**Bug 3. Nets met 48 salmon and took none.**
- **Cause, traced in part:**
  1. The fowling net's take table holds salmon at 3.0, by the trait match `social: flock` (methods.py:63 to 66; kinds.py:855:
     "a run is a shoal").
  2. A meeting is taken at `1 - e^(-0.25 x skill x (1 - flee) x familiarity)` (wild.py:2252), about 0.14 at skill 1 with salmon's flee
     0.4.
  3. **Each salmon taken adds 30 to the salmon's learned wariness in the village area**, because the divisor is the area's resident
     heads (`WARY["take"] / max(1, pop x km2)`, wild.py:2436) and a run's salmon have none. A run's fish are new fish each night and
     should learn nothing.
  4. Each net act adds `0.5 x share` to the wariness of every kind in its table (wild.py:2345), salmon included, met or not. At
     Eelmouth the net sweeps 0.6 km² of a 0.72 km² village area [m], so each act adds about 0.42.
  5. Learned wariness divides meetings by `1 + 1.5 x learned` and raises flight (`1 - 0.6 / (1 + 0.15 x learned)`).
- **Probe [m]:**

  | Pulse at Eelmouth | Each act on a fresh copy | 24 acts in a row on one world | Salmon wariness after |
  |---|---|---|---|
  | 120 salmon | met 192, took 22 (0.11 a meeting) | met 69, took 6 (0.09) | 30 on a fresh copy after one act; 190 after 24 (learned 7.7 of 8) |
  | 20 salmon | met 183, took 21 (0.11) | met 18, took 2 | 70 (learned 7.2) |
  | 6 salmon | met 85, took 9 (0.11) | met 4, took 1 | 40 (learned 6.7) |

  So the net takes about one salmon a meeting in nine; and once one is taken the salmon all but vanish to nets for weeks (a 32-day
  half-life). Forty-eight misses in a row at 0.11 is about 1 in 270, and rarer at the high arm's skill 1.6; wariness from the acts
  alone lowers the rate toward 0.07 and the meetings by about half to two thirds over 19 acts [e from the formula]. The live runs'
  records are not on this disk, so the last part stays untraced: the probe makes the outcome likely, not certain.
- **Fix:** (a) fowling split ([[D2-264 The fishing, hunting and materials network|D2-264]]): the fowling net reaches what flies; a gill net set overnight reaches salmon (§2.4); (b) **a
  run's fish learn no wariness**: wariness and pressure apply to the resident share only (a phase-1 bug fix, question 5); (c) the
  net's result in its own words (§2.4).
- **Test:** `test_a_runs_fish_learn_no_wariness`: net or trap salmon from a pulse on 10 days running; `state.wary.salmon` stays 0;
  `test_the_fowling_net_meets_no_fish`: a salmon pulse, fowling at the Isel meets no salmon; `test_a_set_gill_net_takes_salmon_in_a_run`.

**Bug 4. The weir known to everyone in every arm.**
- **Cause:** MONUMENTS weir has `"basic": True` (data.py:346), so the prompt lists "building a fish weir" under "Everyone knows"
  [m: Peter's system prompt, line 36], in the low and medium arms where no one has the craft (02zzy2 §1).
- **Fix:** not basic. Building a weir section is a practised craft (trying_and_learning §1), known by the weir's holders and the
  weir-and-nets expert (wave4 §3.5.1); anyone may work on its crew led by one who knows it ([[D2-66 Field works in the first worlds, before weather exists|D2-66]], as `crew` allows now,
  verbs.py:518); the build line says what it does (02zzy2 fix 4).
- **Test:** `test_the_weir_is_not_everyones_craft`: in the low arm no adult's prompt lists the weir under what they know; a crew
  led by the high arm's weir builder may include a novice.

**Bug 5. "the Brook" read as Brook House.**
- **Cause:** `here.building` strips "the" and then matches a household's id ("Brook" is the Brooks' id) and returns that household's
  house (here.py:219 to 232); `_take` tries the parcel only if `here.building(src_name) is None` (verbs.py:1641) and then falls to the
  building (verbs.py:1660).
- **Probe [m]:** at Eelmouth, `take fish from the Brook` gave "Refused: take: you find no fish in Brook House".
- **Fix:** resolve a parcel's exact name before any building; a household's name resolves to its house only when said as the
  household ("the Brooks", "Brook's", "Brook House"), never a bare word that is also a place's name; when two things answer,
  refuse naming both.
- **Test:** `test_a_place_named_like_a_household_is_the_place`: a world with a water called the Brook and a household Brook;
  `take from the Brook` reaches the water; `take from the Brooks` the house.

### 3.2 Found beside them

| # | Fault | Cause (file:line) | Probe or evidence | Fix in this design |
|---|---|---|---|---|
| 6 | **A take "from my snares" empties a neighbour's** | `things.find` takes the most recently known set matching the set words, with no preference for one's own (things.py:622 to 655) | [m] Peter (Marsh) and Hamon (Shepherd) snared Clay Field; Peter knew both; "take from my snares at Clay Field" emptied Hamon's T2, Peter's T1 untouched | §2.0 rules 2 and 3 ([[Q-80 Whether acts on owned things default to one's own|Q-80]]) |
| 7 | **No theft wording on another's set** | the store's theft path is for buildings (verbs.py:1670 to 1676); a set gets only `robbed` and an event (1689 to 1698) | [m] the same take returned "You took 1.2 meat from the snares at Clay Field." | "...from Hamon's snares (T2), which are not yours to take from. Whether anyone saw, you will learn." |
| 8 | **Tags given to sets but not shown** | `set_line` (things.py:394 to 411) writes no tag; [[D4-68 Short tags, and names given|D4-68]] says tagged things show their tag wherever named | [m] "Lying about, that you know of: wicker traps you set in the water at the Isel (summer day 4)" while the trap is T1 | the tag and the count in every line of one's own things (§2.1 "Before") |
| 9 | **"Today you could" hides every fishing craft from a fisher** | `knowledge.options` walks TECHNIQUES in table order and keeps the first ten (knowledge.py:411 to 432, `limit=10`); farming and wood rows come first | [m] Peter, medium arm, day 1: fell, firewood, clear, cut, sow, hay, wild food, clappers, fence, wall; no trap, net or edge. Also "gather gather wild food", "make make clappers" | the person's livelihood's crafts first, then by level (wave4 §2.2); in phase 1, a sort by the household's crafts before the cap (37.4; question 4) |
| 10 | **A run's fish learn wariness** | wild.py:2436 (and 2345 for every kind in a table) | bug 3's probe | question 5 |
| 11 | **The net's result says "You hunted"** | `_hunt_lines` (wild.py:2573, 2585) | 02zzy2 §3: "You hunted the Isel and came on nothing" fed "fished out" | §2.4 |
| 12 | **Set gear costs nothing and leaves nothing** | `set_work` makes a container from nothing (wild.py:912 to 916) | engine_audit finding 2 | gear in hand |
| 13 | **A fen trap meets the run in full and is never wrecked** | the wreck loop skips parcels that are not river (wild.py:3160 `_river_parcel`) | river_signs question 5 | half the share, a twentieth of the wreck [e] (question 7) |
| 14 | **Snares set at the water take otters** | snare covers include water; otter's traits match (methods.py:57 to 60) | engine_audit §4 | snare covers by edges on land; the otter by den work at its holt |
| 15 | **Water acts turn up wood finds** | WORK_NOTICES' hunt group for any take, no cover check (wild.py:406) | engine_audit §1h: "a cast antler lying in the leaves" after setting a trap | a cover condition on each row |

---

## 4. The river's signs, tied to the acts ([[W-72 Signs of the river|W-72]])

### 4.1 The problem in one line each

- **Too late.** The run rows (RUN_SIGNS, kinds.py:888 to 892) read tonight's pulse and are rolled in the evening at the water. The
  trap must be set by day. The lead is zero: one learns of a run night after the day's acts are spent.
- **Too local.** Every run row is read at the water parcel. The Street is three steps from the Isel at Eelmouth (the Isel, the
  Fen, Eelmouth Field, the Street [m: the parcel graph]), and sight reads nothing from three steps for an own under about 2.
- **Too thin on the axis that matters.** A failed act reads as an empty river (02zzy2 §3: "the Isel is fished out").

### 4.2 What tells a person a run has begun: leads, distances, senses

For the first eel run of the year at Eelmouth. The state each row reads is named; every row takes its chance from the noticing rule
([[D4-75 Every perceived line about the world comes from the one noticing rule|D4-75]]); `own` is set so the outcome lands on the intended chance, which the build checks through `perceive.chance_of` (guide step 4).
Intended chances use NOTICING's factors as river_signs §8 does (presence 0.5 working there, 0.3 next door, 0.05 elsewhere for own
0.8 or more; sound by steps 0.5, 0.45, 0.2, 0.1; fog x0.3 on sight; night sight x0.1).

| Lead | Sign | Sense, own | Who | Where read | Reads (state) | Intended: at the water / next door / the Street |
|---|---|---|---|---|---|---|
| **a season ahead** | the lore line FI1 (wave4 §3.5.1), from `run_lore` | memory | every adult of a household with a water craft ([[D2-265 The river's signs|D2-265]]) | anywhere | RUNS.eel window and cue; the station's nights | held, not rolled |
| **days ahead** | "the nights drawing in, dark and still: the eels will move soon" | sight 0.7 | expert, elder | the village, at dawn | the window opens within two days (`RUNS` seasons; the set nights under `runs_set_nights`) | 0.35 for the expert anywhere at the village |
| **days ahead, from upriver** | none written: news travels with people from a village upstream, which sees the run on its lag first (`RU` lag, 10 km a day) | | | | | carried by people only (guide: news by presence) |
| **the same day, at dawn** | "the Isel rising and dark after the first heavy rain in weeks" | sight 1.0 | anyone | the water and next door, at dawn | the eel cue `rain_after_dry`, where the runs read the weather | 0.5 / 0.3 / 0 |
| **the same day, at dawn** (expert) | "dark, wet and the water rising after the dry weeks: an eel night" | sight 0.6 | expert | the water, at dawn | the same; under set nights, a set night | 0.3 (reworded from kinds.py:412: §4.4) |
| **the run in the reach, at dawn** | "dark eels moving in the slack water under the banks of the Isel this morning, all one way, downstream" | sight 1.2 / 1.6 / 2.0 by band | anyone | the water, around (next door) | today's pulse at the village (`RU.today`), its band (river_signs §1.1) | running 0.6 / 0.36 / 0; thick 0.8 / 0.48 / 0; glut 1.0 / 0.6 / 0 |
| **the run, at dawn, village-wide** | "herons flying down to the Isel from first light, one after another" | sight 2.5 | anyone | the village | a heronry at the village and a band thick or more ([[D2-265 The river's signs|D2-265]]) | 1.0 / 0.75 / 0.13; someone of 12 at the Street 0.8 |
| **the run, by day** | "eels against your legs in the water, cold and strong, all going the one way" | touch 2.0 | the doer: anyone who worked in the water | as it happens | band running or more | 1.0 for the doer |
| **the run, by day, village-wide** ★ | "Peter came up from the Isel with his creel heaving with live eels" | sight 1.0 | anyone at the place where the catch is carried | the Street, the houses | a person's hands or creel holding 5 kg or more of fresh fish, and their work at the water today | 0.5 for those at the Street that evening; certain for the household (inside) |
| **the run, by smell** | "a sweetish smell of fish and mud off the Isel" | smell 0.8 | anyone | the water and the fen | band thick or more | 0.4 / 0.24 / 0.04 |
| **the run at night** | "the water at the Isel alive with eels in the dark" (kept) | sight 0.6, night | anyone | the water | band running or more | low: one who sleeps out or fuses at the water |
| **after, at dawn** | "slime trails across the mud of the fen's paths, all toward the Isel" | sight 0.8 | anyone | the fen | band thick or more on a rain night, the next morning | 0.4 on the fen |
| **after, at tend** | the tend's two axes (§2.1): what one took; what passed | result | the doer | | the trap's catch and the night's passing | certain |
| **after, the weir** | "fish milling against the weir's wattle and turning back" | sight 1.2 | anyone at the water | dawn | `turned` over 0 (river_signs §1) | 0.6 / 0.36 / 0 |

★ The carried-catch row is new. It reads a body and its load, which the guide allows ("signs of a person's body are fine"), and the
day's work at the water, which the event already holds; it puts no act or feeling in anyone's mouth. It is the sign that takes
news of a run from the water to the houses, which is what was missing: in the live runs the households who never went to the water
never learned there was a run.

### 4.3 The other states of the water, as they bear on the acts

| State | The act it changes | Rows (river_signs §2, with [[D2-265 The river's signs|D2-265]] applied) |
|---|---|---|
| **spate, flood** | take up or move river traps; set in the fen; shut or open the gap | the roar from the houses (sound 2.5, village-wide, dawn); "a spate: wicker traps in the main stream tonight will be torn away" (one who fishes, dawn, own traps in the river); "the river is falling: traps set now will stand" |
| **otters about** | tend at dawn, not at dusk | "otters working this stretch: a trap left full overnight will be robbed" (one who fishes); the robbed tend |
| **low water** | the edge pays (shallows concentrate); the eels wait | "the Isel low and clear, stones showing at the edges"; the expert's "too low and clear for the eels to move" |
| **a run slackening** | take up the traps; stop | "fewer eels each night in the Isel now: the run is passing"; "the eel run is over at the Isel for this year" |
| **a freeze** | set gear idle; fowl crowd; the edge and lines stop | §4.5 |

### 4.4 Rows that direct an act ([[D2-269 Experts' signs are observations of what is happening now, which may…|D2-269]])

| Row now | Where | Reworded |
|---|---|---|
| "an eel night: dark, wet and the water rising after the dry weeks; set the traps tonight" | kinds.py:412 | "dark, wet and the water rising after the dry weeks: an eel night" |
| "{kind} crowding in the pool below the dam at {place}: net them, or draw the hatches and let them up" | kinds.py:894 | "{kind} crowding in the pool below the dam at {place}, more each hour, unable to get up" |
| river_signs §2.1 expert: "a run like this is most of a year's eels in a few nights: what is in the water tonight, and kept, is the winter" | draft | allowed: an observation that implies; keep (river_signs question 7 recommended it) |
| lore FI2 "A house that means to eat from the run sets many before the nights come, and lifts every one each morning" | wave4 §3.5.1 | lore, not a sign: [[D2-269 Experts' signs are observations of what is happening now, which may…|D2-269]] binds signs; but "sets many ... lifts" is advice in the family's voice. Allowed as lore (a family's knowing), flagged for Zach with question 12 |

### 4.5 A freeze ([[D2-265 The river's signs|D2-265]]: a freeze stops fishing)

What stops, read from the state (`frozen_run`, `_frozen_day`, wild.py:1202 to 1214), and the signs that say it:

| Act | In a freeze | Sign or refusal |
|---|---|---|
| wicker traps, set line, gill net | idle: take nothing, not wrecked, wear by time; a trap in a fen dyke frozen in may be crushed at the thaw [e: 0.1] | "the fen's pools skinned with ice, the reeds stiff with rime" (anyone, dawn); the tend: "Your traps in the dyke (T7) are frozen in: nothing has come to them." |
| the edge, lines from the bank | refused (§2.5, §2.6) | refusal words |
| the weir | its traps ice up; the gap shut in ice wears it (as built) | "ice along the edges of the Isel, the main stream still running black between" |
| the runs | the eels wait (a run's night under a hard frost is held for the next open night) [e; question 10] | none: nothing passes |
| fowling | the fowl crowd onto the last open water (kinds.PUSHED, as built): the best fowling of the year | "duck and geese packed on the last open water below the weir" (anyone, dawn) |
| snares | work; hares tracked in snow; scavengers hungrier | "fresh hare tracks along the hedge on the Leaze, in the new snow" (anyone at the parcel, conditional on snow) |

The river_signs row "the river frozen from bank to bank; birds lying dead on the ice" (the great freeze) stays as written: under
[[D2-265 The river's signs|D2-265]] the engine now agrees with it.

### 4.6 Checked against the guide (guides/senses.md)

| Test | How the bundle meets it |
|---|---|
| reads only what the state holds | every row names its state; the moon is not in state, so "dark nights" read from the window and the weather (river_signs §2.12); the carried catch reads hands and the day's work |
| worth acting on | each row is placed at a lead the act can use: dawn rows for the day's set and tend; the lore for the season's making |
| a change, not a standing fact | when the eels come is lore; the sign is the run coming this year |
| a bundle | each state has sight, sound or smell, touch for the doer, a lingering trace and a conditional row |
| the chance from the rule | own set, chances intended, checked at build |
| concrete, in-world, counts only where people count | bands, a creelful, scores, meals |
| not repeating what the doer knows | the tend's result is the doer's; the carried catch is for others |
| quiet when nothing matters | no ambient river line in spate (the spate rows say it); the quiet-water row only between runs |
| no act or feeling put on a person | the carried-catch row reads a load and a place; no row says anyone hurried, rejoiced or ran |

---

## 5. Worked nights

Numbers marked [m] are the bot run's river (runs_medium, seed 5, 44 days, every person dead by day 16 because bots do not fish, so
the river ran untouched): what passed Eelmouth each night is read from the night's `moved.sea` count, Eelmouth being the lowest
village (an approximation: it is what reached the sea that night). Catches are the design's expected values at the reaches set in §2
[e]. Food: fish 0.46 a kg fresh, smoked 0.92 [w1 §1.1]; fresh fish half gone in 1.5 nights in the open (0.37 a night), a keeping
smoke in 9.7 nights (0.069 a night), salt fish 33.8 [w1 §2.2].

### 5.1 A trap household through the first autumn run (the Marshs at Eelmouth)

**The house:** Peter (head, traps and the runs, a master's hand), Nichola (keeping, capable), Nigel (youth, apprenticed to the traps,
a rough idea), Henry (a child), Denise (a baby). They eat about 4.7 food a night, about 10 kg of fresh fish.

**Capital at the start of autumn, made in late summer** [w1 §3.2 at 1/7]: 12 wicker traps (two lines of 6: 6 units, 5.4 withies
from the willows on the fen), 1 gill net (3.5 units and 1 cord, bought from a flax household), 2 creels (1 unit), a dip net (0.5), a
wattle smoke hut with one set of racks (about 250 kg a night on a keeping smoke, [[D2-284 A smokehouse's capacity comes from the racks fitted, about 250 kg of…|D2-284]]), 20 firewood, 10 salt boiled at the brine
spring (40 kg of fish salted in 1 unit, [[D2-283 Salting fish runs at about 20 kg an hour with gutting, at 1 kg of…|D2-283]]). About 11 units of making, two days of one person's autumn, before the run.

**What they know:** Peter holds FI1, FI2, FI4, FI6, FI7, FI8 (wave4); Nichola FI3, FI16 to FI18; Nigel FI1, FI2.

**The river** [m]:

| Night | Flow | Eels past Eelmouth | Band | Salmon up past it |
|---|---|---|---|---|
| 4 (autumn day 0) | low | 0 | | |
| 5 | normal | 0 (the run starts upriver: 4,358 set off) | | 589 start from the sea |
| 6 | **flood** | 968 | thick | |
| 7 | **flood** | 620 | thick | |
| 8 | **spate** | 352 | running | 383 start |
| 9 | **flood** | 1,114 | thick | |
| 10 | **flood** | 961 | thick | |
| 11 | normal | 554 | thick | |
| 12 | normal | 525 | thick | |
| 13 | low | 422 | running | |
| 14 | low | 266 | running | |
| 15 | low | 162 | running | 711 start |

About 5,900 eels in ten nights, about 3.4 t at 0.58 kg; five of the first six run nights in flood or spate. Bands against this
year's total (river_signs §1.1: running 2 to 8%, thick 8 to 20%).

**Night by night** (acts by day, the night's take after, read at the next dawn):

| Day | What they sense | What they decide | Units | The night's take | Kept and eaten |
|---|---|---|---|---|---|
| 4 | Peter, expert, at dawn: "the nights drawing in, dark and still: the eels will move soon" (0.35). FI1 in memory | Peter sets line A (T7, 6 traps) in the Isel, Nigel sets line B (T8, 6) in the fen's dyke, so both are in before the run | 1 + 1 | the shallows only: about 0.5 kg a line [e] | the larder (dried meat, roots) |
| 5 | Heavy rain at dawn: "the Isel rising and dark after the first heavy rain in weeks" (anyone at the water 0.5); Peter's "an eel night" (0.3) | Peter tends both lines (2 units), nothing much; sets the gill net in the Isel's pool for the salmon (1) | 3 | traps about 1 kg; the net, on the first salmon (589 starting below): 2 salmon, 8 kg [e: 0.01 of those passing its place, half the run passing that night] | eat fresh 9 kg |
| 6 | Dawn: the Isel in flood, the roar heard from the Street (sound 2.5: 1.0 at the water, 0.25 at the Street; someone of 12, 0.97); Peter, one who fishes, with traps in the river: "a spate: wicker traps in the main stream tonight will be torn away" | **the decision of the run:** Peter tends line A with `up` and sets it in the fen beside B (2 units); takes up the net (a flood tears it at 0.3) (1) | 3 + Nichola 1 at the racks | 968 eels past: in the fen, 12 traps x 968 x 0.003 = 35 eels, about 20 kg; wreck 0.05 a trap: about 1 trap lost with its catch [e]. **Had A stayed in the river:** 6 x 3.4 kg, but 0.85 wrecked: about 3 kg kept and 5 traps gone | 20 kg: 10 eaten fresh, 10 hung (Nichola, 0.6 unit at 17 kg a unit of hanging) |
| 7 | the flood again; at the fen, "traps in the fen's dykes stand when the river tears the rest away" (one who fishes, 0.7); Nigel tended in the water: "eels against your legs ... all going the one way" | tend the fen lines at dawn (1 unit: both lines are at the fen); otters about at Eelmouth: tend at dawn, before them | 1 | 620 past: 11 traps x 1.9 eels: about 12 kg | 12 kg: 10 fresh, 2 hung; yesterday's 10 kg smoked to 5 kg |
| 8 | spate; Oliver (the Brooks) seen at the Street with his creel heaving (the carried-catch row): the Shepherds, who have not been to the water, learn of the run from it | tend (1) | 1 | 352 past: about 7 kg | 7 eaten fresh |
| 9 | flood | tend (1); mending is part 2's | 1 | 1,114 past: about 21 kg; a second trap lost (10 left: A 6, B 4) | 10 fresh, 11 hung |
| 10 | flood | tend (1) | 1 | 961 past: about 17 kg | 10 fresh, 7 hung |
| 11 | normal: "the river is falling: traps set now will stand" (one who fishes) | Peter takes line A up out of the fen and back into the Isel's edge at twice the share (tend `up`, set: 2 units) | 2 | 554 past: A in the river 6 x 554 x 0.006 = 20 eels (11.6 kg); B in the fen, 4 traps, about 3.9 kg | 15.5 kg: 10 fresh, 5.5 salted (0.15 unit) |
| 12 | normal | tend both (2) | 2 | 525 past: about 14.6 kg | 10 fresh, 4.6 salted |
| 13 | low; "fewer eels each night in the Isel now: the run is passing" (one who fishes, 0.8) | tend both (2) | 2 | 422: about 11.7 kg | 10 fresh, 1.7 salted |
| 14 | low | tend (2) | 2 | 266: about 7.4 kg | all fresh |
| 15 | low; a salmon run starting from the sea (711) | tend (2); set the gill net again in the pool (1) | 3 | 162 eels: 4.5 kg; the net about 10 kg of salmon [e] | 14.5 kg: 10 fresh, 4.5 salted |
| 16 to 17 | "the eel run is over at the Isel for this year" (two nights after the last) | tend `up` both lines: the traps home, dried, stored for next year (2) | 2 | | |

**The run's account:**

| | |
|---|---|
| Caught | about 132 kg of eels and 18 kg of salmon in 12 nights: 150 kg, about 69 food |
| Units | about 27 units of setting, tending and moving, about 2 a day of the household's 15 to 18; hanging and salting about 2.5; making beforehand 11 |
| Food a unit of work | about 69 food over about 41 units with the making: **about 1.7 food a unit**, near the top of the network's band for set gear off a run (0.4 to 2) and well under the weir's (5 to 18) |
| Eaten in the run | about 104 kg fresh (48 food), the house fed |
| Banked | about 30 kg hung, smoked to about 15 kg (14 food); about 16 kg salted (7.5 food): about five nights of food |
| What is left by midwinter (night 26) | smoked, hung about night 8: 15 kg x 0.931^16 ≈ 5 kg (4.4 food); salt: 16 x 0.98^13 ≈ 12.6 kg (5.8 food). **About two nights of food for the winter** |
| Gear worn | each trap about 11 uses of its 30 to 45; 2 traps lost in the floods; the net 2 sets; nothing of the creels |

**What it shows:**
1. **Twelve traps feed a household through the run and no further.** To bank a winter of 16 nights (about 75 food), the house needs
   about 180 kg salted beyond its eating (salt fish keeps; a keeping smoke does not reach spring): 30 to 40 traps at these reaches
   (each adds about 11 kg over the run; 40 traps are about 18 withies and 20 units at 1/7), or a share of a weir, and about 45 kg
   of salt (about 11 units of boiling at the brine spring at 4 firewood to 4 salt). This is the binding the network wants
   (stocks and keeping, not hourly rates), and it gives the nudge somewhere to point: more traps, the weir, salt. Whether 2 to 5 kg a
   trap on a good night (the reach that gives this) is the calibration Zach wants is question 11.
2. **The decision that matters is night 6.** With the dawn spate reading and the fen dyke as a known safe place, the house loses one
   trap; without them, five and the night's catch. The sign must be at dawn ([[D2-265 The river's signs|D2-265]]) and graded to one who fishes, and the fen's
   lower share and wreck must exist in the engine (question 7).
3. **The smoke hut is not the bind for a trap house.** 250 kg a night of racks against at most 11 kg hung a night. For a weir house
   the hands and the salt are (§5.2).
4. **The keeping curve makes the keeping smoke a run-season food**, not a winter one; salt carries to midwinter. A household without
   salt (the medium arm) eats its run and has nothing in spring, which is the medium arm's design ([[D2-256 A hunting trip is travelling out to a wild node, camping there…|D2-256]]'s arms).

### 5.2 The weir house beside it (the high arm's Marshs, three sections)

The same river with the gap shut. The first section takes 30% of what passes up to 100 kg, each added 7% up to 70 kg [m WATER_WORKS].
Night 6: 968 eels x 0.44 = 426 eels, about 247 kg, held to 240 kg by the holds (100 + 70 + 70). A flood with the gap shut wears a wattle section
about 1.7 levels (as built); the Marshs open the gap in the floods and take 0.1 of the share (about 25 kg) or keep it shut and pay in
mending (part 2's).

| | Gap shut through the run | Gap open in the floods (nights 6, 7, 9, 10), shut otherwise |
|---|---|---|
| Caught over nights 6 to 15 | about 1,450 kg [e: 0.44 of 5,944 eels at 0.58 kg; the holds of 240 kg bind on three nights] | about 680 kg |
| Hanging at 17 kg a unit (smokehouse_capacity) | about 85 units; on a 240 kg night 14, more than the house can spare after eating and tending | about 40 units |
| Salting at 40 kg a unit ([[D2-283 Salting fish runs at about 20 kg an hour with gutting, at 1 kg of…|D2-283]]) | 36 units and about 360 kg of salt | 17 units, 170 kg of salt |
| The bind | hands and salt; the racks (250 kg a night) just hold the biggest night | hands and salt |

So a weir house's run is bound by hands and salt, and it has fish to trade to the houses that have none: the dependence the design
wants (scenario_design §1). The tend line's "they were crammed: as much again went past the gap" (from `turned`) is what tells the
crew that a section more, or a second weir, would take more.

### 5.3 A hunter through a winter (a wood village; eight nights, 5 units a day)

**The house:** Walter (a master hunter), Agnes (snares, capable), Tom (youth). Gear [w1]: a copper spear (30 to 70 uses), a crude
weapon for Tom, two bundles of 25 snares (2 units each, day clock, 0.12 cord each), a withy pack basket (+15, 25 kg in all) and a
leather-strapped frame (+20) for Walter. The wood: red deer lean in winter (condition shown to the expert), roe, boar, hares on the
pastures and the heath's edge.

| Night | State and signs | What they do | Units | The take and the night | Notes |
|---|---|---|---|---|---|
| W0 | The first lying snow: "the first lying snow: the deer will be down at the ricks" (as built); snow raises detection x1.5 for deer and boar (as built) | Agnes sets her 25 snares, 18 on the Leaze's hedge gaps and 7 on the heath edge (one act, 1 unit, two parcels as one line: proposed `at` a list); Walter and Tom hunt the wood near, Tom `with` Walter | Agnes 1; Walter 2, Tom 2 | the hunt: Walter meets a hind in the snow and takes it: 33 meat (about 40 kg of venison), a hide; their carry 25 + 10 = 35 kg: about 29 meat home, 4 left with the carcass, cached (Walter's, tagged) | the spear's first use of 30 to 70 |
| W1 | At dawn the snares: 25 snares, about 7% a snare-night on known runs → about 2 catches. One hare dead in the noose, one alive; tracks in the snow to the line | Agnes tends (1 unit): "two hares, one dead in the noose and one alive, which you killed; three nooses sprung and set again." Walter goes back for the cached 5 kg (0 units: on the way); ravens over the wood where the carcass lay | 1 | the cache: wolves had been at it in the night (as built): about 1.5 meat left | the wolf's sign at the carcass: KILL_READINGS |
| W2 | The hunted wood: Walter reads the deer's state (expert): "deer about the wood, few, and wary from the hunting" | **thin or shy decides the trip.** Few and wary: Walter goes `the wood around` (+1 unit) with Tom | 3 + 3 | the wood around: nothing met in the snow; the result: "you came on nothing: old slots only, none fresh in the snow" (thin, not shy: no deer there) | the design's thin-or-shy words (§2.7) |
| W3 | Snares at dawn: nothing, and a fox's tracks along the line; one noose torn | Agnes tends (1): nothing; drops the torn; moves 7 snares from the heath (no tracks) to the Common's field edge | 1 | a hare caught overnight, eaten by the fox before dawn (scavenged: 1 in 4, 1 in 3 in a frost) | "fur and a torn noose left" |
| W4 | A hard frost begins; the fen's pools skinned with ice; duck packed on the last open water (as built) | Walter, two nights out with the frame (far, +3, a camp): far ground, unhunted | 5 + 5 (Tom with him) | far: a red deer and a roe, 41 meat, about 50 kg (master far 3 to 6 food a unit, [[D2-255 A very skilled hunter brings in a disproportionate amount of food…|D2-255]]); carry 30 + 10 = 40 kg: about 33 meat home, the rest left at the camp | the frost keeps the meat (fresh meat's open penalty eased in a freeze [w1 §2.3]) |
| W5 | Snares in the frost: two hares, both dead and frozen stiff in the nooses | Agnes tends (1) | 1 | 2 hares; nothing scavenged (tended at dawn) | |
| W6 | Walter and Tom home with 40 kg; Agnes salts (meat 1 salt to 8, 20 kg an hour with the dressing [d [[D2-283 Salting fish runs at about 20 kg an hour with gutting, at 1 kg of…|D2-283]]]) | Walter dresses the deer (part 2's work on the carcass thing); Agnes salts 30 kg (0.75 unit, 3.75 salt) | 1 + 1 | | the hide and bone to trade: the tanner, the hook maker |
| W7 | The thaw; the snares' runs in mud; "the hares are off the Leaze: no fresh tracks for two nights" | Agnes takes the line up (tend `up`, 1 unit): 22 snares sound, 3 torn | 1 | | |

**The winter's account:** about 29 + 1.5 + 33 = 64 meat brought home from the hunts (38 food) of 74 taken, for 20 hunting units
(1.9 food a unit: a master's band near home, [[D2-255 A very skilled hunter brings in a disproportionate amount of food…|D2-255]]'s far trip lifting it); and 4 hares from the snares (5 meat, 3 food) for 5 units
of setting and tending (0.6 a unit, in the network's 0.4 to 1.2). The snare line is the second adult's steady small food; the
master's trips are the big food, bound by the carry (10 of 74 meat left in the wood) and by wariness near home.

**What it shows:**
1. **The snare line's clock is the night.** A catch dies, lives, is scavenged or spoils by the night; tending at dawn is worth a
   catch in four; a frost keeps it and makes the fox bolder. All of it reads state the engine holds or would hold (`set_state`, the
   wild's foxes, the weather).
2. **Thin against shy is the trip decision** (engine_audit finding 8). Without the two words in the hunt's result, Walter's W2 is a
   guess.
3. **The carry binds the hunt** in kilograms (part 1 §4.2): a lone hunter brings 25 kg of a 40 kg deer; the frame and a second
   person bring it all. A pack ox (100 kg) would bring two.

---

## 6. Bespoke verbs against shapes and techniques

### 6.1 The prompt text each needs

**(a) Bespoke verbs, one an act** (the alternative Zach asked about: "how is setting a snare technique under set verb different from
just a bespoke setting a snare verb?"):

```
- set_traps {"at": water, "n"?: up to 6}: lay wicker traps you carry in the water; they fish by night until you lift them (1 unit)
- lift_traps {"traps"?: a tag, "at"?: water, "leave"?: true}: take what your traps caught and set them again; leave: bring them home (1 unit)
- set_snares {"at": a place, "n"?: up to 25}: set snares you carry on the runs (1 unit)
- walk_snares {"snares"?: a tag, "at"?: place, "to"?: a place to move them}: take what is caught, reset the sprung (1 unit)
- set_net {"at": water}: set a gill net overnight in open water (1 unit)
- lift_net {"net"?: a tag}: (1 unit)
- set_line {"at": water, "bait"?: offal}: (1 unit)
- lift_line {"line"?: a tag}: (1 unit)
- empty_weir {"weir"?: a tag}: (1 unit)
- fish_edge {"at": water, "with"?: dip net | spear}: (1 unit)
- fish_line {"at": water}: (1 unit)
- fowl {"at": a place, "with"?: net}: (2 units)
- hunt / stalk / drive / den_work {...}: as now
```

About 420 words with their docs; 14 or more verbs added to 38 (against [[Q-27 Keep the 38 built verbs, or fold them back to about 22 to 24|Q-27]]'s rule that a new verb needs Zach's yes); each new gear
adds a pair. Confusion moves from set-for-lift to picking among 14 names, and each pair repeats the same shape.

**(b) Shapes with techniques** (verb_grammar; part 4 §5):

```
- set {"what": a way of setting gear you carry (wicker traps, snares, a gill net, a set line), "at": place, "qty"?: how many}: lay
  gear you hold where it catches by night; it stays, yours, until you take it up (1 unit; traps up to 6, snares up to 25)
- tend {"thing"?: a tag (T7), "at"?: place, "up"?: true}: go to your gear set at a place: take what it caught and set again what
  was sprung; up: bring it home. With no tag, all of yours there (1 unit a place)
- gather {"what": a way of taking (the edge, a line, fowling, hunt, stalk, drive, den work), "at": place, ...}: as now
```

About 90 words for all of taking; the techniques under each shape are listed with the person's level (part 4 §2.2), so the agent sees
"Yours: wicker traps (6 in hand; 6 in the Isel, T7), snares (a bundle of 25)" under set, and "Yours: T7 in the Isel, T4 on the
Leaze" under tend.

**(c) Technique named alone** (part 4 §5.2): `{"do": "wicker traps", "at": "the Isel"}`, the engine choosing the shape. Fewest words
for the agent; safe for taking only with the state rule of §6.3.

### 6.2 Measured against the failures

| Failure in the runs | Bespoke | Shapes (b) | Technique alone (c), part 4's rule | Technique alone with §6.3's rule |
|---|---|---|---|---|
| set for lift (about 40% of trap acts) | gone if the agent picks the right of two names; Jory's misreading of a note still possible | gone: set is refused without gear in hand and points to tend; tend is its own word | **returns**: named alone, a technique takes its first shape (set) | gone: with one's own gear standing, the technique alone tends |
| acts took places, not things | needs the tag argument on each lift verb | tend takes the thing, default one's own | as (b) for tend | as (b) |
| hand fishing as plain "fish" | `fish_edge` is plain | the edge is a named technique; "fish" alone is refused with the list of one's own ways | "fish" must not resolve to hand fishing by alias (§6.4) | as (c) |
| nets as a lure | two verbs, fowl and set_net, plain | the technique names say what each is for | as (b) | as (b) |
| prompt length | about 420 words | about 90 | about 60 | about 60 |
| a new gear later (a fyke, a keep box) | two more verbs | a technique row | a row | a row |

### 6.3 The state rule for a technique named alone

A technique with two shapes (set and tend), named alone at a place:
1. one's own gear of that technique stands there: **tend** it;
2. none stands and one holds the gear: **set** it;
3. neither: refused, saying where one's gear is or that one has none, and how it is made.

The result always says which shape was done and how to ask for the other ("You tended T7 ... To lay the 6 traps you carry beside
them, set wicker traps"). This replaces part 4 §5.2's "takes its first (set)", which is the bug of [[Q-79 Whether to fix the fishing bugs the live runs exposed|Q-79]] in a new form.

### 6.4 Where part 4's ten shapes fail for taking

| # | Part 4 says | The failure | Fix |
|---|---|---|---|
| 1 | §5.2: a technique with two shapes, named alone, takes its first (set) | reproduces set-for-lift whenever one also holds gear | §6.3 |
| 2 | §5.1: the shape is named "set and lift" | lift is a trap's word; snares are walked, nets lifted, the weir emptied; agents wrote lift, check, empty, collect and walk | name it **tend**, with all five as its words (question 1) |
| 3 | §5.1: set and lift's units "set: units by the gear; lift: 1 a place" | a snare line runs along edges over more than one parcel; a place-based tend cannot walk it | tend takes a thing (a line may span the parcels it was set on) or a place |
| 4 | §5.1: "ret flax" under set and lift | retting is processing (part 3a's containers that change goods over nights), not a take | move it to 3a's keeping shape |
| 5 | §5.3: several of one's own: "a lift takes all"; Zach's [[Q-80 Whether acts on owned things default to one's own|Q-80]] note: "several: asked" | the two disagree, and Zach's word stands until he changes it | question 2 |
| 6 | §5.2: `do` a free string, resolved "by name, alias or label word, preferring one the person knows" | "fish" is an alias of fish by hand (data.py:598); a fisher who knows traps writing "fish" gets the edge | drop "fish" and "fishing" as aliases of the edge; refuse with the person's own fishing ways listed |
| 7 | §5.1: gather includes hunt, drive and fowling | right for the hunt; the drive's crew is a declared party (`with`), not agree: part 4 is consistent if `with` stays a modifier on gather | keep `with` |
| 8 | §5.4: take from a set folds into "lift" | taking from another's set (theft) and tending one's own are one act on a named thing; the theft wording follows the owner, not the shape | §2.0 rule 3 |

Part 4's ten shapes otherwise carry every act of taking: go (a trip out, a camp), gather (worked takes), set and tend (placed gear),
work (dressing a kill, the weir's mending: part 2's), build (a weir section), move (carrying a catch home, giving it), change (the
weir's gap). Nothing in taking needs an eleventh shape.

---

## 7. Conflicts with decisions, proposals and code

| # | Where | What conflicts | Effect | Proposed |
|---|---|---|---|---|
| 1 | records: [[Q-80 Whether acts on owned things default to one's own|Q-80]] open, no D2; acts_on_owned_things.md "discussion" | Zach's 21 Nov yes in [[Q-80 Whether acts on owned things default to one's own|Q-80]]'s notes | the rule this whole note rests on is not recorded as decided | record it as a decision with question 2's answer (question 3) |
| 2 | [[Q-80 Whether acts on owned things default to one's own|Q-80]] notes, wave4 §5.3 | several of one's own: asked, or all | §6.4 row 5 | question 2 |
| 3 | hunt_fish §5 and §7.7 | snares as 5 or 25, 0.02 or 0.15 cord, 10 sets or used up | prices and the tend's cost | §7.7, as part 1 prices it |
| 4 | hunt_fish §5, §7.7, verb_grammar, wave4 | lift or tend | the prompt word | question 1 |
| 5 | VERB `set` (verbs.py:53) | the word is taken by doors and gaps | a set shape collides until wave4's change shape lands | §0.2 row 4 |
| 6 | [[D2-265 The river's signs|D2-265]] against river_signs question 6 and the code | a freeze stops fishing; the code fishes on under ice | traps, nets and the edge in a freeze; the frozen signs | §4.5; an engine change in phase 1 |
| 7 | [[D2-269 Experts' signs are observations of what is happening now, which may…|D2-269]] against kinds.py:412, 894 | signs that direct | two rows | §4.4 |
| 8 | [[D2-264 The fishing, hunting and materials network|D2-264]] (up to 6 traps a set) against SETS line 1 (methods.py:87) and wave4 "set: units by the gear" | one trap an act today | set act costs | 6 traps 1 unit; 25 snares 1 unit |
| 9 | [[D2-276 Making durable things runs on the year clock|D2-276]] and part 1 against hunt_fish §5's gear units (trap 2.5, net 30) | the proposal's units are real hours | gear prices | part 1's (§2 above) |
| 10 | [[D2-273 Three clocks, each system on one|D2-273]] against `_set_night`'s life in nights | a set's life in nights mixes the day clock into gear's life | sets spring while sound | lives in uses (§1.3) |
| 11 | [[D2-211 Fresh fish keep as meat in hand, and alive in a trap or a weir until…|D2-211]] (fish alive in a set until lifted) and §2.2 (most snared beasts dead by morning) | not a conflict: water keeps fish alive, a noose does not | | both, by technique |
| 12 | river_signs §3 and §4.4 ("lift it with take, from its tag") | the lift by take | prompt and craft lines | tend |
| 13 | hunt_fish §7.1 ("fish at the edge ... a run where it passes a shallows or a pinch point") and today's `run_take` (any river parcel with a run) | today any river parcel is a pinch | the edge in a run too rich or too poor by place | the pinch is a parcel feature (below a dam or weir, a ford's shallows) from the generator; elsewhere a few heads |
| 14 | wave4 FI2 ("lifts every one each morning") | consistent with tend at dawn | | the lore's word should be the shape's word |
| 15 | part 1 §4.1: carry limits apply on the road only | a hunter far out is on no road (the far range is off-road) | the carry binds the hunt (`wild.carry_of`, wild.py:2222) but not set gear within a village | keep: the hunt's carry stands as built, in kg |
| 16 | `seed_by_land` (methods.py:270) seeds net and trap in water on the trade curve's 0.5 | a household that learnt from its land starts worse than a bare novice (engine_audit finding 7) | trap skill in the runs arms | part 4's learning (wave4 §4) |
| 17 | [[W-72 Signs of the river|W-72]]'s hand-fishing truth and the shallows stock ([[D2-264 The fishing, hunting and materials network|D2-264]]) | with a shallows stock everywhere, the runs world's "no resident fish" design ([[D2-256 A hunting trip is travelling out to a wild node, camping there…|D2-256]]'s isolation) gains a small edge stock | the runs-only arms are less isolated | the runs world's shallows thin (a big river), stated in its README |

---

## 8. Questions for Zach

Each stands alone. Ids in brackets are existing records; new ones are to be filed under this thread ([[W-81 Design wave part 3b, taking|W-81]]).

1. **What to call coming back to set gear: tend, or lift** (to file; touches the verb list, [[Q-27 Keep the 38 built verbs, or fold them back to about 22 to 24|Q-27]]). One act takes the catch, sets
   again what was sprung, and with `up` brings the gear home. Options: (a) tend, with lift, check, empty, walk and collect as its
   words; (b) lift (part 4's word), with the others as its words; (c) two acts, lift and take up. Recommended: (a); "lift" fits traps
   and nets but not snares or the weir, and the agents used all five words. Blocks: the prompt's shape lines and the resolver.

2. **Several of one's own things at a place, with no tag named** ([[Q-80 Whether acts on owned things default to one's own|Q-80]]). Your 21 Nov answer was "several: asked". Options: (a) asked,
   for every act; (b) a tend takes all of one's own of that technique at the place, and acts that use a thing up (a slaughter, a take
   from a pile) ask; (c) all, for every act. Recommended: (b): tending one's own gear is harmless and per place, and asking makes the
   commonest act fail; a slaughter or a take that ends a thing should be chosen. Blocks: the tend and [[Q-80 Whether acts on owned things default to one's own|Q-80]]'s build.

3. **Record your yes to the thing as the target, own by default, as a decision** ([[Q-80 Whether acts on owned things default to one's own|Q-80]]; acts_on_owned_things.md). It sits in the
   ask's notes, not in DECISIONS, and the proposal reads "discussion". Options: record it now with question 2's answer; or hold it
   for the verbs and archetypes build ([[W-70 Verbs and livelihood archetypes, before the engine rework|W-70]]). Recommended: record now; three proposals and two design parts rest on it. Blocks:
   nothing to design; the records' truth.

4. **Gear in hand to set** (to file; [[D2-264 The fishing, hunting and materials network|D2-264]] made gear a thing with a life). Set lays traps, snares, a net or a line one holds, and is
   refused without them, naming one's gear already standing. Options: (a) yes, with existing worlds seeded with the gear their arms
   hold (hunt_fish §11); (b) gear optional, free sets kept as today's weaker version. Recommended: (a); it is the fix that makes
   set-for-lift impossible. Blocks: bug 2's fix, wear reaching use, every gear chain.

5. **A run's fish learn no wariness** (to file; the net puzzle of [[Q-79 Whether to fix the fishing bugs the live runs exposed|Q-79]]). One salmon netted from a run raises the salmon's wariness
   by 30 in the village area because a run has no resident heads to divide by, and nets and traps then barely meet a run for weeks.
   Options: (a) fix as a bug in phase 1: wariness and pressure on the resident share only; (b) let runs learn, at a share of their
   size. Recommended: (a); passing fish are new fish each night. Blocks: nets and the edge in a run; any calibration of either.

6. **The edge in a run** ([[Q-79 Whether to fix the fishing bugs the live runs exposed|Q-79]], [[W-72 Signs of the river|W-72]]). Hands at the edge take from the shallows and, at a pinch point (below a dam or weir, a ford's
   shallows), from a run. Options: (a) a few heads at best on open shallows, a few times the shallows rate at a pinch, a dip net
   x3; (b) today's run take on any river parcel. Recommended: (a), with the pinch points written by the generator. Blocks: the edge's
   calibration.

7. **The fen dyke in a flood** (river_signs question 5; [[D2-264 The fishing, hunting and materials network|D2-264]] §7.8). Options: (a) a trap in a fen dyke takes half the river's share
   of a run and is wrecked at about a twentieth of the river's rate (0.05 in flood, 0.02 in spate); (b) the same share, never
   wrecked, as the code does now; (c) the fen meets no run. Recommended: (a); it makes moving traps on a flood dawn the run's real
   decision (§5.1 night 6). Blocks: the worked autumn's numbers; the fen's signs.

8. **A snare line's night** (to file; hunt_fish §7.7). Options for the defaults: about 4 in 5 caught beasts dead by morning; a live
   one breaks free by the next night 1 in 3, tearing the snare; scavengers take an unlifted catch at about 1 in 4 a night (1 in 3 in
   a frost); good snare places by a parcel's edges (10 to 20 a hedged pasture). Recommended: these, to calibrate in bots against 0.4
   to 1.2 food a unit. Blocks: the snare build.

9. **The weir as a craft some know** ([[Q-79 Whether to fix the fishing bugs the live runs exposed|Q-79]]). Options: (a) building a weir section is a practised craft known by its holders and the
   weir-and-nets expert; anyone may work on a crew led by one who knows it; (b) universal, as today. Recommended: (a); the low and
   medium arms are told today that they know a craft their design says they do not. Blocks: the runs arms' prompts.

10. **What a freeze does to the runs** ([[D2-265 The river's signs|D2-265]], to refine with the environment's effects, [[L-150 Environmental effects on fishing refined after the rest works|L-150]]). Options: (a) a hard-frost night
    holds the run (it passes on the next open night); (b) the run passes under the ice and only the weir takes a share; (c) the run
    is lost to the frost. Recommended: (a) for eels (they stop moving in the cold) and (b) for salmon. Blocks: §4.5's run row.

11. **How much a trap takes on a run night** (to file; the calibration). The design's reach gives 2 to 5 kg a trap on a good night
    (fishing_ladder §4), so twelve traps feed a house through the run and bank two or three nights of winter food; banking a winter
    takes about forty traps, a weir share or salt. Options: (a) keep that order; (b) richer traps (about 10 kg a good night, today's
    hold), so a household of traps banks a winter; (c) poorer. Recommended: (a); it makes the weir, salt and many traps the paths to
    a winter, which is the network's dependence. Blocks: the runs arms' calibration and their read against the null arm.

12. **Lore that advises** ([[L-141 How much seeded memory each livelihood starts with|L-141]], with the founders' sets, [[D2-268 The founders' starting knowledge|D2-268]]). Lines such as "a house that means to eat from the run sets many
    before the nights come" are a family's know-how, not a sign. Options: (a) lore may advise in the family's voice ([[D2-269 Experts' signs are observations of what is happening now, which may…|D2-269]] binds
    signs only); (b) lore states facts only, the same rule as experts' signs. Recommended: (a), for founders' seeded lines, which can
    be dropped like any kept line ([[D2-268 The founders' starting knowledge|D2-268]]). Blocks: the fisher's and hunter's seeded sets (wave4 §3.5).

13. **The catch carried home as a sign** ([[W-72 Signs of the river|W-72]]). A person seen at the houses with a creel or hands full of fresh fish, after work at
    the water, tells those who never went that a run is on. Options: (a) yes, for fish, meat and fowl over about 5 kg; (b) no, news
    by talk only. Recommended: (a); it reads a body and a load, puts no act in a mouth, and is the missing reach from the water to the
    village. Blocks: the run's village-wide bundle.

14. **"Today you could" by one's own livelihood first** (to file; 37.4's prompt). The list is the first ten crafts in table order; a
    fisher in the runs world is shown felling, sowing and fencing and none of their fishing. Options: (a) a phase-1 fix: the
    household's crafts first, then by level, before the cap; (b) wait for part 4's "What you can do" section ([[W-70 Verbs and livelihood archetypes, before the engine rework|W-70]]). Recommended: (a)
    now, as a bug; it touches no design. Blocks: any reading of "agents rarely fished" in the next runs.

---

## 9. What building it would take (by seam, [[D2-244 The engine's reworking into feature packages|D2-244]])

| Unit | Holds | Files (owner) |
|---|---|---|
| **placed gear** | the set container's new fields (§1.3); set and tend handlers; the state rule (§6.3); wear a use a night; take up; theft | engine/wild.py `set_work`, `_set_night` (37.2); verbs.py, things.py, tags.py (37.4) |
| **the water's methods** | the shallows stock; the edge, lines, nets by gear reach; the fen's share and wreck; the freeze | wild/methods.py, engine/wild.py, data.py WATER_WORKS (37.2) |
| **the river's senses** | river_signs §1 to §3 with §4 here: dawn rows, the carried catch, the reworded rows | wild/kinds.py, engine/signs.py, perceive.py (37.2 writes, 37.4 reviews) |
| **the hunt's results** | thin and shy words, the kill as a thing, weapon wear | engine/wild.py `hunt`, `_hunt_lines` (37.2) |
| **phase-1 bugs** | bugs 1, 3 (wariness), 4, 5, faults 6 to 9, 11, 13 to 15 | as §3 |

**Bot tests to run before any live arm**, on the three runs arms: the eleven tests of §3; then a scripted fisher bot (sets two lines
before the window, tends at dawn, moves to the fen on a spate dawn, salts the surplus) against today's bots, reading food a unit,
traps lost, and kg banked against §5.1; and the hunter's winter against §5.3. Each read against the null arm (no fishing) and with an
end-state reading of who holds fish in spring (scenario_design §6).

## Sources

- Code (main, 22 Nov): `cybertron2/engine/knowledge.py` (206, 223, 411 to 432), `verbs.py` (53, 518, 610, 678 to 681, 1608 to 1698),
  `wild.py` (909 to 1016, 2235 to 2470, 2573, 2585, 3100 to 3184, 3185 to 3228, 3242 to 3286), `things.py` (284 to 411, 622 to 690),
  `here.py` (219 to 242), `tags.py`, `prompt.py` (775 to 795, 878 to 888), `data.py` (51, 345 to 346, 376 to 391, 597 to 606, 957,
  1010 to 1036), `wild/methods.py` (44 to 114), `wild/kinds.py` (412, 826, 854 to 856, 872 to 902), `wild/gear.py` (172 to 196).
- Probes (scratchpad `w3/`): probe2 (bugs 1, 2, 4, 5; the net on fresh copies), probe3 (the net with wariness), probe4 (the
  neighbour's snares, the net's ground), probe5 (Peter's rendered prompts), a 44-day bot run of runs_medium (the river's nights).
- docs/cybertron2/proposals/hunt_fish_materials.md, river_signs.md, acts_on_owned_things.md, verb_grammar.md, trying_and_learning.md;
  spec/core/clocks.md; guides/senses.md; docs/scenario_design.md.
- docs/review/37_growth/02zzzh_hunt_fish/: wave1_physical_basis.md (final), wave4_people.md (final), fishing_ladder.md,
  hunting_ladder.md, engine_audit.md, crafts_evaluation.md; docs/review/37_growth/02zzy2_fishing_methods_compared.md.
- Records: [[D2-263 A craft a person knows at capable or known shows, where they look|D2-263]] to [[D2-285 The records brief is run by hand after each compaction for now, since…|D2-285]]; [[Q-27 Keep the 38 built verbs, or fold them back to about 22 to 24|Q-27]], [[Q-79 Whether to fix the fishing bugs the live runs exposed|Q-79]], [[Q-80 Whether acts on owned things default to one's own|Q-80]], [[W-72 Signs of the river|W-72]], [[W-73 Fishing, hunting and their materials developed together|W-73]], [[W-81 Design wave part 3b, taking|W-81]], [[L-111 The hunting and resources build, a soon follow-up|L-111]], [[L-141 How much seeded memory each livelihood starts with|L-141]], [[L-150 Environmental effects on fishing refined after the rest works|L-150]].

*Current as of 23 Nov 2026.*
