# Methods and encounters: people answer the wild by general methods, not one action per animal

**Status:** ready for a decision (9 Nov). Nothing here is decided or built. It is the **build brief for stage 0 and stage 1 of the
wild layer's core, and pack K0** (docs/review/37_growth/02zv_wild_consolidation.md §2.1, §4): written so that a builder can work
from this file alone, with the files in §1 for reference.
**Owner:** 37.2 (author; the wild methods' data). The code it changes outside the wild pack (`verbs.py`, `knowledge.py`,
`prompt.py`, `perceive.py`) is 37.4's: building it needs their agreement on the board (CLAUDE.md), which waits on Zach.
**Affects:** spec/environment/wildlife.md (D2-192's "each taken by its own technique and skill"), spec/agents/actions.md,
spec/information/prompts.md and noticing.md (readings by skill), spec/economy/production.md (skill); code on branch `ecology`:
engine/data.py (TECHNIQUES, RESOURCES `taken`), engine/wild.py (`take`, `forage`, `site_work`, `guard`, `watch`, `shut`),
engine/verbs.py (`_technique`), engine/knowledge.py, engine/perceive.py (`practised`), engine/prompt.py (`verb_lines`),
wild/kinds.py (`SKILL_CARRY`, sign rows' `read`).

## Summary

Today each wild kind is met by techniques of its own (`stalk deer`, `boar hunt`, `snare hares`, `take the young herons`, `trap
beavers`, `dig out the fox earth`, four `watch the field` variants, `pick slugs at dusk`, `top the beans`), each with its own table
of what it takes, its own skill, and all of them seeded to everyone. This replaces them with **a small catalogue of general
methods** (stalk, drive, snare, trap, net, gather young, den work, pest work, guard, shut), each with **properties**, and gives
each wild kind **traits**; **one encounter rule** settles what a method meets and takes from the method's and gear's properties
against the traits of what is there. **Skill has two layers:** the method's (a good snarer snares well), and the person's
familiarity with a kind (better with the hares one knows than the rabbits one does not). **Targets are determinate:** the
existing `looking for` names a kind or a sort. **Methods are known by upbringing and by what the land holds**, not by everyone;
the system text describes each known method as a way of doing, with no multipliers and no lists of kinds; refusals no longer list
the catalogue. Each kind's behaviour stays in its own module (D2-203); only how people meet it becomes general.

## 1. For the builder: what to read, what holds, what to ignore

**This file is the single source for this stage.** Where another document differs, this file holds.

Read, in this order:
1. `CLAUDE.md` (both repositories' notes; the rules on spec, proposals, ownership, commits).
2. `docs/scenario_design.md` (why the wild layer exists) and `docs/review/37_growth/02zr_wild_purpose_brief.md`.
3. `docs/review/37_growth/02zv_wild_consolidation.md` §1, §2 (C1, C2, C3, C14, C15) and §4 K0: the plan this stage belongs to.
4. `docs/cybertron2/guides/senses.md` (any sign you touch).
5. The code on branch `ecology` listed under Affects, and `tests/test_cybertron2_wild.py`.

Ignore for this stage (they are superseded or belong to later stages): `wild_behaviour.md` v2's facets (§3) and per-kind designs
(§4); 02zr's conversion of acts into real days, its attention budget and its institutions; 02zr to 02zu's build orders (02zv's
replaces them); forays (stage 5), standing works (stage 3), decay (stage 4), shared perception and wind (stage 2).

**Do not:** build anything social into the engine (no offices, customs, closed seasons, bounties, rights, standing effects);
filter or cap signs for attention; convert acts into real days; put kind names in method code; run live LLM runs (dry runs only,
unless Zach allows one); write run logs into the repository (the session's scratchpad only).

## 2. Traits on kinds (C1)

Each wild kind (RESOURCES rows with `pack: wild`, and the site and load kinds) gains a `traits` row. A trait is a physical fact
about the animal, never about a method. The vocabulary (values `calibrate`):

| Trait | Values | Meaning |
|---|---|---|
| `size` | tiny, small, medium, large | body size; a method's size range selects on it |
| `runs` | true, false | uses fixed runs, racks or paths (a snare or a trap can be set on them) |
| `social` | solitary, group, flock | lives alone; in a group that moves together (a herd, a sounder, a pack); in a flock that lands where its kind feeds |
| `home` | none, den, burrow, lodge, colony, form | a fixed home it returns to (den work, gathering young, a lodge trap) |
| `water` | true, false | lives or moves in water (traps in water, angling) |
| `mover` | false, cue | moves on a cue in a run (the eel night) |
| `scent` | weak, strong | how much scent it leaves (a hound follows it) |
| `senses` | nose, eyes, ears (any of) | what it notices people by (stage 2 reads it; this stage stores it) |
| `active` | day, dusk, night | when it is about |
| `danger` | none, low, high | turns on a taker (D2-193; the existing `danger` rows stay as its numbers) |

The existing per-kind numbers stay where they are and keep their meaning: `taken.detect`, `taken.flee`, `taken.danger`,
`taken.goods`, `taken.family` (the names and sorts that `looking for` resolves).

**The first rows** (values `calibrate`; the builder fills the rest of the wild kinds the same way and lists them in the test):

| Kind | size | runs | social | home | water | scent | active | danger |
|---|---|---|---|---|---|---|---|---|
| red deer | large | true | group | none | false | strong | dusk | low |
| roe deer | medium | true | solitary | none | false | strong | dusk | none |
| wild boar | large | true | group | none | false | strong | night | high |
| brown hare | small | true | solitary | form | false | weak | night | none |
| woodpigeon | small | false | flock | none | false | weak | day | none |
| fox | medium | true | solitary | den | false | strong | night | low |
| wolf | large | true | group | den | false | strong | night | low |
| brown bear | large | false | solitary | den | false | strong | dusk | high |
| wildfowl | small | false | flock | none | true | weak | dusk | none |
| eel | small | false | solitary | none | true | weak | night | none |
| heron (the heronry) | medium | false | group | colony | false | weak | day | none |
| rook (the rookery) | small | false | flock | colony | false | weak | day | none |
| beaver (the lodge) | medium | false | group | lodge | true | weak | night | none |

Eel also carries `mover: cue`. The crop loads (slugs, aphids, the bean grubs) carry `on_crop: true` and `size: tiny`.

## 3. Methods with properties (C1, C3)

A method is a TECHNIQUES row of a new shape. Fields:

| Field | Holds |
|---|---|
| `verb` | gather or work (unchanged verbs) |
| `label`, `aliases` | how people name it; its words in the system text (§7) |
| `needs` | traits a target must have, or the method cannot take it (e.g. snare: `runs: true` and `size` in small to medium) |
| `favours` | traits that raise the match (e.g. net: `social: flock`), each with a factor |
| `size` | the size range it takes |
| `at` | where it can be done (covers, a site, water), as now |
| `units`, `crew` | its units; whether it is crew work and how a crew changes it (more hands raise the take and, from stage 2, the noise) |
| `gear` | gear it needs or that helps, by property (§4) |
| `skill` | its skill family (the first layer, §5) |
| `untaught` | tryable or not (D2-93), as now |
| `basic` | true only for methods anyone could do without being shown (§6) |

**The first catalogue** (replacing the techniques in §8; numbers `calibrate`):

| Method | Verb | Needs | Favours | Gear |
|---|---|---|---|---|
| **hunt** (search on foot and take what comes) | gather | size small to large | | a weapon helps |
| **stalk** | gather | size medium to large; `runs` or `social: solitary` | `active: dusk` | a bow or spear helps much |
| **drive** (a crew beats toward standers) | gather | size medium to large; `social: group` | `danger` met by a crew | spears; a crew needed |
| **snare** | gather | `runs: true`; size small to medium | `home: form` | cord or snares needed |
| **net** | gather | size small; `social: flock` | `water: true` (at water) | a net needed |
| **trap in water** | gather | `water: true`; size small | `mover: cue` on its nights (the existing `when` rows) | traps needed |
| **den work** (dig out a den, burrow or lodge) | gather | `home` in den, burrow, lodge | | spades help; a dog helps |
| **gather young** (from nests or a colony) | gather | `home: colony` | | |
| **gather wild food** | gather | (the plant stocks, unchanged) | | a basket helps |
| **pest work** (pick, top or clear a crop's pests) | work | `on_crop: true` | | |
| **break a dam** | work | a dam at the place | | spades help |
| **burn stubble** | work | (a field after harvest; unchanged) | | firewood |
| **guard** (watch a place by night) | work | (no target: the raiders' rules read it, unchanged) | | deterrents held: a fire, clappers, a horn, a dog |
| **shut** (a door on a building or pen) | work | (no target; a door state, already general for stores) | | |

`gather young` and `den work` keep the site rules that exist (the heronry's and rookery's tolerance and the lodge's state,
`site_work`); the method only replaces the per-site technique names. `pest work` takes the action by the load's own row (what
removing it does: pick, top or clear), so one method answers every crop load.

## 4. Gear by property

Gear carried (in hands or led) contributes properties the encounter rule reads; the method's `gear` says which it needs and which
help. This replaces the techniques' `weapon: {none, armed}` and, for these methods, the tool multipliers.

| Gear | Property | Used by |
|---|---|---|
| a weapon (spear, bow; the engine's weapons) | `strike` by its strength | hunt, stalk, drive |
| cord or snares | `noose` | snare |
| a net | `mesh` | net |
| traps (wicker) | `trap` | trap in water |
| a spade (a tool) | `dig` | den work, break a dam |
| a dog led (D4-58) | `scent`, `scare` | hunt, den work, guard |
| a fire, clappers, a horn | `scare` by kind (the existing D2-198 rows) | guard |

Where a needed gear is missing the method cannot be done and the refusal says what is missing ("you have no net"); help gear
missing lowers the take.

## 5. The encounter rule and skill (C1, C3)

**One rule for every take** (generalising `wild.take`, whose structure it keeps): for each kind `k` in the areas the act reaches,

```
weight(k, area) = count(k, area) x detect(k) x effects(k) x quiet(pressure) x match(method, gear, k) x focus(target, k) x when x reach_falloff
match(method, gear, k) = 0 if any `needs` fails, else  product(favour factors met) x size_fit(method, k) x calibration(method, k)
```

The rest of `take` stays: one draw among the candidates, then danger (D2-193), flight, the take, the wounded beast, legends,
leaders, pressure, the litter. `calibration(method, k)` is 1.0 unless a row on the **kind** says otherwise: per-pair numbers are
allowed only as audited calibration rows on the kind's data (`taken.calibrate: {method: x}`), each with a comment saying why, and
a guard test counts them (at most one per kind for this stage).

**Calibration target for K0:** with the new rule, the share of each kind among takes, per old technique, on fixed seeds, lands
within about a third of the old tables:

| Old technique | Old weights (what each took) |
|---|---|
| hunt the wild | red deer 1.0, roe deer 1.0, boar 0.6, hare 0.8, woodpigeon 0.3, fox 0.3, wolf 0.2, bear 0.1 |
| stalk deer | red deer 2.5, roe deer 2.5, boar 0.3, wolf 0.1 |
| boar hunt | boar 3.0, red deer 0.3, bear 0.2 |
| snare hares | hare 3.0, fox 0.2 |
| fowling | wildfowl 3.0, woodpigeon 0.2 |
| set eel traps | eel 3.0 (x2 on eel nights) |
| dig out the fox earth | fox 4.0 (and the cubs in spring) |

**Skill in two layers** (Zach, 9 Nov):
- **The method's skill:** the existing knowledge record and multiplier (knowledge.py `skill`, D2-52), kept per method (so per
  family: stalking, snaring, netting), earned by practice and teaching as now. It carries to every target the method can take.
  `SKILL_CARRY` is no longer needed.
- **Familiarity with a kind:** `Mind.know` gains a record per kind or sort met by the person (`familiar: {kind: x}`, 0 to 1), raised
  by taking it, by seeing its signs while working (the noticing rule's events), and by being taught about it; it carries in part to
  kinds that share most traits (deer to deer, `calibrate`), never to a whole method. It multiplies the take for that kind (about
  1.0 unfamiliar to 1.5 well known, `calibrate`), and it gates the per-kind expert readings that exist today (`expert:t`,
  `reads_as`): one reads a kind's expert signs when familiar with it, and its ordinary signs by the method family one practises.
- Both are told in words, never numbers (agent_view.md): "you snare well; you know the hares of these fields".

## 6. Who knows what (seeding)

- **Basic** (known to everyone, D4-103): only what anyone could do without being shown: `hunt`, `gather wild food`, `guard`,
  `shut`, `pest work`, `burn stubble`.
- **By upbringing and the land** (D4-21): at a world's start each household knows the methods whose targets its land holds within
  the ring (wild/areas.py), and its members carry familiarity with those kinds; a household by water knows `trap in water` and
  `net`; one by a wood with deer knows `stalk`; one by a heronry or rookery knows `gather young`; one with a fox earth near knows
  `den work`; `drive` is known where a wood holds a group kind. The generator's experts (run 5's expert heads) keep their levels.
- **Not known:** a method nobody's land calls for is known by nobody at the start; it can be learnt as any craft (D4-24: watching,
  being told, being taught, trying where tryable).
- Methods that need being shown (`drive`, `den work`) are not tryable untaught; the rest are tryable at the lowest level.

## 7. What the agent sees

- **Method lines in the system text**, for methods the person knows only (as now, `prompt.verb_lines` filters by level): each as a
  way of doing, in a sentence, with its gear and its place, at the person's level, and no multipliers and no kinds:
  "snare: set nooses of cord where beasts run (you need cord or snares); you snare well".
- **Familiarity lines**, in the person's know-how: "You know the hares and the roe of these parts" (from `familiar`).
- **The target** is the existing `looking for` slot ("name it, a kind or a sort"): it resolves against `taken.family` names of the
  world's kinds; a name that resolves is accepted whether or not the kind is here (finding out is the act); a word that names no
  kind is refused with "you know of no beast called that", **without listing the catalogue**.
- **Refusals** for an unknown method say so without listing the verb's techniques (today `verbs._technique` lists them all);
  a method whose gear is missing says what is missing.
- **Results** say what happened in the world's terms and name the kind and, where it failed, why ("a covey rose before the net";
  "nothing uses runs on this ground").

## 8. K0: converting what is built

| Built technique | Becomes |
|---|---|
| `hunt the wild` | `hunt` |
| `stalk deer` | `stalk`; `looking for: deer` where the agent says so |
| `boar hunt` | `drive`; `looking for: boar` |
| `snare hares` | `snare` |
| `fowling` | `net` |
| `set eel traps` | `trap in water` |
| `dig out the fox earth` | `den work` (any den, burrow or lodge; the fox's litter rule stays on the fox) |
| `take the young herons`, `take the young rooks` | `gather young` at the site |
| `trap beavers` | `den work` at a lodge |
| `break the beaver dam` | `break a dam` |
| `pick slugs at dusk`, `top the beans`, `clear the grubs off the beans` | `pest work` (the load's row says how) |
| `burn the stubble` | `burn stubble` (unchanged; it names no kind) |
| `watch the field (fire / clapper / horn / dog)` | `guard`, with the deterrents held as gear |
| `shut the hens in` | `shut` |
| `make clappers`, `make a horn`, `leach acorns` | unchanged (recipes that name goods, not kinds) |
| `range: near / the wood around / far`, `looking for` | unchanged modifiers (reach is the forays' later) |

Old names stay as aliases of the new methods for one release, so replayed and older worlds still resolve; the journal's recorded
acts replay unchanged.

## 9. Diagnostics and world options (C15, C14: stage 0)

- **Diagnostics** (measured, never acted on): per run, takes by method and kind; distinct methods used per household; familiarity
  gained; refusals by reason; wild sign lines per agent-day; written to the run's analysis, never read by the engine.
- **World options:** a `world.wild.methods_known` override (which households know which methods), so arms can start a world with
  more or fewer methods known; forest law and D2-194 rights wait for later stages.

## 10. Tests

**Guard tests:**
- no TECHNIQUES row of the wild pack names a wild kind in its label, needs, favours or yield (the kind names come from RESOURCES);
- calibration rows on kinds are counted and at most one per kind;
- the system text for any person contains no tool multipliers for these methods and no list of kinds;
- a refusal never lists the catalogue.

**Unit tests:**
- `match` is zero when a need fails (a snare on ground with no runs takes nothing; a net takes no deer);
- one method answers several kinds: the snare takes hares and, rarely, a fox; the net takes fowl and pigeons; den work answers a
  fox earth and a beaver lodge;
- skill: practice at stalking raises the take of red deer and roe alike; familiarity with hares raises the snare's take of hares
  and not of foxes; two snarers of equal method skill, one familiar with hares and one with rabbits (when rabbits exist), each does
  better on its own kind; both beat an unpractised snarer;
- seeding: a household with no water in its ring does not know `trap in water`; one by a heronry knows `gather young`;
- old names resolve as aliases; replay of a recorded run with the old names is exact.

**Regression (dry runs, no LLM):** the scripted-bot runs used for waves 1 to 5 (the wild_year probes in the scratchpad's
`eco/probe`) on fixed seeds: food from wild takes per household-season within about a third of before; the calibration table in §5;
the 467 existing tests pass (amended only where a technique was renamed).

## Why

- Zach (9 Nov): "bespoke single actions should in general usually instead be using general methods in a specific way"; "we don't
  want to entrench the nature of villages and societies in their current methods because each animal requires the action 'do this
  thing at this time'"; "skill can still vary within a technique based on target as another layer"; "someone should only ever know
  the things they know"; "they should know enough to at least know how to use the different techniques"; targets "need to be
  determinate".
- 02zs §7 and §8.1, 02zu §C.5 and C.7, 02zv C1 to C3: one rule over traits and properties lets new kinds be answered by existing
  methods, and better gear or skill answer more of them.
- Run 6's recorded system text: every agent was seeded about 60 crafts, including taking young herons and trapping beavers in
  villages with neither; the know-how list grew from about 1,700 to 2,750 characters with the pack.

## Alternatives considered

- **Keep per-kind techniques, fix only the seeding:** cheaper, but every new kind needs a new technique, and skill never transfers.
- **Skill per method only (no familiarity):** simpler, but it loses the hunter who knows these hares, and D2-192's own skill.
- **Free-text targets:** not feasible outside forays (Zach); the determinate `looking for` is kept.
- **A trait-property rule with no calibration rows:** cleaner, but the old tables hold real asymmetries (the bear rarely met);
  audited rows keep them without growing back into tables.

## Open questions (for Zach)

1. Adopt this as stage 1 (02zv §6, items 1, 2, 5, 6), replacing D2-192's "each taken by its own technique and skill" with
   "general methods, with skill by method and familiarity by kind"?
2. May 37.2 raise the changes to `verbs.py`, `knowledge.py`, `prompt.py` and `perceive.py` with 37.4 on the board, and build them on a
   branch of `ecology` once agreed?
3. A target name resolves whether or not the kind is here (finding out is the act): agreed, or only kinds the person has met?
4. Which methods are basic (§6): is the list right?

## History

- 9 Nov 2026: written as the build brief for stages 0 and 1 and pack K0 of 02zv, after Zach asked whether everything was written up
  well enough for another agent to build it without doing things wrong (it was not: the spec's D2-192 points the other way, the
  notes disagree, nothing was decided, and the design lacked the details a builder needs). With Zach's answers of 9 Nov: targets
  determinate on `looking for`; the system text lists only what one knows, as ways of doing; a second layer of skill by target.

## Sources

docs/review/37_growth/02zv_wild_consolidation.md (C1 to C3, C14, C15, K0), 02zu_wild_chains_capital_actions.md §C, 02zs_wild_development.md
§7 and §8.1, 02zq_wild_audit.md; proposals/knowledge.md, agent_view.md, use_by_physics.md, wild_behaviour.md; spec/environment/wildlife.md;
branch `ecology`: cybertron2/engine/data.py, wild.py, verbs.py, knowledge.py, prompt.py, perceive.py, wild/kinds.py; the scratchpad's
wild_run6/run.json (system text sizes); D2-52, D2-93, D2-192, D2-193, D2-198, D2-203, D4-21, D4-24, D4-58, D4-103.
