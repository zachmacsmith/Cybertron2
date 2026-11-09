# 02zr: wild behaviour, an outside critique (9 Nov)

> **Superseded in part (9 Nov):** consolidated in [02zv_wild_consolidation.md](02zv_wild_consolidation.md), whose ledger places every item here in a pack, a deferral or a proposed cut; where they differ, 02zv holds, and the build brief for the first stage is [proposals/methods_and_encounters.md](../../cybertron2/proposals/methods_and_encounters.md). Withdrawn readings are listed in 02zv §3.9 (among them: real-day conversions of acts, the attention budget, institutions written into the wildlife).

An independent critique of `docs/cybertron2/proposals/wild_behaviour.md` (the 13 facets, the transitions, the kinds redesigned), read
with the audit (`02zq_wild_audit.md`), the catalogue (`wild_systems.md`), the kinds and their economy (`wildlife.md`), the system as
built (`wild_layer.md`, the `ecology` branch), the deep dive's prototype and LLM tests (`02zp` §23-§31), the senses guide, the
scenario design rules and the purpose brief (`02zr_wild_purpose_brief.md`). It is a session note: it proposes, it decides nothing.
Nothing here is in the spec. Where it recommends a change to the proposal, the change belongs to 37.2 to take or leave, and to Zach
to decide.

**How to read it.** §0 gives the findings in one page. §1 critiques the framing and proposes a replacement. §2 surveys games,
models and real practice for lessons that transfer. §3 goes through every mechanism of the proposal, §4 every kind. §5 proposes new
kinds of mechanism. §6 proposes 39 new kinds and composite systems and ranks them. §7 maps everything onto the purposes in the
brief. §8 gives the recommendations: what to change, what to build first, what to stop doing. Sources are at the end.

**Time.** Throughout, Y = 32: an engine day is about 11.4 real days, a season 8 engine days, a unit of work a sixth of an engine day
(about 1.9 real days). "A night" in the engine is a stretch of about eleven real nights.

## 0. The findings in brief

1. **The facets are kinds of encounter, not kinds of animal.** They classify how people meet a beast (quarry, raider, run, site).
   Within each facet the mechanism is shared, so the boar, the fox, the woodpigeon and the deer at the ricks all run F2, and twelve
   kinds run F1. That is the one-machine problem again at a finer grain. Constitutional difference has to come from what the animal
   *is*: what it senses, how it decides, what it remembers and from whom, how it lives with its own kind, how fast its life runs,
   how it uses space. The encounters should fall out of that. §1.3 proposes a framing of three layers (constitution, encounter,
   social footprint) under one budget.
2. **The behaviours are written in real nights, but the engine runs in stretches of eleven.** "Gets used to a scare in about a
   week", "comes back nightly", "learns which nights a field is watched", "wary for days", "come tame a week into a freeze": each of
   these happens inside one engine night. As written they cannot be built faithfully, and they cannot be learned. Every behaviour
   needs rewriting in engine time (§1.2 b gives a conversion table), and contests at night should be resolved over the stretch
   (§5, M2).
3. **What agents "learn" about real species is mostly recall.** The deep dive showed models reading eel nights from prior knowledge
   and failing to learn a rule that differs between kinds. The learning worth designing is *local and particular*: this wood's lie
   in an east wind, this river's lag after rain, this sounder's gap, this heronry's tolerance, the field that killed cattle forty
   years ago. Real traditional knowledge is mostly of this kind. Each world should hold particulars that no model can know in
   advance (§1.2 c; §5, M15).
4. **The proposal says almost nothing about who comes to need whom.** Its criteria (§1.2-1.3) are about animals and single
   households. The purpose brief and scenario_design make dependence, chokepoints, chains and enforcement the reason the layer
   exists, and the six runs have produced no wild institution. Every kind should name the dependence edge, the thing that can be
   held, and the institution it invites, and every kind should be tested against a null arm at the level of the society (§7).
5. **Deterrence displaces, and the proposal never uses it.** Scaring pigeons sends them to the neighbour's field; a lapse at one
   house brings the fox to the hamlet; a fox killed is replaced from the ring. Externalities are what turn a household's problem
   into a society's problem, and they are cheap to build (§5, M3). Without them, every defence stays private and the watch rota
   never appears.
6. **Cutting red deer as raiders removes the strongest social lever in the whole ecology.** node_ecology.md found the forest-law
   conflict (the lord's deer eat the villagers' crops, and the villagers may not kill them) the sharpest grievance the wild gives.
   The proposal's red deer keeps the rights and drops the damage. Keep a modest raid, and let the law constrain the levers (dogs
   lawed, fences kept low, a fence month), as it did (§4.2).
7. **The flagship kinds live in few worlds.** Boar and red deer were present in 3 of 20 generated villages. The kinds every village
   meets (rats and mice, birds at the corn, the fox at the hens, rabbits, moles, slugs) get the least design. Design weight should
   follow exposure; boar and deer are the frontier's (§4).
8. **Agents' attention is the binding constraint, and nothing in the proposal budgets it.** Twenty-odd kinds, each with sign
   bundles, will flood a 400-token view; the senses guide shows that standing facts and forecasts with no lever are ignored, and the
   runs show the rut, the plovers and the first frost drew no comment. Each kind should declare its expected lines per agent-day and
   its units per household-season, and signs with no lever today should go (§1.2 d).
9. **Several valuable mechanism types are missing:** animals perceiving people by the same noticing rule (wind, sound, sight);
   sentinels and alarm networks that work in both directions; emergent routes; personality and selective harvest; culture within
   groups; animals that remember particular people; commensal niches set by waste and buildings; long projects that are wild
   capital; obligations denominated in wild things; laws that constrain levers; races for a ripening pulse; carcasses with
   stakeholders (§5).
10. **The best new kinds are the ones that make specialists and rights cheaply:** the rabbit and its warren, the cat, the mole and
    its catcher, the duck decoy, the deer park and its leap, corvids that remember faces, the jay as sentinel and planter, poisonous
    lookalikes, the hazel nutting race, stoats and weasels (the small gap), and the cursed field (§6).

## 1. The framing

### 1.1 What the facet framing gets right
- It escapes "five dials". A kind composed of several encounter modes is richer than one machine with settings, and Zach's "something
  you have to seek but can also domesticate" is answered directly (F1 with F11).
- The shared state (position, condition, memory, make-up, calendar) means consequences cross facets: a hunted sounder raids warier;
  a piglet taken is a sow fewer. That cross-talk is the right idea.
- The learning problems (P1-P18) are a good checklist, and spreading them across kinds (§6 of the proposal) is the right instinct.
- The transitions (wild, kept, feral, legend) are where the wild joins husbandry, law and stories, and the proposal names them.
- The "cut" lines for each kind are honest; the proposal admits what the first build taught nobody.

### 1.2 Seven problems with it

**(a) Facets are encounters, so the machine is shared again.** The facet table (proposal §6) has eleven columns, and a facet's
mechanism is written once: F2 is "ranging by value, defences that work physically, memory of people's pattern" for boar, fox,
pigeon, hare, deer in winter, bear in spring, heron at the weir. What makes a boar unlike a woodpigeon at the corn is not which
facets they have (both are F1 and F2) but how each decides where to go and what it learns:
- the sounder decides by a matriarch's remembered map, learns places and harms, and keeps its knowledge in one old animal;
- the woodpigeon flock decides by where other pigeons are already feeding (local enhancement), remembers almost nothing, and is
  steered by its own kind, which is why decoys work and why a scarecrow fails once the flock sees birds feeding near it;
- the fox decides alone on a fixed nightly circuit, probes for lapses, and caches surplus;
- the rat does not decide about people at all: it lives where the structure lets it.

These are four different decision architectures. The proposal's F2 has one. If the facets stay, each facet must be allowed to call
a kind's own decision rule, memory and social machinery; at that point the facets are views, and the real modules are elsewhere.

**(b) The time base.** The proposal writes behaviour at the scale of real nights. The engine's night is about eleven of them, and a
unit of work is about two real days. Most of the specific rules then fall inside one step:

| Behaviour as written | Real time | Engine time (Y = 32) | Consequence |
|---|---|---|---|
| boar "gets used to one kind of scare in about a week" | 7 nights | 0.6 engine night | habituation completes inside the first watched engine night; there is nothing to vary between nights |
| sounder "comes back nightly" | 1 night | 0.09 | an engine night holds about eleven visits; the outcome is a count, not a yes or no |
| "learns which nights a field is watched and comes on the others" (P12) | weeks | a season's raid window is about 5-7 engine nights | at most six samples a year; neither the boar nor an agent can learn a schedule from that |
| a spooked animal "wary for days" | 2-5 nights | under half an engine night | the spoiling lasts the rest of the stretch at most |
| deer "drift back after weeks of quiet" | 3-6 weeks | 2-4 engine days | inside a run: good |
| wildfowl "come tame a week into a freeze" | 7 days | 0.6 engine day | any freeze of an engine day is already the tame phase |
| the eel run "passes down the river chain over nights" | 2-5 nights | under half an engine night | the whole chain fills in one engine night unless the lag is set in engine days (D2-197) |
| a herd "hunted of its hinds dwindles in two years" | 2 years | 64 engine days | beyond every run; lore only |
| fox cubs at the earth, April-June | 10 weeks | about 6 engine days | inside a run: good |
| taming a piglet; training an eyass | weeks; 1-3 months | 1-3; 3-8 engine days | inside a run: good |
| a hunter "follows a trail to the next parcel" as its next act | an hour | a unit is about two real days | a trail is followed to its end inside one act; acts are not steps of a stalk |

Two consequences. First, contests that repeat nightly in real life (watch against raider) should be resolved over the engine night
as a contest between two portfolios: the household's deterrents over the stretch (how many nights watched, with which distinct
scares, with a dog or not) against the group's habits (§5, M2). "Vary the scare" then becomes "have several distinct deterrents
at hand", which is a material requirement (a dog, clappers, firewood, a boy) and so a dependence. Second, behaviour slower than a
season reaches people only as lore, records and the world's seeded history; the proposal should say for each kind which of its
behaviours a run can show and which only the elders can.

**(c) Learning is mostly recall.** The deep dive (02zp §29-30) found models reading the eel night from what they already know, and
failing in two seasons to learn that birds habituate to a scarecrow while hares are scared off by it. LLMs carry the natural
history of every kind the proposal lists. What they cannot carry is the particular: which parcel the hinds lie in under an east
wind, how many engine days this river takes to rise after rain, which hedge gap this sounder uses, whether this heronry deserts at
one disturbance or three, where the cattle that died of the black bane were buried. Real traditional knowledge (Liebenberg's
trackers, the Cree tallyman's map of his territory, a warrener's knowledge of his warren) is mostly of this local, idiographic
kind. Designing learning around particulars has three gains: it cannot be recalled, it differs by world (so lore carried from
another village is miscalibrated, as wild_systems principle 8 wants), and it is exactly what makes a local expert worth more than
a clever newcomer, which is a dependence. The proposal's learning problems mix general rules (P1 timing, P11 misreads) with
particular ones (P2 place); the particular ones should be favoured, and each world should seed **quirks**: particular values that
keep the real direction but vary the magnitude, threshold or place (§5, M15).

**(d) Attention is not budgeted.** An agent's view is small (a Haiku seat's institutional state is about 400 tokens), its units are
few, and it decides once a day. The proposal adds or deepens about 24 kinds, each with sign bundles across four senses. The senses
guide's measure (14,387 lines) is plain: lines that change what to do today are used; standing facts, ambience and forecasts with
no lever are not. The runs confirm it: the rut, plovers before a freeze and the first frost drew no comment; wolf tracks and the
night's bellowing did. The deep dive found models over-watching (work three times the scripted expert's), which is what an agent
does when every sign looks like a threat and nothing tells it the base rate. The proposal needs, per kind:
- expected wild sign lines per agent-day (mean and peak), and a world cap (say three a day on average, six on a peak day, more for
  the specialist who works that kind);
- expected units per household-season to answer it well;
- a rule that a sign with no lever *today* for *this reader* is not shown (the plovers lead a freeze; shown only to someone with a
  fowling net, a rick to cover or beasts to bring in).

**(e) The society is an afterthought.** The proposal's tests (§1.2) are about animals and the single household's outcome. Its
criteria (§1.3) mention "involves other people", but no facet's mechanism produces a dependence. The purpose brief lists nine ways
the wild should enrich a society; the proposal's design touches three of them (danger and collective action through F1 drives and
F9, commons through F4 and F5, status through F12). After six runs no wild institution has appeared. The framing should make the
social footprint a required part of every kind's design, with a null-arm signature (§1.3, layer C; §7).

**(f) The interaction is one-way.** The animal interface lets a module perceive "what is physically there (a watch, a dog,
people)" as a list. Real animals sense people through wind, sound and sight, and people sense animals the same way. The engine
already has one noticing rule (sense x visibility x presence x attention). Running animals' perception of people through the same
rule makes stealth, wind, crew size, dogs, fire and noise matter consistently and teach one lesson across kinds (§5, M1). It is
also the cheapest way to make F1's approach "downwind finds it unaware" real. (The climate has wind speed but no wind direction:
an engine gap to record.)

**(g) There is no structure for the long game.** People's real relation to wild things was built over years: warrens dug and
stocked, decoy ponds cut, deer parks paled, fishponds made, hedges laid, heronries protected, coppice cut in rotation, rights
claimed and defended in court. These are wild capital: built by many hands over many days, paying over years, inherited, and
worth fighting over. The proposal has sites (F5) but nothing for building, holding and inheriting wild capital across continued
runs (§5, M12).

### 1.3 A better framing: three layers under one budget

**Layer A, constitution (what the animal is).** Eight organs. Each has a small set of alternative modules, not dials. A kind chooses
one module per organ (or none), and constitutional difference is a different choice.

| Organ | Alternative modules (each its own code) | Examples |
|---|---|---|
| **A1 senses** | which senses it uses on people and at what range, through the engine's noticing rule: nose on the wind (deer, boar, fox); eyes and movement (pigeon, hare, corvids); ears and alarms of others (deer reading jays); none (rats, slugs, insects) | deer winded upwind; pigeon flock flares at a moving boy, not a still scarecrow |
| **A2 decision rule** | forager by value; habit follower on its own routes; social follower (lands where its kind feeds); central-place forager (from a nest, roost, rookery or den); sit and wait; cue-triggered mover (runs on a threshold); no decision (lives where the structure lets it) | sounder by value with a matriarch's map; pigeons as social followers; eels cue-triggered; rats structural |
| **A3 memory and learning** | none; place memory (fed here, harmed here); association with people's signals (habituation and sensitisation by kind of scare, D2-198); memory of individual people; spatial avoidance of watched gaps | boar: place and harm; crows: individual faces; fox: lapses found |
| **A4 sociality and information** | solitary territorial; pair; matriarchal group (knowledge held by an old individual); fission-fusion flock; colony; with social learning inside the group (culture) or not; with alarm calls others read or not | sounder (matriarch, culture); flock (copy and flee together); heronry (colony); jays (alarm) |
| **A5 individuality** | none (a density); a group as one; named individuals with a bold-shy trait, scars and history | hares as density; the old sow; the legend |
| **A6 life history and tempo** | fast (a season or less: slugs, aphids, voles); middling (a year: foxes, hares, rabbits); slow (years: deer, boar, wolves); very slow (decades: beaver, heronry, pearl mussel); and its clocks (cohorts, cycles, pulses) | what a run can show and what only lore can |
| **A7 space use** | territory with a holder (refills from the ring when emptied); home range with lies; route network with gaps; migration or run along the chain or flyway; site-bound | roe patches; boar routes; eels on the river chain; heronry |
| **A8 body and yield** | danger (when, to whom), goods and their quality by how it was taken, disease carried, what its carcass draws | boar at bay; fox pelt in winter; murrain carcass |

**Layer B, encounters (how people meet it).** The proposal's facets, kept and renamed as views: seek, raid, prey on beasts, run,
site, engineer, outbreak, lodger, danger, informant, take and tame, legend, calendar. An encounter is computed from layer A, not
written per facet. A kind's encounter list should follow from its organs: a central-place forager with a colony has a site; a
cue-triggered mover on the river chain has a run; a social follower at the corn is a raider whose answer to scares is set by its
flock's copying.

**Layer C, social footprint (what it makes in a society).** Required for every kind, in one table row each:
- **dependence edge:** who comes to need whom (the warrener, the decoyman, the hound keeper, the harbourer, the rat-catcher, the weir
  crew, the falconer, the beekeeper, the rope-holder);
- **what can be held:** a right, a site, a structure, a skill, a beast, a record;
- **what can be traded:** goods and their chain, or a service;
- **what must be enforced, and by whom:** a closed season, a lawed dog, a bounty claim, a mark, a close time on a weir;
- **what people can argue about:** damage and who pays, a theft, a claim, a broken custom, a free-rider;
- **what becomes a story:** a feat, a loss, a legend, a place named for it;
- **null-arm signature:** what an observer would see in the state with the pack on that is absent with it off.

**Budget D, cost and time.** Per kind: its fast arm in engine days (at least one within a 12-day run where present); its expected
sign lines per agent-day; its expected units per household-season; its run cost (engine time per night); its presence by world (in
how many of the generated villages it matters).

**How the proposal's facets map onto this.**

| Proposal facet | In this framing |
|---|---|
| F1 quarry | an encounter of A1 senses + A7 lies and routes + A5 individuality; the search is an act with a plan (§3.5) |
| F2 raider | an encounter of A2 decision rule + A3 memory; contest resolved over the stretch (§5, M2) with displacement (M3) |
| F3 predator of beasts | an encounter of A2 (value, prey-switching) + A7 territory with refill |
| F4 run or pulse | A2 cue-triggered mover + A7 chain; with idiographic lags (M15) |
| F5 site | A4 colony or A7 site-bound + A6 slow tempo; with layer C claims |
| F6 engineer | A8 effects on land (a primitive), not a facet |
| F7 outbreak | A6 fast tempo + A2 none; the built loads |
| F8 lodger | A2 structural + M9 commensal niches |
| F9 danger | A8 body, read by state and situation |
| F10 informant | A4 alarm + M7 sentinels; and any kind's traces |
| F11 taking and taming | a transition, with A5 individual bonded to a person (§3.5) |
| F12 legend | A5 individuality + layer C stories; emergent from records (§3.5) |
| F13 calendar | A6 clocks; signs only where they carry a lever |

**Dimensions the facets miss, and where they now live.** Sensory worlds (A1); what an animal notices of people (A1 with M1);
social structure and information transfer (A4); learning and culture (A3, A4, M6); personality and reputation (A5, M5, M8); life
history and time scales (A6, budget D); territories, corridors and refuges (A7, M4); how animals use people's landscapes (A2
structural, M9); mutualisms and commensalisms (M9, M10); signalling and deception (M11); rhythms (A6); what people must do over
years (M12); animals as characters in stories, law and economy (layer C, M13, M14).

## 2. Lessons from other systems and from real practice

For each: what it did, what worked or failed, and the lesson that transfers to an engine whose players are LLM agents acting
through verbs and signs. Bracketed numbers refer to the sources at the end, which are grouped by field.

### 2.1 Games

| System | What it did | What worked, what failed | Lesson, and how it transfers |
|---|---|---|---|
| **Ultima Online's ecology** (1997) | a closed resource loop: creatures spawned from a fixed pool, predators and prey with needs | the popular account is that players killed everything faster than it could respawn; Koster's own account is that player hoarding (sheep killed, wool turned into shirts to grind skill) drained the closed pool, that the system was rewritten by someone who did not understand it, and that much of the team thought it a boondoggle because players could not see it [1] | (1) agents will strip a stock faster and more single-mindedly than designers expect; the substrate must degrade gracefully, not collapse in a night; (2) a simulation nobody can see is wasted and will be cut; (3) a closed loop needs sinks and refills that are themselves legible. For Cybertron: the strip-mining is the commons experiment, so keep it, but give the stock a ring that refills (the reservoir) and signs of depletion before collapse (catch per effort, emptier lies) |
| **Dwarf Fortress** | consistent physical rules produce chains (cats walk through spilled alcohol, lick their paws, get drunk); cats choose their owners rather than being assigned; cats breed until a "catsplosion"; legends mode records every beast's history [2] | the chains delight because each step is plain once seen; the catsplosion shows that unbounded breeding of a commensal swamps everything; legends emerge from records, not scripts | (1) build chains from consistent primitives, and make each link a sign; (2) bound commensal breeding by the structure that feeds it; (3) let an animal choose its people (the cat): a cheap way to make a household's ties to a beast its own; (4) legends should be read from the record of what happened (§3.5 F12) |
| **RimWorld** | each species has a "manhunter chance when harmed" (revenge), shown in the wildlife tab; a whole herd may turn when one does; tamed animals lose training without a handler; wildness sets how hard taming is [3] | one legible number per species makes hunting decisions differ by kind (a hare never turns, a boar sometimes, an elephant often), and players learn it from one bad experience; the herd turning makes a hunt a group decision; training decay creates a dependence on the handler | (1) a few constitutional numbers shown plainly through early experience teach more than many hidden ones; (2) a danger that spreads through a group (the sounder at bay) makes crew size matter; (3) a trained beast that decays without its trainer creates a specialist dependence (hounds, hawks) |
| **Red Dead Redemption 2** | about 200 species; apex predators with routines; scavengers drawn to carcasses; pelt and meat quality set by weapon and shot placement; legendary animals found through clues and maps [4] | the carcass as an attractor (vultures, then predators) makes a kill an event in the land; quality by method makes the right tool for the right animal a skill; legendary animals become journeys | (1) a carcass is an object with stakeholders (§5, M18); (2) the take has a quality, and the quality depends on craft and gear (a hide spoiled by a spear thrust; a hare snared clean), which is a specialisation; (3) a legend is a trail of clues across places |
| **theHunter: Call of the Wild** | each species has need zones (feed, drink, rest) at set times of day; kills raise hunting pressure, which removes zones and moves them elsewhere; wind, noise and scent decide detection; callers work on some species [5] | the map of need zones is learnable and personal; pressure relocating zones teaches restraint and moving on; once a map's schedule is known the game is solved, and players grind | (1) per-world tables of where and when are learnable and engaging, (2) but fixed tables are solved once: let them shift with season, weather and pressure; (3) pressure that moves animals rather than killing the stock is a cheap and legible commons signal |
| **Rain World** | creatures with their own goals living off-screen in abstraction; modular AI modules attached and configured per creature; lizards are individuals that can learn to recognise the player, and feeding one can befriend it; audio driven by the AI's threat state [6][7] | validates D2-203: per-creature modules on a shared interface give constitutional difference; the risk named by its designer is frustration when creatures care for themselves too well | (1) modules per kind on one interface is the right architecture; (2) individual recognition and befriending by provisioning are cheap and strong; (3) make threat state audible (a sign that rises with danger), so the agent can read it |
| **The Long Dark** | wolves with stalk-then-charge states; fear triggers (fire, flares, lights, a brandished weapon); carried raw meat raises their interest [8] | few states with clear tells (the growl, the stalk) let players learn by dying; inconsistent triggers drew complaints | (1) a handful of states with tells beats a hidden score; (2) what a person carries changes what wild things do (meat through wolf country, a blood trail, a hive's honey near a bear) |
| **Monster Hunter: World** | tracking by collecting clues (prints, mucus) that raise a per-species research level until the monster is located; monsters with habits (sleep in the nest, limp when weak, flee to the nest); turf wars between monsters [9] | clue accumulation and per-species expertise are compelling; visible state (limping) makes condition readable | (1) expertise as per-kind accumulated knowledge that unlocks readings matches wild_systems' readings by skill; (2) visible condition (a lean herd in March, a limping boar) is a good sign because it changes the decision |
| **Don't Starve** | koalefants found by following a trail of suspicious dirt piles; hound waves announced by growls that grow louder; befriending some creatures by feeding them [10] | the trail as a sequence of acts works for a human player with a mouse; the escalating warning is a perfect lead sign | (1) a lead that escalates over engine days (rooting nearer; howling nearer) is legible; (2) multi-step trails cost an LLM agent a decision each; fold the trail into one act (§3.5 F1) |
| **Stardew Valley** | each fish has a location, season, weather and time table, and a movement type in the catch (mixed, smooth, sinker, floater, dart); legendary fish once [11] | the tables are learnable and players love filling them; the act itself differs by kind | the engagement is in the act differing by kind, not in the table. In Cybertron the act's parameters (gear, place, time, crew, approach) should differ by kind, so a good fowler is a poor stalker (wildlife.md §5 says this) |
| **Banished** | a hunting cabin draws deer from a radius; foresters | players report cabins emptying in a season or two with no visible reason, and dispute whether overhunting matters [12] | a production building that hides the stock leaves players confused when output falls; show depletion in catch per effort and in signs |
| **Eco** (Strange Loop) | a simulated food web where species can go extinct; data on populations shown in graphs and maps; players pass laws in a government, enforced by the server [13] | the closest system to Cybertron's aim: evidence for laws comes from in-game data; extinction is permanent | (1) give a society instruments (a forester's tally, a count at the weir, the chronicle) so laws about wild things can rest on evidence; (2) unlike Eco, enforcement should need people (scenario_design rule 4), not the server |
| **Creatures** (Grand) | norns with simulated biochemistry and neural-network brains, learning from reward and punishment [14] | deep attachment and real learning; but the minds were opaque and slow, and players could not tell why a norn did anything | individual learning is compelling when its causes are legible; keep animal learning to a few named kinds (habituation, place, faces) with signs |
| **Black & White** (Evans) | a creature that learns from a single slap or stroke, with desires and beliefs of its own [15] | training a beast by feedback is memorable; one-shot learning is hard to make consistent | a trained beast (hound, hawk) whose dispositions reflect who trained it and how: a bond between a person and a beast that others can borrow but not reproduce |
| **Valheim, ARK** | Valheim: tame by feeding and staying near without frightening, with visible progress; ARK: knock out and feed kibble, with imprinting giving the imprinter a bonus [16][17] | Valheim's proximity taming is a gentle, legible process; ARK's is a resource grind; imprinting binds a beast to one person | taming as time, patience and presence, with a bond to a specific person (the falconer's hawk, the warrener's ferret), not a resource sink |
| **Breath of the Wild** | few consistent rules (fire spreads, wind carries, noise scares) apply to every creature and object | multiplicative play from consistency | the same few physical rules (wind carries scent, fire and noise scare, snow shows tracks, rain erases) should apply to every kind; that is what makes a lesson carry |
| **Kenshi, Cataclysm: DDA** | animals as factions with herds; in Cataclysm, sound and smell attract creatures across the map; species as bundles of flags | sound as a long-range attractor is a cheap global mechanism; flag soups give variety but little legibility | a few global attractors (noise, smell of meat and blood, light at night) beat many per-kind flags |
| **Spore** | creature form fully designable; behaviour shallow | variety of form without variety of behaviour felt hollow | exactly Zach's worry: different names and numbers on one behaviour read as one animal |
| **SimLife, SimEarth, Ecosystem, Gridworld** | parameterised or evolved food webs and brains [18] | food webs crash without stabilisers; evolved brains are illegible | keep dynamics simple and stable (mechanics before realism, as Zach said), and keep behaviour authored |
| **Darwinia** | a population of simple digital creatures to herd and protect | little transfers beyond "a population you protect that is visible as individuals" | none of weight |

### 2.2 Agent-based ecology

- **ODD and pattern-oriented modelling** (Grimm, Railsback and others) [19]: describe a model by its purpose, state, scales, process
  schedule and design concepts; validate it against several patterns at once rather than one. Transfer: each kind's module should
  have an ODD-style card (purpose, state, schedule, what it senses, what it learns, what it emits) and be tested against two or three
  patterns at once (a run reaches the downstream weir a day after the upstream one *and* its size falls when the upstream weir is
  shut *and* the catch per effort falls before the stock collapses).
- **Super-individuals and resolution on demand:** individual-based models condense animals into super-individuals where detail is
  not needed. The wild layer's condensing of groups near people is the same idea; keep individuals only for what people can tell
  apart (the old sow, a legend, a marked swan, a bonded hawk).
- **Compensatory immigration** (Lieury and others, 2015) [20]: local fox culls are refilled from outside; culling in the breeding
  season was fully offset by immigration by the next February, culling in winter after dispersal worked better. Transfer: a
  vacated territory refills from the ring unless neighbours also cull; control works at the scale of several villages (§4.5).
- **Animal personality** (Sih and others; trappability studies) [21]: individuals differ consistently on a bold-shy axis; bold
  animals enter traps first, so trapping samples and removes the bold. Transfer: §5, M5.
- **Matriarchs** (McComb and others, 2001) [22]: families led by older elephant matriarchs discriminate threats better, and their
  groups breed better; removing old individuals harms the group. Transfer: the old sow's knowledge is real biology in spirit; the
  boar hunt's choice of animal is a real decision (§4.1).
- **Culture in wild birds** (Fisher and Hinde 1949; Aplin and others 2015) [23]: blue tits opening milk bottles spread across Britain;
  experimentally seeded foraging techniques spread through great tit populations by social learning with conformity. Transfer: a
  raiding trick can spread within and between groups and villages over seasons (§5, M6).
- **Corvids remember faces** (Cornell, Marzluff and Pecoraro 2012) [24]: crows scolded the mask worn by those who had trapped them,
  and crows never trapped learned to scold it from others, for years. Transfer: animals as carriers of people's reputations (§5, M8).

### 2.3 Real practice

| Practice | What it was | Lesson, and how it transfers |
|---|---|---|
| **Tracking** (Liebenberg; the Ju/'hoan trackers) [47]; **bird language** (Jon Young) [48] | simple, systematic and speculative tracking; reconstruction of individual animals from tracks | readings by skill (already in wild_systems §9); and tracking as hypothesis-testing, where the expert's edge is local knowledge of particular animals |
| **Family hunting territories** (the James Bay Cree; Speck, Feit, Berkes) [25] | hunting leaders (tallymen) with authority over a territory, rotating use and restraint, later formalised in beaver reserves | a territory held by a person who knows it and restrains its use is a working commons institution; the tallyman is a dependence and an enforcer. Transfer: a wood's or warren's keeper with a tally |
| **Forest law** [26][27] | the king's beasts and their cover (venison and vert); verderers, regarders, the swanimote and the eyre; mastiffs within the forest lawed (three toes of a forefoot cut, by the Assize of 1184 and the Charter of 1217, inspected every three years by the regarders, or a fine paid); the **fence month**, about fifteen days either side of Midsummer, when hinds fawned and grazing and disturbance were barred [28] | the law did not only forbid taking; it constrained the defences: dogs lawed, fences kept low, beasts removed in the fence month. That is the mechanism that makes the lord's deer a grievance (§4.2; §5, M14) |
| **The medieval hunt** (*The Master of Game*, after Gaston Phoebus) [29] | the harbourer (lymerer) went out at dawn with a leashed scent hound to find where a hart lay, marked the trail with boughs, and brought its droppings (fewmets) to the assembly, where the master chose which hart to hunt | information about where game lies was a role with evidence, presented to an assembly that decided. Transfer: a harbourer's report as a service; the assembly as a collective decision (§4.2) |
| **Deer parks** [30] | a pale of cleft oak on a bank and ditch; a licence to empark; a **deer leap** (salter), licensed by the Crown, that let deer jump into the park from the forest but not out | a one-way gate that draws a common or royal stock into private property: a chokepoint and a grievance (§6, no. 25) |
| **Rabbit warrens** [31] | rabbits introduced (or reintroduced) by the Normans; pillow mounds; a warrener in a lodge paying a high rent in carcasses or money; free warren as a granted right | a wild-kept boundary held as a right, with a specialist, rent and poaching (§6, no. 8) |
| **Duck decoys** [32] | curved, netted pipes off a pond; a decoyman behind screens and a fox-like dog that lures ducks up the pipe; silence around the pond; 41 still working in England and Wales in 1905 | a structure that is a chokepoint, a specialist with a trained dog, and an externality (noise nearby spoils it) (§6, no. 32) |
| **Swan upping** [33] | swans owned by marks nicked on the beak; a registry of about 630 marks between 1450 and 1600; an annual gathering to mark the cygnets; unmarked swans the Crown's | property in a wild thing made visible, kept by a yearly collective act (§4.23) |
| **Eel rents** [34] | Domesday and later records of rents in eels counted in sticks of 25; Harmston owed 75,000 a year; mills paid in eels | an obligation denominated in a wild good forces a fishery to be worked and makes the weir a held asset (§5, M13) |
| **Serjeanty** [35] | land held by keeping a sparrowhawk for the king and mewing it at one's own cost; two lanner falcons kept for heron-hawking with a greyhound to make the heron rise; later commuted to rent | a duty paid in wild skill makes a specialist out of a landholder; heron-hawking ties the heronry's protection to falconry (§4.18, §4.22) |
| **Salmon close times and weirs** [36] | Magna Carta clause 33 against weirs; Scottish law's weekly close time (now Friday evening to Monday morning) when fixed engines must let fish pass | a negotiated gap in time is an institution that splits the run between upstream and downstream (§4.15) |
| **Vermin laws** [37] | Tudor acts for "preservation of grain" by killing crows and other vermin, paid by parishes; the 1533-4 act excluded bounties on kites and ravens in towns | bounties are collective payments that need a collector and evidence (a head, a foot); they create a paid specialist and a fraud problem (§5, M13) |
| **Red kites and ravens in towns** [38] | tolerated as scavengers of refuse in medieval and early modern London, while also counted vermin elsewhere | a commensal is both ally and pest depending on the waste stream (§6, no. 2) |
| **Animal trials** (Chassenée and the rats of Autun) [39] | rats summoned to an ecclesiastical court; their advocate argued that one summons could not reach rats scattered over many villages | a society's institutions reach for the wild; an LLM society may well produce the like (a by-law against a fox, a bounty, a curse). Leave room for it in the state (records, rules about kinds) |
| **Weather lore and phenology** (Gilbert White) [40] | close local observation of arrivals and departures, with some wrong explanations (swallows hibernating) held for decades | true signs with false explanations persist: misreads as beliefs (wild_systems §9) are realistic, and local calendars are idiographic |
| **The Four Pests campaign** (China, 1958) [41] | sparrows killed in a mass campaign; locusts and other insects followed; the campaign was changed | the trade-off of a pest that eats pests (rooks, sparrows) is real and large; lore that "the rooks are only a pest" is a costly misread |
| **Fowling, falconry, pannage, beekeeping, bird-scaring, mole-catching** | (in the kinds below) | each made a trade, a right or a duty |

## 3. The mechanisms, one by one

Each entry: what is strongest; what is weak or wrong; the fundamental critique if there is one; the alternative, with state, rule,
signs, levers, test; and which purpose of the brief it serves (numbered as the brief's §3: 3.1 dependence and leverage, 3.2
problems no individual can solve, 3.3 hidden state and information, 3.4 commons, 3.5 a land that threatens unequally, 3.6 seasons
and preparation, 3.7 status, law and stories, 3.8 differences between villages, 3.9 land that changes).

### 3.1 The shared state (position, condition, memory, make-up, calendar)
- **Strongest:** one state read by all facets is what makes cross-talk (a hunted sounder raids warier) possible.
- **Weak:** it lacks four things the behaviours need: **what the animal senses of people** (A1); **individual traits** (a bold-shy
  value per group or individual; scars; a history of hunts survived); **social knowledge** (who in the group holds the routes and
  fears; what has been learned from others); and **its standing toward a village** (fed here, harmed here, by whom). "Memory:
  places fed, harmed, disturbed; people's patterns" folds all of these into one bag.
- **Alternative:** split memory into typed stores, each with its own decay in engine days: `places` (parcel to value, with sign and
  age), `harms` (parcel and kind of harm), `scares` (kind of scare to habituation level), `people` (only for kinds that recognise
  individuals: person id to standing), `routes` (edges used, with strength; §5, M4), and `knowledge_holder` (the individual whose
  death clears `places`, `routes` and half of `harms`). Add `trait` (bold-shy, 0 to 1) per group or individual.
- **Test:** clearing the knowledge holder clears exactly the stores it holds; a new group formed by splitting inherits a share.

### 3.2 The animal interface (D2-203)
- **Strongest:** modules perceive only their own state, the land they can reach and what is physically there, and act only through
  primitives with keyed randomness. This is the right discipline, and Rain World's modular AI supports it.
- **Weak:** perception of people is a list (a watch, a dog, people). It needs a perception call through the engine's noticing rule
  in reverse: the animal's senses (A1) against a person's presence, noise, light, smell and the wind (§5, M1). The primitives lack
  **emit an alarm** (a sound sign others read), **follow** (move toward a group of one's kind), **probe** (test a door or a gap
  without entering) and **cache** (store food at a place, for foxes, jays, squirrels).
- **Guard tests to add:** a module may not read another kind's private state, only what that kind has emitted (traces, alarms,
  carcasses, presence); a module may not read any person's plans, only their presence and traces; every number a module uses comes
  from data.

### 3.3 Ranging by value, and memory
- **Strongest:** routes and gaps emerging where cover meets fields is the right idea, and value less remembered danger plus
  remembered food is a fair forager.
- **Weak:** "each night the group goes to the best reachable parcel" makes every kind a myopic optimiser. Real animals are path
  dependent: they use the same racks, runs and gaps for years, and they move between a few known places rather than recomputing the
  best. The optimiser also makes the outcome jump between parcels when values are close, which agents read as noise.
- **Alternative:** ranging over a **route graph** with habit (§5, M4): the group moves along its strongest known edges to known
  places; values decide only which known place; exploration of a new edge is rare and is what a closed gap triggers. Routes are
  state people see (a rack through the hedge, a run across the field) and block.
- **Test:** blocking the strongest edge diverts the group to the next edge within one engine night, and the new edge strengthens
  until it is the habit; the old edge fades over N engine days.
- **Purpose:** 3.3 (a route is particular, idiographic knowledge), 3.2 (a gap in a common hedge is everyone's problem).

### 3.4 Habituation by the kind of scare (D2-198)
- **Strongest:** four answers (gets used to it, scared off, leaves for good, does not answer) are a real taxonomy and a lesson.
- **Weak:** under compression the "gets used to it" answer completes inside one engine night, so variety between nights does
  nothing (§1.2 b). The deep dive found agents did not learn which kind answers which way in two seasons.
- **Alternative:** resolve over the stretch. A household's deterrence over an engine night is a set of distinct scares held (fire,
  noise maker, a person, a dog, harm) and the share of the stretch watched. A habituating kind gets used to each distinct scare
  within the stretch, so its turned share is roughly the number of distinct scares (with harm counting double) against a saturating
  curve; a scared-off kind is turned by any one scare kept up. That keeps D2-198's answers and makes "vary it" a matter of having
  several scares: a reason to own a dog, make clappers, keep firewood, or borrow a neighbour's boy.
- **Make the answer legible:** the turned and not-turned signs must name both the kind and the scare ("the pigeons came down
  beside the scarecrow and fed as if it were a post"; "a hare bolted from the scarecrow's shadow"). The deep dive's failure was
  feedback that did not say which kind ignored which scare.
- **Test:** a household with two distinct scares and a dog loses about half what a household with one scare loses to boar over a
  ripening season; the same two households lose about the same to hares.

### 3.5 The facets

**F1 Quarry you seek: the search game.**
- *Strongest:* finding is the right problem for quarry, and it creates the most valuable expertise there is: a map of where game
  lies in which conditions. Snares and traps as gear left at places, checked, robbed, catching the wrong thing, are excellent
  (property and quarrels from a small act).
- *Weak:* trail-following as successive acts breaks the time scale (a unit is two real days) and costs an LLM call per step; wind
  direction does not exist in the climate (a gap); "how many clues a searcher reads depends on skill and eye" is a sign system the
  agent must read every step.
- *Fundamental:* the search should be inside the act, and the agent's decisions should be the plan: **where** (a parcel or area),
  **when** (dawn, dusk, by day; a stretch after snow), **how** (stalk alone, with a hound, a drive with a crew, set snares on a
  run), **with whom**. The engine resolves the search inside the act: the group's lie this stretch is chosen by its module (cover,
  wind sector, disturbance, season); the act finds it with a chance from (is it in the area searched) x (approach: the hunter's
  noticing of the group against the group's noticing of the hunter, by the wind and noise, §5, M1) x skill; a miss returns the
  clues that point (fresh slots heading to X; old beds), which the hunter remembers.
- *State:* per group, a **lie table** seeded per world (parcels with conditions: wind sector, weather, season, disturbance); per
  hunter, a **lie map** in memory (parcel, conditions, found or not, date).
- *Signs:* the clues returned by a miss; snow lines; a hound giving tongue.
- *Lever:* the plan; a harbourer's report (another person's lie map sold or given, §4.2).
- *Test:* a hunter whose plans follow the lie table's conditions finds game about twice as often as one choosing at random, after
  about six hunts; the same hunter in another world starts again (idiographic).
- *Purpose:* 3.3 (a local expert's map; information worth trading), 3.1 (the harbourer, the hound keeper), 3.8.

**F2 Raider at your door.**
- *Strongest:* the contest of watch against habit was the strongest result of the prototype (boar's expert edge was the answer to
  scares), and defences that work physically (fences, doors, light, a dog) are right.
- *Weak:* one machine for kinds whose raiding differs in kind (§1.2 a); P12's "a learner comes on the other nights" is not learnable
  at six samples a year and is dubious under compression; there is no displacement, so a defence is purely private.
- *Alternative:* raiders by decision rule (A2): **the habit raider** (sounder, deer: route graph, place memory, habituation, a
  knowledge holder); **the social raider** (pigeons, rooks, sparrows: land where others feed, flee together, displaced to the next
  field; §4.8); **the lapse prober** (fox, stoats, rats at a door: probe k structures a stretch for an open door or a gap of its
  size; §4.5, §6 no. 22); **the cue raider** (deer and boar at the ricks in snow; the bear in a hungry spring: a threshold sends
  them, nothing else does). Replace P12's temporal learner with a **spatial adversary**: the habit raider learns which gap is
  watched and shifts to the next gap on its route graph (a watched gap is a harmed edge), which an agent can see in the signs and
  answer by watching both, fencing one, or sharing the watch with the neighbour whose hedge holds the other gap.
- *Displacement (§5, M3):* a raider turned at one field goes to the next best target that stretch, which is often a neighbour's.
- *Test:* fencing one of two gaps sends the sounder through the other within one engine night; a scared pigeon flock lands on the
  nearest field of the same crop; a household that watches while its neighbour does not loses less, and its neighbour more, than
  if neither watches.
- *Purpose:* 3.5 (unequal exposure), 3.2 (the rota, the common fence), 3.1 (the dog, the boy, the hayward).

**F3 Predator of your beasts.**
- *Strongest:* prey switching when wild prey fail is the clearest consequence through another kind; surplus killing in an
  enclosure is real and decisive.
- *Weak:* without territory refill, killing the predator is always good; without a herder's practice (folding at night, a herder
  present, a guard dog), the levers are thin; the herd it preys on (sheep, poultry) mostly does not exist yet.
- *Alternative:* territory with refill (a vacated territory refills from the ring after N engine days, faster if the ring is full);
  predation chance by the herd's state at night (folded, watched, a guard dog, out on the far pasture) rather than a target list;
  and a **kill site** that becomes a carcass with stakeholders (§5, M18).
- *Test:* killing a resident fox lowers hen losses for the stretch it takes to refill and not after, unless neighbours also cull;
  folded flocks lose a fifth of what open ones lose.
- *Purpose:* 3.2 (control at the scale of villages), 3.5.

**F4 The run or the pulse.**
- *Strongest:* the strongest facet: an event read from the weather, a window, many hands at a point, and a commons along the river
  between villages. Eels pass the relevance test where there is a river.
- *Weak:* LLMs know the general rule; under compression the whole chain fills in one engine night.
- *Alternative:* make the run idiographic: each river's **lag** (engine days from the first heavy rain after dry weeks to the run
  at each weir) set by its catchment in the generator, so the rule "after rain" is general and "the second day after rain here, the
  third at Lowford" is local. A weir takes a share by its state (built, kept, its gap open or shut; §4.15). An obligation in the
  run's goods (an eel rent in sticks, §5, M13) forces the crew to turn out.
- *Test:* the run reaches each weir on its lag day; a shut gap upstream lowers the downstream catch that stretch; the expert of
  this river beats a newcomer who knows only the general rule.
- *Purpose:* 3.4 (upstream and downstream), 3.2 (the crew), 3.1 (the weir as a held right), 3.6.

**F5 The site you steward.**
- *Strongest:* restraint and no way back are real lessons, and sites are anchors for rights and stories.
- *Weak:* the dynamics are slow (years); a run sees at most a desertion. The proposal gives no social machinery for claims beyond
  naming D2-194.
- *Alternative:* make the site's fast arm the decisive one (disturbance in the season deserts it this year and for N years; a site
  taken lightly this season shows more nests next spring), and give every site a **holder** field (a person, household, office or
  none), a **custom** (what may be taken, when), and a record of takes. Sites then become things to inherit, rent, poach and quarrel
  over.
- *Purpose:* 3.4, 3.7, 3.1.

**F6 The engineer.**
- *Strongest:* the beaver's dam is the clearest trade-off on land.
- *Weak:* this is a primitive (write to land state), not a way of meeting people; boar rooting and deer browse are written as
  engineering but are just eating. Real engineers missing: the mole (molehills in the hay meadow), the rabbit (turf and sand blow),
  the jay (planting oaks), bracken, gorse and blackthorn creeping over neglected ground.
- *Alternative:* treat engineering as an effect any kind's module may have through a primitive, and judge each by whether the
  change is something people must decide about (break the dam; harrow the molehills; cut the bracken under a common right).

**F7 The outbreak.** Built; fine as a load. *Weak:* relevance mostly small (slugs pass in wet years, aphids barely), and the signs
are ignorable unless tied to a sowing or picking decision. Keep loads whose lever is a farming choice; fold the rest into markers.

**F8 The lodger.**
- *Strongest:* "a door does nothing; a raised floor, stone, a cat or a terrier does" is the best misread in the catalogue, and the
  runs show agents believing the door works.
- *Weak:* lodgers that damage the structure itself (deathwatch beetle and woodworm in timber, jackdaws in chimneys, wasps and
  hornets in roofs, moths in wool) are absent; the cat, the decisive lever, is not an animal.
- *Alternative:* §6 nos. 1, 4, 5, 6, 7.

**F9 Danger.**
- *Strongest:* encounter risk by state and situation (a sow with young, a wounded boar, a stag in rut) is right; D2-193 decided it.
- *Weak:* it is only the hunter's danger. Danger to children herding, to haymakers (adders), to beekeepers (stings), to anyone near
  a carcass a bear has cached, to dogs, and from disease (rabies) is missing. The danger the hunter creates (a wounded animal left in
  the wood endangers the next person through it) is the most social danger and should be explicit: a wounded beast is state with a
  place and days, and whoever wounded it is known to the crew.
- *Test:* the risky meetings happen where and when the state says; a wounded boar left in Oak Hanger raises danger there for all
  for two engine days.

**F10 The informant.**
- *Strongest:* reading one kind through another (ravens over a kill, kestrels over voles) is the purest expertise.
- *Weak:* it is written as a facet of the informant kind, so each case is a one-off. It is one-way (animals inform people about
  animals) when the most useful real case is two-way: birds' alarms tell deer that a hunter comes, and tell a keeper that a
  poacher is in the wood.
- *Alternative:* a general sentinel mechanism (§5, M7): kinds with A4 alarm emit an alarm sign at an intruder of any kind (a fox, a
  hawk, a person), carried by sound; other kinds' modules and people read it. A careless hunter moving fast pushes a wave of alarm
  ahead (Jon Young's "bird plough" [48]), which the deer read and leave; a keeper reads the jays to find the poacher.
- *Purpose:* 3.3; and 3.7 (evidence against poachers).

**F11 Taking and taming.**
- *Strongest:* the link to husbandry; the choice in spring between the sow and her young; the eyass, the swarm.
- *Weak:* the result is "a beast of the husbandry entity": the bond to the person who tamed it is lost, so the specialist is not
  needed once the beast exists.
- *Alternative:* a tamed or trained beast carries a **bond** (person id, strength) that sets how well it works for others, and that
  decays without that person's handling (RimWorld's training decay; ARK's imprinting). A hawk works for its falconer, poorly for
  another; a ferret bolts rabbits for its warrener. The falconer is then needed while the hawk lives.
- *Test:* a hawk lent to another works at half; after N engine days without its falconer it must be re-manned.
- *Purpose:* 3.1 (a specialist bound to a beast), 3.7.

**F12 The legend.**
- *Weak:* "a unique individual with a name and a story" seeded by the generator is a prop. Legends are made by telling.
- *Alternative:* emergent legend. Every individual in A5 carries a history (hunts survived, wounds, kills of beasts, people hurt).
  When the record of what people have said and written about one individual passes a threshold (told by at least k distinct people,
  or entered in the chronicle), it becomes **known**: it takes the name people gave it (from their own words), its size and deeds
  as told (which may exceed the state's) become lore, and a bounty, vow or taboo can attach. The generator may seed one or two known
  beasts with a seeded history, as the elders' stories.
- *Test:* in runs with a wounded boar that escapes twice, some fraction of runs produce a named boar in agents' talk.
- *Purpose:* 3.7.

**F13 The calendar-giver.** Built (markers). *Weak:* markers drew no comment in the runs because they carried no lever. Keep a
marker only if it times a decision someone can make that stretch (sow barley when the elm leaves are the size of a mouse's ear;
set the eel traps when the swallows go; shut the fold when the howling starts). Otherwise cut it.

### 3.6 The transitions
- **Strongest:** wild to kept, kept to feral, site to gone, ordinary to legend.
- **Missing:**
  - **wild to commensal** (a fox that learns the midden; kites at the shambles; sparrows at the threshing floor): an animal moving
    into people's waste stream (§5, M9);
  - **kept to pest** over generations (the warren's rabbits escaping into a plague; feral pigs);
  - **wild to protected** (a heronry claimed by a lord; a swan marked);
  - **extirpated to returning** (wolves coming back after a generation away take more stock than settled packs: wild_systems
    already has this);
  - **individual to lineage** (a matriarch's daughter inherits half her map: culture, §5, M6);
  - **local to known** (a beast passing into talk, F12).

### 3.7 The learning problems
- **Keep:** P1 timing, P2 place, P5 restraint, P6 no way back, P7 many hands, P8 a consequence through another kind, P10 a
  trade-off, P11 a misread, P13 reading its state, P14 when not to go near, P15 emptied and refilled, P17 patience and craft, P18
  property.
- **Rework:** P3 and P4 under the stretch semantics (§3.4); P12 as a spatial adversary (§3.5 F2); P9 (a season foretells the next)
  is good but its yearly arms are invisible, so keep only its seasonal arms in runs.
- **Add:**
  - **P19 attribution:** which kind (or which person) did this? The deep dive's failure; also a social problem (the neighbour's
    dog or the fox; the poacher or the wolf).
  - **P20 the base rate:** most nights nothing comes. The cost of vigilance against the cost of loss; the over-watching the deep
    dive found.
  - **P21 externality:** my defence moves the problem to you; my lapse brings it to all of us (§5, M3).
  - **P22 scale of control:** control works only if neighbours do it too (foxes, wolves, rabbits, pigeons).
  - **P23 whom to believe:** a harbourer's report, a warrener's count, a bounty claim, an elder's saying.
  - **P24 the particular:** this river, this wood, this sounder (idiographic knowledge; §1.2 c).

### 3.8 The tests in the proposal's §1.2
- *Relevance at a tenth of a household's food or work* is a good floor but a poor ceiling: a kind can pass it and make nothing
  social (slugs), or fail it and make a great deal (swans; the fox's externality; bee trees and wax for seals). Add a second test:
  **it creates at least one dependence edge, holdable thing or dispute that a null arm lacks** (layer C).
- *Inside a run where possible:* make it a hard rule with numbers: at least one fast arm of one to three engine days for every kind
  present in a world, shown in at least half of 12-day windows where the kind is present.
- *The animal tests* are good; add **society tests** (§7): with a strong cast on several seeds, against the pack off, do watch
  rotas, fence duties, bounties, claims, trades in wild goods and specialists appear more often?

### 3.9 The mechanisms judged against the purposes

The brief asks of every mechanism: which purpose it serves, through which mechanism, who comes to need whom, what can be held,
traded, enforced or argued about, and whether a null arm would look different. As the proposal writes them, and as reworked here:

| Mechanism | Purpose (brief §3) | As proposed: who needs whom | As reworked here: who needs whom; what is held or argued | Null arm differs? |
|---|---|---|---|---|
| shared state | enabler | none | the knowledge holder makes "which animal" a crew's decision | only through others |
| animal interface | enabler | none | perception through the noticing rule makes the quiet stalker and the keeper skilled | only through others |
| ranging by value | 3.5 | none (private losses) | route graph: the common hedge's gap is the hayward's business | as proposed, barely; reworked, yes (fence duties) |
| habituation (D2-198) | 3.5, 3.2 weakly | none | the stretch contest: dogs, clappers and boys lent or hired | as proposed, no; reworked, yes (lending, hiring) |
| F1 quarry | 3.3, 3.7 | the drive needs beaters | the harbourer's report, the hound keeper, the lie map as tradable knowledge; snares robbed | yes (reports, thefts) |
| F2 raider | 3.5, 3.2 | none | displacement: rotas, pooled boys, by-laws, free-rider quarrels | as proposed, no; reworked, yes |
| F3 predator | 3.2, 3.5 | none | refill: culls across villages; folding as a duty | reworked, yes |
| F4 run | 3.4, 3.1, 3.2 | the weir crew | close times, rents, the bailiff; downstream quarrels | yes |
| F5 site | 3.4, 3.7 | a claim (D2-194) | a holder, a custom, a record; inheritance, rent, poaching | yes once rights exist |
| F6 engineer | 3.9 | none | the dam's two parties (pond users, meadow holder) | reworked, yes |
| F7 outbreak | 3.6 | none | little; keep where it times a farm act | barely |
| F8 lodger | 3.5 | none | the cat given, the rat-catcher paid | reworked, yes |
| F9 danger | 3.2, 3.7 | the crew | the wounded beast's maker known; the crew's trust | yes (crews) |
| F10 informant | 3.3 | none | sentinels: keepers and poachers; evidence | reworked, yes |
| F11 taking and taming | 3.1 | none after taming | the bond: the falconer, the warrener's ferret, the setting dog | reworked, yes |
| F12 legend | 3.7 | none (seeded) | emergent from telling: names, bounties, vows, taboos | reworked, yes (named beasts in talk) |
| F13 calendar | 3.6 | none | the elder's sowing rule | slightly |
| transitions | 3.1, 3.9 | husbandry | commensal and feral phases: the warren's edge, the midden | yes |

The pattern is plain: as written, only F1's drive, F4's crew, F5's claims and F9's crew create any need between people. Every
other mechanism needs displacement, refill, bonds, records or law (§5) before a null arm would look different at the level of the
society.

## 4. The kinds, one by one

Each kind: a **verdict** (keep, rework, merge, defer, cut); what is **strongest**; what is **weak or wrong**; its **social
footprint** (purpose served; who comes to need whom; what can be held, traded, enforced or argued about; what a null arm would lack);
and **alternative or additional behaviours**, each with its state, rule, signs, levers, why it is interesting and a test.

### 4.1 Wild boar
**Verdict: keep, rework the raider and the calibration; make it a frontier kind, not the flagship.**
- *Strongest:* a real contest at the field; danger that needs a crew; the mast's arm; piglets as a link to pigs. The deep dive's
  strongest relevance and its clearest "the depth is in the acts".
- *Weak or wrong:*
  - present in 3 of 20 generated villages; designing the layer around it designs for the minority of worlds;
  - unwatched losses of 22% of need (median) are about twice the real upper range near woods; at that level boar dominate the
    economy where present and make food more than 30% of actions;
  - P12's watch-schedule learner is not learnable (§1.2 b);
  - "kill the matriarch and the sounder scatters and loses them": partly real in spirit (old animals hold knowledge, [22]), but
    hunting that breaks up sounders can raise damage, because the fragments raid separately and young sows breed earlier. The
    proposal treats killing her as a pure gain.
  - the mast's two-year arm is invisible in most runs; only its same-autumn arm (mast falls, the fields are quiet) can be seen.
  - hunting pressure moves boar's activity toward the middle of the night in some studies and not in others [43]; the proposal's
    "made wary for longer only by harm" is fair, but a hunted sounder should also come later in the night, which changes what a
    watch at dusk catches.
- *Social footprint:* 3.2 (the watch rota, the common fence, the boar hunt crew), 3.5 (the fields by the wood), 3.7 (the hunt as a
  feat; the boar as a forest beast under the lord's right). Who needs whom: households by the wood need the far households' watch
  nights or their dogs; the crew needs a spear-maker and a hound keeper; under forest law, villagers need the lord's leave. Held: the
  right to hunt; the hounds; the gap's hedge. Argued: who watches; who pays for the far field's loss; whether to hunt the old sow.
  Null arm: no rotas, no shared fences, no crews by the wood.
- *Behaviours:*
  1. **The stretch contest at the field** (§3.4; §5, M2). *State:* per sounder, habituation per scare kind; per field, the
     household's deterrent set over the stretch. *Rule:* turned share by distinct scares and harm, saturating; a dog's bite counts as
     harm and makes the sounder wary of that field for N engine days. *Signs:* rooting nearer (lead, one engine day); the watcher's
     line naming the scare and the outcome. *Lever:* own or borrow more distinct scares; a dog. *Why:* turns "vary the scare" into
     dependence on things and people. *Test:* §3.4.
  2. **The spatial adversary.** *State:* the route graph's edges into the field; harm on an edge. *Rule:* a watched gap with harm is
     a harmed edge; the sounder takes the next edge. *Signs:* "fresh rooting at the thorn gap by Ash Field, none at the old gap".
     *Lever:* watch both, fence one, ask the neighbour whose hedge holds the other. *Test:* §3.5 F2.
  3. **Splitting.** *State:* sounder size and cohesion. *Rule:* a hunt that kills the knowledge holder splits a sounder of more than
     six into two that raid separately for the rest of the year, each with half the map; a hunt that kills young animals does not.
     *Signs:* two sets of rooting at different gaps. *Why:* "which animal" becomes a real decision with a cost either way (P10).
     *Test:* killing the old sow raises raid nights the next stretch and lowers them over the season.
  4. **The mast race** (D2-202's one stock). *State:* acorns on the parcels of the wood. *Rule:* boar and the village's pigs (at
     pannage, with husbandry) draw on the same fall; the first in takes the best; a heavy mast feeds both, a poor one starts a race.
     *Signs:* "the ground under the oaks rooted bare already". *Lever:* turn the pigs in early (a right and its date). *Why:* the
     pannage date becomes a decision and a quarrel (who turns in before the agreed day). *Test:* an early turn-in takes more mast and
     sends the sounder to the fields sooner.
  5. **The wallow as the lie.** *State:* one or two wallows per sounder in the lie table. *Rule:* in warm weather the sounder lies
     within one area of its wallow. *Signs:* "a wallow churned fresh, mud rubbed high on the oaks" (the expert reads it as the lie).
     *Lever:* the boar hunt planned at the wallow. *Why:* particular knowledge that finds the sounder.
- *Calibration:* aim at 3-10% of need unwatched in a wooded village (median), 20-30% in a bad year; most of the lesson survives.

### 4.2 Red deer
**Verdict: keep, and restore the raid under the law.**
- *Strongest:* stalking, slot reading, the herd's make-up, the hunted wood emptying and drifting back, the coppice that does not
  regrow, rights.
- *Weak or wrong:*
  - "Cut: red deer as raiders of the corn" removes the forest-law grievance, which node_ecology.md found the strongest social lever
    the ecology gives (the lord's deer eat the villagers' crops; the villagers may not kill them);
  - the stalk's detail (wind, slots) is good but needs wind direction (a gap) and should be inside one act (§3.5 F1);
  - "a herd hunted of its hinds dwindles in two years": a run cannot see it; it needs a keeper's count to be visible at all;
  - present in few worlds (wooded ones).
- *Social footprint:* 3.7 and 3.1 (the lord's beast; poaching as crime; venison as a gift that marks favour), 3.3 (the harbourer's
  knowledge), 3.4 (a herd under restraint), 3.5 (the villagers' crops). Who needs whom: the lord needs the forester and harbourer to
  find and keep the deer; villagers need the lord's leave or a poacher's venison; the poacher needs a buyer and silence. Held: the
  right (vert and venison), the hounds, the forester's office, the record of the herd. Enforced: no taking; dogs lawed; fences kept
  low; the fence month. Argued: damage; poaching accusations; who saw what. Null arm: no forester, no poaching, no grievance.
- *Behaviours:*
  1. **The lord's deer at the corn, and the law on the levers** (§5, M14). *State:* a world flag that red deer are a forest beast;
     per household, its dogs (lawed or not); per field, fence height. *Rule:* deer raid young and ripening corn modestly (about 3-5%
     of a field by the wood a season); within the forest, a household may scare deer but not kill them; a lawed dog chases but does
     not catch; a fence above the forest's height is unlawful and can be presented at the forest court; in the fence month no
     beasts may graze the wood and no one may disturb it. *Signs:* "a herd of about nine deer was at the corn in Long Field in the
     night: tops bitten"; "the forester measured the hedge at Long Field". *Levers:* scare only; petition for compensation; raise the
     hedge and risk the fine; poach. *Why:* the grievance with a constrained defence is the real historical engine of conflict, and
     it needs enforcers to act (scenario_design rule 4). *Test:* with the flag on, more disputes and petitions in the records
     against the null arm; with the flag off, the deer are hunted near the fields.
  2. **The harbourer and the assembly** [29]. *State:* the herd's lie this stretch; a harbourer's lie map. *Rule:* a "harbour"
     act at dawn (one unit, with a scent hound or alone) reports the lie with evidence (fewmets: the reading gives size and sex);
     the hunt that uses the report finds with high chance; a false or stale report fails. *Signs:* the report itself, a thing that
     can be passed on. *Lever:* hire a harbourer; trust or not. *Why:* information as a service with evidence and a reputation (P23).
     *Test:* hunts with a harbourer's fresh report find twice as often; reports more than one engine day old are worth half.
  3. **The stalk inside one act** (§3.5 F1), with the lie table by wind sector and weather, and the hunter's own lie map.
  4. **Venison as a gift.** *State:* a carcass's owner and its parts (haunch, umbles: the "humble pie" of the lower orders).
     *Rule:* parts can be given; the giver's standing rises with the recipient. *Why:* medieval venison circulated as patronage; it
     makes the hunt a source of social ties, not food (node_ecology.md: hunted deer and boar about 1% of food). *Test:* agents with a venison gift
     trade or ally more with the giver than a control.
  5. **The herd's count.** *State:* the herd's make-up. *Rule:* a forester's census act yields a noisy count by age and sex; the
     count is a record others can read. *Why:* makes restraint possible within a run (the hinds counted fewer this spring).
  6. **Winter at the ricks and the bark** (as built), **the rut** (stags bold, a stag at bay dangerous) and **calves to a park**
     (defer to §6 no. 25).

### 4.3 Roe deer
**Verdict: keep, cheap; make it the commoner's deer.**
- *Strongest:* one to a patch is a map to learn; the patch empties and refills (P15); calling the buck in the summer rut is a knack
  with a window, and red-deer lore gets it wrong (P11).
- *Weak:* little relevance as food; the rut call is a small window (in July-August, about four engine days) that most runs miss.
- *Social footprint:* where red deer are the lord's, roe can be a lesser beast (by an English ruling of the 1330s they were held a
  beast of the warren, not of the forest), so a household with a free warren grant may take them: a graded right, and an argument
  over which deer is which. Null arm: no graded taking.
- *Behaviours:* patches with holders (refill by dispersal in spring and autumn, a few engine days); the call in the rut; the bark
  alarm as a sentinel that warns red deer and the hunter alike (§5, M7); browse on new coppice (so roe, not red deer, are the
  coppice's main enemy in small woods, which is closer to life).

### 4.4 Wolf
**Verdict: keep in frontier and upland worlds; rework around territory, refill and the multi-village public good.**
- *Strongest:* the circuit with howls whose direction tells where it is; deer first, herds when deer fail; dispersers as a
  different problem; the drive and the bounty; ravens following.
- *Weak or wrong:*
  - at real density a pack holds 100-300 km², so most four-village worlds have one pack or none; its visits to any one village are
    rare, so its fast arm (a fold that fed it, back within days) needs the fold first (sheep and folds do not exist yet);
  - the bounty is written as a lever, but it is an institution: who pays, who collects, what counts as proof;
  - killing breeders can break a pack into dispersers that take more stock (this effect is contested in the literature, so present
    it as a regime the world may hold, not as a law).
- *Social footprint:* 3.2 and 3.4 between villages (one pack, several villages: a drive or a bounty is a public good with free
  riders), 3.5 (the far pasture, the child herding alone), 3.7 (the wolf's head at the reeve's door; Wolfpit as a place name).
  Who needs whom: villages need each other for a drive; the bounty needs a collector who can tell a wolf's head from a dog's (the
  misread as fraud, P23). Null arm: no inter-village agreement.
- *Behaviours:*
  1. **The circuit across villages.** *State:* the pack's position on a loop of areas, a few areas a night; its hunger. *Signs:*
     howls by direction and distance; ravens; tracks. *Lever:* fold and watch on the nights it is near; tell the next village.
     *Test:* agents who pass news of the pack's direction lose fewer beasts than those who do not.
  2. **The bounty as an institution** (§5, M13). *State:* an agreement with a payer, a collector and a proof (head or pelt).
     *Rule:* a head brought to the collector is paid; a dog's head can be passed off to a collector who cannot tell. *Why:* creates
     an office and a fraud problem. *Test:* a bounty raises wolf kills and dog deaths both.
  3. **Folding and the guard dog** (with husbandry). *Rule:* predation by the herd's night state (folded, watched, dog, far
     pasture). *Lever:* fold every night (costs units); a mastiff (lawed in the forest, §4.2).
  4. **Dispersers** (as proposed): a lone young wolf crossing farmland in autumn to spring, bold, easy to trap.
  5. **The persecuted pack grows shy** (§5, M5): a pack that has lost members avoids people's land more and kills less near
     villages, but is harder to drive.

### 4.5 Fox
**Verdict: keep as a cheap kind; its value is the door discipline, the hamlet externality and the treadmill.**
- *Strongest:* the lapse finder (it tries doors and finds the ones left open); surplus killing once in; the vole crash reaching the
  hen house; the pelt.
- *Weak or wrong:* fails the relevance test at 3% of need; the spring earth versus winter cull is partly reversed by the
  evidence: in the study of [20], culling in the breeding season was fully offset by immigration by the next February, and culling
  in winter after dispersal worked better. Spring den control ends this spring's provisioning raids (true), but not next year's.
- *Social footprint:* 3.2 (control only works if neighbours do it too), 3.5 (one house's lapse is the hamlet's problem). Who needs
  whom: households need each other's door discipline; the terrier man or the earth-stopper is a specialist; geese as watchers are
  a household good. Argued: whose open door brought it; whose dog killed whose hens (attribution, P19). Null arm: no shared
  discipline, no paid fox-killer.
- *Behaviours:*
  1. **The lapse prober** (§5, M3). *State:* the fox's circuit over the hamlet's structures; memory of where it fed. *Rule:* each
     stretch it probes k doors; an open one is fed at and returned to; a hamlet where it fed is probed more next stretch, so one
     household's lapse raises its neighbours' risk. *Signs:* "earth scraped under the hen-house door at Hale House"; feathers. *Test:*
     a hamlet with one lax household loses more hens in the other households than a hamlet with none.
  2. **The treadmill.** *State:* a territory with a holder. *Rule:* a killed holder is replaced from the ring in a few engine days
     (faster in autumn, when the young disperse), unless the ring is also culled. *Lever:* cull together, in winter. *Test:* §3.5 F3.
  3. **Vole year, hen year** (as proposed, through the macro web).
  4. **Geese as the watch** (with husbandry): geese alarm (§5, M7) and turn a fox at the door.

### 4.6 Brown bear
**Verdict: keep as a rare kind for frontier wildwood; centre it on the carcass and the hungry spring.**
- *Strongest:* the bear's year legible from the autumn; the hungry spring; danger; the great hunt; legend.
- *Weak:* encounters too rare to learn from in a run; hives need bees; one or two per world.
- *Alternative:* **the cached carcass**: a bear that kills or finds a carcass covers it and lies up near; whoever goes to the
  carcass (to skin the cow the night killed) meets the bear. *Signs:* "the dead cow half-buried in leaves and earth"; the expert:
  "a bear has cached it; it is lying up near". *Lever:* leave it, burn it, or go with a crew and dogs. *Why:* turns "when not to go
  near" into a concrete decision a household makes, with an expert's reading that saves a life (P14, P23). Keep the hungry spring
  and the den (a denned bear cannot be met).
- *Social footprint:* 3.7 (feat and legend), 3.2 (the great hunt). Low cost if the carcass rule is shared with wolves and ravens
  (§5, M18).

### 4.7 Brown hare
**Verdict: keep cheap; merge its gear with rabbits and partridge into one "small game and gear" module.**
- *Strongest:* runs and snares as place knowledge for the poorest food; snares as property that can be robbed or take a
  neighbour's dog.
- *Weak:* about 1-2% of food; coursing needs hounds and status.
- *Additional:* the hare's **form** faces the wind and the hare sits tight until close (a lie that a walker almost treads on); the
  folklore of the hare (witches turned hares) as story material. *Social footprint:* 3.1 small (the snarer), 3.7 (coursing as a
  sport of standing; poaching hares as the commonest offence). Null arm: no snare thefts.

### 4.8 Woodpigeon
**Verdict: rework as a social follower; merge with rooks and sparrows into a "birds at the corn" constitution with kind-level
differences.**
- *Strongest:* mast failure sends the flocks to the winter corn and greens (P8); children's work.
- *Weak or wrong:* written as F2 with habituation; the real mechanism is social attraction (flocks land where pigeons are feeding;
  practitioners lay out decoys in a feeding pattern, and a regimented line of heads-up birds turns the flock away) [42].
- *Behaviours:*
  1. **Local enhancement.** *State:* flocks per area; the fields of a crop in season. *Rule:* a flock lands on the field with the
     most birds already feeding (weighted by food); a still scarecrow is read as a post once birds feed near it; a moving person or
     a shot lifts the whole flock. *Signs:* "a few pigeons down on Long Field this morning, more by noon". *Lever:* scare the first
     birds before the flock builds (a child at dawn), or decoy and net or shoot. *Why:* timing within the day matters, and the lesson
     differs from the hare's.
  2. **Displacement.** *Rule:* a lifted flock lands on the next field of the same crop. *Signs:* the neighbour sees the flock
     arrive. *Why:* scaring is redistribution unless the hamlet scares together or kills birds; this is the cheapest route to a
     shared bird-scaring rota (P21). *Test:* two neighbouring fields: one scared, one not; the unscared loses more than with no
     scaring at all.
  3. **Decoyed** (with nets): birds shot or netted are set as decoys, which draws more. *Social footprint:* 3.2, 3.5; children's
     work (a dependence of households on children or on a hired boy). Null arm: no rota.

### 4.9 Rook and the rookery
**Verdict: keep, with the trade-off and the misread of the Four Pests.**
- *Strongest:* a real trade-off (grubs eaten, sown corn pulled); children with clappers; the rookery for generations; branchers
  shot in May.
- *Weak:* "a rookery's size shows the grubs" is weak; the trade-off is invisible unless both sides have signs a household connects.
- *Behaviours:*
  1. **Central-place foraging** from the rookery: fields within a radius are worked; the nearest worst.
  2. **The trade-off shown:** rooks on a pasture lower the leatherjacket and wireworm loads on that parcel (signs: "rooks working
     the low pasture, probing"; next spring: "the grass on the low pasture is sound where the rooks worked"). Destroying the rookery
     raises grub damage in the radius the next season (the misread, [41]).
  3. **The rookery and the house:** folklore holds that rooks leaving a rookery mean the family's fortune falls (story); a
     rookery's holder can protect it or shoot it.
- *Social footprint:* 3.5 (fields by the rookery), 3.7 (story), and children's work. Null arm: no rota; no quarrel over shooting.

### 4.10 Raven
**Verdict: keep as the carcass informant; merge its memory with a corvid module (§6 no. 3).**
- *Strongest:* the purest informant; follows wolves; gathers over carcasses within a day.
- *Weak:* a kind that is only a sign could be part of the carcass's bundle. Its value rises with corvid individual recognition and
  with omen lore (ravens over a battlefield).
- *Alternative:* ravens over a carcass as part of the carcass object (§5, M18); individual pairs that hold a territory and remember
  people (§5, M8).

### 4.11 Voles and mice, owls and kestrels
**Verdict: keep the cycle as lore and history; build the barn owl and the owl hole now.**
- *Strongest:* a multi-year pattern carried by elders; predators following; the barn owl as an ally you steward.
- *Weak:* the three-to-four year cycle is beyond runs; relevance 1-2%; kestrels and owls as presence signs carry no lever.
- *Behaviours:* the **owl hole** (a fitting in a barn's gable; an owl takes it if the barn is quiet in spring; mice in that barn fall
  by a share); **mowing drives the voles to the ricks** (a fast arm with a lever: build ricks on staddles or away from long grass);
  **pellets** read by the expert as the phase. Social footprint is small; keep cheap.

### 4.12 Rats and mice in the stores
**Verdict: keep and deepen; it is in every village.**
- *Strongest:* the misread door; structure as defence; the harvest pulse.
- *Weak:* the cat and the terrier are fittings or flags, not animals; no rat-catcher.
- *Behaviours:* the **cat** (§6 no. 1); a **rat-catcher** as a paid specialist (a technique that clears a store for a season, with
  a terrier, paid by the household or by the parish); **poison** later (with risk to dogs, cats and people). Black rats in thatch
  and roofs. Plague: do not build (a regime too large for the engine's people and too dark for the runs' purpose). Null arm: no
  rat-catcher; no cat exchange.

### 4.13 Wildfowl
**Verdict: keep; centre it on flight lines, the decoy and the fen commons.**
- *Strongest:* pushed in by the cold with a lead (plovers west); flight lines; restraint against an easy harvest.
- *Weak:* "come tame a week into the freeze" falls inside an engine day; the engine's climate gives long freezes in 40-70% of
  winters (02zp §26), so the rare condition is common; restraint over winters is invisible.
- *Behaviours:* flight lines as particular knowledge (which channel at dusk, by wind); **the decoy pond** (§6 no. 32) as a held
  structure with a quiet zone that neighbours' shooting spoils (an externality); feathers and down to bedding.
- *Social footprint:* 3.1, 3.4, 3.8 (fen villages). Null arm: no quiet-zone dispute.

### 4.14 Eel
**Verdict: keep; the strongest run. Make it idiographic and an obligation.**
- *Strongest:* the eel night read from the weather; the weir and the river below; spearing in winter.
- *Weak:* the general rule is known to every model (02zp §29); the run fills the chain in one engine night.
- *Behaviours:* river lag by catchment (§3.5 F4); **eel rents** in sticks owed by the weir's holder to the lord, so the crew must
  turn out and short years cause debt (§5, M13); **eel traps as property** (the wicker grig set at night, checked at dawn, robbed).
- *Social footprint:* 3.1 (the weir's holder; the crew), 3.4 (downstream), 3.6 (smoked eels for winter). Null arm: no rent, no crew,
  no downstream quarrel.

### 4.15 Salmon
**Verdict: build with the eel's module, with the weekly gap as the institution.**
- *Strongest:* upstream against downstream with a lag of years; Magna Carta.
- *Weak:* the lag of years is invisible; the proposal gives no institution.
- *Behaviours:* the **gap in the weir** (a close time, as in Scottish law's weekly close [36]): state per weir, a gap open for some
  days of each stretch by agreement; fish pass upstream when open. *Signs:* "the gap at Lowford weir stood shut through the close".
  *Lever:* agree a close time; enforce it with a water bailiff; break it at night. *Why:* the negotiated gap is the institution the
  upstream-downstream conflict needs. **Pearl mussels upstream** depend on salmon and trout (§6 no. 27). Null arm: no close time.

### 4.16 Trout
**Verdict: cut as a kind; leave it in the water pack's fish stock** (it adds nothing the stock and tickling as a technique do not).

### 4.17 Otter
**Verdict: defer; merge into the fishpond and weir composite (§6 no. 26)** as a rival at the stews and the weir, hunted with
hounds for its fur when furs have uses.

### 4.18 Heron and the heronry
**Verdict: keep; tie it to falconry.**
- *Strongest:* restraint and no way back; a lord's claim; built.
- *Weak:* slow; the "size shows the fish" reading is weak.
- *Additional:* heron-hawking was the noblest flight, and land was held by keeping lanner falcons for it [35]; the heronry is
  protected because it supplies the lord's hawking. *Rule:* heron-hawking needs a heronry within reach; the heronry's holder may
  forbid taking young. *Social footprint:* 3.7, 3.1. Null arm: no protected heronry.

### 4.19 Beaver
**Verdict: keep for frontier worlds only; the dam's trade-off is excellent.**
- *Weak:* largely gone from England in the era; present in few generated worlds.
- *Additional:* the **flooded meadow belongs to someone downstream of the pond**: the dam helps the fishers and fowlers of the pond
  and harms the hay of the meadow's holder: a quarrel between two households about whether to break the dam. Castoreum as a good.

### 4.20 Wild bees
**Verdict: build early with husbandry; the wax-to-seals chain makes it one of the most valuable kinds.**
- *Strongest:* lining the bees home is a search procedure unlike any other; the bee tree as property; the swarm into a skep.
- *Behaviours:* **bee-lining as two-point triangulation** (an act at a flowering parcel gives a bearing as a sector of parcels; two
  acts at different parcels intersect to a few candidate trees); **marking a bee tree** (a mark is a claim others may respect or
  rob); **brimstoning versus driving** (harvesting a skep by killing the colony with sulphur fumes, or by driving the bees into a
  new skep, a knack that keeps the colony: restraint as skill); **"telling the bees"** (a custom: a death in the household told to
  the hives, as story material).
- *Social footprint:* 3.1 (wax for seals and candles: documents need the beekeeper), 3.7, 3.4 (bee trees in the commons). Null arm:
  no wax, no claims on trees.

### 4.21 Pine marten
**Verdict: defer; merge into the mustelid module (§6 no. 22)** until furs have uses.

### 4.22 Falcon
**Verdict: rework: goshawk and sparrowhawk for the wooded lowland; peregrine only where there are cliffs.**
- *Strongest:* the eyass, manning, prestige, rights.
- *Weak:* peregrines need high rock, rare in the generated lowland; the goshawk (woodland, the yeoman's hawk) and the sparrowhawk
  are the hawks of this landscape.
- *Additional:* the **bond** (§3.5 F11); **hawk theft** as a grave crime; **serjeanty**: land held by keeping a hawk for the lord
  (an obligation paid in skill, §5, M13); a hawk's **rank** (folklore of which hawk suits which station) as status display.
- *Social footprint:* 3.1, 3.7. Null arm: no falconer.

### 4.23 Swan
**Verdict: keep, cheap, and early once rights exist.**
- *Strongest:* marks on the beak; the yearly gathering; unmarked swans to the lord.
- *Behaviours:* swans as individuals (few per water); a **mark** as a tag on each; the **upping** as a collective act in summer where
  cygnets are marked by the parents' owner; an unmarked or wrongly marked bird as a dispute. *Social footprint:* 3.7, 3.1 (the swan
  master). Null arm: no marks.

### 4.24 The built loads, diseases, plants and markers
- **Slugs, aphids and ladybirds:** keep where they meet a sowing or picking decision; the misread larvae is excellent.
- **Fungi and poisonous mushrooms:** keep; knowledge as safety; extend to poisonous lookalike plants (§6 no. 16).
- **The mast:** keep as the shared pulse (D2-202); give it the race (§4.1 behaviour 4; §6 no. 19).
- **Markers:** keep only those with a lever this stretch (§3.5 F13).
- **Murrain, mange, hare sickness, swine fever:** keep; the lever that makes them social is quarantine (a collective choice) and
  burning carcasses (a cost someone bears for others).

### 4.25 Summary of verdicts

| Kind | Verdict |
|---|---|
| wild boar | keep; rework raider (stretch contest, spatial adversary, splitting, mast race); calibrate down; frontier kind |
| red deer | keep; restore raid under forest law; harbourer, venison gifts, count |
| roe | keep cheap; the commoner's deer; bark as sentinel |
| wolf | keep in frontier and upland; circuit across villages; bounty as institution; folding |
| fox | keep cheap; lapse prober with hamlet externality; treadmill |
| bear | keep rare; the cached carcass |
| hare | keep cheap; merge gear with rabbits and partridge |
| woodpigeon | rework as social follower with displacement; merge into birds at the corn |
| rook | keep; trade-off shown both ways; central-place |
| raven | keep as carcass informant; merge memory with corvids |
| voles, owls, kestrels | keep as lore; build the owl hole and mowing-to-ricks now |
| rats, mice | keep and deepen: the cat, the rat-catcher |
| wildfowl | keep; flight lines; the decoy |
| eel | keep; idiographic lag; eel rents; traps as property |
| salmon | build with the eel; the gap in the weir |
| trout | cut (water pack's stock) |
| otter | defer; into the fishpond composite |
| heron | keep; tie to heron-hawking |
| beaver | keep frontier; the downstream meadow quarrel |
| wild bees | build early with husbandry; bee-lining as triangulation; wax |
| pine marten | defer; into mustelids |
| falcon | rework: goshawk and sparrowhawk; bond; serjeanty |
| swan | keep, early with rights |
| loads, diseases, plants, markers | keep those with a lever; cut markers without one |

## 5. New types of mechanism

Each: how it would work in this engine; what it teaches or creates socially; its risks. All act through the animal interface and
the engine's primitives (D2-203), with keyed randomness, and replay exactly.

### M1 Shared perception: animals notice people by the same rule people use
- **How:** a module's "what is there" call becomes the noticing rule run from the animal's side: for each person (or dog, fire,
  noise) within reach, a chance from the kind's senses (A1: nose, eyes, ears with their `own` strengths) x the visibility for that
  sense (cover, the dark, fog; for smell, the **wind's direction** relative to the two parcels, which needs a wind-direction field in
  the climate: an engine gap) x presence (steps in the parcel graph) x the person's **conspicuousness** (crew size, a dog, noise of
  gear, a light, moving fast or still, carried meat or blood). A hunt's approach, a watch's light, a poacher's crossing of a wood,
  a decoyman's silence and a child scaring birds all resolve through it.
- **Teaches:** one physical lesson across kinds (come upwind and you are smelt; a light is seen far off; a crew is heard), so
  knowledge carries between kinds where it should and fails where the kind's senses differ (pigeons do not smell you; deer do).
- **Socially:** quiet as a skill (a stalker, a decoyman, a poacher); crew size has a cost as well as a benefit (more hands, more
  noise), so who goes with whom matters.
- **Risks:** cost (a person-by-group check each night: bounded by only checking groups within two steps of people); a new climate
  field; agents cannot see the wind's direction unless it is in the "Now" section (add it there).

### M2 The stretch contest
- **How:** a contest that repeats nightly in real life is resolved once per engine night as a contest between portfolios: the
  household's deterrents over the stretch (the set of distinct scares held, the share of the stretch watched, a dog, harm done)
  against the group's habits (habituation per scare, wariness from harm, hunger). The outcome is a share of the stretch's raid
  nights turned (D2-198's answers become curves over the number of distinct scares). The watcher's cost follows D2-21 (the night's
  sleep, the guard's food, units off tomorrow) for each person watching, scaled to the share watched.
- **Teaches:** variety as possession and cooperation, not as a nightly trick.
- **Socially:** dogs, clappers, horns and boys become things to own, lend and hire; a household with one scare needs a neighbour
  with another.
- **Risks:** abstracting the night loses the drama of one night's meeting; keep the watcher's one vivid line (the crash at midnight)
  as the stretch's representative event.

### M3 Displacement and externalities
- **How:** when a group is turned or a flock lifted, its module chooses the next target the same stretch from its known places;
  when a lapse prober feeds, its memory raises the probe rate for the whole hamlet; when a territorial holder dies, the ring refills
  it after N engine days unless the ring's own holders are also gone.
- **Teaches:** P21 (my defence is your loss) and P22 (control works only at scale).
- **Socially:** the reason for a rota, a common fence, a bird-scaring boy paid by several households, an inter-village cull, a by-law
  ("every house shall shut its hens at dusk"), and quarrels when someone free-rides.
- **Risks:** zero-sum feelings may make agents hostile rather than cooperative; that is a legitimate outcome, but measure it.

### M4 The route graph (desire lines)
- **How:** per group, a weighted graph over parcels and areas; edges strengthen with use and fade without it; blocked or harmed
  edges lose weight; new edges are explored rarely and mostly when old ones close. Hedges have gaps as parcel-edge features; a route
  through a gap is a trace ("a rack broken through the thorn hedge at Ash Field").
- **Teaches:** place (P2) as a network: block one way and the animal finds the next; and the long memory of routes (the same rack
  used for years).
- **Socially:** a gap in a common hedge is the hayward's business; blocking a route onto your land can send it onto a neighbour's.
- **Risks:** more state per group; keep edges few (the group's top five).

### M5 Personality and selective harvest
- **How:** each group or individual (and each density kind, as a distribution) carries a bold-shy trait. Takes, traps and easy
  shots take the bold first [21]. The remaining population is shyer: it raids less, is harder to snare and to find, and breeds as
  before. Catch per effort falls faster than the stock (hyperdepletion), and raids fall while numbers hold.
- **Teaches:** a misread (P11: "we have killed most of them" when only the bold are gone); and restraint read through effort.
- **Socially:** the hunter's tally becomes misleading evidence; a warrener's count and a trapper's catch can disagree, which is a
  dispute about evidence (P23).
- **Risks:** a hidden variable with subtle effects; give it signs (the shy remaining "never show by day now"; snares sprung and
  empty).

### M6 Culture in animals
- **How:** a group's learned stores (places, routes, scares, a trick such as lifting a latch) belong to its knowledge holder and are
  passed to its young and to groups it meets, with conformity [23]. A trick learned by one sounder or one fox family can spread
  across villages over seasons; killing the holder can erase it.
- **Teaches:** that an animal problem can be new and can travel ("they never used to open the hurdles").
- **Socially:** news of a trick travels between villages as talk; lore can lag the animals.
- **Risks:** invention must be rare and named; agents may attribute a spreading trick to sorcery or a neighbour (which is a story,
  not a failure).

### M7 Sentinels and alarm networks
- **How:** kinds with an alarm module (jays, blackbirds, magpies, wrens, geese, roe barking, dogs) emit an alarm sound sign at an
  intruder (a fox, a hawk, a person), with its own `own` and reach. Other kinds' modules read alarms (deer leave a parcel whose jays
  are scolding); so do people (the knack of reading alarms: "the jays are going off in Hanger Wood, and nobody of ours is there").
  A fast-moving or noisy person pushes a band of alarm ahead (Young's "bird plough"); a still person lets the baseline return.
- **Teaches:** reading others through animals (P16) in both directions; patience and stillness as craft.
- **Socially:** a keeper can find a poacher by the jays (evidence of presence); a poacher learns to move like a stalker; geese as the
  household's watch.
- **Risks:** a lot of sound signs; keep alarms to parcels with people near and to readers with the knack, and gate them by the
  attention budget.

### M8 Animals that remember people
- **How:** kinds with face memory (crows, ravens, magpies, jays, geese, dogs, tamed beasts) hold a `people` store: person id to
  standing (harmed us, fed us), shared within the group and passed on socially, decaying over seasons [24]. They mob or follow that
  person; the mobbing is a sign others see ("the crows go up screaming wherever Wat walks").
- **Teaches:** that animals carry reputations.
- **Socially:** evidence: the crows' hostility marks the one who has been trapping or shooting them (a poacher, a warrener, a nest
  robber); a dog that knows a man reveals he has been to a house. This is information leverage that does not depend on anyone
  speaking.
- **Risks:** it could feel like magic surveillance; keep it to kinds where it is real, keep the sign plain and occasional.

### M9 Commensal niches set by waste and buildings
- **How:** each settlement keeps a few waste and structure stocks: the midden (refuse, offal), the threshing floor's spill, thatch,
  eaves, chimneys, timber. Commensal kinds' habitat is those stocks (kites and ravens at offal, sparrows at spill, black rats in
  thatch, jackdaws in chimneys, house martins at eaves, deathwatch beetle in old oak). People's choices (where the midden is, whether
  offal is buried, whether chimneys are capped, how stores are built) set which commensals live there and how many.
- **Teaches:** that a village's own habits make its ecology (P10).
- **Socially:** sanitation and building become shared choices with shared costs (the midden by the well; a neighbour's offal pit).
- **Risks:** a new stock family; keep to three or four waste stocks.

### M10 Provisioning and cultivated allies
- **How:** fittings and acts that invite an ally: an owl hole in a barn gable; a dovecote (a lord's privilege); nest sites for
  martins (luck in folklore; insects eaten); feeding the cat; leaving the rookery; a heronry kept quiet. Each ally lowers a pest load
  in its radius and costs something (a gap in a wall, grain to the doves, the dovecote's pigeons eating neighbours' seed).
- **Teaches:** investment with a lag and a radius.
- **Socially:** a dovecote's birds eat the villagers' corn (a grievance famous in France); an owl helps only its barn.
- **Risks:** small effects; build only the owl hole and the dovecote at first.

### M11 Deception and signalling
- **How:** people's decoys and lures (decoy birds, a doe's call, a stalking horse, scent baits, a tame decoy duck, bird lime) work
  through the kind's decision rule (social followers come to decoys; habit raiders do not); scarecrows decay as the kind learns (A3).
  Animals deceive too: the lapwing's broken-wing display leads an egg-gatherer away from the nest [44], so the knack is to watch
  where the bird *came from*; the cuckoo's egg in another's nest.
- **Teaches:** misreads (P11) as craft; the expert reads the deception.
- **Socially:** people deceive each other through animals (a dog's head for a wolf's at the bounty; a poacher's snares on a
  neighbour's run so the neighbour is blamed).
- **Risks:** few; keep each deception tied to a concrete act and a concrete sign.

### M12 Long projects and wild capital
- **How:** structures that take many units over many days and pay over years: a warren (pillow mounds, a lodge), a decoy pond (pipes,
  screens), a fishpond (a dam, stocking), a deer park (a pale, a leap), a heronry protected, a coppice in rotation, a hedge laid.
  Each is a building or a parcel feature with an owner, upkeep and decay; it persists across continued runs.
- **Teaches:** the long run (restraint and investment) inside runs as building and outside them as inheritance.
- **Socially:** wild capital is held, rented, inherited and fought over; it makes the holder a chokepoint (the decoyman, the
  warrener).
- **Risks:** it may only pay off beyond a run; give each a first return within a run (the first rabbits in a season; the first
  pipe of ducks in a winter stretch).

### M13 Obligations denominated in wild things
- **How:** agreements and seeded customs can name wild goods or wild services: rents in eels by the stick [34], a lamprey pie owed to
  the lord, a sparrowhawk kept for the king (serjeanty) [35], pannage paid in pigs, a bounty in heads paid from a common purse [37].
  Each obligation is a DUE item with a creditor and a date.
- **Teaches:** that a stock's yield is spoken for.
- **Socially:** the obligation forces a crew, a specialist or a purchase; a short year makes debt; a collector must judge evidence.
  This is scenario_design's "enforcement that needs people to act".
- **Risks:** needs the agreements system to carry goods and services; small worlds may have no lord to owe.

### M14 Laws that constrain levers
- **How:** world rules that change which acts are allowed and what they do: lawed dogs cannot catch deer; fences in the forest may
  not exceed a height; the fence month bars grazing and disturbance in the wood for about four engine days around midsummer [28]; a
  weir's close time; a licence to empark; a closed season on hinds. Breaking a rule is possible and leaves traces that a warden can
  find and present.
- **Teaches:** that the law shapes the ecology people face.
- **Socially:** enforcers (forester, regarder, verderer, water bailiff) and courts; grievance; petitions; poaching as resistance.
- **Risks:** heavy for small worlds; make it a world option and verify every access gate in a dry run (scenario_design §4: the
  March's forest law blocked foraging but not hunting).

### M15 Places that remember, and quirks
- **How:** the generator's history before the run leaves particulars in the land: place names from events (Wolfpit, Boar's Hill,
  Cockshoot, Hartley), a field where cattle dead of the black bane (anthrax) were buried (§6 no. 36), a wood whose oaks mast together, a river's lag, a
  heronry's tolerance, a sounder's gap. Each world seeds **quirks**: values that keep the real direction but differ in magnitude,
  threshold or place.
- **Teaches:** P24, the particular; and why an elder or a local expert is worth more than general knowledge.
- **Socially:** dependence on locals; miscalibrated lore from another village; a stranger who reads the land wrongly.
- **Risks:** quirks must stay plausible; a model that knows the real rule should not be punished for it, only out-performed by a
  local.

### M16 Contested attribution
- **How:** every damage event carries its true cause in the state and signs designed to tell kinds apart (rooted strips against bitten
  tops against nibbled edges; a fox's neat head bite against a dog's mauling; a wolf's straight line of tracks against a dog's
  wandering); readings by skill give the cause; the untaught reading may name the wrong kind or a person.
- **Teaches:** P19.
- **Socially:** the neighbour's dog accused of the fox's work; a poacher's kill blamed on wolves; compensation that depends on cause.
- **Risks:** low; it is mostly sign work.

### M17 Races for a ripening pulse
- **How:** a shared stock that ripens over a window (hazel nuts, acorns, beech mast, berries, apples) is drawn by wild kinds
  (squirrels, jays, mice, pigeons, boar, badgers) from before ripeness; people who wait for ripeness get less; people who take early
  get poorer goods. A customary opening day (the nutting day, the pannage day) is an institution that holds everyone back to the
  same date.
- **Teaches:** timing against competitors, and the commons problem in time rather than in amount.
- **Socially:** the custom, its breakers, and quarrels over early gathering.
- **Risks:** small food values (nuts about a tenth of autumn need): enough for a custom, not for a crisis.

### M18 The carcass as an object with stakeholders
- **How:** any death in the land (a wolf's kill, a murrain cow, a deer wounded and lost, a poached deer's leavings) makes a carcass
  thing with an owner (or none), a claim (whose deer), a disease load, and an attraction to scavengers (ravens within a day, then
  foxes, wolves, a bear that caches it). Its signs travel far (ravens over it) and linger (bones).
- **Teaches:** reading the land through carcasses; danger at a carcass (§4.6).
- **Socially:** a carcass is evidence (a poached deer's umbles in someone's pot; murrain carried by moving a carcass), a claim and a
  hazard; burning one is a cost for others' benefit.
- **Risks:** low; carcass things exist (things.py); this generalises them.

## 6. New wildlife and composite systems (39)

Each entry gives: natural history in brief; its **constitution** (§1.3 organs A1-A8; only those that matter); the **behaviours**
worth building, with state and rules; **signs**; **levers**; the **learning problems** (P numbers, §1.3 of the proposal and §3.7
here); **connections** to other kinds and to economy, law and stories; the **social footprint** (purpose from the brief; who needs
whom; what is held, traded, enforced or argued; the null-arm signature); **relevance**; why it is **not redundant**; **risks**; and
a **cost** (S under 300 lines, M 300 to 1,000, L more). Ranked by value for cost at the end (§6.8).

### 6.1 The village, its buildings and stores

**1. The cat (the mouser that chooses its house).**
- *Natural history:* half-wild in the period, living on mice and rats about barns and houses, breeding freely, attaching itself to
  places and people that suit it; folklore both fond and suspicious.
- *Constitution:* A2 forager by value over the settlement's stores; A3 place memory; A4 solitary; A5 individuals; A6 middling;
  A7 home range over a few buildings.
- *Behaviours:* (1) **choosing a house**: a stray cat settles at the building with the most mice and the most scraps, and a household
  that feeds it a little (milk, offal) and keeps no dog that chases it keeps it; it may leave for a better house. (2) **the radius**:
  mice and rats in the buildings within its range fall by a share each stretch (most in the barn it favours). (3) **breeding**: kittens
  each spring; surplus kittens are given away (a small gift economy) or drowned (a dark lever). (4) **the cat's own risks**: foxes, dogs,
  traps set for rats.
- *Signs:* "a grey cat sleeping on the sacks in Hale's barn"; "a row of dead mice laid on the doorstone"; "the cat has gone over to
  Wat's".
- *Levers:* feed it; keep the dog off it; give a kitten; set traps carefully.
- *Learning:* P10, P11 (the door does nothing, the cat does), P19 (whose cat?).
- *Connections:* rats and mice; the barn owl (competition and complement); dogs; terriers.
- *Social footprint:* 3.1 small (a kitten from a good mouser is wanted), 3.5 (the household whose cat leaves). Null arm: no cats
  passed between households.
- *Relevance:* rats and mice cost about 5% of need; a cat halves its barn's share: passes for a store-heavy household.
- *Not redundant:* the only ally with its own choice; DF's lesson (cats choosing owners) made into a household tie.
- *Risks:* catsplosion; bound breeding by mice and scraps. *Cost:* S.

**2. Red kite and the midden (with the scavengers of the settlement).**
- *Natural history:* kites (and ravens) scavenged refuse in medieval and early modern towns and villages, snatched food, and took
  chicks; tolerated as cleaners in towns while counted vermin elsewhere [38].
- *Constitution:* A2 central-place from a nest wood, forager on the waste stock; A3 place memory; A4 loose groups at food; A6
  middling.
- *Behaviours:* (1) **the waste stream as habitat** (§5, M9): the midden's offal and refuse stock sets how many kites, crows, rats and
  dogs work the settlement. (2) **cleaning**: scavengers lower the midden's stock, which lowers flies and stink (a small health term
  when illness exists). (3) **snatching**: kites take a share of food left out to dry (fish, meat) and of young chicks. (4) **nesting
  with rags**: kites line nests with rags and washing taken from hedges (a folkloric and real habit) [a minor sign].
- *Signs:* "kites wheeling low over the midden"; "a kite took a fish off the drying rack".
- *Levers:* bury offal (fewer kites, more work); guard the drying racks; shoot or leave the kites.
- *Learning:* P10 (cleaner and thief).
- *Connections:* rats (competing for the midden); ravens; the slaughter bundle's leavings (signs.py already has crows over leavings).
- *Social footprint:* 3.5 (whose rack), 3.2 (where the midden is and who keeps it: a shared nuisance). Null arm: no midden rule.
- *Relevance:* small as food; moderate as a shared choice. *Not redundant:* the only kind whose numbers people set by sanitation.
- *Risks:* low value in small hamlets. *Cost:* S (with M9).

**3. Carrion crow and magpie (corvids that remember people).**
- *Natural history:* crows and magpies take eggs and chicks, peck the eyes of weak lambs, pull seed; they mob predators and people
  who harm them, and learn dangerous faces from each other for years [24]; Tudor vermin acts paid for their heads [37].
- *Constitution:* A1 eyes; A3 memory of individual people; A4 pairs with territories and winter flocks; alarm calls (M7).
- *Behaviours:* (1) **the people store** (§5, M8): a person who traps, shoots or robs their nests is mobbed wherever they go within the
  pair's territory; others learn it. (2) **egg and chick theft** from hens and wild nests near cover. (3) **the lambing field**:
  crows at weak lambs. (4) **sentinel**: their alarm marks a fox or a person in the wood.
- *Signs:* "the crows went up screaming over Wat as he crossed the Long Field"; "two crows at the ewe that is down in the far pasture".
- *Levers:* shoot or trap them (and be marked); a lamb watched; eggs collected early.
- *Learning:* P16 (reading people through animals), P19.
- *Connections:* vermin bounties; the warrener and the keeper (who are mobbed); lambs (husbandry).
- *Social footprint:* 3.3 and 3.7: the crows' mobbing is evidence about who has been trapping in a wood (a poacher, a keeper's
  rival); a bounty on heads needs a collector. Null arm: no animal-borne evidence about people.
- *Relevance:* small in food; real in information. *Not redundant:* the only kind that carries a person's reputation.
- *Risks:* reads as surveillance; keep rare. *Cost:* S-M (with M8).

**4. House sparrow and the threshing floor.**
- *Natural history:* sparrows nest in thatch and eaves and feed on spilt and stored grain, worst at threshing and in ricks; parishes
  later paid for their heads (sparrow clubs).
- *Constitution:* A2 social follower on spill; A4 flocks; A7 site-bound to buildings; A3 little memory.
- *Behaviours:* (1) **the spill stock**: threshing in the open leaves a spill share that sparrows take; a barn floor with doors shut
  leaves less. (2) **ricks** thatched poorly are entered. (3) **nests in thatch** (a small wear on roofs; luck lore).
- *Signs:* "sparrows thick on the threshing floor as soon as the flails stop".
- *Levers:* thresh in the barn; net the eaves at dusk (sparrow batfowling: a clap net and a light at night, a real village pastime);
  pay for heads.
- *Learning:* P10. *Connections:* the threshing technique; thatch; vermin bounties.
- *Social footprint:* 3.2 small (a parish bounty). Null arm: no bounty.
- *Relevance:* a few per cent of grain where threshing is outdoors. *Not redundant:* the one granivore tied to people's work
  rather than fields. *Risks:* low interest alone; build as part of "birds at the corn". *Cost:* S.

**5. Jackdaw in the chimney.**
- *Natural history:* jackdaws nest in chimneys, church towers and hollow trees, dropping sticks down a flue until it blocks; smoke
  backs up; nests can catch fire.
- *Constitution:* A7 site-bound to chimneys and towers; A4 colonies; A6 annual (nests each spring).
- *Behaviours:* (1) **the spring nest**: an uncapped flue unused for a few days in spring gets a nest; (2) **blocked flue**: the next
  fire smokes the house (a health and comfort cost) and has a small chance to set the nest alight and the thatch with it (ties to the
  fire bundle); (3) **sweeping** clears it.
- *Signs:* "sticks falling into the hearth at Hale House"; "smoke pouring back into the room".
- *Levers:* cap the chimney (a fitting), light a fire daily in spring, sweep.
- *Learning:* P1 (spring), P10. *Connections:* buildings, fire, fuel.
- *Social footprint:* 3.5 small; a chimney-sweep as a service where chimneys exist. Null arm: no sweeping.
- *Relevance:* rare but sharp (a house fire). *Not redundant:* the only kind that endangers a building. *Risks:* chimneys may be rare in
  the era's houses (open hearths with smoke holes); check the building catalogue. *Cost:* S.

**6. Deathwatch beetle, woodworm and dry rot (the house that is eaten).**
- *Natural history:* beetle larvae bore oak and other timber for years; the deathwatch's tapping at night in spring was taken as an
  omen of death in the house; damp timber rots.
- *Constitution:* A2 none (structural); A6 slow (years in timber); A8 effect on the building's wear.
- *Behaviours:* (1) **a load per building** by timber, damp and age, raising its wear rate; (2) **the tapping** in spring nights as a
  sign with a famous misread (an omen of death); (3) **damp** (no gutter, earth against the wall) speeds it.
- *Signs:* "a dry ticking in the roof timbers in the night"; "fine dust under the beam".
- *Levers:* replace timbers; keep timber dry; choose seasoned oak.
- *Learning:* P11 (the omen), P10. *Connections:* buildings' wear (engine has wear); timber types (D2-191's wood types).
- *Social footprint:* 3.7 (an omen talked of); a carpenter's work. Null arm: no omens tied to buildings.
- *Relevance:* small, slow. *Not redundant:* the only kind on the built fabric. *Risks:* slow; mostly lore. *Cost:* S.

**7. The store's slow pests: grain weevil, clothes moth and mites.**
- *Natural history:* weevils breed in warm, damp grain, which heats; moths eat wool, fur and feathers in chests; mites in flour.
- *Constitution:* A6 fast (weeks); A2 structural; loads per container.
- *Behaviours:* (1) **the heating heap**: grain stored damp or deep warms, and weevils multiply; turning the heap and drying it stops
  them; (2) **the wool chest**: wool, fur and down lose a share each warm stretch unless aired, beaten or kept with strong-smelling
  herbs (which the lore over-credits); (3) furs and feathers become goods that need care, which makes a furrier's or a
  housewife's knowledge worth something.
- *Signs:* "the grain in the bin is warm to the hand and smells sour"; "moth in the fleece chest".
- *Levers:* dry the grain before storing; turn it; air the wool; beat the furs.
- *Learning:* P11 (herbs), P13. *Connections:* stores; furs (wildlife goods); down and feathers.
- *Social footprint:* 3.6 (preparation); small. Null arm: none much.
- *Relevance:* a few per cent of stored grain in a wet harvest; more once wool and furs are goods. *Not redundant:* gives the
  wild goods a cost of keeping. *Cost:* S.

### 6.2 Fields, meadows and grazing

**8. Rabbit and the warren (a wild-kept boundary).**
- *Natural history:* introduced (or reintroduced) by the Normans; kept in warrens on light soils, with pillow mounds, a warrener
  in a lodge paying high rent in carcasses or money; free warren a granted right; ferrets and nets to take them; escapes became wild
  populations that grazed turf and crops; poaching common [31].
- *Constitution:* A2 forager by value from the burrow (central place); A4 colonies; A5 density; A6 fast (several litters a year);
  A7 site-bound to the warren and its banks; A8 engineer (turf, sand).
- *Behaviours:* (1) **the warren as a held structure** (§5, M12): mounds built with units, a lodge, a holder, a rent; numbers grow
  fast on light soil; the warrener takes a share by ferret and net each winter stretch. (2) **the warren's edge**: rabbits graze the
  neighbours' crops and pasture within a radius (a cost the holder does not bear). (3) **escape and feral**: a warren unkept, or banks
  broken, leaks rabbits that found wild colonies; over years they become a pest on the commons. (4) **poaching**: at night with nets
  and a dog; the warrener watches from the lodge.
- *Signs:* "the barley next to the warren grazed down in a band"; "purse nets left by a burrow mouth".
- *Levers:* build, keep, ferret, net; fence the crop; petition the holder; poach.
- *Learning:* P5 (take within the warren's growth), P18 (property in a wild-kept thing), P21 (the edge cost).
- *Connections:* ferrets (a bonded beast, F11); stoats (predators); foxes; soils (light, sandy); the lord's right.
- *Social footprint:* 3.1 (the warrener as specialist and chokepoint, holding rent and stock), 3.4 (feral rabbits on the commons),
  3.5 (the neighbours' crops), 3.7 (poaching, rights). Who needs whom: the lord needs the warrener; the warrener needs ferrets and
  nets; neighbours need the holder to fence or pay. Null arm: no warrener, no rent, no edge quarrel.
- *Relevance:* rabbits gave meat and fur valued in the period; a warren's edge can cost a neighbour's field 5-10%.
- *Not redundant:* the only kind that sits deliberately between wild and kept, with a holder.
- *Risks:* rabbits as pests can dominate if feral spread is fast; slow the feral phase. *Cost:* M.

**9. Mole and the mole-catcher.**
- *Natural history:* moles throw hills in meadows and pasture, worst in wet spring and autumn; soil in the hay spoils it and blunts
  scythes; mole-catchers were parish or farm employees paid per mole; moleskins sold.
- *Constitution:* A2 forager on soil invertebrates; A6 middling; A7 territory in the soil; A8 engineer (hills).
- *Behaviours:* (1) **molehills by soil wetness and worms** on meadow parcels; (2) **the hay penalty**: hills not harrowed before
  mowing lower the hay's yield and quality; (3) **trapping** as a skill: traps set in the runs, checked, a knack to find the main run;
  (4) a meadow cleared refills from the hedges in a season.
- *Signs:* "fresh molehills across the hay meadow after the rain".
- *Levers:* harrow the hills (units in spring); hire the mole-catcher; trap.
- *Learning:* P15, P1. *Connections:* hay; worms (soil wetness); moleskins as a good.
- *Social footprint:* 3.1 and 3.2: a mole-catcher hired by several households or the village (a pooled payment with free-riders
  whose meadows adjoin). Null arm: no catcher.
- *Relevance:* a few per cent of hay; the hay is winter feed, so more in a hay-short year.
- *Not redundant:* a cheap paid specialist in every village with meadow. *Risks:* small. *Cost:* S.

**10. Grey partridge and quail (the stubble game).**
- *Natural history:* coveys on stubble and field edges; nest in hay and corn margins; taken with a setting dog and a drawn net (the
  dog points, the net is drawn over the crouched covey), or with hawks; the hay harvest destroys nests.
- *Constitution:* A1 eyes; A2 social (covey); A3 little; A6 annual; A7 home range in fields.
- *Behaviours:* (1) **the covey crouches** at a dog's point, which is what the net needs; (2) **the setting dog** as a bonded trained
  beast (F11); (3) **nest loss at mowing** sets next year's coveys.
- *Signs:* "a covey of about twelve on the barley stubble at dusk".
- *Levers:* net with a setting dog; mow late or from the middle out; leave margins.
- *Learning:* P17 (training the dog), P5. *Connections:* hawks; hay timing; foxes.
- *Social footprint:* 3.1 (the dog's trainer), 3.7 (game rights later). Null arm: no setting dog.
- *Relevance:* small food; a sport. *Not redundant:* the cooperative take between a dog and a net. *Cost:* S-M.

**11. Corncrake in the hay.**
- *Natural history:* calls "crex crex" all night from the hay meadows in May and June; nests in the hay; mowing from the outside in
  kills chicks and adults that run to the middle.
- *Constitution:* A6 annual migrant; A7 site-bound to tall grass; A2 none much.
- *Behaviours:* (1) **the call** as a marker of the hay's growth; (2) **mowing pattern**: mown from the outside in, the birds die in
  the last stand; from the middle out, they escape; (3) **return** next year by how many escaped (a slow arm).
- *Signs:* "a corncrake rasping all night in the Lammas meadow".
- *Levers:* mow middle-out; leave a strip.
- *Learning:* P5, P6. *Connections:* hay; partridge.
- *Social footprint:* small; a custom or not. Null arm: none.
- *Relevance:* small. *Not redundant:* a restraint lever inside an ordinary farm act. *Risks:* low value. *Cost:* S. (Low rank.)

**12. Lapwing and the egg harvest.**
- *Natural history:* lapwings nest on open fields and wet grass in spring; eggs gathered as a delicacy (the race for the first egg
  survives as a Frisian custom); a robbed nest is relaid; the adult's distraction display leads intruders away [44].
- *Constitution:* A1 eyes; A4 loose colonies; A6 annual; A7 site-bound to open wet ground; deception (M11).
- *Behaviours:* (1) **relaying**: a first clutch taken is relaid within days (an engine day); a second taken is not; (2) **the display**:
  the untaught follows the bird, the expert watches where it rose from; (3) **the first egg**: a prestige find (a custom).
- *Signs:* "a peewit tumbling and crying over the wet pasture, dragging a wing".
- *Levers:* take the first clutch only (restraint); find nests by the knack.
- *Learning:* P5, P11. *Connections:* plovers (the freeze sign); crows (who also take eggs).
- *Social footprint:* 3.4 (a custom of first clutch only), 3.7 (the first egg's prestige). Null arm: no custom.
- *Relevance:* small food in the hungry spring gap (which matters: wild_plants found spring's gap the leanest). *Not redundant:* a
  restraint with a quick test inside a run. *Cost:* S.

**13. Adder.**
- *Natural history:* basks on heath, banks and hay meadows in spring; bites haymakers, children, dogs and cattle; rarely kills a
  healthy adult; folk cures mostly useless.
- *Constitution:* A6 hibernates; A7 site-bound to basking banks; A8 danger.
- *Behaviours:* (1) **danger by season and place** (spring basking banks; hay meadows at mowing); (2) **bites** to dogs and calves; (3)
  **the cure lore** (wrong but persistent: adder's fat, charms).
- *Signs:* "an adder coiled on the warm bank by the gate"; "the dog's face swollen after the heath".
- *Levers:* boots; beat ahead with a stick; keep children off the bank.
- *Learning:* P14, P11. *Connections:* heath; dogs; illness in people (when it exists).
- *Social footprint:* small; a healer's demand. Null arm: none. *Relevance:* rare. *Not redundant:* danger in ordinary work, not
  hunting. *Risks:* needs illness in people. *Cost:* S. (Defer until illness exists.)

**14. Warble and horse-flies (the gadding herd).**
- *Natural history:* on hot, sunny, still days in early summer, warble (heel) flies laying on cattle's legs set them galloping with
  tails up ("gadding"), through fences and into crops; cattle seek water and shade; milk and weight fall [46].
- *Constitution:* A6 fast and weather-triggered (a load); A2 none; A8 effect on kept beasts' behaviour.
- *Behaviours:* (1) **gadding** on hot still days: herds on open pasture break out with a chance by fence and distance to crops;
  (2) **water and shade** cut it (a herd with a pond or a wood stands quiet); (3) **milk** falls that stretch.
- *Signs:* "the cows came galloping down the pasture with their tails in the air and went through the hedge".
- *Levers:* graze at dawn and dusk, house at midday; a pond or shade; mend the hedge.
- *Learning:* P1, P19 (the untaught blames the herder). *Connections:* herds (exists), fences (exists), crops.
- *Social footprint:* 3.5 and 3.2: one herd breaking into another's crop is a damage dispute (who pays?), and a herder's duty.
  Null arm: no gadding disputes.
- *Relevance:* modest; sharp on a bad day. *Not redundant:* a wild insect acting through kept beasts on neighbours' fields; uses
  what the engine already has (herds, fences, trampling). *Cost:* S.

**15. Cockchafer, crane fly and wireworm (the grub years).**
- *Natural history:* chafer grubs live three to four years in soil and fly in great years; leatherjackets follow a wet September;
  wireworm follows ploughed old grass; rooks and starlings eat them (wild_systems already catalogues these).
- *Constitution:* A6 cohort clocks; loads in soil.
- *Behaviours:* (1) **the spadeful count** as a forecast (an act: dig and count); (2) **rooks on the parcel** lower the load (§4.9);
  (3) **ploughing old grass** starts wireworm for the next crops.
- *Signs:* "fat white grubs in every spadeful"; "thin yellow patches in the barley on the old pasture".
- *Levers:* fallow; plough and let the rooks in; choose the crop.
- *Learning:* P8 (with rooks), P9, P10. *Connections:* rooks; the plough; the field's history (M15).
- *Social footprint:* small; with rooks, the rookery quarrel. Null arm: none. *Relevance:* real in grub years (root damage of a
  tenth). *Not redundant:* the proposal dropped them; they are the rook's other half. *Cost:* S (loads exist).

**16. Poisonous lookalikes: hemlock, water dropwort, ragwort and yew.**
- *Natural history:* hemlock and hemlock water dropwort resemble wild parsnip, celery and chervil and kill; ragwort poisons stock
  slowly; yew kills cattle and horses that eat clippings, while its wood made bows.
- *Constitution:* plants as actors: A8 danger; A7 site-bound (water's edge, churchyards, waste).
- *Behaviours:* (1) **the gatherer's misread** (D2-201's mushroom rule extended): an untaught gatherer of roots by water may take
  dropwort; (2) **yew in the pasture**: clippings or a fallen branch kill a beast within a day; (3) **ragwort** in hay harms stock over a
  season (cumulative).
- *Signs:* "white umbels by the ditch; a root like a parsnip"; "a cow dead by the churchyard wall, yew needles in her mouth".
- *Levers:* teach; clear the clippings; pull the ragwort (a common duty).
- *Learning:* P11, knowledge as safety (wildlife.md §11). *Connections:* gathering; herds; bows (yew staves).
- *Social footprint:* 3.3 (who knows what is safe: a dependence on the wise), 3.2 (ragwort pulling as a duty), 3.7 (the churchyard
  yew). Null arm: no teaching of plants.
- *Relevance:* rare but grave. *Not redundant:* extends a built rule cheaply. *Risks:* needs illness and beast deaths (exist for
  beasts). *Cost:* S.

**17. Bracken, gorse and blackthorn (the encroaching commons).**
- *Natural history:* bracken spreads over under-grazed ground and is cut for bedding and potash; gorse burns hot (oven fuel) and is
  burned in strips; blackthorn suckers across neglected field edges; rights of cutting (estovers, turbary) regulated their use.
- *Constitution:* plants as engineers: A6 slow (seasons to years); A7 spreading by parcel edges.
- *Behaviours:* (1) **encroachment** on parcels by grazing and cutting pressure (succession, wild_plants step 4); (2) **cutting rights**
  (each household may cut so much a season); (3) **gorse fire**: burned in strips in late winter, a fire risk when wind turns.
- *Signs:* "bracken creeping down from the heath into the top pasture".
- *Levers:* graze cattle (they trample bracken), cut, burn.
- *Learning:* P10, the long run. *Connections:* pasture; ovens and fuel; bedding; fire.
- *Social footprint:* 3.4 (the common's upkeep is everyone's; rights of cutting), 3.9. Null arm: no cutting rules.
- *Relevance:* slow but cumulative on pasture. *Not redundant:* the commons that degrades without use, the opposite of overuse.
  *Cost:* S-M (with succession).

### 6.3 Woods

**18. Jay (the sentinel and the planter).**
- *Natural history:* jays scold loudly at foxes, owls, hawks and people in the wood ("the keeper's policeman"); each autumn a jay
  caches thousands of acorns, many forgotten, so jays plant oaks, notably in open ground next to woods.
- *Constitution:* A1 eyes; A4 alarm module (M7); A3 cache memory; A8 engineer (oak regeneration); A6 annual.
- *Behaviours:* (1) **alarm**: an intruder within a jay's parcel triggers a scold carried by sound; deer and boar modules leave a
  scolding parcel; people with the knack read who or what (§5, M7); (2) **caching**: in a mast autumn jays take a share of acorns
  from the wood's stock (the race, M17) and plant a share in adjoining open parcels, where oak seedlings appear in later years
  (succession).
- *Signs:* "a jay screaming in Hanger Wood, then another further in"; "young oaks coming up in the rough pasture under the wood".
- *Levers:* move slowly in the wood; read the jays to find a poacher or a fox.
- *Learning:* P16 both ways, P2. *Connections:* deer and boar (warned), the hunter (betrayed), the keeper (helped), mast, succession.
- *Social footprint:* 3.3 (evidence of presence in a wood; a keeper's tool), 3.9 (woods spreading where grazing is light). Null arm:
  stalks never spoiled by noise; no poacher found by birds.
- *Relevance:* indirect but broad (raises the value of stillness and of the stalker). *Not redundant:* the single most useful
  sentinel; the cheapest test of M7. *Cost:* S-M (with M7).

**19. Red squirrel and the nutting race.**
- *Natural history:* squirrels, jays, mice and woodpigeons take hazel nuts before they ripen; people gathered nuts on a customary
  nutting day (Holy Rood Day, 14 September, in English custom); squirrel fur (vair) was a major medieval fur, much of it imported.
- *Constitution:* A2 forager by value; A3 cache memory; A6 annual; A7 home range in woods with hazel.
- *Behaviours:* (1) **the race** (§5, M17): wild takers draw the hazel stock from late summer; each engine day earlier that people
  gather, they get more but less ripe nuts (poorer keeping); (2) **the custom**: a nutting day agreed by the village holds everyone to
  one date; breakers take more and are resented; (3) **caches** found by people in winter (a small windfall).
- *Signs:* "half-eaten green nuts under the hazels already"; "squirrels busy in the coppice".
- *Levers:* gather early, wait for the day, trap squirrels (fur when furs have uses).
- *Learning:* P1, P5, P21. *Connections:* nuts (built plant stock), mice, jays, pigeons, furs.
- *Social footprint:* 3.4 (a timing commons with a custom), 3.7 (custom-breaking). Null arm: no nutting day.
- *Relevance:* nuts are about a tenth of autumn need where hazel is common (02zp part three). *Not redundant:* the commons problem in
  time. *Cost:* S.

**20. Badger and the sett.**
- *Natural history:* setts used for generations; badgers dig out wasps' and bees' nests, eat worms, windfall fruit, and some corn;
  their paths are fixed; baited and dug for sport; fat and hair used.
- *Constitution:* A7 site-bound (the sett) and fixed routes (M4); A4 clans; A6 slow; A8 engineer (setts undermine banks).
- *Behaviours:* (1) **fixed paths** from the sett to feeding grounds, through gaps that are a trace and a place to set a snare or a
  watch; (2) **digging** wasps' and bees' nests (a check on wasps; a threat to ground hives); (3) **the sett as a site** for generations;
  (4) **undermining** a bank or a dyke.
- *Signs:* "a broad path worn under the hedge to the sett"; "a wasps' nest dug out in the bank".
- *Levers:* leave the sett; dig it (crew, terriers, danger to dogs); block a path.
- *Learning:* P2, P10. *Connections:* wasps; bees; foxes (share setts); terriers.
- *Social footprint:* 3.7 (baiting as a sport and status display), small otherwise. Null arm: little.
- *Relevance:* small. *Not redundant:* an engineer and route-holder whose effects are mostly good. *Cost:* S. (Low rank.)

**21. Woodcock and the cockshoot.**
- *Natural history:* woodcock arrive in November with east winds and fly at dusk along fixed rides between wood and feeding fields;
  medieval fowlers hung nets across these glades ("cockshoots"; the place name survives).
- *Constitution:* A6 migrant on a wind cue; A7 fixed flight lines (M4); A2 cue-triggered.
- *Behaviours:* (1) **arrival** after an east wind (a cue in the weather); (2) **flight lines** through particular glades at dusk (an
  idiographic map); (3) **the cockshoot net** strung across a ride, a held place.
- *Signs:* "woodcock flighting low down the ride at dusk".
- *Levers:* hang a net in the right glade on the right evening; claim the cockshoot.
- *Learning:* P1, P2, P24. *Connections:* wildfowl (the freeze), the woodcock moon lore (a false cause).
- *Social footprint:* 3.1 (a held glade), 3.8. Null arm: no held cockshoot.
- *Relevance:* small. *Not redundant:* the purest particular-place fowling; cheap. *Cost:* S.

**22. Stoat, weasel, polecat and pine marten (the small-gap killers).**
- *Natural history:* weasels pass through a gap the size of a ring, stoats a little larger, polecats larger still; they kill hens and
  take eggs, rabbits and rats; polecats in particular kill many hens at once; furs (ermine from winter stoats; polecat "fitch"; marten).
- *Constitution:* A2 lapse prober by gap size (not by door); A4 solitary; A5 individuals; A6 middling.
- *Behaviours:* (1) **gap size**: each kind enters a structure whose smallest gap admits it; a shut door stops the fox but not the
  weasel; a mesh or a mended wall does (the misread that the door is enough, P11); (2) **rabbit and rat control**: they lower rabbits
  in a warren (the warrener's enemy) and rats in a barn (a farmer's friend); (3) **ermine** in a hard winter (fur).
- *Signs:* "two hens dead in the shut hen house, bitten at the neck, no way in but the crack by the sill".
- *Levers:* mend the crack; trap at the gap; keep them for the rats.
- *Learning:* P10, P11, P19. *Connections:* fox (contrast), rabbits, rats, warrens, furs.
- *Social footprint:* 3.5 small; the warrener and the farmer disagree on them (a quarrel of interest). Null arm: little.
- *Relevance:* small. *Not redundant:* the lesson that a defence is particular to a kind (the door against the fox, the mesh against
  the weasel), which the deep dive showed agents fail to learn; very cheap with the fox's prober. *Cost:* S.

**23. Oak caterpillar years (winter moth and the oak roller).**
- *Natural history:* in some springs caterpillars strip the oaks in May; the trees re-leaf at midsummer; the acorn crop that year is
  poor; birds feed their young on the caterpillars.
- *Constitution:* A6 a weather-triggered load in the canopy.
- *Behaviours:* (1) **defoliation** in a warm early spring after a mild winter; (2) **the mast cut** that autumn (couples to boar,
  pigeons, mice); (3) **a bird year** (tits, more young).
- *Signs:* "the oaks in Hanger Wood bare in May as if in winter; caterpillars dropping on threads".
- *Levers:* none on the trees; expect a poor mast, plan pannage.
- *Learning:* P8, P9 (the season's foretelling with a lever: plan the pigs). *Connections:* mast, boar, pigeons, mice.
- *Social footprint:* 3.6 (preparation). Null arm: none. *Relevance:* indirect, through the mast. *Not redundant:* a spring sign that
  foretells the autumn, with a lever. *Cost:* S.

**24. The veteran tree (a composite hub).**
- *Natural history:* old pollards and hollow oaks hold bee colonies, owls, bats, jackdaws, woodpeckers and fungi; pollards were cut
  for poles and leaf fodder by right; felling an old tree ends many things at once.
- *Constitution:* a site with occupants: a parcel feature holding sites for other kinds.
- *Behaviours:* (1) **occupancy**: bees, owls, jackdaws or bats take a hollow with a chance by age; (2) **the pollard's crop** (poles
  every N years, leaf fodder in a dry summer); (3) **felling** removes all occupants for good.
- *Signs:* "bees going in and out of a hole high in the old oak by the lane".
- *Levers:* pollard, fell, protect.
- *Learning:* P6, P10. *Connections:* bees, owls, jackdaws, mast, timber.
- *Social footprint:* 3.4, 3.7 (a named tree, a boundary marker, a meeting place). Null arm: no named trees.
- *Relevance:* moderate through bees. *Not redundant:* connects several kinds through one decision (to fell). *Cost:* S.

**25. The deer park, fallow deer and the deer leap.**
- *Natural history:* fallow deer, a Norman introduction, were the park deer: herding, grazing, tolerant of enclosure. A park was paled
  with cleft oak on a bank and ditch under a licence; a licensed deer leap let forest deer jump in but not out [30].
- *Constitution:* A4 herd; A2 forager by value within the pale; A6 slow; A7 enclosed; A8 venison and hide.
- *Behaviours:* (1) **the pale as a held structure** (M12) with upkeep (a pale decays; a gap lets the deer out and into neighbours'
  corn); (2) **the leap**: a one-way gate that draws wild deer from the forest or the commons into the park each stretch, by the herd's
  ranging; (3) **winter feeding** (hay and browse cut for the park); (4) **poaching** over the pale.
- *Signs:* "the park pale down by the brook, deer slots going out into the barley"; "fresh deer in the park this morning".
- *Levers:* empark (needs a licence: a lord's or an office's act); mend the pale; hunt in the park; poach.
- *Learning:* P18, P21. *Connections:* red deer (the leap draws them), forest law, venison gifts, hay.
- *Social footprint:* 3.1 (a chokepoint that converts a common stock into a private one), 3.7 (status), 3.5 (the broken pale's
  damage), 3.4 (the forest's deer drawn away). Who needs whom: the park holder needs a parker and pale-mending labour; neighbours
  need the pale kept. Null arm: no parks, no pale disputes.
- *Relevance:* moderate where a lord exists. *Not redundant:* the only structure that moves wild stock into private hands. *Cost:* M.

### 6.4 Waters

**26. The fishpond (stews, pike and the otter).**
- *Natural history:* manors and monasteries kept fishponds (stews) for Lent and fast days; pike grew in them; ponds were drained and
  restocked on cycles; otters, herons and poachers took from them.
- *Constitution:* a held structure (M12) with a fish stock and predators.
- *Behaviours:* (1) **stocking and growth** over seasons; (2) **draining** every few years (a crew act) to harvest and clean; (3)
  **predation** by otters and herons (heronry coupling), and by poachers at night; (4) **fast days** raising demand (if the calendar has
  them).
- *Signs:* "an otter's spraint on the stone by the stew"; "the stew low and green after the dry weeks".
- *Levers:* build, stock, drain, guard, trap the otter.
- *Learning:* P5, P17. *Connections:* heron, otter, the weir, fast days.
- *Social footprint:* 3.1 (a holder, a chokepoint for fish), 3.7. Null arm: no stews.
- *Relevance:* moderate in fish-poor worlds. *Not redundant:* the water's equivalent of the warren: kept wild capital. *Cost:* M.

**27. Freshwater pearl mussel.**
- *Natural history:* lives decades in clean, fast rivers; its larvae ride on the gills of salmon and trout for months; medieval and
  later pearl fishing in Scottish and other rivers; very slow to recover once fished out.
- *Constitution:* A6 very slow; A7 site-bound beds; depends on salmon and trout.
- *Behaviours:* (1) **beds** at particular reaches; (2) **pearls** rare per shell (most opened shells hold nothing, so fishing kills
  many for few pearls); (3) **recruitment** only where salmon or trout pass, so a weir that blocks the run kills recruitment upstream
  (a lag of years).
- *Signs:* "dark shells packed in the gravel at the ford"; "a pearl the size of a pea".
- *Levers:* fish the bed; leave it; open the weir's gap.
- *Learning:* P6, P8 (through salmon, with a very long lag). *Connections:* salmon, trout, the weir.
- *Social footprint:* 3.4 (a commons with a treasure), 3.7 (a pearl as a gift or a seal of a deal). Null arm: none.
- *Relevance:* small in food; high in value per find. *Not redundant:* the strongest case of a lag through another kind; a
  treasure-hunting temptation with an irreversible cost. *Risks:* invisible in runs except as lore. *Cost:* S. (Medium rank.)

**28. The medicinal leech.**
- *Natural history:* gathered by wading bare-legged in ponds and letting leeches attach; sold to healers for bleeding; overcollected
  to scarcity in the 19th century.
- *Constitution:* A6 slow; A7 ponds.
- *Behaviours:* (1) **gathering** as a poor person's trade (units in the pond; a small loss of blood); (2) **the pond's stock** with slow
  recovery; (3) **demand** from a healer (when illness and treatment exist).
- *Signs:* "leeches thick in the cattle pond".
- *Levers:* gather; restrain.
- *Learning:* P5. *Connections:* healing (Q-16), ponds.
- *Social footprint:* 3.1 (a supplier to the healer). Null arm: none. *Relevance:* only with healing. *Risks:* waits on illness.
  *Cost:* S. (Defer.)

**29. Lamprey (the render).**
- *Natural history:* lampreys run up rivers in spring to spawn; prized at royal tables; Gloucester sent a lamprey pie to the monarch
  by custom.
- *Constitution:* A2 cue-triggered run (spring flow and warmth); A7 the river chain.
- *Behaviours:* (1) **the spring run** on the eel module run the other way; (2) **the render**: a seeded obligation to send the first
  lampreys (or a pie) to the lord by a date (M13).
- *Signs:* "lampreys clinging to the stones below the weir".
- *Levers:* net at the weir; meet the render or pay its cost.
- *Learning:* P1. *Connections:* eels, salmon, weirs.
- *Social footprint:* 3.1, 3.7: a render owed by a village to a lord, which must be organised. Null arm: no render.
- *Relevance:* small. *Not redundant:* the cheapest obligation in a wild good; it reuses the run module. *Cost:* S.

**30. Crayfish and the flax retting.**
- *Natural history:* native crayfish were trapped in clean streams in summer; flax and hemp were retted (rotted) in ponds and streams,
  which fouled the water and killed fish and crayfish; laws restricted retting in running water.
- *Constitution:* A6 middling; A7 streams; sensitive to water quality.
- *Behaviours:* (1) **retting load**: retting flax in a stream raises a pollution load downstream for a stretch, killing crayfish and
  fish; (2) **crayfish traps** (baited baskets) set at night.
- *Signs:* "the brook below the retting pool stinks and the crayfish are floating".
- *Levers:* ret in a pond, not the stream; agree where to ret.
- *Learning:* P8, P21. *Connections:* flax (if the economy has linen), fish, the downstream village.
- *Social footprint:* 3.4 and 3.2: an upstream household's work harms downstream fishers; a by-law on retting. Null arm: no retting
  rule.
- *Relevance:* only with flax. *Not redundant:* pollution as a commons problem. *Cost:* S (with flax).

**31. Common crane and bittern (the fen birds).**
- *Natural history:* cranes bred in English fens until about 1600, were feast birds, and were kept tame; their eggs were protected by
  statute in the 1530s with other fowl; the bittern's boom marks a reedbed in spring.
- *Constitution:* A6 slow (cranes); A7 site-bound breeders; A4 pairs; markers (bittern).
- *Behaviours:* (1) **breeding sites** in undrained fen, deserted when drained or disturbed; (2) **eggs and young** taken for feasts or
  for tame birds; (3) **the boom** as a marker of a reedbed's health.
- *Signs:* "cranes dancing on the wet meadow in March"; "a bittern booming in the reeds at dusk".
- *Levers:* protect eggs (a law); drain (ends them).
- *Learning:* P6. *Connections:* drainage (land change), reeds, feasts.
- *Social footprint:* 3.7 (a lord's feast bird), 3.9 (drainage). Null arm: none. *Relevance:* small. *Not redundant:* the cost of
  drainage made visible. *Cost:* S. (Low rank.)

**32. The duck decoy (pipes, a dog and silence).**
- *Natural history:* a pond with curved, netted pipes; a decoyman behind reed screens working a fox-like dog that draws ducks up the
  pipe out of curiosity; tame ducks as lures; silence and no shooting nearby; dozens worked in England into the 20th century [32].
- *Constitution:* a held structure (M12) acting on wildfowl's curiosity toward a fox-like dog (a decision rule: mobbing a predator at
  a safe distance).
- *Behaviours:* (1) **a pipe per wind**: a pipe works when the wind blows down it (ducks are approached from downwind of the decoyman),
  so a decoy with more pipes works on more days; (2) **the dog's work** as a bonded beast (F11); (3) **silence**: any shooting or noise
  within a radius that stretch empties the pond (an externality on neighbours, M3); (4) **the take**: a share of the ducks on the pond
  each working stretch in winter.
- *Signs:* "the decoy pond black with duck this morning"; "a gun went off on the mere and the decoy lifted".
- *Levers:* build, train the dog, keep the quiet; sue or bargain with the shooters.
- *Learning:* P17, P21. *Connections:* wildfowl; the freeze; the fen commons; feathers and down.
- *Social footprint:* 3.1 (a chokepoint and a specialist), 3.4 (the quiet zone over others' fowling), 3.8 (fen villages). Who needs
  whom: the decoy holder needs the neighbours' silence; neighbours want a share or compensation. Null arm: no quiet-zone agreement.
- *Relevance:* real in fen worlds (decoys took thousands of ducks a season). *Not redundant:* turns fowling into a held asset with an
  externality. *Cost:* M.

### 6.5 Coast and cliff

**33. Seabird cliffs and the egg harvest (the cragsman and the rope).**
- *Natural history:* guillemots, puffins, gannets and gulls nest on cliffs; egg and bird harvests were made by climbers on ropes held
  by partners above (St Kilda, the Faroes, Flamborough's climmers).
- *Constitution:* A4 colonies; A6 annual; A7 site-bound ledges.
- *Behaviours:* (1) **the harvest window** in early summer; relaying after a first take; (2) **the climb**: danger to the climber set
  by the rope-holder's skill and the weather; (3) **ledges as rights** (each family's ledge).
- *Signs:* "the cliff white with birds and loud".
- *Levers:* climb, hold, restrain (first eggs only).
- *Learning:* P5, P14. *Connections:* the coast; feathers; oil.
- *Social footprint:* 3.1 (a two-person dependence: the climber's life is in the holder's hands; trust as a precondition), 3.4 (ledges).
  Null arm: no climbing pairs.
- *Relevance:* high in coastal worlds' spring gap. *Not redundant:* the most direct trust dependence in the wild. *Cost:* S-M.

**34. Seals and the stranded whale.**
- *Natural history:* seals hauled out on sandbanks were clubbed for oil, meat and skins; a stranded whale was a windfall of meat and
  oil claimed by the Crown as a royal fish.
- *Constitution:* A7 haul-outs; A6 slow (seals); an event (the whale).
- *Behaviours:* (1) **haul-outs** at low tide (a tide clock, if the engine has one); (2) **the whale**: a rare event that puts a huge
  carcass on one village's shore; claims (the lord's, the finder's, the village's), division and a race against rot and other villages.
- *Signs:* "a great carcass on the sands at Northmouth, gulls in clouds over it".
- *Levers:* claim, cut, share, hide it from the lord.
- *Learning:* P14 (tides), P18. *Connections:* the coast; oil and light.
- *Social footprint:* 3.7 and 3.1: the whale is a windfall worth a fight (wildlife.md §11 named it). Null arm: no division dispute.
- *Relevance:* rare, large. *Not redundant:* a commons of a single object. *Cost:* S (the whale as an incident). 

### 6.6 Disease and the hidden

**35. Rabies (the mad dog).**
- *Natural history:* spread by bites among dogs, foxes and wolves; a rabid animal changes behaviour (wanders, bites without fear);
  fatal to people once symptoms show; dogs were killed or chained in outbreaks.
- *Constitution:* a disease load on dogs, foxes and wolves with a behaviour change in the host.
- *Behaviours:* (1) **the changed animal**: a rabid fox or dog comes into the village by day, unafraid; (2) **bites** pass it to dogs and
  people; (3) **the response**: kill or chain all dogs (a collective act with a cost to every dog-owner).
- *Signs:* "a fox walked into the yard at noon and stood, then snapped at the dog".
- *Levers:* chain the dogs; kill the strays; keep children in.
- *Learning:* P14, P11 (a tame fox is not a tame fox). *Connections:* dogs, foxes, wolves, hounds.
- *Social footprint:* 3.2 (quarantine and the dog cull as collective choices with unequal costs: the hound keeper loses most).
  Null arm: no dog cull.
- *Relevance:* rare, grave. *Risks:* needs illness in people. *Cost:* M. (Rare regime; defer until illness exists.)

**36. The black bane field (anthrax and the cursed ground).**
- *Natural history:* anthrax spores persist in soil for decades; burial pits of infected cattle and the fields around them cause
  repeated outbreaks when dug, ploughed or flooded [45]; folklore of cursed or unlucky fields may come from this.
- *Constitution:* a hidden, place-bound load with a very long memory (M15).
- *Behaviours:* (1) **the seeded pit**: the generator's history may leave a burial pit on some parcel; (2) **disturbance**: ploughing,
  digging or flooding releases it; beasts grazing there sicken within an engine day or two; (3) **lore**: elders call it the bad field;
  the lore is true, its explanation (a curse) wrong.
- *Signs:* "nobody grazes the Hollow; the old men say it is unlucky"; "two bullocks dead on the Hollow overnight, dark blood at the
  mouth".
- *Levers:* keep beasts off; never plough it; burn carcasses rather than bury them.
- *Learning:* P11 (true lore, false cause), P24 (a particular place). *Connections:* murrain, carcass handling (M18), the field's
  history.
- *Social footprint:* 3.3 (elders' knowledge as leverage; a newcomer ploughs it), 3.7. Null arm: no unlucky field honoured.
- *Relevance:* rare, sharp. *Not redundant:* the purest idiographic hidden state. *Risks:* it punishes newcomers heavily; keep it
  rare and signed. *Cost:* S.

**37. The fen ague (mosquito and the marsh fever).**
- *Natural history:* malaria was endemic in the English fens and marshes until the 19th century, with fevers in late summer; natives
  had some tolerance; incomers suffered more.
- *Constitution:* a load by standing water and warmth.
- *Behaviours:* (1) **seasonal fever** in late summer by water and warmth; (2) **tolerance** for natives (a trait by birth place);
  (3) **draining** lowers it.
- *Signs:* "the shaking fever in three houses by the dyke".
- *Levers:* live on higher ground; drain; (later) remedies.
- *Learning:* P1, P10 (the fen feeds and sickens). *Connections:* fowl, eels (the fen's riches), drainage.
- *Social footprint:* 3.5 (whose house is by the water), 3.9. Null arm: none. *Risks:* needs illness in people. *Cost:* S. (Defer.)

### 6.7 Sky

**38. Starling roost.**
- *Natural history:* winter roosts of tens of thousands in reedbeds or thickets; droppings kill trees and foul reeds; flocks strip
  fruit and grain locally; netted for food in places.
- *Constitution:* A4 huge flocks; A6 seasonal; A7 a roost site that moves between years.
- *Behaviours:* (1) **the roost**: a site chosen in late autumn; the reeds or the wood under it fouled (a cost to the reed-cutter or
  the coppice holder); (2) **daytime flocks** on pasture eating grubs (good) and on ricks (bad); (3) **moving the roost** by noise
  over several nights (a collective effort).
- *Signs:* "the starlings came in to the reedbed at dusk like smoke".
- *Levers:* drive the roost (crew, noise, several engine nights); net.
- *Learning:* P10, P7. *Connections:* reeds (thatch), grubs, rooks.
- *Social footprint:* 3.2 (driving the roost needs many), 3.5 (whose reeds). Null arm: no drive.
- *Relevance:* small. *Not redundant:* a collective deterrence problem with a site. *Cost:* S. (Low rank.)

**39. The cuckoo, swallows and the farming calendar (markers with levers).**
- *Natural history:* the cuckoo's first call, swallows' arrival, the elm's leaves, blackthorn flower: folk sowing rules were tied to
  these ("sow barley when the elm leaves are as big as a mouse's ear").
- *Constitution:* markers by warmth (built).
- *Behaviours:* (1) **sowing rules** tied to markers: a marker's date tracks the warmth that sets the right sowing date; sowing by the
  marker beats sowing by the calendar in a late or early year; (2) **local offsets** (the hills a week later; lore carried from the vale
  miscalibrated).
- *Signs:* the markers as built, now paired with the sowing decision.
- *Levers:* sow by the marker.
- *Learning:* P1, P11 (oak and ash: a true reading, a false forecast). *Connections:* farming.
- *Social footprint:* 3.3 small (the elder who knows the rule). Null arm: sowing by the calendar alone.
- *Relevance:* the timing of sowing moves yields by several per cent. *Not redundant:* it gives the built markers a lever; the runs
  showed markers ignored without one. *Cost:* S.

### 6.8 Ranking by value for cost

Value weighs: the brief's purposes served (especially dependence, problems no individual can solve, information, commons); presence
across generated worlds; a fast arm inside a run; novelty of the lesson; agent attention cost. Cost is build size and engine work
needed first.

| Rank | Kind | Value | Cost | Waits on | Why |
|---|---|---|---|---|---|
| 1 | 8 rabbit and warren | high | M | rights (D2-194) | a specialist, a chokepoint, rent, poaching, an edge externality, feral risk; light soils common |
| 2 | 1 cat | high | S | nothing | in every village; the misread door fixed by an animal with its own choice |
| 3 | 18 jay (with M7) | high | S-M | M1, M7 | the sentinel that makes stealth, keepers and poachers matter |
| 4 | 9 mole and mole-catcher | high | S | nothing | a cheap paid specialist and pooled payment in every meadow village |
| 5 | 3 crow and magpie (with M8) | high | S-M | M8 | animals as carriers of reputation; evidence about people |
| 6 | 19 nutting race (with M17) | high | S | built nut stock | a timing commons and a custom, cheap |
| 7 | 16 poisonous lookalikes | high | S | built poisoning rule | knowledge as safety; teaching |
| 8 | 22 stoat, weasel, polecat | medium-high | S | the fox's prober | the defence particular to a kind |
| 9 | 14 gadding herd | medium-high | S | nothing (herds exist) | a wild insect through kept beasts into neighbours' crops |
| 10 | 32 duck decoy | high in fen | M | M12 | a chokepoint with an externality |
| 11 | 25 deer park and leap | high with a lord | M | rights, M12 | stock moved into private hands; status |
| 12 | 39 markers with sowing rules | medium | S | built markers | gives built signs a lever |
| 13 | 36 the black bane field | medium | S | history before the run | idiographic hidden state; true lore with false cause |
| 14 | 33 seabird cliffs | high on coasts | S-M | coast worlds | a trust dependence |
| 15 | 15 grub years | medium | S | built loads | the rook's other half |
| 16 | 29 lamprey render | medium | S | the run module, agreements | the cheapest wild obligation |
| 17 | 2 kite and midden | medium | S | M9 | sanitation as ecology |
| 18 | 26 fishpond | medium | M | M12 | kept capital in water |
| 19 | 12 lapwing eggs | medium | S | nothing | restraint tested within a run, in the spring gap |
| 20 | 17 bracken, gorse, blackthorn | medium | S-M | succession | the commons that degrades without use |
| 21 | 24 veteran tree | medium | S | bees | one decision touching several kinds |
| 22 | 23 oak caterpillar years | medium | S | mast | spring foretells autumn, with a lever |
| 23 | 7 store pests | medium | S | furs and wool as goods | a cost of keeping wild goods |
| 24 | 10 partridge and quail | medium | S-M | dogs as beasts | dog and net |
| 25 | 30 crayfish and retting | medium with flax | S | flax | pollution as commons |
| 26 | 21 woodcock and cockshoot | low-medium | S | M4 | a particular place |
| 27 | 4 sparrow | low-medium | S | birds at the corn | threshing spill |
| 28 | 5 jackdaw in the chimney | low-medium | S | chimneys | a building hazard |
| 29 | 34 seals and the whale | medium on coasts | S | incidents | a windfall worth a fight |
| 30 | 27 pearl mussel | low-medium | S | salmon | the longest lag through another kind |
| 31 | 6 deathwatch and rot | low | S | building wear | omen lore |
| 32 | 20 badger | low | S | wasps, bees | route-holder |
| 33 | 38 starling roost | low | S | reeds | collective drive |
| 34 | 31 crane and bittern | low | S | drainage | drainage's cost |
| 35 | 11 corncrake | low | S | hay | a restraint in mowing |
| 36 | 13 adder | low (until illness) | S | illness in people | danger in work |
| 37 | 35 rabies | medium (as rare regime) | M | illness in people | collective dog cull |
| 38 | 37 fen ague | medium in fen | S | illness in people | the fen that sickens |
| 39 | 28 leech | low | S | healing | a supplier to the healer |

**The top ten new kinds:** the rabbit and its warren; the cat; the jay; the mole and the mole-catcher; crows and magpies; the nutting
race; poisonous lookalikes; stoats and weasels; the gadding herd; the duck decoy (with the deer park close behind).

## 7. The recommendations mapped onto the purposes

The brief (`02zr_wild_purpose_brief.md` §3) lists nine ways the wild should enrich a society. For each: the mechanisms and kinds
that serve it best (from §3 to §6 here), who comes to need whom, what can be held, traded, enforced or argued about, and what a null
arm (the wild pack off, same seeds, strong cast) would lack. The last column is what an experiment should look for in the state and
the records, not in the agents' prose alone.

| Purpose | Mechanisms and kinds | Who needs whom | Held, traded, enforced, argued | Null-arm signature (what the pack-off arm lacks) |
|---|---|---|---|---|
| **3.1 dependence and leverage** | warren (no. 8), decoy (32), deer park and leap (25), fishpond (26), weir with rents (4.14, M13), hounds and hawks with bonds (F11), harbourer (4.2), mole-catcher (9), rat-catcher (4.12), beekeeper and wax (4.20), the cat (1) | lords on warreners, decoymen, parkers, harbourers; households on catchers, kennels, beekeepers; climbers on rope-holders (33) | rights and sites held; rents owed (M13); services bought; beasts lent; claims argued | exchanges whose goods or services are wild (venison given, eels paid as rent, a catcher paid, a hawk lent); offices tied to wild things |
| **3.2 problems no individual can solve** | the stretch contest with several scares (M2), displacement (M3), the fox treadmill and wolf circuit (4.4, 4.5), the common hedge and its gaps (M4), drives and crews, the starling roost (38), rabies dog cull (35), ragwort pulling (16) | households by the wood on far households; villages on each other for culls and drives | rotas, pooled payments, by-laws ("shut the hens at dusk"), free-riders accused | watch rotas, shared fence duties, pooled bounties, inter-village agreements about a predator; complaints about free-riders |
| **3.3 hidden state and an information economy** | idiographic lies, lags and quirks (M15, F1), the harbourer's report, sentinels (M7, jay 18), animals that remember people (M8, crows 3), selective harvest (M5), contested attribution (M16), the black bane field (36), readings by skill | newcomers on locals; lords on harbourers and foresters; accusers on those who can read signs | reports, counts and tallies as records; testimony; lore disputed | more told and written statements about wild things that change acts; records (counts, tallies) kept; expertise concentrated and taught |
| **3.4 commons and management** | runs with weirs and close times (4.14, 4.15), the nutting race (19), lapwing first clutch (12), fowling quiet zones (32), feral rabbits (8), bracken cutting rights (17), retting rule (30), heronry and swans (4.18, 4.23), the herd's count (4.2) | upstream on downstream; early gatherers on those who wait; holders on commoners | customs (nutting day, close time), closed seasons, gear limits, wardens | a stock trajectory above the null's open-access path (where one exists); customs and rules about takes; enforcement acts |
| **3.5 a land that threatens unequally** | raiders by decision rule (F2) with displacement (M3), the gadding herd (14), the fox's hamlet externality (4.5), the warren's edge (8), the lord's deer under forest law (4.2), the broken pale (25) | the exposed on the sheltered; neighbours on each other's discipline | compensation, mutual aid, petitions, damage disputes | losses concentrated by position; transfers to the exposed; disputes about damage |
| **3.6 seasons and preparation** | the run's lag (4.14), the mast race and the caterpillar year (4.1, 23), markers with sowing rules (39), the hungry spring (bear, 4.6), store pests (7), lapwing eggs in the spring gap (12) | households on those who read the season | stores, smoked eels, timed sowing | storage and timing acts that anticipate wild events, more than the null's |
| **3.7 status, inequality, law and stories** | forest law and laws on levers (M14), venison gifts (4.2), swans marked (4.23), serjeanty and hawks (4.22), heron-hawking (4.18), emergent legends (F12), deer park (25), the whale (34), omens (6, 4.9) | the lord on enforcers; poachers on buyers; the many on the storyteller | rights, crimes, gifts, feats, taboos | poaching cases, petitions, gifts of venison, named beasts in talk and chronicle |
| **3.8 differences between villages** | presence by land (fen decoys, coast cliffs, wooded boar, meadow moles, light-soil warrens), quirks (M15), idiographic lags | villages trade what their land gives | wild goods traded between villages | trade in wild goods between villages that differ by land |
| **3.9 land that changes and is changed** | the jay planting oaks (18), bracken creep (17), beaver's dam and the meadow below (4.19), drainage ending cranes and ague (31, 37), warren rabbits on turf (8), felling the veteran tree (24) | holders of the changed land on those who change it | decisions to fell, drain, dam, graze; disputes about them | land states diverging from the null's under people's choices |

**Two warnings from the runs.** First, the six runs showed the wild nights depend mostly on the seed (the same wolf kills on the
same nights), so every comparison needs several seeds. Second, no wild institution has yet appeared; runs were 8 days with food
short and elders dying. The society tests above need runs of at least 24 engine days (most of a year), food at about 25% of
actions, and a strong cast (Opus at the poles of leverage: a lord, a warrener or forester, the weir's holder, an exposed household's
head).

## 8. Recommendations

### 8.1 What to change in the proposal
1. **Adopt the three-layer framing** (§1.3): constitution modules (A1-A8) as the code, encounters (the facets) as views, and a
   social-footprint row for every kind with its null-arm signature, under a budget of time, attention and cost. Keep D2-203's
   interface; add the primitives emit alarm, follow, probe and cache (§3.2).
2. **Rewrite every behaviour in engine time** (§1.2 b). Resolve nightly contests over the stretch (M2). Drop P12's watch-schedule
   learner; use the spatial adversary (§3.5 F2).
3. **Add displacement and refill** (M3) to every raider and territorial predator. It is the cheapest route to collective action.
4. **Put the search inside one act** (§3.5 F1): the agent chooses a plan; the engine resolves the search with the group's lie
   table and the hunter's lie map. Record wind direction as an engine gap (`docs/engine_gaps.md` is Cybertron 1's; for cybertron2,
   OPEN.md under 37.4).
5. **Restore red deer as a modest raider under forest law**, with laws that constrain levers (M14): lawed dogs, low fences, the
   fence month, a forester who presents offences. Add the harbourer and venison gifts.
6. **Favour particular knowledge over general rules** (§1.2 c): seed quirks and places that remember (M15); test learning with arms
   that change magnitudes or places, not only names (02zp's masking did not separate learning from knowing).
7. **Budget attention** (§1.2 d): lines per agent-day per kind and a world cap; suppress signs with no lever for that reader today;
   make feedback name the kind and the scare (§3.4).
8. **Design weight should follow exposure:** rats and mice with the cat, birds at the corn as social followers, the fox with its
   externality, moles, rabbits, and the stoat's gap first; boar and red deer as frontier kinds. Calibrate boar to 3-10% of need
   unwatched (median) where present.
9. **Make legends emergent** from records and telling (§3.5 F12), and give tamed beasts a bond to their trainer (§3.5 F11).
10. **Add society-level tests** to the proposal's §1.2 (§3.8; §7).

### 8.2 What to build first (in order)
1. **The shared perception call (M1)** and **the stretch contest (M2)** in the animal interface, with **displacement and refill
   (M3)**, on three existing kinds that live in many worlds: birds at the corn (as social followers), the fox (as a lapse prober with
   the hamlet externality and the treadmill) and the boar (habit raider with the spatial adversary). Test: the D2-198 answers survive
   under the stretch; displacement sends birds to the neighbour; one lax house raises its neighbours' losses.
2. **The cat, the rat-catcher, the stoat's gap and the mole-catcher**: four cheap kinds or services that put a specialist or an
   animal ally in every village and fix the door misread.
3. **Runs with idiographic lags and obligations:** eels (and salmon on the same module) with river lags from the generator, a weir with
   a gap and a close time, and an eel rent in sticks (M13).
4. **Red deer under forest law** (M14) with the harbourer, in wooded worlds with a lord.
5. **The jay and sentinels (M7)** on top of M1, so stealth and keepers matter.
6. **The rabbit warren** (M12) when rights are ready (D2-194), then the duck decoy and the deer park.
7. **Then** the bear's cached carcass and the wolf's circuit across villages, in frontier worlds; bees, falconry and swans with
   husbandry and rights.

For each step, the experiment: several seeds; the pack on and off; a strong cast; at least 24 engine days; read dependence edges,
institutions, specialisation, trade in wild goods and disputes from the state and records against the null (§7), and read the end
state qualitatively.

### 8.3 What to stop doing
1. **Stop writing behaviour in real nights.** Every number is in engine days.
2. **Stop adding signs that carry no lever** for the reader that day (the rut, plovers, the first frost drew no comment; standing
   facts are never used).
3. **Stop treating relevance as a share of food alone.** A kind that makes a dependence or a dispute is worth more than one that moves
   food by a tenth and makes nothing social.
4. **Stop testing learning on species the models already know** without arms that change particulars.
5. **Stop designing defences as private.** Without displacement, refill and shared structures, nothing pushes a household to its
   neighbours.
6. **Stop seeding legends and lore as props.** Let them come from what happened and what people said, with a few seeded elders'
   stories.
7. **Stop building multi-year arms first.** A behaviour with no fast arm in engine days goes to lore and history, after the fast arms
   are working.
8. **Stop cutting a kind's conflict to simplify it** (red deer's raid): the conflict is usually the point.

## Sources

Games and simulations:
1. Raph Koster, "Did players destroy the UO ecology?": https://www.raphkoster.com/?p=46439 ; MIT Technology Review on Ultima Online:
   https://www.technologyreview.com/2023/02/17/1068027/ultima-online-oldest-metaverse/amp/ ; Massively OP on Koster's postmortems:
   https://massivelyop.com/2018/06/14/magic-through-serendipity-raph-koster-on-the-glorious-mess-that-was-ultima-online/
2. Dwarf Fortress Wiki, Cat: https://dwarffortresswiki.org/index.php/Cat ; Catsplosion: https://dwarffortresswiki.org/Catsplosion ;
   (the drunk cats) PC Gamer: https://www.pcgamer.com/how-cats-get-drunk-in-dwarf-fortress-and-why-its-creators-havent-figured-out-time-travel-yet
3. RimWorld Wiki, Animals: https://rimworldwiki.com/wiki/Animals ; Turn Manhunter Chance When Attacked:
   https://rimworldwiki.com/wiki/Property:Turn_Manhunter_Chance_When_Attacked ; Animal husbandry (taming):
   https://rimworldwiki.com/wiki/Taming
4. Gematsu, Red Dead Redemption 2 details wildlife, hunting, fishing:
   https://gematsu.com/2018/09/red-dead-redemption-2-details-wildlife-hunting-fishing-and-horses ; Well Played:
   https://www.well-played.com.au/all-about-red-dead-redemption-2s-wildlife-horses-hunting-and-fishing/
5. theHunter: Call of the Wild, Steam discussions on need zones and pressure:
   https://steamcommunity.com/app/518790/discussions/0/3830919351659689157 ;
   https://steamcommunity.com/app/518790/discussions/0/2530372519571058078
6. Game Developer, "Crafting the complex, chaotic ecosystem of Rain World":
   https://gamedeveloper.com/design/crafting-the-complex-chaotic-ecosystem-of-i-rain-world-i-
7. Unity, "Exploring procedural design in Rain World: The Watcher": https://unity.com/blog/exploring-procedural-design-rain-world
8. The Long Dark Wiki, Wolves: https://thelongdark.gamepedia.com/Wolves ; Bear: https://thelongdark.fandom.com/wiki/Bear
9. VideoGamer, Monster Hunter: World review: https://videogamer.com/reviews/monster-hunter-world-review ; Co-Optimus review:
   https://co-optimus.com/review/2087/page/2/monster-hunter-world-co-op-review.html
10. Don't Starve Wiki, Koalefant: https://dontstarve.wiki.gg/wiki/Koalefant ; Suspicious Dirt Pile:
    https://dontstarve.wiki.gg/wiki/Suspicious_Dirt_Pile/DST
11. Stardew Valley Wiki, Fish: https://stardewvalleywiki.com/fish ; Modding: Fish data:
    https://stardewvalleywiki.com/Modding:Fish_data
12. Banished Wiki, Hunting cabin: https://banished.fandom.com/wiki/Hunting_cabin ; Steam discussion:
    https://steamcommunity.com/app/242920/discussions/0/540734792801442593
13. Eco on Steam: https://store.steampowered.com/app/382310/Eco/
14. Creatures (video game series), Wikipedia: https://en.wikipedia.org/wiki/Creatures_(video_game_series)
15. Eurogamer, Black & White at 25 (via reader):
    https://hn.jakechampion.name/reader/https://www.eurogamer.net/black-and-white-lionhead-peter-moylneux-retrospective-google-deepmind-gemini-ai
16. Valheim Wiki, Taming: https://valheim.fandom.com/wiki/Taming
17. ARK Wiki, Taming: https://ark.wiki.gg/wiki/Taming
18. Ecosystem on Steam: https://store.steampowered.com/app/1133120/Ecosystem/ ; Gridworld: https://store.steampowered.com/app/396890/Gridworld/

Ecology and behaviour:
19. Grimm et al., "A standard protocol for describing individual-based and agent-based models" (ODD):
    https://www.usgs.gov/publications/standard-protocol-describing-individual-based-and-agent-based-models ; the first update:
    https://pubs.usgs.gov/publication/70003622
20. Lieury et al. (2015), "Compensatory immigration challenges predator control": https://hal-amu.archives-ouvertes.fr/hal-03559057
21. Sih, Bell and Johnson (2004), behavioural syndromes: https://www.reed.edu/biology/342_old/assets/readings/sih_2004.pdf ;
    "Boldness, trappability and sampling bias in wild lizards":
    https://researchportalplus.anu.edu.au/en/publications/boldness-trappability-and-sampling-bias-in-wild-lizards/
22. McComb et al. (2001), "Matriarchs as repositories of social knowledge in African elephants": https://pubmed.ncbi.nlm.nih.gov/11313492/
23. Aplin et al. (2015), "Experimentally induced innovations lead to persistent culture via conformity in wild birds":
    https://www.doi.org/10.1038/NATURE13998 ; Cambridge, Avian Cognition, social learning and innovation:
    https://www.cambridge.org/core/books/avian-cognition/social-learning-and-innovation/E04D021B2C1FD5750A0A5D3A7D4E702C
24. Cornell, Marzluff and Pecoraro (2012), "Social learning spreads knowledge about dangerous humans among American crows":
    https://carta.anthropogeny.org/node/308894 ; NBC News: https://www.nbcnews.com/news/amp/wbna43570637
43. Johann et al. (2020), "Adaptation of wild boar activity in a human-dominated landscape":
    https://pmc.ncbi.nlm.nih.gov/articles/PMC6953143 ; Bollen et al. (2024), PeerJ: https://www.peerj.com/articles/17390
44. "Distraction, displacement and alarm" (lapwing displays): https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5113542/ ; "The
    broken-wing display across birds": https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8965389/
45. Soil sample analysis of *Bacillus anthracis* at animal burial sites (2024): https://pmc.ncbi.nlm.nih.gov/articles/PMC11509789/ ;
    Mongolian anthrax burial grounds: https://pmc.ncbi.nlm.nih.gov/articles/PMC8604359
46. MSD Veterinary Manual, *Hypoderma* (warble flies, gadding):
    https://www.msdvetmanual.com/integumentary-system/cattle-grubs/hypoderma-spp

Real practice and history:
25. Feit (2005), "Re-cognizing co-management" (James Bay Cree hunting territories and tallymen):
    https://macsphere.mcmaster.ca/bitstream/11375/23908/1/FEIT_Re-cognizing_Co-management-Anthropologica_47%282%29_2005.pdf
26. Royal forest, Wikipedia: https://en.wikipedia.org/wiki/Royal_forest ; the Assize of the Forest (1184):
    https://constitution.org/1-History/sech/sech_035.htm ; the Charter of the Forest (1217):
    https://constitution.org/1-History/sech/sech_045.htm
27. "Regulating the working dog in medieval England" (lawing, expeditation):
    https://legalhistorymiscellany.com/2023/05/09/regulating-the-working-dog-in-medieval-england/
28. University of Nottingham, Sylva: deer hunting (fence month):
    https://www.nottingham.ac.uk/manuscriptsandspecialcollections/documents/exhibitions/sylva/sylva-deer-hunting.pdf ; Yorkshire
    Dictionary, fence month: https://yorkshiredictionary.york.ac.uk/words/fence%20month
29. Edward of Norwich, *The Master of Game* (Baillie-Grohman edition, Project Gutenberg):
    https://gutenberg.org/cache/epub/43452/pg43452-images.html
30. Deer park (England), Wikipedia: https://en.Wikipedia.com/wiki/Medieval_deer_park ; Northamptonshire HER, park pale with deer leap:
    https://her.northamptonshire.gov.uk/Monument/MNN18003 ; Forest of Bowland, Leap in the Park: https://forestofbowland.com/node/3122
31. Warren (burrow), Wikipedia: https://en.wikipedia.org/wiki/Warren_(burrow) ; Herefordshire Through Time, warrens:
    https://htt.herefordshire.gov.uk/herefordshires-past/the-medieval-period/countryside-and-landscape/warrens/
32. Duck decoy (structure), Wikipedia: https://en.wikipedia.org/wiki/Duck_decoy_(structure) ; The Spectator, 1905:
    https://archive.spectator.co.uk/article/15th-april-1905/11/t-he-great-increase-of-wild-fowl-already-seen-in-e
33. The Dyers' Company, Swan Upping: https://www.dyerscompany.co.uk/the-company/swan-upping/ ; Guide London:
    https://guidelondon.org.uk/blog/around-london/swan-upping-counting-the-crowns-swans-on-the-river-thames
34. History Hit, "Paid in fish: eels in medieval England": https://www.historyhit.com/paid-in-fish-strange-uses-for-eels-in-medieval-england/ ;
    Atlas Obscura, medieval eel rent map: https://atlasobscura.com/articles/medieval-eel-rent-map-england
35. Essex Field Club, serjeanty tenures (sparrowhawk, lanner falcons for heron-hawking):
    https://essexfieldclub.org.uk/archivetext.php/s/054/o/0043 ; Serjeanty, Wikipedia: https://en.wikipedia.com/wiki/Sergeanty
36. Salmon and Freshwater Fisheries (Consolidation) (Scotland) Act 2003, close times:
    https://www.legislation.gov.uk/asp/2003/15/part/1/crossheading/close-times-for-salmon/enacted ; Magna Carta (1215) clause 33 (as
    cited in wildlife.md)
37. House of Commons Journal, 20 December 1566 (bill for preservation of grain by killing crows and other vermin):
    https://prod.british-history.ac.uk/node/3162
38. The Open University, "Red kites and ravens swooped through Elizabethan London":
    https://www.open.ac.uk/blogs/news/arts-social-sciences/red-kites-and-ravens-swooped-through-elizabethan-london-and-helped-keep-the-city-clean/ ;
    Raye, early modern attitudes to the ravens and red kites of London: https://orca.cardiff.ac.uk/id/eprint/138499/
39. Le Quotidien du Médecin, on Chassenée and the rats of Autun:
    https://cancerologie.lequotidiendumedecin.fr/liberal-soins-de-ville/justice/quand-les-rats-comparaissaient-devant-les-tribunaux ;
    E. P. Evans, *The Criminal Prosecution and Capital Punishment of Animals* (1906) (not re-read)
40. David Quammen, "The swallow that hibernates underwater" (on Gilbert White): https://davidquammen.com/the-swallow-that-hibernates-underwater/
41. Four Pests campaign, Wikipedia: https://en.wikipedia.org/wiki/Four_Pests_campaign (not re-read in this session)
42. Shooting UK, decoying pigeons: https://www.shootinguk.co.uk/news/when-pigeon-shooting-is-it-possible-to-decoy-from-woods/ ; BPCA,
    wood pigeon control: https://bpca.org.uk/news-and-blog/wood-pigeon-control/275915
47. Liebenberg, *The Origin of Science* (tracking), and Stander et al. (1998), as cited in 02zp §22.
48. Jon Young, bird language (baseline and alarm): https://birdlanguage.com/?p=783 ; Maine Nature News, "What the Robin Knows":
    https://mainenaturenews.com/2014/04/what-the-robin-knows/

Repository sources: `docs/cybertron2/proposals/wild_behaviour.md`, `wild_systems.md`, `wildlife.md`, `node_ecology.md`,
`living_populations.md`, `wild_plants.md`, `wild_layer.md`; `docs/review/37_growth/02zq_wild_audit.md`, `02zp_ecosystems_deep_dive.md`
(§22-§31), `02zr_wild_purpose_brief.md`; `docs/cybertron2/guides/senses.md`; `docs/scenario_design.md`; code on the `ecology` branch
(`/home/user/cyb-ecology/cybertron2/wild/kinds.py`, `engine/wild.py`, `engine/climate.py`).

**Caveats on the sources.** Several game sources are wikis and forum posts, not developers' own accounts; where they conflict
(the Long Dark's fear triggers, theHunter's pressure thresholds, the UO collapse), the lesson drawn above rests on the part they
agree on. Historical details (the fence month's dates, the 1330s ruling on roe, the Holy Rood nutting day, the claimed capital
punishment for killing London's kites, which the Open University piece doubts) should be checked against primary sources before
they enter any spec. The claim that killing wolf breeders raises livestock losses is contested and is offered as a world regime,
not a rule.

## History
- 9 Nov: written as an outside critique at the coordinator's request, after reading the proposal, the audit, the catalogue, the
  kinds, the built system, the deep dive's prototype and LLM tests, the senses guide, scenario_design and the purpose brief.
