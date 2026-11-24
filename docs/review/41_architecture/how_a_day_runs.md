# How the engine actually runs a day, and which patterns hold (W-112)

Session arch, 24 Nov 2026, at Zach's ask: "how does the engine actually currently run? ... what are the actual mechanisms right now
of how a day actually runs, of how everything fits together? What are the patterns, whether ideally sought after and collapsing or
actually held to?" Read from the code on `main` at 82f8b92c (line numbers there). Companion to [target.md](target.md).

## 1. The pieces

- **The world** is one JSON-like dict, `World.s` (`world.py:111-113`): nodes, roads, parcels, buildings, herds, containers, people,
  institutions, claims, offers, agreements, knowledge, minds, the day's events and acts, plus keys features add (`waters`, `wild`,
  `today`). Rows of the data tables (`data.py`: ITEMS, TECHNIQUES, FITTINGS, COVERS, RESOURCES, PHYSICS ...) are module-level
  dicts that the state points to by name.
- **Every change** goes through `World.apply(prim, place, **kw)` (`world.py:461-481`): the place check, hooks, the change, the
  journal entry with its cause. There are 43 primitives (`world.py:1109-1157`); a few are generic (`transfer`, `create`, `draw`,
  `set`), most belong to one feature (`plots`, `leg`, `gear_night`, `set_wild`, `book`).
- **A person's view** is two objects made fresh for each use: `Here(w, name)` (what is at their place, about 80 methods) and
  `Mind(w, name)` (what they know and remember).
- **The run** (`run.py:803-1200`) is one loop over days. Each day is a fixed sequence of **steps** (dawn, decide, talk.0..n, work,
  evening, settle, night, memory), each opened and committed in the journal (`J.open_step`, `J.commit`), so a run can be resumed
  or replayed from the last committed step, with every model reply read back from the journal.

## 2. One day, step by step

| Step | What happens | Code |
|---|---|---|
| **dawn** | the day's events are cleared and `today` is blanked (`run.py:906-908`); `dawn(w)`: the spec's incidents by kind (`stray`, `death`, `fire`, an if per kind), goods left at a door announced, growing up and succession (`life.dawn`), arrivals off the road, the river's dawn cue (`wild/river.dawn_events`), the spec's scripted signs (`run.py:373-427`); then `perceive.dawn` | `run.py:905-911` |
| **decide** | for each acting person: the system prompt and the turn prompt (old prompt, the beliefs view, or the rebuilt core, chosen by world settings: `VW.on`, `CORE.on`), the evening meeting's block spliced in by string replace (`run.py:918-924`); a plan made at last night's hearth used instead of a call if nothing needs the morning (`:925-932`); the model calls in parallel (`_parallel` of `decide`); each reply's notes and the household book's rules applied at once, free | `run.py:912-946` |
| **talk** | `talk()` delivers what was said and told and the offers to those present, and wakes those spoken to; they are called again with a talk prompt (one wave with an evening, two without); their revised acts replace their plans; the morning meeting if one was called | `run.py:947-984` |
| **work** | each person's plan (up to 10 acts) is run in a shuffled order, one act from each person in turn (`:1010-1052`); hunting parties are resolved first (`parties.resolve`); each act's cost in units is checked against the day's budget (speech costs units; overwork allowed up to a limit); `verbs.do` runs it; a refused act is not tried again that day; then the units left go to one's own rules, the standing fallback and the household's chores (`book.spare_units`, `:1053`); the too-heavy-to-travel call; "You rested N units"; then the parties' hunts and the lessons settle (`:1079-1082`); the routes of the day as chains of parcels (`layout.routes`) | `run.py:985-1086` |
| **evening** (worlds with it) | the day's noticing computed (`perceive.evening`) and shown at the hearth; the evening call: talk, plans for tomorrow, night acts | `run.py:1087-1097`; `run.py:470-558` |
| (between) | `labour.close_day`: work's food cost, fatigue, the walk | `run.py:1098-1099` |
| **settle** | partnerships both chose; children's work; agreements settled; joins; thefts; goods left at a door | `run.py:1100-1109` |
| **night** | departures onto roads; the roads' night (`roads.night`: travel, encounters, traces); the urgent calls (`fuse`: raids and other night events that wake people, with their own model calls); then `night.night(w)` (below); the night's noticing; each person's night lines; the turn record written; `perceive.close_day` | `run.py:1110-1131` |
| **memory** | at the end of a chunk of days, each person rewrites their memory with a model call | `run.py:1132-1160` |

**Inside an act** (`verbs.do`, `verbs.py:384-409`): the reply's free form is normalised (`shapes.normalize`, by word lists), aliases
turn leave, put and hide into `give` and lift, check and empty into `tend`; the verb's handler runs inside a cause (so every primitive
it applies is journaled with its actor and verb). For `gather` and `work` the handler is `_technique` (`verbs.py:687-910`): resolve
the craft by name, apply its modifiers, find the site, check the shortfall (skill, tools, inputs), then **switch on the craft's yield
kind**: 22 branches (`stock`, `chance`, `fixed`, `clear`, `pool`, the 14 farming kinds handed to `farm.act`, `bury`, `burn`, `mend`,
`smoke_tend`, `repair`, four kinds of `wild_take`, `wild_den`, `wild_young`, `wild_pest`, `wild_forage`, `wild_site`, `wild_shut`,
`wild_guard`, `wild_watch`, `clear_built`), each calling into its feature module; then the goods made, the tool worn, practice
counted, an event written with hand-written text, and the result returned **as a sentence**. Other verbs (make, build, give, move,
travel, agree, teach ...) have their own handlers, of the same form.

**The night** (`night.py:20-260`) is one long function: fights settled, departures, where everyone sleeps, buildings' shelter
levels, fires in each building (by fitting names: hearth, fire ring; camps by structure name), the processing containers
(`process.night`), open fires, care's food, then for each person in the book's meal order: shelter state, rations, work's food,
the food need, eating from an ordered list of stores (raw food, the book's holds and rations, the cold, deaths); then life's night
(conception, births, old age); spoilage in every container (with named exceptions: a trap in the water, `night.py:201`); lots done
(`process.finish`); camps falling in and buildings' breaks by structure; regrowth of stocks (`_grow`, through the renewal rules);
skill fading; farming's night (`farm.night`: crops, herds, soil); the wild layer's night (`wild.night`, which holds placed gear's
night); gear rotting; offers lapsing (`night.py:139-262`). Each part is called in place; the order is the order of the lines.

**Senses** are computed twice a day, not at each act: acts and the night write **events** (`w.event`, with text and salience); at
the evening (or the night) `perceive.evening` builds each place's **facts** (`signs.facts`: every sign row whose condition holds over
each subject's context, `signs.py:1221-1300`, plus the events), and each person **notices** some of them by the one noticing rule,
with one random sequence per person per day (`perceive.py:421`). What is noticed goes into the mind, and tomorrow's prompt is
written from the mind.

## 3. How things fit together: the actual couplings

- **By name through shared tables.** A feature's rows link to others by name (a process names its fittings, a technique its tools);
  that is sound. But features also *add to* other tables at import (`data.py:129-134`, `:1303-1313`; `process.register_fittings`
  overwrites fields on FITTINGS rows, `process.py:141-148`; `PRIMITIVES.update` in `world.py:1148-1157`).
- **By direct call from the hubs.** The act hub, the night, the world build (`world.py:255-278`: agreements, knowledge, things,
  buildings, the book, waters, wild, shallows, willow installed in order), dawn and the sign walker each import and call every
  feature that takes part. Function-level imports (162 counted on 16 Nov, feature_packages inventory) hide a 26-module import loop.
- **Through `today`.** The day's shared blackboard: about 40 keys with no owner (`worked`, `travel`, `teach`, `learn`, `joins`,
  `thefts`, `partners`, `book` ...), written by acts and read by settle and the night.
- **Through result text.** An act returns a sentence; the work loop reads it (`res.startswith("Refused")`, `"Refused: travel: you
  carry"`, `run.py:1046-1049`), and so does the speech cost (`"You said ("`, `:1001`).
- **Through world settings choosing whole code paths.** `CORE.on`, `VW.on`, `EVN.on`, `SH.on`, `CL.on` and the packs select
  different prompts, parses, evenings and climates; the old paths are kept so old worlds replay. The engine is several engines
  sharing a state.

## 4. The patterns: held, half-held, collapsing

| Pattern | Sought since | Today | Evidence |
|---|---|---|---|
| **Every change through the chokepoint** (D4-34) | 23 Oct | **held**, with leaks | `World.apply` is used everywhere for state; the leaks are 9 writes round it in area C (learning records, teaching's skill, a road stop, a guest's bed: C summary) and the mind's dict written directly |
| **Replay and resume from the journal** | Oct | **held** | steps committed with checkpoints; replies read back; resume from the last memory checkpoint (D4-124) |
| **One noticing rule** (D4-53, D4-75) | 1 Nov | **held**, nearly | one rule reads every sign and event; the road's `mult`, the traces' multiplier and `least` are side paths (feature_packages §5) |
| **Renewal as a registry of rules** (D4-7, D4-103) | 7 Nov | **held**, too narrow | `renewal.py`; the shallows and willow had to add their own context and change K beside it (A §7.3) |
| **Processes as rows** (D4-103, u4) | 7 Nov, wave | **held** in its unit | `process.py`; but `IN_PROCESS_OF` in `data.py:148` beside the rows |
| **Packs as clean switches** (D4-103) | 7 Nov | **half**: rows switch, code does not | `packs.on` filters rows; signs, prompt prose and code paths of a pack stay live (feature_packages §11) |
| **The world grows by data on a few verbs** (D4-24) | Oct | **collapsing** at the acts | 38 verbs held, but the act hub has 22 yield kinds by `elif`, with named cases inside (`verbs.py:776`, `:779`) |
| **Behaviour on properties, not names** (D2-353, 24 Nov; implied since Oct) | Oct, stated 24 Nov | **collapsing** | named-branch density rising at every snapshot (A §8; D §6.2) |
| **Interface and signs rendered from data** (D4-95, D2-350) | Nov | **collapsed in the wave, being restored** | the act table replaced by eleven hand sentences (W-100), being rebuilt from the registry (W-109); 95 hand-written event lines; sign ids by position |
| **A feature as one unit** (D2-244) | 9 Nov | **held as grouping, not as isolation** | units keep their tables and functions together (`process.py`, `gear.py`, `water.py`), but reach into the hubs and edit shared tables; a unit of named branches passes the rule (A §7.4) |
| **Generated worlds carry the physical world entire** | Nov | **collapsing** | resident fish only from makers; livelihoods only for pinned households (build_gaps G68; generality.md) |
| **Nothing fails silently** | implicit | **not held** | sign conditions that raise are dropped (`signs.py:1235`); an unknown yield kind yields nothing; a founder's line dropped when a name is absent; no registry checked at load |

**What it comes to.** The spine has held throughout: the state, the chokepoint, the journal and replay, the day's fixed steps, the
one noticing rule. These were set in the first weeks and are what make the engine trustworthy for experiments. What has collapsed
is everything at the **joins**: how a new kind of act, a new nightly process, a new subject of signs or a new kind of world content
is attached. Each feature has been attached by adding a branch to a hub, a call to a procedure, a key to `today` or a field to
another's table, because the hubs offer no registry to attach to. That is why the units themselves (processes, stores, gear's lives)
look clean and the engine as a whole does not, and why [target.md](target.md) puts its first work on the joins: registries at the
hubs, the night and the world build as declared phases and seed steps, structured results instead of sentences, and a load check.

*Current as of 24 Nov 2026 (82f8b92c).*
