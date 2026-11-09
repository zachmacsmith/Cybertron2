# Proposal: wild behaviour, kinds composed of facets, each a module of its own

**Status:** partly accepted: D2-203 (each kind's behaviour designed first, then built as modules of its own that act only through the
animal interface and the engine's primitives; replaces "no kind has code of its own"). The facets (§3) and the kinds' designs (§4)
are in **discussion (9 Nov), for Zach to check before anything is built**, and **superseded in part** by the outside review (docs/review/37_growth/02zr to 02zv): the facets become views over each kind's constitution, behaviour is written on the day's clock, people's responses are general methods (proposals/methods_and_encounters.md), nothing social is built in; a v3 will follow Zach's decisions on 02zv §6. Until then, read 02zv for what holds. **Owner:** 37.2 (design; the `ecology` branch, D2-199).

**Affects:**
- proposals: wild_layer.md (the system this sits on), wild_systems.md (the catalogue it revises), wildlife.md (the kinds and their
  economy), husbandry.md (where taming leads), node_ecology.md, living_populations.md, wild_plants.md;
- code on the `ecology` branch: `cybertron2/wild/` (a `behaviour/` package of facet modules, the animal interface), `engine/wild.py`;
- spec/information/signs.md (signs from behaviour); spec/conflict/ (danger, the watch); rights (D2-194).

**Builds on:** the audit of what was built (`docs/review/37_growth/02zq_wild_audit.md`): most kinds' behaviour was settings of one
group machine, and much of the catalogue was present only as signs.

## Summary

Zach, 9 Nov:
- "Animals can add specific mechanisms / code but it should just be cleanly modular so they are easily acting within the broader
  system and only through the normal ways of acting with the world through the engine";
- "Not all animals are about types of scares. They should fundamentally different types of behaviors. Like maybe some you just find
  if out searching etc. I don't think they should just be varying five dials but should be multivariate, constitutionally
  different some of them";
- "could not animals be multiple versions of these combinations, eh something you have to seek but can also domesticate";
- "Go through and redesign all of them trying to think of what behavior is most interesting according to our criteria."

Earlier, 8 Nov: "These mechanics etc. are more important than realistic population dynamics."

The design in brief:
1. **A facet is one way people and a kind can meet** (a quarry you seek, a raider at your door, a run that passes, a site you
   steward, something you take and tame, ...). Each facet is a module with **its own core mechanism**, not a setting of a shared
   one (§3).
2. **A kind is a composition of facets**, as many as fit it, all sharing the kind's one state (position, condition, memory,
   make-up), so what happens in one shows in the others: a hunted sounder raids warier; a captured piglet is a sow fewer in the wood.
3. **Transitions** move animals between facets and out of the wild: wild to kept (taming), kept to feral, a site to gone, an ordinary
   beast to a legend (§3.14). They are where the wild joins husbandry, the economy, rights and stories.
4. **Each kind is redesigned** for the behaviour that is most interesting by the criteria (§1): what people must learn, what it
   connects to, what decisions it makes, what it does to the society. Behaviour that teaches nothing new is cut (§4).

## 1. What the wildlife are for, and what makes a behaviour interesting

### 1.1 The purposes (wildlife.md §1; node_ecology.md; wild_systems.md §1-2)
A world that holds hidden, changing state; a land that is a threat as much as a food; regularities learnable at several depths;
dependence and specialisation; commons, rights and restraint; danger and collective action; land that changes and is changed;
consequences that travel between kinds, villages and seasons.

### 1.2 The tests a behaviour must pass
1. **A mechanism with state**, not a multiplier and not a sign alone.
2. **A pattern people can come to expect**, inside a run where possible (wild_systems.md §8: fast and short arms), with slow arms
   carried by lore and history.
3. **A sign and a lever**, and an outcome that differs by what people do.
4. **A learning problem** (§1.3) the kind poses in its own way.
5. **It connects** through a shared driver or another kind (§5).
6. **People's acts change it.**
7. **Relevance**: it moves some household's food, work, safety, wealth or standing by about a tenth in some year or choice, or it is
   an informant whose worth is in what it tells.

### 1.3 What makes it interesting (how the behaviours below were chosen)
Beyond passing the tests, a behaviour was chosen over another when it:
- **creates a decision with a trade-off** (go now or wait; take all or some; guard this or that; spend a child's day scaring rooks
  or weeding);
- **rewards learning at more than one depth** (anyone sees the base rule; the expert reads the condition behind it);
- **involves other people** (a crew, a right, a theft, a neighbour downstream, a quarrel, a gift, a feast);
- **makes stories and differences** between villages and between runs (one village has a boar problem, another a heronry and a weir);
- **is legible**: it shows through signs a person can learn to read.

### 1.4 The learning problems
| # | Problem | | # | Problem |
|---|---|---|---|---|
| P1 | timing: which nights, which weeks | | P9 | a season foretells the next |
| P2 | place: the gap, the run, the lie, the flight line | | P10 | a trade-off: it helps and harms |
| P3 | varying the answer (it gets used to a scare) | | P11 | a misread: the obvious reading is wrong |
| P4 | keeping it up (scared off, comes back) | | P12 | an adversary that learns your pattern |
| P5 | restraint: less now, more later | | P13 | reading its state: few or many, fat or lean |
| P6 | no way back | | P14 | when not to go near |
| P7 | many hands | | P15 | emptied and refilled |
| P8 | a consequence through another kind, with a lag | | P16 | reading others through it |
| P17 | patience and craft over weeks (taming, training) | | P18 | property in a wild thing (marks, claims, theft) |

## 2. Where the current designs came from
| Source | What it gave | What was lost or bent |
|---|---|---|
| wildlife.md (8 Nov; D2-192 to D2-196) | the kinds by habitat and use; how each is taken; goods; rights; hounds; §12 "no kind needs code of its own" | the economy half mostly unbuilt; §12 flattened behaviour (replaced: D2-203) |
| living_populations.md (8 Nov) | populations on the land; diet; movement; resolved into animals where someone looks | resolution into animals became condensed groups with no ranging |
| 02zp deep dive | the food web; the readers (reading pays where lore joins signs; for boar and fox the depth is in the acts); relevance numbers | "the depth is in the acts" not carried into the build |
| node_ecology.md (8 Nov) | design from the village outward; land as threat; the 10% test | visitors became one state machine |
| wild_systems.md (8 Nov; D2-197, D2-198) | the catalogue: layers L0-L4, archetypes, interconnections, lags, needs | prose, not mechanisms with tests; §10 "no kind has code" |
| wild_layer.md, the `ecology` branch (9-9 Nov) | the general system and its foundations | kinds reduced to settings of one machine (02zq) |
| this proposal's first version (9 Nov) | behaviour specs per kind | still one skeleton (a raider turned by scares) for most deep kinds; replaced by this version |

## 3. The facets (each a module with its own core mechanism)

All facets of a kind share its state: **position** (a parcel near a village, or an area beyond), **condition** (from the ecology's
food), **memory** (places fed, harmed, disturbed; people's patterns), **make-up** (age and sex, a leader, the young of the year),
and its **calendar** (what it is doing this week of the year). Each facet reads and writes that state through the animal
interface (§3.15), and acts through the engine's primitives.

### 3.1 F1 Quarry you seek: the search game
The animal is somewhere you cannot see; you must find it.
- **The lie.** Each animal or group chooses where it lies by day by its own rules: cover, the wind's direction (lying where the wind
  brings it scent from its back trail), weather, disturbance, time of year (red deer in the wind's lee of thick wood; a hare in a
  form on open ground facing the wind; a sounder in bramble; a roe in its patch).
- **Searching.** A searcher works a place (a parcel) for a time; the place gives **clues** by what passed or lies there and how
  long ago: fresh slots, beds, droppings, fraying, browse, a run; how many clues a searcher reads depends on skill and eye, the
  weather (snow shows everything for a day or two; rain erases), and the ground. A clue can **point**: a fresh trail leads to the
  parcel the animal went to. The searcher (an agent) decides where to go next; following a trail is the next act at the parcel it
  points to.
- **Finding and the approach.** Being on the lie's parcel gives a chance to find it, by skill, cover and the wind: approaching
  downwind finds it unaware; upwind it scents you and goes. Then the take (skill, weapon, crew); a wound sends it away bleeding (a
  trail to follow, and danger for dangerous kinds: F9).
- **Spooked.** A spooked animal moves far (an area away) and is wary for days: the place is spoiled for a while.
- **Knowledge.** A searcher remembers where game lay, in which wind and weather; over a run this becomes a map of good places
  (and lore: "in an east wind the hinds lie in the Hanger").
- **Help.** A hound finds over more ground and holds dangerous game at bay (D2-196); a **drive** sends beaters through cover to
  push game past standers (many hands, P7).
- **Traps and snares (passive gear):** set at places (on runs, at earths, by water), they work overnight and are checked the next
  day; they take what passes, sometimes the wrong thing (a fox in a hare's snare, a neighbour's dog), and can be robbed.

*What it teaches:* place (P2), reading its state (P13), the wind and the weather (P1), patience; and with traps, property and theft
(P18). *Test:* a searcher who follows trails and works downwind finds more than one who searches at random; snow raises finding;
a spooked animal is not found again at that place for days.

### 3.2 F2 Raider at your door
It comes to your fields, stores and ricks by night.
- **Ranging by value** (wild_behaviour's shared block): each night the group goes to the best reachable parcel by food, cover and
  distance, less remembered danger, plus remembered food. Routes and gaps emerge where cover meets fields.
- **Defences** work physically: a fence by its level, a shut door, a watch's light, noise, a person, a dog; each kind answers by the
  scare's kind (D2-198: gets used to it, scared off, leaves for good, none).
- **Memory of people's pattern:** which nights a place was watched; a learner (P12) comes on the others.
*Teaches:* varying the scare (P3), keeping it up (P4), the gap (P2), the watch rhythm (P12). *Test:* the same scare wears off for a
habituating kind; a rotated watch is beaten by a learner; a fence at the gap turns them to the next way in.

### 3.3 F3 Predator of your beasts
It hunts animals, and your beasts are among them.
- **Prey-following:** it hunts its wild prey where they are on its territory (a circuit over nights).
- **Switching:** when its wild prey fail (hunted out, a hard winter, crusted snow), or a kept beast is easy (an unwatched fold, a
  calf apart), it takes kept beasts; a place that fed it brings it back within days.
- **Surplus killing** in an enclosure.
*Teaches:* the consequence through its prey (P8), keeping the fold (P4), restraint with its prey (P5). *Test:* hunting its wild prey
down raises its kills of kept beasts within a season; a watched fold loses far less.

### 3.4 F4 The run or the pulse
It passes a place for a few days, set off by conditions.
- **A flow:** a share of the population moves along the river chain or the flyway on its triggers (dark wet nights with rising
  water after dry weeks; a freeze to the east; warm still evenings), area to area over nights.
- **Gear at points:** a weir, traps, nets on a flight line take a share of what passes; what is taken upstream does not arrive
  downstream.
- **The window:** being there with the gear and a crew on the right night is everything.
*Teaches:* timing (P1), reading the leads (P13), many hands (P7), the commons between villages (P5, rights). *Test:* the run reaches
a downstream point the night after its trigger; a weir upstream lowers the catch below.

### 3.5 F5 The site you steward
A fixed place held for years: a heronry, rookery, bee tree, eyrie, lodge, warren, earth.
- **A stock at a place** that grows, crashes and recovers over years; what is taken from it and what disturbs it in its season.
- **Claims and inheritance:** a site can be claimed, marked, held, passed on, poached (D2-194).
- **Leaving:** troubled at the wrong time it is deserted for years (D2-198).
*Teaches:* restraint (P5), no way back (P6), property in a wild thing (P18). *Test:* a site taken lightly yields every year; taken
heavily it shrinks; troubled in its season it is deserted.

### 3.6 F6 The engineer
It changes the land, which moves other kinds and people's work.
- **Lasting changes to land state:** a dam floods a meadow and makes a pond; rooting turns the turf; browsing stops a wood regrowing.
*Teaches:* the trade-off (P10), the long run. *Test:* the change persists while the cause stays, and reverses slowly when it goes.

### 3.7 F7 The outbreak
It erupts from the weather, area by area; scares mean nothing to it.
- **A load** (wave 3, built): a level by conditions, harm in windows, natural enemies following.
*Teaches:* timing (P1), the misread (P11), cultivation as defence. *Test:* built (wave 3).

### 3.8 F8 The lodger
It lives inside your buildings and stores.
- **Attrition set by structure:** how a store is built (raised floor, stone, a cat, a terrier), what is in it, the season.
*Teaches:* design (P10), the misread (a door does nothing). *Test:* a raised floor or a terrier cuts losses; a door does not.

### 3.9 F9 Danger
It can hurt or kill people.
- **Encounter risk by state and situation:** a sow with young, a boar at bay or wounded, a bear in spring, a stag in the rut, a wolf
  at bay; less with a crew and hounds (D2-193).
*Teaches:* when not to go near (P14). *Test:* the risky meetings are where and when the rows say.

### 3.10 F10 The informant
Its behaviour answers another kind's state, visibly: ravens over a kill, kestrels over voles, a heronry's size and the fish, rooks
on a field and the grubs, swallows low and the rain, jays scolding at a fox. *Teaches:* reading others (P16). *Test:* its sign
appears where and when the other's state is.

### 3.11 F11 Taking and taming
A wild animal taken and made into something kept, over weeks.
- **Capture** of the right animal at the right time (striped piglets in spring; an eyass from the eyrie before it flies; a swarm in
  May; a red deer calf; geese and ducks for decoys).
- **Taming or training** as a process: work over weeks, with skill; failure (it dies, escapes, never takes); the result is a
  **beast of the husbandry entity** (a pig, a tame deer in a park, a hive) or a **trained asset** (a hawk).
*Teaches:* patience and craft (P17); timing of the capture (P1); what to spare (taking the young costs the wild stock). *Test:* a
capture at the wrong time fails; training takes its weeks; a tamed beast is husbandry's from then on.

### 3.12 F12 The legend
A unique individual with a name and a story (D2-195): rumour, prestige, taboo, a feat to kill.
*Teaches:* the social side of the wild. *Test:* built in wave 5 (to be moved onto a kind's shared state).

### 3.13 F13 The calendar-giver
It marks the season by the year's warmth, with lore true and false (built: markers). *Teaches:* the misread (P11).

### 3.14 Transitions
- **Wild to kept** (F11): the animal leaves the wild kind's state and becomes a husbandry beast or an asset.
- **Kept to feral:** beasts that stray or escape join the wild (pigs into the woods, bees swarming off, a hawk lost).
- **Mixing:** kept sows at pannage in a wood with wild boar bear wilder litters (later, with husbandry).
- **Site to gone:** deserted or destroyed (F5).
- **Ordinary to legend:** a beast that survives many hunts, or a famous kill, becomes known (F12).

### 3.15 The animal interface and the engine
As in the first version of this proposal (D2-203): a module perceives only its own state, the land it can reach tonight, what is
physically there (a watch, a dog, people, other kinds' groups), the weather now; and acts only through the engine's primitives
(move, eat, take, kill, den, breed, die, disperse, leave a trace, make a sound, remember), with keyed randomness. People meet
everything through the usual ways: their acts (techniques with places and gear), signs, events. Guards: only modules name kinds;
modules use only the interface; each facet's tests and each kind's tests.

## 4. The kinds, redesigned

For each kind: its **facets**; the **behaviours chosen** (the most interesting by §1.3), each with what it does, what people see, what
they can do, and its test; what is **cut or deferred** and why; and **why this design**.

### 4.1 Wild boar
**Facets:** raider (F2), quarry (F1), danger (F9), engineer (F6), taking and taming (F11), legend (F12).

**Chosen behaviours:**
1. **The learning sounder (F2).** A sounder (sows, their young, led by the matriarch; boars apart except in the rut) ranges by value
   from its lie-up. It finds a field through the cover that touches it, comes back nightly, gets used to one kind of scare in about a
   week, learns which nights a field is watched and comes on the others, and is made wary for longer only by harm (a dog's bite, a
   boar killed). *Lever:* vary the scare's kind, back it with a dog, watch the gap, watch on unpredictable nights, fence the gap.
   *Why:* the deep dive found boar the strongest wild threat and the expert's edge to be in the acts; this is a real contest.
2. **The matriarch's memory.** The routes, the fields and the fears are the matriarch's; kill her and the sounder scatters and loses
   them. *Lever:* the boar hunt aimed at the old sow. *Why:* turns a hunt into a decision about which animal.
3. **The mast's two years (F2, with the mast).** In a mast autumn the sounder stays in the woods; when the mast fails it is out at the
   fields and stores; after a heavy mast more sows farrow and litters are larger, so the next year has many more boar; a failed mast
   after a heavy one is the worst year. *Signs:* catkins, acorns setting, striped piglets. *Why:* the best cross-season arm (P9), and
   lore with real truth.
4. **The boar hunt (F1, F9).** Finding the sounder's lie-up in thick cover by its sign, then a crew with spears and a hound to hold it
   at bay; a wounded boar lies up and charges whoever follows. *Why:* collective action with real risk (P7, P14), and prestige.
5. **Rooting the turf (F6).** On wet pasture and meadow in spring and autumn it turns the turf for grubs; that ground gives little hay
   that year. *Why:* boar damage where there is no corn, and a reason to fence the hay meadow.
6. **Striped piglets (F11).** Piglets caught in spring can be raised as pigs (a cheap start of a herd, with risk from the sow); a
   piglet too young dies. *Why:* a link to husbandry, and a choice in spring between hunting the sow and taking her young.

**Cut or deferred:** frost to the stores stays as the raider's frost rule (simple, real). Swine fever (wave 4) stays. Kept sows mixing
with wild boar waits for husbandry.

### 4.2 Red deer
**Facets:** quarry (F1, primary), site to steward (F5, a herd under rights or a deer park), engineer (F6), danger (F9, a stag at bay),
taking and taming (F11, calves to a park), legend (the white hart).

**Chosen behaviours:**
1. **Stalking (F1).** Hinds and calves in a herd led by an old hind, stags apart; by day they lie in thick cover on the lee of the
   wind; at dusk they come to the edges. A stalker reads slots (age and sex from their size and depth), beds, fraying; works into the
   wind; is winded and loses them if upwind. In the rut the stags roar, a sound that points to them across a wood. In snow they are
   found by their lines. *Why:* the richest search game; the expert's depth is real (wind, slot-reading, where they lie in which
   weather).
2. **The herd as a stock with a make-up (F5).** Taking hinds lowers next year's calves; taking stags does not; a herd hunted of its
   hinds dwindles in two years. Under a right (D2-194) the herd is the lord's; poaching is a crime; the villagers' crops pay for the
   lord's deer. *Why:* restraint (P5) and rights (P18), and a conflict between people, not between people and deer.
3. **The hunted wood (F1).** Hunting moves the herd to the far side or the next wood within days; it drifts back after weeks of quiet;
   a drive keeps it away longer. *Why:* hunting near the fields is a defence, hunting far is a supply: a choice.
4. **The wood that does not regrow (F6).** Where deer are many, coppice and young trees are browsed back: a cut coppice regrows
   slowly unless fenced. *Why:* ties the deer to the woodward's work and to fuel.
5. **Winter (F2 minor, F6).** In snow the herd comes to the ricks and strips bark; in a hard late winter the calves, the old and the
   spent stags die. *Why:* a seasonal arm with a lever (fence the ricks) and a reading (a herd thin in March).
6. **A calf to a park (F11).** A calf found lying hidden in early summer can be raised tame (a park deer later). *Deferred* until parks
   exist.

**Cut:** red deer as raiders of the corn like boar (the first build): they graze edges and young corn a little, but their story is the
stalk, the herd and the woods.

### 4.3 Roe deer
**Facets:** quarry (F1) with patches; engineer (F6, browse).

**Chosen behaviours:**
1. **One to a patch (F1).** Each roe holds a patch of thicket and edge (a buck's territory with a doe or two in summer). A searcher who
   knows the patches knows where roe are; one killed leaves its patch empty until a young roe disperses into it in spring or autumn.
   *Why:* a map to learn, and P15: hunt one patch out and it stays empty; spread the hunt and they last.
2. **Calling the buck in the summer rut.** In July and August a buck comes to a call that imitates a doe (a leaf or a reed): a knack
   that works only then. Red-deer lore looks for a rut in autumn (P11). *Why:* a technique tied to a window and a misread.
3. **The kid in the long grass.** Kids lie hidden in May and June; the mower finds them. *Sign only*, with the doe's distress.

### 4.4 Wolf
**Facets:** predator of beasts (F3, primary), quarry (F1: the den, a drive), danger (F9), informant (F10, through the ravens and its
howls), legend.

**Chosen behaviours:**
1. **A pack on its circuit (F3).** A pack (a pair and their young) holds a territory of deep wood and the land around several villages;
   it travels a circuit, a few areas a night, hunting deer where the herds are. Its howls carry, and their direction tells where it is
   tonight. *Why:* a predator people can track by sound and sign, to know which nights are dangerous where (P1, P2).
2. **Deer first, herds when the deer fail (F3).** It kills the weak deer of its territory; when the deer are hunted out or a hard late
   winter and crusted snow tire them, it comes to the herds; a herd that fed it is visited again within days; an open fold is
   surplus-killed. *Why:* the clearest consequence through another kind (P8), and a reason for villages to hunt the deer with
   restraint or pay in calves.
3. **Dispersers.** In autumn to spring a young wolf travels alone across farmland where no pack lives, takes stock readily, and is
   easy to trap or kill. *Why:* a different problem from a pack: an individual with no territory.
4. **The drive and the bounty (F1, P7).** A pack is taken by a drive of many (beaters and standers) or at the den in spring (the pups);
   a world may pay a bounty in heads. *Why:* collective action against a common threat, with free-riders.
5. **Ravens follow the pack (F10).** Ravens gather at its kills; ravens over the far wood mean a kill there. *Why:* reading one kind
   through another.
**Cut:** the wolf "gathering from far" by a probability (the first build).

### 4.5 Fox
**Facets:** raider (F2: hens), quarry (F1: the earth, hounds), informant (via jays and blackbirds mobbing it), fur in winter.

**Chosen behaviours:**
1. **One fox, one territory, its habits (F2).** A pair holds a territory with an earth; the dog fox hunts it by the same ways at dusk;
   it finds an open hen house and comes back the next night; a shut door turns it, and it **tries the doors on other nights**,
   learning which are left open (P12). Once in, it kills them all. *Why:* the simplest lesson (shut every night), with an adversary
   that finds your lapses.
2. **What it hunts depends on the voles (F2 with F7).** In a vole year it hunts voles and leaves the hens; in the crash it comes for
   them. *Why:* the vole cycle reaches the hen house (P8).
3. **The earth in spring (F1, F5).** In spring the cubs are at the earth; digging it out then ends that year's trouble; a winter cull
   kills foxes whose places are refilled by spring. *Why:* timing of control (P1), against intuition.
4. **The winter pelt.** A fox taken in winter gives a prime pelt (a good for trade when furs have uses).

### 4.6 Brown bear
**Facets:** danger (F9, primary), quarry (F1: a great hunt), raider (F2: hives, calves in spring), a sleeper (its calendar), legend,
taking and taming (F11: a cub trained as a dancing bear, deferred).

**Chosen behaviours:**
1. **The bear's year.** It fattens in autumn on fruit, nuts and mast; dens in late autumn in deep wood or rock; sleeps until spring
   and cannot be met; wakes by its condition (thin wakes early and hungry), a sow with cubs late. *Signs:* claw marks, turned stones,
   the den (an expert's). *Why:* a year legible from the autumn (P9).
2. **The hungry spring (F2).** A bear that went in thin comes to carrion, calves and hives near villages in late spring. *Lever:*
   guard the calves and hives after a bare autumn. *Why:* the autumn's mast and fruit foretell the spring's danger.
3. **Meeting a bear (F9).** A sow with cubs attacks; a wounded bear is deadly; a bear surprised at close range charges. The meeting is
   where and when it ranges (its den and its feeding places by season). *Why:* when not to go (P14).
4. **The great hunt (F1, P7).** Many with spears and hounds; a feat (prestige, a legend if it is one).
5. **Rarity.** Present in few worlds (wildwood, upland), one or two.

### 4.7 Brown hare
**Facets:** quarry (F1 with traps: snares), raider (minor: young crops), taking (the warren: deferred to husbandry, as rabbits).

**Chosen behaviours:**
1. **Forms and runs (F1).** Hares lie by day in forms on open ground and cross hedges and banks by the same runs. A snare on a run
   takes; one set elsewhere seldom does. A practised eye reads the runs. *Why:* a map of places (P2) for the poorest food.
2. **Snares are property (F1).** Snares are set at dusk and checked at dawn; they can be robbed, and sometimes take a fox, a cat or a
   neighbour's dog. *Why:* property and quarrels (P18) from a small act.
3. **Snared out and refilled.** A field snared hard is empty for weeks until hares from around refill it (P15).
4. **Coursing** with a hound (D2-196) on open ground: a sport and a status.

### 4.8 Woodpigeon
**Facets:** raider (F2: flocks), quarry (F1: decoyed, netted).

**Chosen behaviours:**
1. **Flocks follow the food across the land.** In a mast autumn they are in the woods; when it fails, the whole flock comes to the
   young winter corn and the peas and strips patches (P8). They get used to a scarecrow in days; a child moving about lasts longer
   (children's work).
2. **Decoyed (F1).** Shooting or netting over decoys on a field they are using. *Deferred* until gear exists.
**Note:** the dovecote pigeon is a different bird (the rock dove), kept as a lord's privilege: husbandry.

### 4.9 Rook and the rookery
**Facets:** site (F5), raider (F2: seed and sprouting corn), ally (they eat the grubs), informant (F10: rooks working a field show grubs),
quarry (the young: rook pie).

**Chosen behaviours:**
1. **The trade-off.** Rooks follow the plough and work pasture for grubs (leatherjackets, wireworm: lowering those loads), and pull
   sown and sprouting corn near the rookery. A child with a clapper keeps them off a sown field for the days that matter. *Why:* a
   real trade-off (P10) and children's work.
2. **The rookery.** Nests in the same trees for generations; young taken as they branch in May; shooting the old birds empties it.

### 4.10 Raven
**Facets:** informant (F10).
1. **Ravens to carrion and to the wolves.** They gather over a carcass within a day and follow the packs. *Why:* the purest information
   kind; worth having because wolves and kills are worth knowing.

### 4.11 Voles and mice, owls and kestrels
**Facets:** outbreak (F7, the cycle), lodger (F8: mice in the stores), informant (F10: owls and kestrels), site (F5: a barn owl's barn).

**Chosen behaviours:**
1. **The vole years** (built: the phase clock, three to four years, sevenfold). *Why:* a multi-year pattern carried by lore and elders.
2. **Kestrels and owls follow them.** Kestrels hang over every field in a vole year; owls breed well and then fall silent in the crash.
3. **The barn owl in the barn (F5).** A barn owl nesting in a barn keeps the mice of that barn down; it leaves if the barn is disturbed in
   spring. *Why:* an ally you steward, cheaper than a cat (P10).
4. **The crash reaches the hens** through the fox (§4.5).

### 4.12 Rats and mice in the stores
**Facets:** lodger (F8).
1. **To the barns after the harvest; held by how stores are built.** A raised granary floor, stone, a cat or a terrier cut losses; a
   door does nothing (the misread run 6 showed). In the era the rat of the houses is the black rat, in thatch and roofs. *Why:* design
   as defence.

### 4.13 Wildfowl
**Facets:** run (F4: pushed in by freezes), quarry (F1: flight lines, nets), taking (F11: geese and decoy ducks, deferred).

**Chosen behaviours:**
1. **Pushed in by the cold.** Flocks come in autumn and many more within days of a freeze to the east; ahead of a freeze, plovers and
   redwings fly west all day (a lead the climate gives). *Why:* a run read from the weather (P1, P13).
2. **Flight lines.** At dawn and dusk they fly the same lines between water and feeding; nets on a line, worked by several, take far
   more. *Why:* place (P2) and many hands (P7).
3. **Weak in a long freeze, and the next winter.** A week into a freeze they come tame; many taken then means fewer next winter (they
   return by how many left). *Why:* restraint (P5) against an easy harvest.

### 4.14 Eel
**Facets:** run (F4: the silver eels), quarry (F1: spearing in the mud in winter), site (F5: a weir as a held right).

**Chosen behaviours:**
1. **The silver run.** In autumn a share of the eels turns silver and runs downstream on dark, wet nights with the water rising; a dry
   autumn holds them, so the first heavy rain after dry weeks brings a great run. The run passes down the river chain over nights.
   *Why:* the eel night (P1) read from the weather; the deep dive's strongest case of reading paying.
2. **The weir and the river below.** A weir (a work by many, a held right) takes a share of what passes; a village downstream gets
   what the weir leaves. *Why:* the commons between villages (P5, rights), Domesday's eel rents.
3. **Spearing in winter.** Resident eels lie in the mud of pools and dykes; a spear probing the mud finds them (a search, F1). *Why:* a
   winter food for the fen.

### 4.15 Salmon (wildlife.md wave 1; not yet built)
**Facets:** run (F4, upstream), site (the weir), quarry (the pools).
1. **Up on the spate.** After autumn rain they run upstream; low warm water holds them in the pools below; cold stops them.
2. **The weir and the spawning upstream.** A weir below takes the run; what passes spawns upstream, and a run fished out below is a
   poor run in later years (Magna Carta's weirs). *Why:* the strongest commons between villages (upstream against downstream) with a
   lag of years.
**Recommendation:** build with the eel's run module, since it is the same facet run the other way.

### 4.16 Trout
**Facets:** quarry (F1: resident, tickled by hand or taken by rod). **Chosen:** each pool holds its fish; tickling is a knack; a pool
fished out refills slowly (P15). Simple, a steady small catch.

### 4.17 Otter (deferred)
**Facets:** raider (F2: fish at the weir and the fishpond), quarry (F1: hunted with hounds; fur). A rival at the weir; a fur.

### 4.18 Heron and the heronry
**Facets:** site (F5), informant (F10: its size shows the fish), quarry (the young: a lord's feast), raider (fish at the weir).
1. **The heronry** (built): same trees for generations; a hard winter halves it and it recovers over years; troubled at the nests in
   spring it is deserted for years. **2. The young taken** as a feast (a right). **3. Its size shows the fish** (to an expert).
*Why:* restraint and no way back (P5, P6), and a lord's claim.

### 4.19 Beaver
**Facets:** engineer (F6, primary), site (F5: the lodge), quarry (F1: trapping for pelt and castoreum).
1. **The dam's trade-off** (built): the pond holds water in a dry summer, cuts floods, holds fish and fowl; floods the meadow; drowned
   trees become deadwood; broken, it is rebuilt within days while the family lives. **2. Slow to breed:** trapped out, gone for good
   (P6). *Why:* the clearest trade-off on land, and the classic open-access extinction.

### 4.20 Wild bees
**Facets:** site (F5: the bee tree) found by search (F1: lining the bees home), run (F4: swarms in May and June), taking and taming
(F11: a swarm into a skep), raided (by a bear, by wasps).

**Chosen behaviours:**
1. **Lining the bees home (F1).** Bees working flowers fly straight home; a hunter who watches their line from two places finds the
   tree where the lines cross. *Why:* a search procedure unlike any other (a skill, a knack).
2. **The bee tree as property (F5, P18).** A found tree is marked as someone's; its honey and wax taken in late summer; taking all of it
   kills the colony over winter (P5).
3. **The swarm (F4, F11).** In May and June a strong colony swarms; a swarm taken into a skep is a hive (husbandry); "a swarm in May"
   is worth more than one in July (lore with truth: the flow left).
4. **Raided** by a hungry bear in spring and by wasps in a wasp year.
**Recommendation:** wave 2 with husbandry, as wildlife.md planned.

### 4.21 Pine marten (deferred)
**Facets:** quarry (F1: traplines in old wood cores; winter fur). Rare, a fine fur; waits for furs to have uses.

### 4.22 Falcon
**Facets:** site (F5: the eyrie, used for generations), taking and training (F11: an eyass taken before it flies, then months of
manning and training), quarry for the hawk (fowl, hares).
1. **The eyass and its training.** Taken at the right age; trained over weeks with skill; the result is a hawk that takes fowl and
   hares with its keeper; it can be lost. *Why:* patience and craft (P17), prestige, rights (the lord's hawks).
**Recommendation:** with D2-196's hawks (wave 3).

### 4.23 Swan
**Facets:** site (F5: a pair's water), property (P18: marked on the beak by its owner), quarry (easy).
1. **Marking.** Swans are owned by marks cut on the beak; the year's cygnets are marked at a gathering; an unmarked swan is the
   lord's. *Why:* property in a wild thing, made visible; a social institution from a bird. *Deferred* with rights.

### 4.24 The loads, diseases, plants, markers (built)
Their facets are the outbreak (slugs, aphids and ladybirds), the calendar-giver (markers), the site and the pulse (plants, the
mast, fungi), and disease (wave 4). Kept as built.

## 5. The web between kinds (consequences that travel)

| Chain | Through | Lag |
|---|---|---|
| hunt out the deer → wolves at the herds | wolf 2; red deer 2 | a season |
| a heavy mast → more boar next year → a failed mast after it: the worst year | boar 3 | one to two years |
| a failed mast → pigeons on the winter corn, boar at the fields, mice in the stores | boar 3, pigeon 1, mice | weeks |
| the vole crash → foxes and owls at the hens and nests | voles 1-2, fox 2 | a year |
| a bare autumn → a thin bear → calves and hives in spring | bear 1-2 | a season |
| a wolf kill → ravens → a fox and a bear at the carrion | raven 1, wolf 5 | a day |
| a beaver dam → fish and fowl up, the meadow flooded | beaver 1 | a season |
| a weir upstream → less below (eels this year; salmon in later years) | eel 2, salmon 2 | nights; years |
| rooks eat the grubs → less root damage; they pull the corn | rook 1 | a season |
| deer browse → the coppice does not regrow → less fuel | red deer 4 | years |
| felling a wood → deer, boar and the bear move; less mast | the ranging and the sites | a season to years |
| a long freeze → fowl many and weak → over-taken → fewer next winter | wildfowl 3 | a year |
| the first rain after dry weeks → the eel run, slugs out, mushrooms later | eel 1, slugs, fungi | days to weeks |
| a barn owl in the barn → fewer mice in that barn | owls 3 | a season |

## 6. Diversity

**Facets by kind:**

| Kind | F1 quarry | F2 raider | F3 predator | F4 run | F5 site | F6 engineer | F8 lodger | F9 danger | F10 informant | F11 take/tame | F12 legend |
|---|---|---|---|---|---|---|---|---|---|---|---|
| wild boar | x | **x** | | | | x | | x | | x | x |
| red deer | **x** | (x) | | | x | x | | x | | x | x |
| roe | **x** | | | | | x | | | | | |
| wolf | x | | **x** | | | | | x | x | | x |
| fox | x | **x** | | | x | | | | | | |
| bear | x | x | | | | | | **x** | | (x) | x |
| hare | **x** | (x) | | | | | | | | (x) | |
| woodpigeon | x | **x** | | | | | | | | | |
| rook | x | x | | | **x** | | | | x | | |
| raven | | | | | | | | | **x** | | |
| voles, owls | | | | | x | | x | | **x** | | |
| rats, mice | | | | | | | **x** | | | | |
| wildfowl | x | | | **x** | | | | | | (x) | |
| eel | x | | | **x** | x | | | | | | |
| salmon | x | | | **x** | x | | | | | | |
| heron | x | (x) | | | **x** | | | | x | | |
| beaver | x | | | | x | **x** | | | | | |
| wild bees | **x** | | | x | x | | | | | x | |
| falcon | | | | | x | | | | | **x** | |
| swan | (x) | | | | **x** | | | | | | |

(bold: the kind's main facet; (x): minor or deferred)

**The learning problems are now spread:** the search game (P2, P13) belongs mainly to deer, roe, hare and bees; varying the scare (P3)
and the learning adversary (P12) to the boar, the fox and the pigeon; the consequence through another kind (P8) to the wolf, the
pigeon and the fox; the season's foretelling (P9) to the boar and the bear; the run (P1, P7) to the eel, salmon and fowl; restraint
and no way back (P5, P6) to the deer herd, the heronry, the beaver, the bees and the fowl; property (P18) to snares, the bee tree,
the weir and the swan; patience and craft (P17) to the falcon, the bees and the piglets.

**What the first build taught nobody:** red deer as raiders; roe as small red deer; the wolf as a probability at the herds; the hare,
pigeon and eel with nothing of their own. Each now has a distinct facet and problem.

## 7. What changes in what is built
- The shared blocks become: the shared state (position, condition, memory, make-up, calendar), ranging by value, habituation by the
  scare's kind, and the facets' modules: F1 search game (new, the biggest), F2 raider (from the group machine), F3 predator (new:
  prey-following and switching), F4 run (new: flows on the river chain and flyway), F5 site (from wave 5's sites), F6 engineer, F7
  outbreak (the loads), F8 lodger (from the store bridge), F9 danger, F10 informant, F11 taking and taming (new, needs the husbandry
  entity), F12 legend, F13 calendar.
- **Hunting** for quarry kinds becomes the search game in place of the draw by density; traps and snares as gear left at places.
- **Immediate fixes:** a denned bear cannot be met; the readings that claim behaviour nothing implements are cut until their behaviour
  exists.

## 8. Steps
1. **Zach checks the facets and the kinds' designs** (this proposal).
2. The shared state and the interface, with the guard tests; F1 (the search game) and F2 (the raider with ranging and memory).
3. Red deer (the search game, the herd), boar (the learning sounder, the mast's two years, the hunt), wolf (F3 with the deer).
4. A run on generated worlds with the pack on and off.
5. The runs (F4: eels, fowl, then salmon); the bear's year; the fox; roe; hare; pigeon; rook.
6. F11 and the kinds waiting on husbandry, hounds, hawks, rights and furs (bees, falcon, swan, marten, otter).

## Open questions (for Zach)
1. **The facets** (§3): the right set? Anything missing (for example the animal as a companion, or as a sacred or taboo thing)?
2. **The search game** (F1): agents choosing where to look and following trails, with the wind deciding the approach. Is this the
   level of detail wanted, or should a hunt stay one act with the search inside it?
3. **Red deer** as quarry, herd and woods (not corn raiders); **roe** as patches.
4. **The learning adversary** (P12): the boar and the fox learning which nights and doors are watched or left open?
5. **Taming** (F11): piglets to pigs, swarms to skeps, eyasses to hawks, calves to a park, in the order husbandry allows?
6. **Property in wild things** (P18): snares that can be robbed, marked bee trees, swans marked on the beak, weirs held as rights?
7. **Cruel but real levers:** digging out a fox earth with cubs, killing wolf pups at the den. Keep?
8. **Order:** the search game and the raider first, with red deer, boar and wolf?

## History
- 9 Nov: written at Zach's request after the audit (02zq) showed most kinds' behaviour to be settings of one machine and much of the
  catalogue present only as signs. D2-203 recorded (modules per kind, through the animal interface).
- 9 Nov (later): rewritten after Zach's points that kinds should be "constitutionally different", not dials, and can combine several
  ways of being met ("something you have to seek but can also domesticate"). The first version still gave most deep kinds one
  skeleton (a raider turned by scares). Now: thirteen facets with their own core mechanisms (§3), transitions between wild, kept,
  feral and legend (§3.14), and every specced kind redesigned for its most interesting behaviour by the criteria (§1.3, §4), with
  what was cut and why.

## Sources
- proposals: wildlife.md (§1-§12), wild_systems.md (§4-§10, §12), node_ecology.md, living_populations.md, wild_layer.md,
  wild_plants.md, husbandry.md; the audit `docs/review/37_growth/02zq_wild_audit.md`; the deep dive `02zp_ecosystems_deep_dive.md`
  (§23-§25).
- decisions D2-192 to D2-203.
- natural history as summarised in wild_systems.md §12 and 02zp's sources, and well-established practice: mast cycles and pannage;
  vole cycles and their predators; the silver eel run and eel weirs; salmon runs and weirs (Magna Carta clause 33); heronry censuses
  and hard winters; wolf predation on livestock when wild prey is scarce; boar damage to crops and grassland; red deer herd structure,
  the rut and stalking into the wind; roe territories, the summer rut and calling the buck; brown bear denning and autumn feeding;
  fox territories, cubs and surplus killing; hare forms and runs; bee-lining and skeps; falconry's eyasses; swan-marking.
- 9 Nov: superseded in part by the outside review (02zr critique, 02zs development, 02zt dependences, 02zu chains, capital, actions and decay, 02zv consolidation) and Zach's principles (nothing social forced; general methods, not one action per animal; no attention filtering; a day is a day for acts; places in memory). Status line updated; v3 to follow his decisions on 02zv §6.
