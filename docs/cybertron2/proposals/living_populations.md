# Proposal: living populations on the land (a generalised ecology layer)

**Status:** discussion (8 Nov). Nothing decided, nothing to build. **Owner:** 37.2 (design, kinds and numbers: spec/environment/),
with 37.4 (the engine: it sits on D4-103's process model and D4-104's renewal rules and packs). **Affects:** spec/environment/resources.md,
spec/core/processes.md; data.py (RESOURCES, a new KINDS table); engine renewal.py, packs.py, night.py, herds.py, environment.py, signs.py;
landgen/ecology.py (the starting populations); OPEN L-2, L-37, D2-77, D2-95.

## Summary

Today wildlife is a number per parcel that regrows where it is. Zach, 8 Nov: populations that "live on the land, their populations
evolve and interact, maybe they sometimes move, eg if a tree is felled then the wolves might attack villages, ... fish populations
killed in one place could impact elsewhere", varying by terrain, at the right resolution, sitting cleanly on top of the world.

The proposal, in one sentence: **every wild population is one kind held as a distribution over the land (a coarse field beneath
the graph), with a declared habitat, growth, diet, home range, seasons and response to people; it is resolved into actual animals
only where someone looks.** One night step applies, in order:
1. growth toward what its habitat holds;
2. eating and being eaten;
3. movement toward the land that suits it best, held back by home fidelity;
4. people's take, through the existing acts, which collapse the field where they happen.

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
- the renewal rules, response to density and outcome distributions (D4-103, D4-104);
- the parcel graph and roads;
- the river network (the generator records flow);
- herds as moving counted groups (herds.py: wandering, drift, being found);
- signs and the noticing rule;
- incidents.

## 2. The abstraction

**Revised 8 Nov (Zach): the animals live on the land, not on the graph.** The generator's land covers the whole region; only the
villages and a few wild places are nodes. So mobile animals live on a coarse field over the land, and parcels and nodes are windows
onto it. The graph version (each population on a parcel, node or river stretch) stays as the fallback for hand-made worlds, which
have no land beneath them.

### 2a. The substrate: a field over the land

- **Patches:** the generator's land coarsened to about 1 km squares (2,500 for a 50 km region). Each patch has, for each kind, a
  **habitat score**: its K, from the ecosystems and depth bands under it (D2-191), less what people have done there (felled,
  cleared, busy). Rivers are chains of patches along their course, with direction; the coast is a band.
- **Beyond the window:** the map's edges are a reservoir, the land beyond. Animals arrive from it and leave into it, so a place is
  never sealed unless it is enclosed.
- **Parcels and nodes are windows:**
  - the deer "in" a wood parcel are the field summed over that parcel's land;
  - felling a wood changes the land under that parcel, so its habitat score falls;
  - cause and effect stay in one place.
- **What stays on parcels:** plants, grass, trees, young growth and dead wood are sessile stocks, as now (D4-103, D4-104). The parcel
  is their right scale.
- **The run needs the land.** The engine has run on the graph alone (D2-177), and a run does not yet carry its land (G-33). This is
  the first use of the land during a run; the coarse patches travel with the run's record.

### 2b. Populations and kinds

**A population** is one kind in a region, held as **a distribution over patches**: how many are expected where. It also holds what
the kind's dynamics need (a condition, a hunger).
- **Density kinds** (fish, fowl, hares) are just that distribution.
- **Whole-counted kinds** (deer herds, wolf packs, a bear) are a set of groups. Each group is an object with a size and **a
  distribution over where it is**: the "particle" Zach described.

**A kind** is one row of data, the KINDS table:

| Field | Meaning | Example (wolves) |
|---|---|---|
| `count` | `whole` (groups of whole animals: one wolf is one) or `density` | whole: packs of 3 to 8 |
| `habitat` | its K by ecosystem and depth band, per km² | large woods' cores |
| `home` | how strongly it keeps to its range (home fidelity), and how far it wanders from it in a day | a pack ranges 100 to 300 km² |
| `growth` | a renewal rule (D4-104), on its clock | breeds once a year, spring |
| `diet` | what it eats (other kinds or stocks), with a functional response (more when plentiful, saturating) | deer and boar; herds and carcasses when they fail |
| `season` | seasonal ranges or routes, if any | winter: down to lower ground |
| `split` | how a group divides (a share peeling off) and joins | young disperse in autumn |
| `people` | hunted (by which acts), avoids people, raids (herds, crops, stores), dangerous | hunted with a crew; raids herds; dangerous in winter |
| `signs` | what it leaves to be sensed (guides/senses.md) | tracks, howling, a kill, a missing beast |

Claims and holdings mean nothing to it: a wolf does not ask whose parcel it is.

### 2c. One movement rule

Each night, every distribution moves part of the way toward **where the land suits it best**, at the kind's own speed. Ecology
calls the endpoint the ideal free distribution: animals spread in proportion to how good each place is, less the crowding. Every
behaviour Zach named comes from this one rule and the kind's row:

| Behaviour | How it comes from the rule |
|---|---|
| **A resident range with wandering** | Home fidelity is a cost on leaving the range, so the distribution is concentrated at home, but not zero beside it. Deer live in the wood; on a given day a few are at its edge, and now and then one is in a village field. |
| **Part of a herd going elsewhere** | A group splits when a draw says so: a share peels off, peaked at about a quarter (as domestic herds already do, D2-131). Density kinds simply spread. |
| **Several destinations, gradually** | The distribution relaxes toward every good place in proportion to its quality, at the kind's speed. Animals don't all go to one place at once unless one place is far better. |
| **Seasonal movement** | The kind has two target ranges that alternate by season: salmon up the river in autumn, fowl in for the winter, deer down to lower ground. |
| **Permanent shifts, in response to people** | Felling, clearing, a busy road or heavy hunting lower the habitat score, so over the following nights the distribution moves to the next suitable land. Restoring the land draws it back, slowly. |
| **Arriving and leaving** | The edge reservoir exchanges animals with the window: a run arrives from the sea; a hunted-out wood refills, slowly, from beyond the map. |

### 2d. One night step

Applied to every population in a fixed order:
1. **Grow** toward the habitat's K by the kind's renewal rule.
2. **Eat:** consumers take from their diet; prey and stocks are drawn down, and a consumer short of food loses condition, then
   numbers.
3. **Move** by the rule above.
4. **People's take** happens in the day's acts, through observation (§3).

Each step is a pure function, so the capacity model can run the ecology forward under a harvest (D4-103 part 3).

**Damping:** bounded steps, and no population below zero or above its habitat. Predator and prey models oscillate and crash; the
edge reservoir and bounds keep them in hand. The step is tested over simulated years on its own before it goes in a run.

## 3. Observation: the field collapses where someone looks

- **The engine holds only expectations:** how many deer are likely in each patch, where a pack is likely to be.
- **When someone is at a place** (hunting, fishing, minding the field, crossing the wood), the engine draws what is actually there,
  from the expectation at that place: 3 deer at the wood's edge today; the pack, or not. That draw is the collapse, and it is
  keyed, so runs replay.
- **The take and the encounter update the field:**
  - deer killed come off the count;
  - a pack met is placed where it was met, and its distribution re-centres there.

  Everywhere else stays expected.
- **One animal matters when it is whole-counted.** A lone bear is a group of one whose place is a distribution until someone meets
  it.

**Individuals on demand.** When a whole-counted group meets people (a wolf seen, a deer shot, a calf taken), the engine names one of
them for the event: "the grey bitch with the torn ear". It is kept only while it recurs:
- the same pack raiding again is seen as the same animal;
- people's memories can hold it;
- killing it lowers the count by one.

It is the level-of-detail pattern from games and simulations: aggregate by default, promoted to an individual at the moment of
contact, demoted after.

**People never see the numbers.** They see:
- signs, drawn from the field near them by the noticing rule (tracks, howling, "few fish rising");
- what their own work brings (D4-104's response to density).

**Resolution by kind:**

| Kind | Count | Where it is held | Why |
|---|---|---|---|
| plants, grass, trees | density | parcels (sessile stocks) | as now; nobody notices one plant |
| fish, eels, fowl, hares | density | the field, along rivers for fish | catches are many and small |
| deer, boar | whole (herds, sounders) | the field, as groups | a herd is seen |
| wolves, a bear | whole (a pack; one bear) | the field, as groups | **one matters** |
| the salmon run | density | the river's patches, by season | it passes through many places |

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

The first kinds, their purposes and their waves are designed in [wildlife.md](wildlife.md); the table below is the short
version.

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
- one store, one step and one data table: about 800 to 1,200 lines of engine and data with the field (400 to 700 for the graph
  version alone);
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
| 1 | **Populations generalise stocks:** the coarse field (2a), the movement rule (2c) and observation (§3); game and fish become kinds with habitat from the ecosystems, and the edge reservoir. No predators. The catch reported as what the day's work brought (D4-104's response); the capacity model's sustainable take per population. | S-M | hunted-out places refill from neighbours; fishing one reach is felt by the next; capacity as a trajectory |
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
- 8 Nov (later): Zach: "the animals should have resident places but still be able to wander ... a small number of the herd go
  somewhere else ... migration could happen over time ... what if they wanted to migrate to different places? ... the environment
  (from the terrain generator) does exist beyond the nodes ... populations as probability distributions over space ... that collapse
  when observed". §2 and §3 revised: a coarse field over the land with parcels and nodes as windows; one movement rule (toward the
  ideal free distribution, with home fidelity, splitting, seasons and the edge reservoir); observation as the collapse; the graph
  version kept for hand-made worlds. The first kinds are designed in proposals/wildlife.md.
- 8 Nov: Zach framed it as part of the core aim, "a complex, partially observable environment", tied to carrying capacity, seasonal
  and long-term shifts, and their management. Added §0, step 1's catch signal and capacity trajectory, and questions 6 and 7. Terms
  brought in line with D4-104 (renewal rules, packs, response to density).

## Sources

- engine/renewal.py (D4-104; was regimes.py), packs.py, night.py (regrow), forests.py, herds.py, data.py RESOURCES;
- spec/core/processes.md (D4-103);
- proposals/process_model.md, engine_overhaul.md (37.4);
- proposals/ecosystems.md §7 (guilds), temperate_landscapes.md (D2-191), water_and_preservation.md, environment_state.md;
- OPEN L-2, L-37; D2-77, D2-95.
