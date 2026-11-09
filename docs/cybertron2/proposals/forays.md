# Forays: going out from the village and coming back

**Status:** discussion (9 Nov). Zach's answers so far are in History; nothing is in the spec or DECISIONS.md yet. Design only.
**Owner:** 37.2 (author). Acts, places, the parcel graph, memory and model calls are 37.4's (spec/agents/, spec/world/,
spec/information/memory.md, spec/record/execution.md), so the built form goes to them through the board when Zach allows.
**Affects:** spec/agents/actions.md (a new act), spec/world/places.md and parcel_graph.md (land beyond the village reachable by
an act; features), spec/information/memory.md (what a foray leaves in memory), spec/record/execution.md (an interpreter call and
its replay), spec/environment/wildlife.md (takes resolved along a route), spec/economy/lodging.md (a night out in the wild).

## Summary

Hunting, gathering and similar trips become a **foray**: a person (or a party) says in its own words where it means to go and
what for ("up the Ashbeck to the falls and lie up for the hinds at the pool; if nothing, on past the falls"), with how many of the
day's units and with whom. A **small model call, one per foray a day**, with the route syntax in its instructions, translates that
intent into the most faithful route over the places the person knows. The engine then walks the route in order: travel spends
units by terrain, noticing runs along the way, animals are met where their own modules put them, takes and finds are settled,
and the person comes back, or does not. It returns a **short story of what happened**, in order, every line from state. What
places it went through and what it saw there stay in **the person's own memory**, in its own words, and it may **name** them;
next time it can say "back to Hind Pool" or "the old split oak where I saw the squirrel", and the interpreter reads its memory to
find the place. More units reach further: the village's parcels and the ring around it within a day, the wild blocks beyond only
with a night out. For now a foray has two outcomes: the person **returns**, or it **does not** and spends the night out where it
is. Camps, moving out and new nodes come later.

## The proposal

### 1. The act

`foray {intent: "<free text>", for: hunt | gather | look for, units: N, with: [people], gear: [...]}`

- **intent** is the person's own description of the route and purpose, as long or short as it likes ("the wood around", "north
  past the last field and on into whatever lies beyond", "back to Hind Pool, then the hazel brake beyond it").
- **for:** hunting and gathering both go in the first version (Zach, 9 Nov); looking for a person or a strayed beast uses the same
  act and needs nothing new.
- **units:** the share of the day it gives. A unit is a part of one in-game day: the foray is a day out (or part of one), and its
  story is told as one day (setting out, the morning, the afternoon, toward dusk). It is not converted into real days (Zach,
  9 Nov). The ecology's own rates stay as they are; only the act and its story are on the day's clock.
- **with:** a party moves together at the pace of the slowest, shares one route and one story; each member spends its own units.
- **gear:** what it carries (a bow, snares, nets, a dog led, a basket, food); it sets what can be taken and carried (D4-32's load).

### 2. The interpreter

One small model call per foray each day, the same model for every agent whatever the cast (so a strong agent does not also get a
stronger translator), at low temperature, with the route syntax in its instructions.

**It is given** only what the person could know:
- the intent, the purpose, the units and the party;
- the person's memory and kept lines (D4-61, D4-64), and the stories of its own recent forays as it received them (from its
  conversation this stretch);
- the land as the person knows it: its node's parcels with their neighbours and sides (as `attend {to: the village}` gives them,
  D2-116), the road ends, and the places beyond the village it has been to or been told of, in the words it was given;
- the cost of a step by terrain, and the units needed to come home from each known place.

**It is never given** where animals are, how many, what lies anywhere unseen, or any other state the person has not met. It
cannot plan well for the person; it can only translate.

**It returns** a route in the syntax: an ordered list of legs (go to a known place; go on in a direction beyond a known place;
search a place for N units by a method; follow what is found; come home by a known way), with a turn-home rule (by default, keep
the units needed to get back). Where the intent is unclear it takes the most literal reading; where it names a place it cannot
find, it heads the way described and marks the leg as going into the unknown; it adds no stops of its own.

**The engine checks** the route against the graph and the units, repairs what is impossible by fixed rules (the nearest valid
place; cut the last legs when units run short), and records the interpreter's request and reply in the journal like any other
model call, so replay reads the recorded reply (spec/record/execution.md).

**Bias** (Zach: "I probably don't want to add too much bias"): the interpreter's only job is fidelity. Its instructions say so,
it sees nothing the person does not know, and it is tested on a fixed set of intents with the routes a careful reader would draw
(§7). Its translation and the person's words are both kept, so analysis can check where it read them differently.

### 3. Walking the route

- **Travel** spends units by terrain per step (open ground fast, wood and marsh slow, a river crossed at a known ford or not);
  the village's parcels and the ring around it (wild/areas.py on branch `ecology`: unheld land within 2.5 km) are within a day,
  the wild blocks beyond (about 8 km) only with a night out.
- **Noticing** runs along the way by the one noticing rule (D4-48, D2-115), with the presence of a searcher where it searches and
  of a passer elsewhere, as on a road (D2-97).
- **Animals** are met where their own modules put them this stretch (D2-203), with the chance of the approach (the person's
  noticing of them against theirs of the person) and the method's properties against the kind's traits (02zs §8.1).
- **Takes and finds** settle by method and gear; what cannot be carried is left at the place where it happened, as a thing lying
  there (D2-85), for ravens, a fox or a neighbour to find.
- **The land's features:** the story needs words for places, so the land beyond the parcels carries a few features per area from
  the generated land (falls where a river drops, a pool, a ford, a crag, a spring, an old wood's core, a clearing), as physical
  state the animals' modules also use (a wallow, a drinking place, a lie). Features are land, not knowledge: knowing one is the
  person's memory.

### 4. The story

The walk's events, in order, become a short story (about three to eight lines), each line from an event in state, worded as signs
are (grounded, a change, never a feeling the person did not choose: guides/senses.md):

> You went out by Long Acre and up the Ashbeck through the alder carr. At the falls, fresh slots of hinds at the pool, a day old.
> You lay up under a split oak above it, the wind in your face. Toward dusk three hinds came down to drink; your arrow took the
> second behind the shoulder. You followed her blood into a hazel brake beyond the falls and found her down. You carried home 30
> venison and the hide; the rest hangs in the brake. Home after dark, tired.

The order of events is state; the words for the time of day are a presentation choice, named as one and keyed so replay is exact.

### 5. Memory, spots and names

- **No engine table of spots.** What the person saw where is in its memory, as it chose to keep it (D4-61); the engine keeps only
  the record of the foray (its route and events, in the day's record, as D4-62 keeps a day's route), for the journal, the map and
  analysis.
- **Names** (Zach: naming should be supported): a person can call a place what it likes in its memory or kept lines ("Hind Pool:
  the pool below the Ashbeck falls"), and use the name in a later intent; the interpreter resolves it from the person's own
  memory. Telling others a name gives them the words, not the place: they find it if the description is good enough, or by being
  led there (as D4-47 for unexplored places).
- **Fading:** a place it does not keep in memory is lost to it, as any memory is. Nothing is capped or filtered for attention.

### 6. Not coming back

- A foray can end out in the wild: the units run out before home (a long chase, a far place, a slow party), a carcass too heavy
  to leave, a hurt, a high ford, a fog in unfamiliar ground where it loses the way. Then **the person spends the night out where it
  is** (D4-12: 1.5 food, 2 in winter, and the cold; risks by weather and season).
- **Next morning** it wakes at that place, which is a place like a road's stretch (D4-35): it sees what is there, and its acts are
  those the place allows: forage or hunt there, or another foray (home, or on).
- **At home** the household sees only that it did not come back (D2-4: nothing is announced); a search is a foray with the purpose
  `look for`.
- **Later (deferred, Zach 9 Nov):** a foray meant to make a camp (D2-68); moving out; a regular way becoming a path (D2-90); a
  camp becoming a node, from latent sites the generator cuts in advance (D4-47) with some choice in how the camp is set up (37.5).

### 7. Tests (dry runs, before any live run)

- The interpreter on a fixed set of about thirty intents (plain, vague, naming known places, naming unknown ones, too long for the
  units, a party, a search), scored against routes drawn by hand; it adds no stop the intent did not ask for.
- A guard test: the interpreter's request contains no population, stock or unseen state.
- Units are spent as the route says; a route too long ends with a night out; the party moves at the slowest.
- Every story line maps to an event; replay with recorded replies is exact.
- A person who keeps a place in memory and names it reaches it again by name; one who did not keep it cannot.

## Why

- Zach (9 Nov): "a more complex system where you actually map out the route they travel, and sequences of events, places they go.
  Then, when hunting in the future, they can do things like hunt revisiting the old oak tree that I saw a squirrel at last time,
  or hunt further beyond the waterfalls ... the distance they can travel (and time spent) and thus likelihood of finding animals
  depends on how many units." And: "let them describe in natural language their hunting path / intent, and then a different small
  model call happens per day with all the syntax instructions that translates the intent into the best interpretation."
- Local, particular knowledge (this river, this wood, this pool) is what a model cannot bring from training and what makes a local
  hunter worth more than a clever newcomer (02zr §1.2 c, M15); a foray makes it the person's own, in its own words.
- It replaces 02zr's "search inside one act" (§3.5 F1) with places the person can see, name and tell (Zach, 9 Nov).
- It uses what exists: the parcel graph and the day's route (D2-114, D4-62), the land beyond the village already in the ecology's
  areas with the populations living in them, the road's stretches, notices and finds (world/roads.md), unexplored places (D4-47),
  nights out (D4-12), things left at places (D2-85).
- It fits 02zs's take, know and reach ladders: better hunting is better planning, places known, gear, dogs, companions and range.

## Alternatives considered

- **Basic chances per hunt** (as built): no places, no memory of them, no reach; the one-machine problem.
- **A structured route syntax written by the agent:** exact, but hard for weak models and a cost in every prompt; the interpreter
  keeps the syntax out of the agent's view.
- **A deterministic parser of the agent's words:** replayable without a model, but brittle on free text.
- **An engine table of known spots per person:** reliable, but it decides for the person what it remembers, and Zach prefers
  memory; the engine keeps only the foray's record.
- **Free movement with coordinates:** not needed, and against D2-114.

## Open questions

1. Is the story worded by templates from the events (as signs are), or by the small model under strict grounding?
2. Are a person's names for places recorded by the engine as well (for the map and analysis), or only in its memory?
3. How many features an area holds, and which (from the land only, or also made by animals and by people: a wallow, a hide, a
   cairn).
4. The units a step costs by terrain, and whether the turn-home rule is a default the person can waive.
5. What a person out overnight can do the next morning beyond foraging and a foray (wait for others; signal with a fire).
6. How it relates to acting at different times of the day (OPEN L-102): a dawn start, a night foray, coming home after dark.
7. Whether one interpreter call can serve all of a day's forays (cheaper) without their contexts mixing.

## History

- 9 Nov 2026: Zach proposed hunting as a storied route through places remembered and revisited, with reach by units, beyond the
  village's edges. Explored in conversation (what exists: the parcel graph and day's route, the ecology's areas, roads, D4-47,
  camps; a general foray rather than hunting alone; spots, the act, the story, memory).
- 9 Nov 2026: Zach: let people describe their route and intent in their own words, with a small model call per day to translate
  it into a route; a unit is a part of an in-game day, not real days; places stay in the person's memory rather than the engine
  (though what one has seen there makes sense), without adding much bias; for now a foray either returns or does not (a night
  out), with camps, moving out and new sites later (latent nodes with some choice in setting up a camp); hunting and gathering
  both in the first version; naming supported; it replaces 02zr's search inside one act. Written up (this file).

## Sources

docs/review/37_growth/02zr_wild_behaviour_critique.md §1.2, §3.5 F1, M1, M15; 02zs_wild_development.md §3.6, §8.2, §10;
02zt_wild_dependences.md; 37_growth/05_frontier.md; proposals/journeys.md, day_route.md, parcel_graph.md, hidden_ways.md,
search_on_take.md; spec/world/places.md, edges.md, roads.md, parcel_graph.md; spec/information/memory.md; cybertron2/wild/areas.py
(branch `ecology`); D2-4, D2-68, D2-85, D2-90, D2-97, D2-114 to D2-116, D2-203, D4-12, D4-32, D4-35, D4-47, D4-48, D4-61, D4-62,
D4-64.
