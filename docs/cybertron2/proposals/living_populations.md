# Proposal: living populations on the land (a generalised ecology layer)

**Status:** discussion (8 Nov). Nothing decided, nothing to build. **Owner:** 37.2 (design, kinds and numbers: spec/environment/),
with 37.4 (the engine: it sits on D4-103's process model and D4-104's renewal rules and packs). **Affects:** spec/environment/resources.md,
spec/core/processes.md; data.py (RESOURCES, a new KINDS table); engine regimes.py, night.py, herds.py, environment.py, signs.py;
landgen/ecology.py (the starting populations); OPEN L-2, L-37, D2-77, D2-95.

## Summary

Today wildlife is a number per parcel that regrows where it is. Zach, 8 Nov: populations that "live on the land, their populations
evolve and interact, maybe they sometimes move, eg if a tree is felled then the wolves might attack villages, ... fish populations
killed in one place could impact elsewhere", varying by terrain, at the right resolution, sitting cleanly on top of the world.

The proposal, in one sentence: **every wild population is a count of one kind on one place in a habitat graph, with a declared
growth, diet, movement and response to people.** One night step applies, in order:
1. growth toward what its habitat holds;
2. eating and being eaten;
3. movement along the graph;
4. people's take, through the existing acts.

Today's stocks (plants, grass, game, fish) become the simplest cases: no diet, no movement. Large animals are counted whole, so
"there is actually one wolf" is just a count of 1, and a single animal can be followed and remembered when it matters.

It is built in three small steps, each switchable as a pack (D4-103, D4-104), and is worth building for two things:
- the effects it makes between villages: a commons, a river shared upstream and down, a forest whose loss is felt elsewhere;
- the hidden, shifting state it gives the world, which people must infer and manage (§0).

## 0. Why: a complex, partially observable environment (Zach, 8 Nov)

Zach: "this fits into the 'complex, partially observable environment' that is a core aim of the simulation. Wildlife is core
relation to carrying capacity, and also seasonal / long term shifts + how they are managed." Four consequences for the design.

1. **The populations are hidden state; people infer them.** Nobody sees a number. They see:
   - signs (tracks, howling, "few fish rising"), drawn by the noticing rule;
   - **what their own work brings:** the catch for a day's fishing. D4-104's response to density already makes a take scale with
     how full the stock is, so catch per effort is a real, noisy signal, as it is in real fisheries.
   - **A hyperstable stock is the classic trap:** catches stay good while the stock collapses (D4-104's `hyperstable`). Which kinds
     are hyperstable is a design choice with consequences.
   - memory across seasons, and records: a forester's tally, the chronicle, a custom that says "the salmon fail if the weir stands
     at the run".

   So knowledge, records and those who keep them (a forester, a warden, an elder) gain value. That is the information economy
   (information_economics.md) given something real to know.
2. **Wildlife is part of carrying capacity, and capacity moves.**
   - The capacity model (D4-102) must count each population's sustainable take, not its standing stock (02zl §1.3: people live off
     flows).
   - Taking more than that lowers next year's capacity. So capacity is a trajectory: the day-0 forecast each run stores becomes a
     forecast under a harvest, which the model can simulate (D4-103 part 3).
   - Overhunting, overfishing and clearing show as capacity lost, measurable against the run's own day-0 baseline.
3. **Shifts on three clocks** (D4-103's clocks):
   - **seasonal:** runs, breeding, winter hunger driving predators toward people, fowl arriving in winter;
   - **year to year:** D2-76's ecology era family, "mast and bust", becomes concrete: a mast year swells boar and deer, and a bust
     year sends them, and the wolves, hungry;
   - **long term:** clearing, overhunting and recovery, over continued runs.
4. **Management is the point.** Real societies managed wildlife with rules:
   - closed seasons;
   - who may fish which water or hunt which wood (forest law, the warren, the fishery as a held right);
   - quotas and gear limits;
   - husbandry instead of hunting (fishponds, warrens, the deer park);
   - wardens to watch, and penalties.

   All of these need people: monitoring and enforcement are work and institutions (scenario_design: "enforcement that needs
   people"). The engine needs nothing new for the rules themselves: claims, customs as kept lines (D4-64) and agreements carry them.
   **The experiment:** does a society discover restraint, monitoring and enforcement before the stock fails? Compare it against a
   null arm with no shared stock. The stock's trajectory against its sustainable take is a clean outcome measure, read with the end
   state as scenario_design asks.

## 1. What exists now (8 Nov)

| Stock | Regime | Lives on | Interacts with |
|---|---|---|---|
| plants (forage) | fast | parcels (forest, meadow, pasture, heath, moor, fen, saltmarsh) | nothing |
| grass | fast | pasture, meadow, rough grazing (D2-189) | herds graze it down; overgrazing wears it |
| game | threshold: no regrowth below a share of K | woods; K by wood type and depth (D2-191) | nothing. Hunting draws it; a hunted-out wood never refills from its neighbours. |
| trees, young growth, dead wood | slow, young, dead | woods | trees shed dead wood; beasts stop young growth; felling leaves brash; a gale throws trees; under 40% of its trees a wood turns to scrub |
| fish (water system, 7 Nov) | periodic: a resident stock, and a run that arrives in its seasons toward `run_K` | water parcels | nothing. The run arrives from nowhere and leaves to nowhere. |
| herds (domestic) | counts by role on a parcel | parcels, roads | graze grass, stop young growth, trample crops, drop dung; wander along the parcel graph and on roads, are lost, found and driven |

So:
- **Interactions exist only between the woods' three stocks and domestic herds.**
- **Nothing wild moves, eats anything wild, or responds to people other than by being drawn down.**
- **Decided but not built:**
  - wolves in the first-world set (D2-77);
  - scavengers and wild animals that attack herds and hunters and are drawn to food (D2-95, L-2);
  - wildlife by terrain (L-37).

**What already exists to build on:**
- the regime registry and outcome distributions (D4-103);
- the parcel graph and roads;
- the river network (the generator records flow);
- herds as moving counted groups (herds.py: wandering, drift, being found);
- signs and the noticing rule;
- incidents.

## 2. The abstraction

**A population** is `{kind, place, n}`, plus whatever the kind's dynamics need (a condition, a hunger, a memory of where food was).

**A kind** is one row of data, the KINDS table:

| Field | Meaning | Example (wolves) |
|---|---|---|
| `scale` | the place it lives on: parcel, reach (a stretch of river), node (a home range), or region (a migration) | node |
| `count` | `whole` (integers: one wolf is one) or `density` (a real number: fish, fowl, plants) | whole |
| `habitat` | its K by ecosystem and depth band (ecology.py's palette, D2-191), per unit of size | old oak-ash core 0.02 a unit; edge 0.005 |
| `growth` | a renewal rule from the registry (D4-104), on its clock (year or season) | breeds once a year, spring |
| `diet` | what it eats (other kinds or stocks), how much, with a functional response (more when plentiful, saturating) | deer, then herds and carcasses when deer are scarce |
| `moves` | `none`, `diffuse` (spreads toward space), `roam` (a group moves as one toward food), or `migrate` (seasonal, along a route) | roam |
| `people` | how it meets people: hunted (which acts draw it), avoids people (K falls near busy places), raids (herds, crops, stores), dangerous | hunted; avoids; raids herds; dangerous in winter |
| `signs` | what it leaves to be sensed (the sign rules, guides/senses.md) | tracks, howling, a kill, a missing beast |

**The habitat graph** is the world's own graphs, chosen per kind:
- the parcel graph inside a node;
- roads between nodes;
- the river network, downstream and upstream (a reach is the water parcels of a river within a node, linked node to node as the
  river runs);
- the coast.

Claims and holdings mean nothing to it: a wolf does not ask whose parcel it is.

**One night step** (or one a week, on the season clock, for slow kinds), applied to every population in a fixed order:
1. **Grow** toward the habitat's K by the kind's renewal rule. Today's rules are kept, so today's stocks are this with no diet and no
   movement.
2. **Eat:** each consumer takes from its diet by its functional response. Prey and stocks are drawn down; a consumer that eats too
   little loses condition, then numbers.
3. **Move** along the graph:
   - **diffuse:** a share flows toward neighbours with more room (density against K);
   - **roam:** a group goes to the neighbour where its food is best, or stays;
   - **migrate:** in its season a run moves along its route, and what is taken or blocked on the way (a weir) does not arrive.
4. **People's take** happens in the day's acts, as now: hunting, fishing and foraging draw on the place's population.

Each step is a pure function, as D4-103 wants, so analyses simulate it and the capacity model can run the ecology forward.

**Damping** (environment_state.md Q5): bounded steps, and no population below zero or above its habitat. Predator and prey models
oscillate and crash; a little immigration from the edge of the map (the land beyond the window) keeps a hunted-out place from
staying empty for ever, unless it is enclosed.

## 3. Resolution: when one animal matters

| Kind | Count | Scale | Why |
|---|---|---|---|
| plants, grass, trees | density | parcel | as now; nobody notices one plant |
| fish, eels, fowl, small game (hares) | density | parcel, reach | catches are many and small |
| deer | whole (a herd of 12) | node | a herd is seen; numbers in the tens |
| wolves, a bear, boar | whole (a pack of 5; one bear) | node | **one matters**: a single wolf taking a calf is the story |
| the salmon run | density | region, along the river | it passes through many places |

**Individuals on demand.** When a whole-counted population meets people (a wolf seen, a deer shot, a calf taken), the engine names
one of them for the event: "the grey bitch with the torn ear". It is kept only while it recurs:
- the same pack raiding again is seen as the same animal;
- people's memories can hold it;
- killing it lowers the count by one.

It is the level-of-detail pattern from games and simulations: aggregate by default, promoted to an individual at the moment of
contact, demoted after.

**People never see the numbers.** They see signs (tracks, howling, a kill, "few fish rising"), drawn from the population's state by
the noticing rule, as today's game and fish signs already are.

## 4. What it makes possible: the cases Zach named

- **A felled forest sends wolves to the villages.**
  - Felling lowers the wood's deer habitat (K by depth band), so deer fall.
  - Wolves' diet runs short, so they roam toward food, and their diet's second choice is herds and carcasses.
  - The pack appears at the village with the nearest herd: tracks, a missing calf, an incident.
  - That presses for the watch, fences, dogs, a collective hunt, or keeping the forest: an institution.
- **Fish killed in one place felt elsewhere.**
  - The salmon run migrates upstream along the river network. What is taken or blocked downstream (a weir, heavy netting) does not
    reach upstream villages.
  - Resident fish diffuse along reaches, so a fished-out reach refills slowly from its neighbours.
  - This is the classic upstream-downstream commons: a weir held by one village starves another's run.
- **Shared land:**
  - Deer and herds compete for young growth and grass.
  - Hunting out a wood near one village thins the deer that drifted toward the next.
  - A common grazed bare drives the hares off.

These are externalities between villages, which is exactly the leverage and dependence scenario_design asks for. Coordination
problems (the commons, a shared river) are a research target in their own right (docs/review/37_growth: coordination problems).

## 5. Variety by terrain

Each landscape system's palette (D2-191) gives each kind its habitat:

| Kind | Where it lives |
|---|---|
| deer | wood edges and interiors |
| boar | oak and beech woods (mast) |
| wolves | large woods' cores, roaming |
| hares | grassland, downs |
| wildfowl | fen, saltmarsh, meres |
| eels | rivers and fen |
| salmon | large rivers, by the run |
| shellfish | the foreshore |

The generator seeds the starting populations from the same habitat table, so a fen world, a moor world and a wildwood frontier have
different animals without any code of their own.

## 6. Is it too much?

**The framework is small:**
- one store, one step and one data table, in about 400 to 700 lines of engine and data;
- each kind is a row.

The risk is not size.

**Three costs are real:**
1. **Calibration.** Coupled populations can oscillate, crash or explode. Damping, immigration and bounds handle most of it, and the
   step must be checked over years on its own before it goes in a run.
2. **The runs are short.** A run is 20 to 40 days, about one compressed year (a year is 24 to 32 days). Fast effects show within a
   run:
   - a reach fished out;
   - a run blocked by a weir;
   - a pack drawn to a herd.

   Slow ones need long runs or continued runs: wolves following years of felling, deer recovering. Population cycles over many
   years will not show, and should not be the goal.
3. **Attention.** Agents meet it only through signs and incidents. If they don't notice or act, it is scenery (the meat-drying
   lesson, 02zl and the water proposal §2).

**What stays out:**
- genetic evolution: "evolve" here means numbers and where they are, not traits;
- disease in wildlife (with Q-16);
- many species at once.

Two to five kinds carry every case in §4.

## 7. Steps

| Step | What | Size | Shows |
|---|---|---|---|
| 1 | **Populations generalise stocks:** game and fish become kinds with habitat K from the ecosystems, diffusion along the parcel graph and river reaches, and immigration from the map's edge. No predators. The catch reported as what the day's work brought (D4-104's response); the capacity model's sustainable take per population. | S-M | hunted-out places refill from neighbours; fishing one reach is felt by the next; capacity as a trajectory |
| 2 | **The run migrates:** salmon along the river network in their season; the weir (water proposal §4) blocks or takes it | S | the upstream-downstream commons |
| 3 | **One predator:** wolves, whole-counted at node scale, roaming; deer then herds and carcasses as diet; raids as incidents; individuals on demand | M | the forest's loss felt as wolves at the village; the watch and fences with a reason |

Later, each as rows: deer and herds competing for young growth; boar and mast with pigs (L-36); scavengers on carcasses (L-2);
wildfowl by season.

Each step is a system a world switches on (D4-103), so existing worlds and runs are untouched.

## Alternatives considered

- **Keep stocks per parcel, add special cases** (a "wolf incident" when a wood is felled). Cheap, but it is a patch per story, and
  the stories don't compose. Rejected for the same reason D4-103 replaced bespoke mechanics.
- **Individual agents for every animal** (agent-based). Faithful, but costly and hard to analyse. Nobody notices one fish. Only
  whole-counted large animals get individuals, and only on demand.
- **A full ecosystem model** (food webs, many species, nutrient cycles). Unanalysable, unsteerable, and no gain in leverage.

## Open questions (for Zach)

1. The abstraction: kinds as data on the world's own graphs, one night step, whole counts for large animals with individuals on
   demand. Right?
2. Steps 1 to 3 in that order, or the predator first, for the story?
3. Immigration from beyond the map's edge: yes (nothing stays empty for ever), or let places be emptied for good?
4. Whether agents may ever see more than signs: a hunter's estimate ("a pack of five"), a tally kept by the lord's forester?
5. When: after the engine overhaul's stage 3 (it is mostly rows on D4-103's registry), with the fishing acceptance test?
6. Which kinds are hyperstable (catches hold up while the stock falls), and so most deceptive: the fish of a shoal or run, by D4-104?
7. A first experiment on management: a shared fishery or wood between two villages, with and without a held right or custom, against
   a null arm?

## History

- 8 Nov: Zach asked for generalised ecosystems: populations that live on the land, interact and move, by terrain, at the right
  resolution, as a clean layer. 37.2 surveyed what exists (§1) and proposed this.
- 8 Nov: Zach framed it as part of the core aim, "a complex, partially observable environment", tied to carrying capacity, seasonal
  and long-term shifts, and their management. Added §0, step 1's catch signal and capacity trajectory, and questions 6 and 7. Terms
  brought in line with D4-104 (renewal rules, packs, response to density).

## Sources

- engine/renewal.py (D4-104; was regimes.py), packs.py, night.py (regrow), forests.py, herds.py, data.py RESOURCES;
- spec/core/processes.md (D4-103);
- proposals/process_model.md, engine_overhaul.md (37.4);
- proposals/ecosystems.md §7 (guilds), temperate_landscapes.md (D2-191), water_and_preservation.md, environment_state.md;
- OPEN L-2, L-37; D2-77, D2-95.
