# Proposal: wild behaviour, a design for each kind and a module of its own

**Status:** partly accepted: D2-203 (each kind's behaviour designed first, then built as a module of its own that acts only through
the animal interface and the engine's primitives; replaces "no kind has code of its own"). The behaviour specs per kind (§4) are
in **discussion (10 Nov), for Zach to check before anything is built.** **Owner:** 37.2 (design; the `ecology` branch, D2-199).

**Affects:**
- proposals: wild_layer.md (the system this sits on), wild_systems.md (the catalogue it revises), wildlife.md (the kinds and their
  economy), node_ecology.md, living_populations.md, wild_plants.md, husbandry.md;
- code on the `ecology` branch: `cybertron2/wild/` (a new `behaviour/` package and the animal interface), `engine/wild.py`;
- spec/information/signs.md (signs from behaviour), spec/conflict/ (danger, the watch).

**Builds on:** the audit of what was built (`docs/review/37_growth/02zq_wild_audit.md`), which found most kinds' behaviour to be
numbers fed to one shared machine, with much of the catalogue present only as signs.

## Summary

Zach, 10 Nov:
- "Animals can add specific mechanisms / code but it should just be cleanly modular so they are easily acting within the broader
  system and only through the normal ways of acting with the world through the engine";
- "Yes, I do want the design per wildlife and then each has modules";
- "The first thing to nail down is to ensure the behavioral specs are actually what we would want."

Earlier, 8 Nov: "These mechanics etc. are more important than realistic population dynamics", and "Each should have different
layers ... maybe even the simpler ones have some deeper more nuance so experts actually have more to learn."

What this proposal does:
1. **Sets the architecture (D2-203):** each kind, or each pattern several kinds share, is a behaviour module. It perceives through a
   narrow animal interface and acts only through the engine's primitives, as agents act through verbs. The food web stays the
   population base; modules run the groups and individuals on it (§3).
2. **States what the wildlife are for**, and the tests a behaviour must pass to be worth building: a mechanism with state, a pattern
   people can come to expect, a sign and a lever, a learning problem other kinds do not pose, a consequence that travels, and a
   response to what people do (§1).
3. **Traces where the current designs came from**, and what was lost on the way (§2).
4. **Examines every specced kind** against those tests, says what is right, wrong or missing, and gives a behaviour spec for each:
   numbered behaviours, each with its state, its rule, what people see, what they can do, and the test that shows it working
   (§4).
5. **Draws the web between kinds**: the consequences that travel, with their lags (§5).
6. **Checks diversity**: which learning problem each kind brings, the gaps and the overlaps (§6).

## 1. What the wildlife are for, and what a behaviour must do

### 1.1 The purposes (from wildlife.md §1, node_ecology.md, wild_systems.md §1-2)
- **A world that holds hidden, changing state** that people must infer from signs, catches and lore (partial observability).
- **A land that is a threat as much as a food** (node_ecology.md's finding): crops, stores and beasts lost, so watching, fencing and
  hunting matter.
- **Learnable regularities at several depths**: a base rule anyone learns, conditions that only some notice, an expert's reading,
  a rare regime (the L0-L4 layers).
- **Dependence and specialisation**: skills, gear, crews, trained beasts; trades worth having.
- **Commons and management**: stocks that can be overdrawn, rights (D2-194), restraint.
- **Danger and collective action**: threats that need many hands.
- **Land that changes and is changed**: what people do to the land moves the animals, and some animals change the land.
- **Consequences that travel**: between kinds, between villages, across seasons.

### 1.2 What makes a behaviour worth building (the tests for every row in §4)
1. **It is a mechanism with state.** Something the module holds and changes (a position, a memory, a den, a make-up, a condition),
   not a multiplier on a shared rule and not a sign alone. (The audit's main finding is that most "depth" failed this.)
2. **It makes a pattern a person can come to expect**, within a run where possible (a fast arm, a night to two weeks; a short arm,
   two weeks to two months: wild_systems.md §8), with slower arms carried by lore and history.
3. **The pattern shows in signs, and a lever answers it**, and the outcome differs by what people do (principle 4 of
   wild_systems.md: a forecast is worth nothing without the act it pays for).
4. **It poses a learning problem** (§1.3) that another kind does not already pose in the same way.
5. **It connects**: through a shared driver (weather, the mast, the vole phase) or another kind, so consequences travel (§5).
6. **People's acts change it**: hunting, felling, clearing, watching, fencing, storing, shutting a door. The land is to be managed,
   not watched.
7. **It passes the relevance test** (node_ecology.md): it moves some household's food, work or safety by about a tenth in some year
   or under some choice; or it is plainly marked as a sign-giver (an information kind, like the raven) whose value is in what it
   tells about others.

### 1.3 The learning problems
The kinds should differ less in what they are than in **what a person has to learn to deal with them**. The problems this design
uses:

| # | Problem | What has to be learned |
|---|---|---|
| P1 | **Timing** | which nights, which week of the year |
| P2 | **Place** | where: the gap, the run, the earth, the flight line, the patch |
| P3 | **Varying the answer** | the animal gets used to the same scare; vary it or back it with harm |
| P4 | **Keeping it up** | the animal is scared off but returns; the answer must be kept, not varied |
| P5 | **Restraint** | taking less now keeps more for later |
| P6 | **No way back** | a mistake that cannot be undone (a site deserted, a slow breeder trapped out) |
| P7 | **Many hands** | a crew, a drive, a weir, a bounty: one person cannot |
| P8 | **A consequence through another kind, with a lag** | hunting the deer brings the wolves to the herds |
| P9 | **A season foretells the next** | a bare autumn means a hungry bear in spring |
| P10 | **A trade-off** | the same animal helps and harms |
| P11 | **A misread** | the obvious reading is wrong (a wolf's track as a dog's; the ladybird's grub as a pest) |
| P12 | **An adversary that learns you** | it learns your pattern (the unwatched nights) |
| P13 | **Reading its state** | fat or lean, few or many, wary or not: what it will do next |
| P14 | **When not to go near** | a sow with young, a wounded boar, a bear in spring |
| P15 | **Emptied and refilled** | taking one empties its place until another moves in |
| P16 | **Reading others through it** | an information kind: ravens over a kill, a heronry's size and the fish |

## 2. Where the current designs came from

| Source (date) | What it gave | What was lost or bent on the way |
|---|---|---|
| **wildlife.md** (8 Nov; D2-192 waves, D2-193 danger, D2-194 rights, D2-195 legends, D2-196 hounds) | the kinds by habitat and use: what each gives, how it is taken, its role (food, danger, rights, trade, land change), the waves by economy; §12: "no kind needs code of its own" | the economy half (furs, wax, rights, hounds, weirs) is mostly unbuilt; §12's rule, meant to stop one-off handlers, became the reason behaviour was flattened (now replaced: D2-203) |
| **living_populations.md** (8 Nov) | populations as distributions over the land: growth, diet, movement toward good land with home fidelity, people's take collapsing the field where they look | built as the food web on coarse areas; the "resolved into actual animals where someone looks" half became groups condensed at villages, with no ranging |
| **02zp, the ecosystem deep dive** (parts one to six) | the W2 food web (Kleiber eating, condition, crowding, movement); the reader models (novice, systematic, expert) showing reading pays where lore joins signs (eels, the mast, voles) and little where yesterday's damage tells everyone (boar, fox); the relevance numbers (boar 22% of need unwatched, eels 11%, slugs 4%, fox 3%) | the finding that "for boar and the fox the depth must sit in the acts, not the forecast" (§25.2) was not carried into the build: the acts got one shared machine |
| **node_ecology.md** (8 Nov) | design from the village outward; the land matters as threat more than food; the 10% relevance test | the reservoir and visits became the ring and its groups; the "visitors as events" became the group state machine |
| **wild_systems.md** (8 Nov; D2-197 leads in engine days, D2-198 answers to scares) | the catalogue: each kind's L0-L4 layers, signs, levers and couplings; the archetypes; the interconnection tables; the lags; the needs (readings by skill, misreads, lore as tested belief, creature memory); §10: "no kind has code of its own" | rich prose, but not written as mechanisms with tests, so the build could satisfy it with multipliers and signs |
| **wild_layer.md and the `ecology` branch** (9 to 10 Nov; D2-199, D2-200 to D2-202) | the general system: land summary, kinds as data, the ecology step, groups near people, traces, signs by skill, takes, loads, diseases, plants, sites, legends | per-kind behaviour reduced to settings of one group machine plus windows of multipliers; the catalogue's rows ticked when only a sign or a multiplier existed (02zq §1, §4) |
| **Research grounding** (wild_systems.md §12; 02zp's sources) | the real phenomena: mast cycles and pannage, vole cycles and their predators, the eel run, heronry censuses, wolf and livestock conflict, boar damage | sound; the behaviour below keeps to well-established natural history and marks where it simplifies |

## 3. The architecture (D2-203)

### 3.1 Modules
- A package `cybertron2/wild/behaviour/`, one module per kind (`boar.py`, `red_deer.py`, `wolf.py`, ...) or per pattern several
  kinds share (`denning.py`, `flocks.py`, `colonies.py`, `runs.py`). A kind's data row names its module(s).
- A module holds the kind's own logic: what it decides, when, and from what. Its numbers stay in its data row, so calibration is
  data.
- **Shared building blocks** that modules compose rather than copy: ranging over parcels (§3.4), memory maps, habituation by the
  kind of scare (light, noise, a person, a dog), group make-up and ageing, the activity calendar.
- **Scales:** a kind counted by density stays in the food web, and a module may hook it (the eel run, fowl arriving with the frost,
  the vole phase); a kind counted whole has groups or individuals the module runs (a sounder, a herd, a pack, a pair of foxes, a
  bear); a site (a heronry, a rookery, a lodge, a bee tree) is a place-bound group.

### 3.2 The animal interface (what a module may see and do)
Like the `Here` and `Mind` agents get, and checked the same way (a test that modules touch nothing else).

**Perceive:**
- its own group: size and make-up (age and sex), condition (from its area's food in the ecology), memory, position, den or site;
- the land it can reach tonight: the parcels near its position (cover, standing crops and their stage, stocks it eats, fences and
  gates, doors of stores, carcasses), the area beyond;
- what is physically there tonight: a watch's light or noise, a dog, people working or sleeping out, other kinds' groups near (a
  pack, a herd);
- the weather and snow now (not tomorrow: animals do not forecast; signs that lead the weather are the climate's, not theirs);
- what happened to it: harmed, chased, fed, where.

It does **not** perceive people's plans, the engine's other state, or anything a real animal could not sense from where it is.

**Act** (each through an existing engine primitive, so the journal, replay, perception and signs work unchanged):
- move: to a parcel or an area (`set_wild`);
- eat: draw a stock (`draw`), trample or root a crop or turf (`draw`), take from a store (`destroy`);
- kill: a beast of a herd (the herd's count and a carcass: `set`, `leave_carcass`), another kind's member (the ecology's counts);
- den, leave a den, found or leave a site (`set_wild`);
- give birth, die, disperse (its group's make-up; the area's count kept by the conservation rule);
- leave a trace or make a sound (a trace record or an event; signs read them by the senses guide);
- remember (its memory, `set_wild`).

**Keyed randomness** through the interface (`rng(day, group, purpose)`), so every run replays exactly.

### 3.3 Order of the night
The ecology step (populations, foods, condition, breeding, disease); then each kind's module for its groups, in a fixed order by
kind; then the signs read the traces and events at dawn. A module never acts in the day phase: animals act at night or at dusk
and dawn; people meet the results.

### 3.4 Ranging and memory (the core shared blocks)
- **Position:** a group near a village holds a parcel (or the area beyond) as its position each night.
- **Choice of where to go:** a value for each reachable parcel: food there (by the kind's diet and the crop's stage), cover (woods,
  scrub, high crops), distance from its lie-up, minus remembered danger and disturbance, plus remembered food; the group goes to
  the best, with a keyed draw among near-equals. Routes emerge from cover and the land's shape: the gap is where the cover meets
  the field, found by the sounder, not set by code.
- **Memory maps:** fed here, harmed here, met a watch here, disturbed here (people at work, a hunt); each fading over engine days at
  the kind's rate (D2-197).
- **Habituation by the kind of scare:** light, noise, a person, a dog, harm; a new scare of a kind already learned wears off faster.
- **People's patterns:** a group remembers which nights a place was watched; a kind that learns (P12) tests a watched place on
  another night and comes when it was unwatched.

### 3.5 Guards and tests
- Only behaviour modules name a kind; engine code names none (the existing guard test, moved to the modules' boundary).
- Modules import the interface only (a test like the agent-facing modules' one).
- Every behaviour in §4 has its test: the rule as an outcome a test can check on a generated world.
- The conservation test (counts kept between areas, groups and takes) holds with the modules.

## 4. The kinds, examined

Each kind: where its design came from; what is right and wrong with it; its role and its learning problems; the behaviour spec
(B rows: the mechanism, what people see, what they can do, the test); and the changes from the current spec. Real behaviour is kept
to well-established natural history; simplifications are marked. Engine time: Y = 32, a season of 8 days, an engine day about 11
real days (wild_systems.md §8).

### 4.1 Wild boar (deep)
**From:** wildlife.md (a crew hunt, crop damage, mast-driven); wild_systems.md §6 (the learned field, frost to the stores, mast to the
fields, the two-year sequence, the gap, the old sow, swine fever); 02zp's readers (yesterday's damage tells everyone; the expert's edge
is in varying the scare).

**What is right:** the learned field and habituation (P3) is a good problem and true to boar. Frost sending them to stores, a failed
mast sending them out, are real.

**What is wrong or missing:**
- **Damage is too big and too uniform.** The deep dive's 22% of need unwatched is above real damage (1-10% near woods, more locally
  in bad years). It should depend on the cover beside a field, the mast and the sounder's learning, so some villages have a boar
  problem and others none.
- **Boar barely follow the mast** in the ecology (3% between years). The strongest real effect is on breeding: after a heavy mast
  more sows breed and litters are larger, so the next year has many more boar. This is the cross-season arm (P9) and it is absent.
- **The gap is fixed by code**, not found. The old sow is a multiplier.
- **Rooting of pasture and meadow** (boar as an engineer: turf turned over, hay lost) is missing, though it is the commonest boar
  damage on grassland.
- **The sounder is shapeless:** no sows, young and boars; no farrowing that changes it; no lone boar.

**Role and problems:** crop and turf damage near woods (the strongest wild threat); P3 varying the answer, P2 the gap, P12 a learner
of watches, P9 the mast to next year's numbers, P14 sows with young and a wounded boar, P7 the crew hunt, P13 reading the sounder.

**Behaviour spec:**
- **B1 A sounder and its range.** Sows, their young of the year and yearlings, led by the eldest sow (the matriarch); adult boars apart,
  joining in the rut (autumn's end into winter). The sounder has a lie-up in the densest cover of its range by day. *Test:* a
  sounder's make-up has a matriarch, sows and young; boars alone except in the rut.
- **B2 Night foraging by value.** Each night the sounder goes to the best parcel by its value (§3.4): mast in the woods in a mast autumn
  beats any crop; milk-ripe corn and newly sown corn beat roots; pasture and meadow are rooted for grubs and roots when wet. *Signs:*
  rooting where they fed, slots, wallows. *Test:* in a heavy mast autumn the sounder stays in the woods; in a failed one it goes to the
  fields; a field with no cover beside it is seldom reached.
- **B3 Routes and the gap.** It reaches fields by the cover that touches them, the same way each night while nothing goes wrong there.
  *Signs:* a run worn through the hedge (lingering). *Lever:* a watch at the gap meets them before the field; a fence or hedge mended
  there turns them to the next way in. *Test:* with two ways in, a watch at one moves them to the other.
- **B4 Learning the field and the watch.** It remembers a field that fed it and comes back nightly; it gets used to a scare of one
  kind (light, noise) in a few nights; harm (a dog's bite, a boar killed) makes it wary of that place for longer; it remembers which
  nights a field was watched and comes on the others. *Lever:* vary the scare, back it with harm, watch on unpredictable nights.
  *Test:* the same fire every night stops working within about a week; a fire on alternate nights is beaten by coming on the off
  nights; a dog's bite keeps them off for longer than any harmless scare.
- **B5 Frost and snow.** Frozen ground stops rooting; the sounder goes to clamps, stores and ricks it can reach. *Lever:* a shut,
  sound store. *Test:* in a frozen run a sounder near a village raids an open store.
- **B6 Rooting the grass (an engineer).** On wet pasture and meadow in spring and autumn they root for grubs and roots, turning the
  turf: the parcel's grass is cut back for a season. *Signs:* turf turned in strips. *Lever:* a fence; hunting. *Test:* a rooted
  meadow gives less hay.
- **B7 The mast and next year.** After a heavy mast more sows farrow and litters are larger (breeding from condition and the mast); after
  a failed one few. *Signs:* many striped piglets in spring after a mast year. *Test:* the year after a heavy mast the sounder is
  larger than after a failure.
- **B8 Danger.** A sow with young charges in spring; a wounded boar lies up and charges whoever follows; a boar at bay wounds hunters
  (D2-193). *Lever:* hunt with a crew and a hound (D2-196); leave a wounded boar or go in with others. *Test:* a lone hunter is hurt
  more often than a crew; following a blood trail alone is the most dangerous act in the wood.
- **B9 The matriarch.** The eldest sow carries the sounder's memory (its fields, its routes, its fear of places). Kill her and the
  sounder breaks up: its memory is lost, the young scatter and raid less, more erratically. *Test:* after the matriarch is killed the
  group's remembered field and route are gone.
- **B10 Swine fever** (wave 4's disease): runs through crowded sounders and through village pigs (husbandry); worst in cold weather.

**Changes from the current spec:** damage made local and learnable (B2, B3); breeding from the mast (B7) as the cross-season arm;
rooting the grass (B6); the matriarch carries memory (B9); a run on unpredictable nights is beaten by a learner (B4, P12).

### 4.2 Red deer (middling)
**From:** wildlife.md (herds, the rut, stalking, the noble's beast, forest law); wild_systems.md (dusk grazing, the rut, hard winter to
the ricks, the hunted wood, snow, the slot readings).

**What is right:** the rut and the hard winter are true and give timing (P1) and a seasonal arm.

**What is wrong:** the current build makes red deer **a second boar** (raids on the corn with the same machine). That wastes the kind.
Red deer are mostly grazers and browsers of the wood's edge and of young trees; their real conflict is with coppice and young
woodland, and with hay in hard winters; and they are above all **a resource with rights and with restraint** (forest law, D2-194), and
a test of how a herd answers hunting.

**Role and problems:** P5 restraint (hinds are next year's calves), P1 the rut and the winter, P13 reading the herd, P15 a hunted wood
emptied and slowly refilled, P10 trade-off (deer and coppice), rights and poaching (D2-194).

**Behaviour spec:**
- **B1 Herds by sex.** Outside the rut, hinds with their calves and yearlings in a herd led by an old hind; stags apart in small groups.
  *Test:* a herd near a village is hinds and calves; stags elsewhere.
- **B2 Dusk to the edges.** They graze the wood's edge, pasture and young corn at dusk and dawn, and browse young growth; by day they lie
  in the wood. Their damage is grazing (a share of a field's young crop) and **browsing the coppice regrowth**, which kills young growth
  for a season. *Lever:* a fence round the coppice; hunting the edges. *Test:* a coppice cut beside a deer wood regrows slower unfenced.
- **B3 The rut.** In early autumn the stags gather hinds; they roar (a sound that carries), are careless and bold, and a stag at bay is
  dangerous. *Signs:* roaring; rutting stands. *Lever:* the rut is when stags are easy to approach; a stag's meat is rank then (lower
  value). *Test:* stags are found more easily in the rut.
- **B4 Winter yards and the ricks.** In snow and hard frost they come down to sheltered low woods, strip bark, and come to ricks; the
  weakest (calves, old hinds, stags spent from the rut) die in late winter. *Lever:* fence the ricks. *Test:* in a hard late winter the
  herd loses mostly calves and old animals.
- **B5 The hunted wood.** Hunting disturbs the herd: it moves to the far side of its range or the next wood within days, and drifts back
  after weeks of quiet; a drive with many keeps it away longer than a lone stalk. *Lever:* leave the wood quiet to keep them; hunt hard
  to drive them from the fields. *Test:* after a drive the herd's position is out of the village's land for longer than after a stalk.
- **B6 What the herd is.** Each herd has a make-up; killing hinds lowers next year's calves; killing stags does not. *Lever:* take
  stags, spare hinds (restraint). *Test:* a herd hunted of hinds shrinks the next year; one hunted of stags holds.
- **B7 Calving and the hidden calf.** Calves are born in early summer and lie hidden; a hind will not go far. *Signs:* a hind alone and
  restless at the edge.

**Changes:** red deer stop being crop raiders like boar (B2: edge grazing and coppice browsing instead); herd make-up and sex-selective
hunting (B1, B6) as restraint; the rut's value trade (B3); winter mortality by age (B4).

### 4.3 Roe deer (middling; a niche rule)
**From:** wildlife.md (not in the tables), wild_systems.md (single and small groups, the summer rut, roe rings, barking, the hidden kid).

**What is wrong:** built as red deer with smaller numbers, so it teaches nothing new. Its niche is the point: **small, territorial,
each to its own patch.**

**Role and problems:** P15 emptied and refilled (a patch is empty until another moves in), P11 the misread (red-deer lore gets the roe
rut wrong), P2 place (each patch), coppice browsing (P10 with the woodward).

**Behaviour spec:**
- **B1 Patches.** Each roe (a buck's territory with does in it, in summer) holds a patch of thicket and edge; they do not gather in
  herds except loosely in winter on open fields. *Test:* roe near a village are spread one or two to a parcel of cover.
- **B2 Emptied and refilled.** Killing the roe of a patch leaves it empty until a young roe disperses into it (spring and autumn).
  *Lever:* hunting one patch hard empties it; spreading the hunt keeps all. *Test:* after a patch's roe is killed, no roe is met there
  until the next dispersal.
- **B3 The summer rut** (July-August), not autumn: rings trodden round a bush; bucks bark. Kids born in May lie hidden in long grass and
  the mower finds them. *Signs:* rings, barking. *Misread:* one carrying red-deer lore looks for a rut in autumn.
- **B4 Browsing.** Roe browse buds and young shoots: coppice and young hedges suffer where roe are many. *Lever:* a fence.

**Changes:** territorial patches and refilling (B1, B2) in place of a red-deer copy.

### 4.4 Wolf (deep; a territorial predator)
**From:** wildlife.md (danger and collective action, deer then herds, the bounty); wild_systems.md (a fold that fed them, deer hunted out
makes them bold, crusted snow, dispersing young, surplus killing, wolves returning, the track misread, ravens over kills, rabies).

**What is right:** a fold that fed them; the deer-to-herds link; dispersing young; surplus killing in a fold; the track misread.

**What is wrong:** the current wolves never hunt deer as a pack. They "gather from far" and come at herds by a probability. So the
cross-kind consequence (P8: hunt out the deer and the wolves come to the herds) exists only through the ecology's hunger, untested.
A lone disperser behaves exactly like a pack. Ravens do not follow wolves.

**Role and problems:** P8 the deer-to-herds consequence, P7 a drive or a bounty, P4 a kept fold, P11 the track misread, P14 a wolf at
bay, P16 read through the ravens, P9 a hard late winter.

**Behaviour spec:**
- **B1 A pack and its territory.** A pack (a breeding pair and their young of one to two years) holds a large territory around deep
  wood, spanning the land beyond several villages; it travels a circuit of it, a few areas a night. *Signs:* howling (strongest in late
  winter, a territorial call), tracks on rides and in snow. *Test:* a pack's position moves along its territory over nights.
- **B2 Hunting deer.** The pack hunts where the deer are, as groups: it follows the herds of its territory, kills the weak (calves, the
  old, the starved in late winter), and its kills feed ravens and foxes. *Test:* deer killed by wolves are mostly calves and the weak;
  a pack's position follows the deer.
- **B3 To the herds when the deer fail.** When the deer of its territory are few (hunted out, or a hard winter), or crusted snow tires
  them, the pack comes to the village herds at night. *Lever:* do not hunt the deer out; fold and watch the herds; dogs. *Test:* after
  the deer of a territory are hunted down, herd losses to wolves rise within a season.
- **B4 A fold that fed them.** A kill at an unwatched fold or herd brings the pack back within days, until the fold is closed or watched
  or a wolf is hurt. An open fold is surplus-killed (several beasts in a night). *Lever:* fold, watch, dog (P4: keep it up). *Test:* a
  herd raided once is raided again within days unless watched.
- **B5 Pups and the den.** In spring the pair dens; the pack hunts hard near it all summer (rendezvous places). *Signs:* a worn path to
  a den (an expert's). *Lever:* den-hunting (historic, cruel, effective): killing pups ends the next generation.
- **B6 Dispersers.** Young wolves leave in autumn to spring; a lone disperser crosses farmland where no pack lives, and takes stock more
  readily than a pack (it cannot hunt deer well alone). *Test:* a lone wolf's kills are more often stock than a pack's.
- **B7 Fear of people, and boldness.** Wolves avoid people, and come close only hungry; they are wary of a watched place for days after
  a wolf is hurt. A wolf at bay wounds (D2-193). *Test:* a watched herd is taken far less often.
- **B8 Ravens.** Ravens follow the pack and gather at its kills (§4.13). *Test:* ravens over the far wood mean a kill there.
- **B9 Rabies (rare; blocked):** a rabid wolf, the one true danger to people, needs illness in people.

**Changes:** wolves hunt deer as groups (B2) and turn to herds when the deer fail (B3), the cross-kind arm made a mechanism; dispersers
behave differently (B6); ravens follow them (B8); the territory is a circuit (B1).

### 4.5 Fox (middling)
**From:** wildlife.md (a pest, lambs, a scavenger); wild_systems.md (back the next night, cubs April-June, vole-crash years, surplus
killing, mange, the earth, den control, scent, birds mobbing).

**What is right:** the fox at the hens is the simplest P4 lesson (shut the hens, keep it up), and the deep dive found it is mostly that.
Back the next night, surplus killing, and mange are true.

**What is wrong or missing:** the fox is a sign and a probability, not a fox in a place. The earth is a sign; den control is a hunt
bonus. The vole link (P8) is through hunger only.

**Role and problems:** P4 shut and keep shut, P2 the earth, P1 spring provisioning, P8 the vole crash, P5 or not (a winter cull is worse
than den control in spring: an interesting problem about *when*, not whether).

**Behaviour spec:**
- **B1 A pair and its earth.** A pair holds a territory of fields and edges near a village, with an earth in a bank or wood. *Signs:*
  the earth (fresh earth, bones, feathers in spring). *Test:* a fox pair has an earth on a parcel.
- **B2 Hunting voles and hares; the hens when it pays.** Each night it hunts what is easiest: voles in a vole year, hares, then the
  hens if a door is open or the run is unfenced. *Test:* in a vole peak the hens are taken less; in a crash, more.
- **B3 Back the next night.** A fox that found an open hen house comes back the next night to the same place; a shut door turns it, and
  it tries again a few nights later (scared off, not used to it: D2-198). *Lever:* shut the hens every night. *Test:* hens shut on the
  night after a raid are not taken.
- **B4 Surplus killing.** Once inside it kills all it can.
- **B5 Spring provisioning.** With cubs (April to June) it hunts by day too and comes to the hens more. *Lever:* dig out the earth in
  spring (the cubs are there); a winter cull kills foxes whose territories are refilled by spring. *Test:* den control in spring lowers
  the hen losses of that year more than the same number killed in winter.
- **B6 Mange** sweeps a crowded fox population (wave 4).

**Changes:** a pair with an earth on a parcel (B1); what it hunts depends on voles (B2, P8); spring provisioning and den control as
timing (B5).

### 4.6 Brown bear (deep; rare)
**From:** wildlife.md (rarity, legend, danger); wild_systems.md (sleeps through winter, wakes hungry, a poor autumn and a hard late winter
bring it to hives, calves and carrion; a sow with cubs; claw marks; the legendary bear, D2-195).

**What is wrong:** hibernation is only "does not eat in winter", and hunters can meet a sleeping bear. The hungry spring is a scripted
window, not the result of a bear's autumn.

**Role and problems:** P9 the autumn foretells the spring, P14 when not to go near, P7 a hunt of many, rarity and legend.

**Behaviour spec:**
- **B1 The activity calendar.** A bear fattens through late summer and autumn on fruit, nuts and mast (its condition rising with the
  year's fruit and mast); dens in late autumn in a den in deep wood or rock; sleeps until spring; wakes by its condition (a fat bear
  later, a thin one early). A sow with cubs dens earliest and wakes latest. While it sleeps it cannot be met. *Signs:* a den (an
  expert's); claw marks and turned stones in autumn. *Test:* no hunter meets a denned bear; a thin bear wakes earlier.
- **B2 The hungry spring.** A bear that went in thin (a poor fruit and mast autumn) wakes hungry and comes to carrion, calves and hives
  in late spring, near villages if the deep wood offers nothing. *Lever:* guard the calves and hives in late spring; burn carrion.
  *Test:* after a poor autumn, spring losses to the bear rise; after a good one, none.
- **B3 Danger.** A sow with cubs attacks; a wounded bear is deadly; a hunt needs many and hounds (D2-193, D2-196). *Test:* a lone hunter
  meeting a bear is hurt more often than any other meeting.
- **B4 Rarity.** A bear is present in few worlds (wildwood, upland cores), one or two at most; the legendary bear (D2-195) is one of
  them.

**Changes:** a real calendar with denning and waking by condition (B1); the hungry spring from the autumn (B2, P9).

### 4.7 Brown hare (simple, with an expert layer)
**From:** wildlife.md (the poor man's food, snaring, coursing, young crops); wild_systems.md (scared off).

**What is wrong:** nothing of its own: a density eaten and snared.

**Role and problems:** P2 place (the runs where snares take), P15 a field snared out and refilled, food for the poor, coursing with
hounds (D2-196).

**Behaviour spec:**
- **B1 Forms and runs.** Hares lie by day in forms on open ground and feed at night; they cross hedges and banks by the same runs.
  *Lever:* a snare set on a run takes far more than one set anywhere. *Signs:* runs through the hedge (a practised reader); forms.
  *Test:* snares set where the runs are take more.
- **B2 Snared out and refilled.** Snaring a field hard empties it; hares from the land around refill it over weeks. *Test:* a field's
  hares fall after heavy snaring and recover.
- **B3 Boxing in spring** (does fending off bucks; a sign of the season and of numbers).
- **B4 Hard winters** kill many; the hare sickness (wave 4).

### 4.8 Woodpigeon (simple)
**From:** wild_systems.md (the mast; winter corn and greens when the mast fails).

**Role and problems:** P8 the mast's failure sends them to the young winter corn, P3 they get used to a scarecrow, children bird-scaring.

**Behaviour spec:**
- **B1 Flocks that go where the food is.** In a mast autumn the flocks feed in the woods; when it fails they come to the young winter
  corn and peas, in flocks that strip patches. *Test:* winter corn losses to pigeons rise after a failed mast.
- **B2 Getting used to scares** (D2-198): a scarecrow or a clapper works for a few days, a child moving about longer.

### 4.9 Rats and mice (followers of people)
**From:** wildlife.md (raise a store's spoilage; cats, dogs, staddles); wild_systems.md (to the barns after the harvest; a mast failure
brings mice in).

**Note:** in a medieval setting the rat of the houses is the black rat (in thatch and roofs); the brown rat came much later. The
behaviour does not depend on which.

**Role and problems:** P10 how a store is built (a raised floor, stone, a terrier or a cat), P1 the harvest in.

**Behaviour spec:**
- **B1 To the barns after the harvest.** Mice and rats move from the hedges and fields into the stores within weeks of the harvest;
  they breed in full stores through a mild winter. *Test:* store losses rise after the harvest.
- **B2 What keeps them out.** A raised granary floor (staddles), a stone floor, a cat or terrier cut losses; a door does not. *Test:* a
  store with a granary floor loses less; a shut door changes nothing (the misread run 6 showed).
- **B3 A mast failure** brings mice into houses and stores.

### 4.10 Voles, owls and kestrels (deep; a cycler)
**From:** wild_systems.md (the cycle, owls and kestrels moving to the voles, pellets, the low year's hungry predators, a vole plague).

**What was done:** the cycle is a phase clock (the deep dive's vole phase, a pulse shared by a world's villages); owls follow it a year
behind. The emergent routes failed (02zq §4c).

**Assessment:** a clock is acceptable here (the mechanics matter more than realistic dynamics: Zach, 8 Nov), and is what the deep dive
designed. What matters is what follows from it.

**Behaviour spec:**
- **B1 The phase** (low, increase, peak, crash, a year each; a mast sets it ahead, a hard winter holds it).
- **B2 Predators move to it.** Owls and kestrels come to land where voles are many (within weeks) and breed well in the peak; in the
  crash they are silent and few. *Signs:* kestrels over every field; owls silent.
- **B3 The hungry gap** after the crash: foxes and owls turn to hens and nests (the fox's B2).
- **B4 Peak damage:** voles strip grass and young crops and get into the stacks in a peak; a plague (rare) gnaws stores through.
- **B5 Mowing and floods** drive voles to the ricks and banks (a sign and a store loss).

### 4.11 Raven (an information kind)
**From:** wildlife.md ("pure information"); wild_systems.md (over a kill).

**Role:** P16: ravens tell where something is dead (a wolf kill, a carcass, a battle); a pair holds the crags.

**Behaviour spec:**
- **B1 Ravens go to carrion.** They gather over a carcass within a day, and follow wolf packs (§4.4 B8). *Signs:* ravens wheeling over
  a place. *Test:* ravens are over the area where a kill lies.

### 4.12 Wildfowl and the hard-weather birds (middling; migrants)
**From:** wildlife.md (winter flocks, fowling, feathers); wild_systems.md (frost brings them, plovers ahead of a freeze, weak a week in,
restraint, woodcock).

**What is wrong:** arrival is by the calendar, not the frost.

**Role and problems:** P1 the freeze brings them, P2 the flight lines where nets are set, P5 restraint in a long freeze.

**Behaviour spec:**
- **B1 Arrive with the cold.** Flocks arrive in autumn and are pushed in by freezes from beyond (a freeze brings many more within a
  day or two); they leave in spring. *Test:* a freeze raises the fowl on the water within days.
- **B2 Flight lines.** They fly at dawn and dusk between roosting water and feeding grounds by the same lines. *Lever:* nets set on a
  flight line take far more. *Test:* fowling on the line beats fowling elsewhere.
- **B3 Weak in a long freeze.** About a week into a freeze they come tame and die; taking many then thins next winter's flocks (they
  return by how many left). *Test:* heavy taking in a freeze lowers the next winter's arrival.

### 4.13 Eel (middling; a run)
**From:** wildlife.md (the run at traps and weirs, rent, a held right); wild_systems.md (dark, wet nights with rising water; a dry autumn
holds it back; the eel night).

**What is wrong:** there is no run: only the traps' yield changes.

**Role and problems:** P1 timing (the eel night), P13 reading the leads (rain after the dry weeks), P7 a crew at the weir, rights
(D2-194), the upstream-downstream commons.

**Behaviour spec:**
- **B1 The silver run.** In autumn a share of the eels turns silver and runs downstream on dark, wet nights with rising water; a dry
  autumn holds them back, so the first heavy rain after the dry weeks brings a great run. The run moves from area to area down the
  river chain. *Test:* the eels at a downstream weir rise on the night after heavy rain after dry weeks.
- **B2 Traps and weirs.** A trap or weir across the run takes a share of what passes; what is taken upstream does not arrive below.
  *Lever:* a crew at the weir on the big night; rights. *Test:* a weir upstream lowers the take at one downstream.
- **B3 Resident eels** in pools and dykes all year, taken by spearing and small traps.

### 4.14 Heronry (a colony)
**From:** wild_systems.md (the same trees for generations, a hard winter crashes them, disturbance in spring deserts the site, the size
shows the fish, a lord's feast).

**Built:** a site that grows, crashes and leaves. Fixed after run 6: only felling, hunting and robbing at the nests trouble it.

**Role and problems:** P5 and P6 restraint and no way back, P16 the size shows the fish, P1 the young taken at the right time (a
feast).

**Behaviour spec:** B1 nesting in the same trees each spring; B2 a hard winter halves it and it recovers over years; B3 trouble at the
nests in spring deserts it for years; B4 herons fish the river and meres (a rival at the weir); B5 the young taken late in spring.

### 4.15 Rookery (followers of people)
**From:** wild_systems.md (rooks follow the plough for grubs and pull the young corn; bird-scaring as children's work; rook pie).

**Role and problems:** P10 the trade-off (grubs eaten, corn pulled), children's work, P1 rook pie in May.

**Behaviour spec:** B1 nest in the same trees; B2 follow the plough and work pasture for grubs (lowering the grub loads: leatherjackets,
wireworm when built); B3 pull sown and sprouting corn beside the rookery (a watch, a child with a clapper turns them, P3); B4 young taken
as they branch.

### 4.16 Beaver (deep; an engineer; rare)
**From:** wildlife.md (fells trees, dams, ponds, fur and castoreum, the open-access extinction); wild_systems.md (the pond holds water and
fish, flooded trees die, the meadow floods, trapping empties a slow breeder for good).

**Built:** a lodge with a dam that floods the meadow and raises the fish; breaking it; rebuilding; trapping out for good.

**Role and problems:** P10 the trade-off (fish, fowl and a summer's water against the hay meadow), P6 trapping out for good, land that
changes.

**Behaviour spec:** B1 a family (a pair and young of two years) on a slow brook with willow and aspen; B2 felling trees by the water
(young growth and timber drawn); B3 the dam and pond: the pond holds water through a dry summer and cuts floods, holds more fish and
fowl, floods the meadow beside it; drowned trees become standing deadwood; B4 a broken dam is rebuilt within days while the family
lives; B5 slow breeding (two or three kits a year, the young leaving at two): trapped hard, the family ends for good.

### 4.17 Wild bees (deep; specced in wildlife.md, not built)
**From:** wildlife.md (colonies in hollow old trees; honey and wax; honey-gathering as a knack); wild_systems.md (swarms in May and June;
the flow; wasps rob weak hives; the bear at the hives).

**Role and problems:** P2 finding the tree (lining the bees home), P1 swarms and the flow, P8 wasps and the bear, P5 taking all the honey
kills the colony.

**Behaviour spec (for wave 2's husbandry link):** B1 colonies in old trees; B2 swarms in May and June found and taken; B3 honey by the
flowers' year (the warm spring); B4 taking all the honey kills a colony over winter; B5 robbed by wasps in a wasp year, raided by a bear.

### 4.18 The smaller loads (slugs, aphids and ladybirds), diseases, plants and markers
These are built as general rules and are mostly sound as designed:
- **slugs:** P1 timing (the first rain after dry, the young crop's window), with a lever (picking at dusk, burning the stubble);
- **aphids and ladybirds:** P11 the misread (the ladybird's grub killed as a pest prolongs it), a lag of a week;
- **diseases:** spread by contact and shared grass; the lever is keeping apart (P7 when herds share a common);
- **plants:** pulses and seasons; restraint where they are shared with the wild kinds (D2-202);
- **markers:** lore that holds and lore that fails (P11).

**Changes:** none of behaviour; their modules are the existing rules.

### 4.19 Specced in wildlife.md, not yet designed here
Salmon (the upstream run and the weir, like the eel's B2 with the run upstream), trout (resident, steady), otter (a rival at the weir),
pine marten (a fur), falcon (an eyass taken and trained, D2-196's hawks), swan (a claimed bird, D2-194). Each needs its spec when its
economy (furs, falconry, rights) arrives.

## 5. The web between kinds (consequences that travel)

| Chain | Mechanism (behaviour rows) | Lag | What people can learn |
|---|---|---|---|
| hunt out the deer → wolves at the herds | wolf B2, B3; deer B5, B6 | a season | restraint with the deer protects the herds (P8) |
| a heavy mast → more boar next year → more raids the year after if the mast fails | boar B2, B7 | one to two years | read the oaks two years ahead (P9) |
| a heavy mast → pigeons and boar in the woods, the fields quiet; a failure → pigeons on the winter corn, boar out | boar B2, pigeon B1 | the same autumn | watch the corn in a failed mast year |
| the vole phase → owls and foxes breed → the crash → foxes at the hens | voles B1-B3, fox B2 | a year | shut the hens hard in the crash year |
| a poor autumn → a thin bear → calves and hives in spring | bear B1, B2 | a season | guard the calves after a bare autumn |
| wolves kill → ravens gather → a fox and a bear come to the carrion | wolf B8, raven B1 | a day | ravens show the pack |
| beaver dam → more fish and fowl, a flooded meadow | beaver B3 | a season | the dam's trade-off |
| heronry and otters → fewer fish at the weir | heronry B4 | a season | (a rival, and the size shows the fish) |
| rooks eat the grubs → less root damage, but pull the corn | rookery B2, B3 | a season | where to scare them, where to leave them |
| felling a wood → the deer and boar move; less mast; the bear's den lost | deer B5, boar B1, bear B1 | a season to years | the land changes the animals |
| shared commons → murrain through the herds | diseases | days | keep the herds apart in an outbreak |
| a long freeze → fowl weak and many → over-taken → fewer next winter | wildfowl B1, B3 | a year | restraint (P5) |
| the first rain after dry → the eel run, slugs out, mushrooms later | eel B1, slugs, fungi | days to weeks | one weather sign, three answers |

## 6. Diversity: the learning problems by kind

| Kind | Main problems | Secondary |
|---|---|---|
| boar | P3 varying, P2 the gap, P12 learns your nights | P9 the mast, P14 danger, P7 the crew |
| red deer | P5 restraint (hinds), P1 the rut and winter | P15 the hunted wood, P10 coppice, rights |
| roe | P15 patches emptied and refilled | P11 the summer rut misread |
| wolf | P8 deer to herds, P7 drive or bounty | P4 the fold, P11 the track, P16 ravens |
| fox | P4 shut and keep shut | P1 spring provisioning, P8 voles, timing of control |
| bear | P9 the autumn foretells the spring | P14 danger, rarity |
| hare | P2 the runs | P15 snared out and refilled |
| woodpigeon | P8 the mast to the winter corn | P3 scarecrows wear off |
| rats and mice | P10 how a store is built | P1 the harvest in, a misread (the door) |
| voles and owls | P9 the cycle (lore) | P8 the crash to the hens |
| raven | P16 information | |
| wildfowl | P1 the freeze, P2 flight lines | P5 restraint |
| eel | P1 the eel night, P13 reading the leads | P7 the weir crew, rights |
| heronry | P6 no way back | P5, P16 |
| rookery | P10 trade-off | P3 |
| beaver | P10 trade-off, P6 no way back | land change |
| bees (later) | P2 finding the tree | P1, P5 |
| slugs, aphids | P1 timing, P11 the misread | |

**Gaps:** P12 (an adversary that learns your pattern) only in the boar; it could also be the fox (testing the door on different nights)
and the wolf (the unwatched nights), cheaply, from the same memory block. P7 (many hands) waits on work by several (D4-103 mechanism
1), which exists as the crew bonus only.

**Overlaps removed by this design:** red deer no longer copy the boar (they graze and browse, and teach restraint); roe no longer copy
red deer (patches); the fox stops being a probability at the hens and becomes a pair with an earth.

## 7. What changes in what is built
- The group state machine, conditions, targets and pressure become shared blocks; each deep kind gets a module: boar, red deer, roe,
  wolf, fox, bear first; then hare, pigeon, wildfowl, eel; the sites (heronry, rookery, lodge) move into a `colonies` and an `engineer`
  module.
- Signs that claim what nothing does are removed until the behaviour exists (the old sow "knows the gap"; the wolves' leader "takes the
  herds"); the expert readings are rewritten from the modules' state.
- The immediate fixes: a denned bear cannot be met (bear B1); the readings above cut.
- Each B row gets its test, and a kind is done when its tests pass.

## 8. Steps
1. **Zach checks these behaviour specs** (this proposal), kind by kind: keep, change, cut.
2. The animal interface and the shared blocks (position, value, memory, habituation by kind of scare, make-up, calendar), with the
   guard tests.
3. The deep kinds' modules in order: boar, wolf with red deer (they are one chain), bear, fox, roe.
4. A run on two generated worlds with the pack on and off (the null arm), and the expert and lay readers, to see whether the patterns
   are learned.
5. The middling and simple kinds; then the kinds waiting on husbandry, hounds and rights.

## Alternatives considered
- **Keep one general machine and add parameters** (the current build): it cannot express denning, patches, herd make-up, prey-following
  or emergent routes without becoming a module system by another name, and it flattened the kinds.
- **A module per kind with free access to the world:** quickest, but breaks replay, signs and the separation of concerns; the interface
  costs little and is how agents already work.
- **Emergent behaviour from one learning agent per animal group** (a small policy each): rich, but unpredictable, expensive and hard to
  calibrate; the rules here keep each behaviour testable.

## Open questions (for Zach)
1. **Red deer:** move them from crop raiders to edge grazers and coppice browsers, with restraint (sparing hinds) as their main lesson?
2. **Boar damage:** aim at real levels (a few percent near woods, a bad local year at a tenth or more) rather than the deep dive's 22%?
3. **The wolves' circuit:** a pack's territory spanning several villages (so one village's deer-hunting brings wolves to its
   neighbours' herds too)?
4. **Learning animals (P12):** boar, fox and wolves learning which nights are watched: wanted, or too adversarial?
5. **Den-hunting wolf pups and digging out foxes:** keep as levers (historically real, effective, cruel)?
6. **The vole phase as a clock:** acceptable, given that the mechanics matter more than realistic dynamics?
7. **Black rat:** name the house rat as the black rat for the era?
8. **Order of building:** boar, then wolves with red deer, then the bear, the fox and roe?

## History
- 10 Nov: written at Zach's request after the audit (02zq) showed most kinds' behaviour to be settings of one machine and much of the
  catalogue present only as signs. D2-203 recorded (modules per kind, through the animal interface). The behaviour specs are for Zach to
  check first.

## Sources
- proposals: wildlife.md (§1, §4, §8-§12), wild_systems.md (§4-§10, §12), node_ecology.md, living_populations.md, wild_layer.md,
  wild_plants.md; the audit `docs/review/37_growth/02zq_wild_audit.md`; the deep dive `02zp_ecosystems_deep_dive.md` (§23-§25).
- decisions D2-192 to D2-203.
- natural history as summarised in wild_systems.md §12 and 02zp's sources (mast and pannage; vole cycles and their predators; the
  silver eel run; heronry censuses and hard winters; wolf predation on livestock when wild prey is scarce; boar damage to crops and
  grassland; red deer herd structure and the rut; roe territoriality and the summer rut with delayed implantation; brown bear denning
  and autumn hyperphagia; fox territories, cubs and surplus killing).
