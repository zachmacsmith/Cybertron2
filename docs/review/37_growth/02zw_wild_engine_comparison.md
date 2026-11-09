# 02zw: the reviews' proposals against how the engine already works (9 Nov)

Zach (9 Nov): "a lot of the reviews done by another agent didn't have context about the existing engine, so might have over
engineered or added new systems or not designed them appropriately, so everything should be seen from the perspective of how the
engine already works." This note takes each core change of 02zv (C1 to C15) and the main content of its first packs, and sets it
against the code on branch `ecology` and the decided spec, read by 37.2 on 9 Nov. For each: what is **built**, what is
**decided**, what the reviews **proposed**, and the **verdict**: *exists* (nothing to build), *extend* (a small change to what
exists), *new* (a genuinely new mechanism), or *drop or defer* (over-engineered, or not needed yet). The briefs
(proposals/methods_and_encounters.md, wild_raiders_and_works.md, carcass_and_decay.md) are written from this note.

**Why 02zv read as an overhaul.** 02zu described a target design (verbs with shared slots, ten general rules, one encounter rule,
standing works) without the engine in view, and 37.2 passed the framing on without checking the code. Checked, most of the
target describes how the engine already works: verbs already take a technique as their object with place, party, `looking for`
and range; techniques are already data rows with gear (`uses`), tools, weapons, crew and readings by skill; one function already
settles every hunt (`wild.take`); groups already raid by targets with fences, watches, dogs and scares (`wild._groups`); things
already lie at places and carcasses already age. What is per kind is mostly **data** (take tables, kind-named technique rows,
seeding), not machinery.

## 1. Core changes

### C1, C2, C3: methods, traits, the encounter rule, verbs and skill
- **Built:** verbs `gather` and `work` take `what` (a technique, resolved by name or alias, `knowledge.resolve`), `at`, `for`, and
  modifiers (`range`, `looking for`: a kind or a sort, resolved against `taken.family`); a technique row holds verb, label,
  aliases, `at` (covers or a site), units, `crew`, `uses` (gear needed in hand: a plough, a rod, clappers, firewood), `tools`
  (grade multipliers), `weapon` (none or armed), `untaught`, `basic`, `reads_as` (readings by skill), `yield` (its kind: wild_take,
  wild_forage, wild_site, wild_guard, wild_watch, wild_shut). `wild.take` is already one rule: candidates are the kinds in the
  areas reached, weighted by count, `taken.detect`, conditional effects, pressure, the technique's `takes[k]`, the target focus,
  `when` rows and distance; then danger, flight, the take, wounds, legends, leaders, litters. Skill is per technique (`knowledge.skill`,
  D2-52), with levels aware, rough, capable, known (D4-24), teaching and trying; `SKILL_CARRY` passes skill between two wild
  techniques. The system text lists only techniques the person knows (`prompt.verb_lines`), with tool multipliers in each note.
- **Decided:** D2-192 (each kind taken by its own technique and skill), D2-93 (tryable untaught), D4-24, D4-103 (basic crafts of a
  pack known to all), D4-78 (no daily menu).
- **Proposed:** traits on kinds, properties on methods and gear, one encounter rule, shared verb slots with ten rules, methods as
  data with skill per family, familiarity by kind (Zach), determinate targets, seeding by upbringing and land, a manual without
  multipliers, refusals without the catalogue.
- **Verdict:** **extend, mostly data.** The verbs, slots, modifiers, technique rows, gear, skill and the take rule exist. What changes:
  general method rows replace kind-named ones; each method's `takes` table is **generated at load** from the kinds' traits and the
  method's needs and favours, so `take` itself is unchanged; **familiarity by kind** is the only new mechanism (a record per kind on
  the person, a factor in `take`, the gate on expert readings); seeding by land replaces `basic` for most wild methods; two small
  text changes (no multipliers for these methods; refusals without the list). 02zu's "ten general rules" and slot redesign are
  **dropped**: they restate the engine.

### C4: shared perception and wind
- **Built:** people notice by one rule (sense, visibility, presence, attention, conspicuousness; `perceive.py`, `things.py`). Animals
  "notice" people coarsely: groups read a watch on the parcel or at the gap, a herd being herded, a dog fitting (`_groups`); the
  ecology lowers use of busy land (`near`: home 1.0, ring 0.4); a hunt's chance falls with pressure. The climate has daily wind
  speed by node and moving storms with a velocity (D4-110), but no prevailing wind direction.
- **Decided:** D4-48 (the noticing rule), D4-110.
- **Proposed:** run the noticing rule from the animal's side (senses, wind direction, the person's noise and light).
- **Verdict:** **defer.** It refines what exists (detect, pressure, the watch) and needs a wind direction from 37.4's climate. If
  wanted, it enters `take` as one *approach* factor (wind from the climate, crew size, a dog) rather than as a reverse noticing call.

### C5: animal interface additions
- **Built:** no separate interface file; behaviour is in `wild._groups` (positions home, edge, ready; drive from hunger and
  conditions; `found`, `memory_days` and `return_p` as memory of a target; habituation per scare with decay and wariness after harm,
  D2-198; rest after being turned; leaders, legends), `wild/ecology.py` (movement toward better land, migrants, pressure flight),
  sites, regimes, follow-the-harvest. D2-203 is decided but no per-kind module exists yet; kinds differ by data rows.
- **Proposed:** alarm, follow, probe, cache; typed memory; bold-shy traits; route graphs.
- **Verdict:** **mostly defer.** The memory and habituation that matter are built. The pieces with a clear use now: *displacement*
  (C6) and *a lapse probe* for the fox (a target row over several houses, below). Alarms (the jay, M7) wait on C4; route graphs
  wait on a need the gap watch does not meet; bold-shy waits on evidence it changes a decision.

### C6: displacement and refill
- **Built:** refill exists: the ecology moves populations toward better land along links each day, so an emptied area refills
  (and a culled fox's area fills from around); hunted areas lose shy kinds and regain them as pressure fades (`HUNTED`). Not built:
  a turned group *rests* (`rest`) rather than going elsewhere.
- **Proposed:** a turned raider takes the next target the same night; a lapse at one house raises the probe at its neighbours.
- **Verdict:** **extend.** In `_groups`, when a group is turned it picks its next target from the same target list that night (or
  the next) instead of resting, by a kind's data (`displace: true` for birds at the corn, boar; `false` for kinds scared off for
  days). The lapse probe is a target row whose targets are several houses' hens or stores, picking an unshut one first. Refill
  needs nothing.

### C7: standing works, condition, upkeep, capacity
- **Built:** things that act each night with no one present already exist: fences and walls (`FENCES` with `through` by level,
  wear by the year, mending, D4-114), stores (`house_spoil`, `STORE_KEEP` for a dog and a granary), shut doors (`wild.shut`, for the
  night), fittings (granary, cellar, bins), buildings with condition and repair (D2-168), tools with grades and wear (`ITEMS` tool,
  life), carrying weights and capacities. Not built: a trap or net *left set* that takes in the night and holds its catch.
- **Proposed:** a general standing work with condition, upkeep, capacity, depreciation, quality.
- **Verdict:** **extend, narrowly.** Barriers, stores and wear exist. The one new piece is the **set trap**: a thing left at a parcel
  (a container of kind `set`, like a pile) with a method, resolved in the night by `take`'s rule against what is there, holding its
  catch for whoever comes (possession is whoever takes, D4-23), wearing by use. Stores' and fences' "properties against traits"
  (a raised granary stops rats, a mesh stops a weasel) extend `STORE_KEEP` and `FENCES` with a kind's trait (`climbs`, `gap`), not a
  new system.

### C8: kept populations, bonds, breeding
- **Built:** herds with births, survival, milk, dung, grazing, straying, watching (`herds.py`, `data.py` cattle); led beasts (D4-58);
  any beast can be worked (D4-114); disease in herds (wave 4); hens kept in buildings that lay (`_hens_lay`); the dog is a **fitting**
  of a house, not a beast.
- **Verdict:** **defer to 37.4** (husbandry.md). The wild layer needs only what exists: the house dog as a fitting, hens as eggs.
  Dogs as beasts, bonds and breeding are K6.

### C9: the butcher step, by-products, delayed processes
- **Built:** `slaughter` yields meat and a hide; carcasses carry meat and hide (`leave_carcass`); goods include meat, dried meat,
  salt fish, hide, antler, horn, egg, salt; recipes (`make`) take inputs (dry meat, salt fish, cheese, charcoal). Not built: tallow
  or fat, bone, sinew, glue, feathers, wax, leather, cord, nets; no process that takes several days.
- **Verdict:** **extend with goods and recipes, defer the rest.** Adding `tallow` to what a slaughter and a carcass yield, and a
  recipe for a rush light or candle (it answers the lantern one-off, 02zq), is data. Cord (from bast or hemp) and a net or snares
  as made goods are data and recipes too, and they let gear be *required* for snaring and netting. Delayed processes (tanning,
  smoking over days) are deferred until a chain needs them.

### C10: decay and scavenging
- **Built:** a carcass is a thing at a parcel: fresh for a day (`carcass_fresh_days` 1, its meat edible), its meat then goes off
  (`night.py`), bones after 6 days, conspicuous by age, read by cause (`KILL_READINGS`, disease); food spoils by item (`spoil`,
  `decay` kinds); bodies lie where people die (D2-4) and are buried with cairns (D4-99). The ecology has a carrion pool per area
  fed by wild deaths and eaten by carrion eaters (`ecology.py`), and ravens over it are a sign. **Not linked:** carcass things do
  not feed the carrion pool or draw any group; the carcass's meat just goes off.
- **Proposed:** stages, a scavenger succession, handling choices, burial depth, spillover predation.
- **Verdict:** **extend.** (1) A carcass at a parcel is a **target** for scavenging groups through the existing target rows
  (`_targets`, `_raid`: a group raids a carcass as it raids a store); its mass is eaten by what comes, not only lost to rot. (2) Its
  stages are the existing ages (fresh, rotten, bones) sized by the beast (a hen goes in a day or two; a cow lasts longer), slowed by
  frost. (3) Spillover falls out of the memory groups already have: a group that fed at a parcel remembers it (`found`,
  `return_p`) and its drive there is raised for some nights, so the fold or the hens beside it are in reach. (4) Burial: a grave's
  depth by units spent and ground; only a shallow one is a target. (5) Ravens over a carcass thing reuse the ravens' sign. No new
  decay system is needed.

### C11: forays
- **Built:** hunting already reaches beyond the village: `range` near (the parcels), the wood around (the ring, 1 unit) and far (the
  wild areas, 3 units) (`_reach`), drawing from those areas' populations; a hunter notices kinds along the way (`_notices`); the
  day's route is recorded (D4-62); roads have stretches, notices, meetings, good places; camps and nights out exist (D2-68, D4-12).
- **Verdict:** **extend, later** (forays.md). A foray is the existing range modifiers turned into a route over areas, with an
  interpreter call and a story; most pieces exist.

### C12: works on parcels and edges
- **Built:** fences and walls on parcels, clearing (clearing.md), field works, roads with landmarks, parcel heights and sides
  (D2-114). Not built: hedges as distinct from fences, rides, high seats, tracks into a wood.
- **Verdict:** **defer.** A hedge is a fence of a kind (`FENCES` gains a row); the rest waits on a need.

### C13: evidence and marks
- **Built:** wild traces at parcels with kind, what (edge, raid, tried, turned, watched), scare and by whom (`_trace`, signs);
  carcasses read by cause; things noticed by one rule; thefts known (thefts_known.md).
- **Verdict:** **exists** for what the first packs need. Marks on animals (swans) wait for K-later.

### C14: world options; C15: diagnostics
- **Built:** packs (`packs: [wild]`), world settings (`view`, `evening`), knowledge seeding by `basic` and the generator's experts;
  run records (turns, perception, days, run.db) and the scratchpad's `analyse_run.py`.
- **Verdict:** **extend.** A world setting for which households know which methods; the diagnostics are a few counts in
  `analyse_run.py`. Forest law and D2-194 rights stay world options for later arms.

## 2. Content of the first packs, against what exists

| Content (02zv) | Built now | Verdict |
|---|---|---|
| birds at the corn as social followers, displaced | woodpigeons eat crops only as a density in the ecology's diet (no group, so no scare turns them); rooks pull corn from the rookery's site, and any watch on a field stops them there (no habituation, `watch_stops`); only red deer, boar, fox and wolf are group raiders (`near_people`) | extend: give woodpigeon a `near_people` row (a flock that habituates) so watches and clappers act on it; `displace` and a flock's "lands where others feed" as its next-target rule |
| the fox, lapses, the treadmill | fox raids hens and stores; `shut`; refill by the ecology | extend: a lapse probe over the hamlet's houses (target row) |
| stoats by gap size | no stoat; `shut` stops any raider | new kind (data) with a trait `gap: small`; a shut door does not stop it, a mended store does |
| the cat | the dog fitting halves store losses (`STORE_KEEP`) | extend: a cat as a fitting like the dog (mice and rats only), settling by itself where there are mice (one rule) |
| traps and snares set | snaring is resolved inside the act | extend: the set trap (C7) |
| stores with properties | granary and dog keep stores; rats follow the harvest | extend: `STORE_KEEP` read against a kind's `climbs`, `gap` |
| boar and deer at the field | built (groups, gap watch, fences, scares) | exists; red deer's raid is already in `NEAR` rows (check calibration: boar at 3 to 10% unwatched) |
| rooks' trade-off; grub loads | rooks raid; loads exist (slugs, aphids, ladybirds) | extend: rooks lower a soil load on parcels they work (data on the load) |
| moles and the mole-catcher | none | new kind as a load on meadow (data) and a method row; the catcher is whoever knows the method |
| markers with sowing rules | markers built as signs | extend: the sowing lore already names windows (D4-114); a marker's sign times it |
| the owl hole | owls are a kind | extend: a fitting that lowers mice in its barn |
| cattle stampeding from flies (gadding) | herds, fences, trampling exist | new condition row on herds (hot, still day) through existing straying |
| butchering, tallow, light | slaughter, carcass, hide; lanterns as a one-off | extend: tallow as a yield; a rush-light recipe |
| scavengers and decay, spillover, burial | carcass things, carrion pool, group memory | extend (C10) |
| the midden | none | defer: a waste stock waits until a kind needs it (the kite) |
| smoking and salt | dry meat, salt fish recipes; salt as a good | exists |
| the bear's cache | bear is a kind; carcass things | extend: a bear's target row on carcasses with a guard danger |
| the cursed field (black bane) | murrain exists; no seeded history | defer to a later pack |

## 3. What this changes in 02zv's build order

- **Stage 1** (C1 to C3) is data plus one new mechanism (familiarity) and two small text edits; mostly 37.2's wild-pack code.
- **Stage 2** shrinks to displacement and the lapse probe in `_groups` (C6); shared perception (C4) and the other interface pieces
  (C5) are deferred.
- **Stage 3** shrinks to the set trap and traits read by fences and stores (C7).
- **Stage 4** is carcasses as targets for scavenging groups, sized stages, spillover by memory, burial depth, and tallow (C9, C10).
- **K1 and K2** are mostly data on these extensions: new kinds as rows (stoat, mole), fittings (cat, owl hole), condition rows
  (gadding), target rows (lapse probe, carcasses, the bear's cache).
- C4, C5 (beyond displacement), C8, C11, C12 and most of C9 move later, each when a pack needs it.

## History
- 9 Nov: written by 37.2 at Zach's request, reading the engine on branch `ecology` and the spec, after he pointed out that the
  reviews lacked the engine's context.
