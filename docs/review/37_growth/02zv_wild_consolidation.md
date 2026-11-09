# 02zv: the wild layer consolidated: core engine changes, content ledger and packs (10 Nov)

Zach (9 Nov): "do a consolidation of what it has suggested into what are the core mechanism / engine changes vs content changes and
then triage all the content changes (kinda like how you already ranked them) and organise into packs. This shouldn't lose content
unless you explicitly decide it shouldn't be added, but can add some of the content to less important packs and the core ones to
prioritise building and testing first."

This note consolidates 02zr (behaviour critique), 02zs (development), 02zt (dependences) and 02zu (chains, capital, actions, decay),
with `proposals/wild_behaviour.md` (v2), `proposals/forays.md`, the audit 02zq and the built kinds on the `ecology` branch. It
separates **core engine changes** (§2) from **content** (§3, the ledger), groups content into **packs** (§4), lists **changes to
existing files** (§5) and **decisions for Zach** (§6). It is a session note; nothing is decided by it.

**Binding answers from Zach (10 Nov), applied throughout:**
1. **Decay runs on the act clock** (a day is a day), soft stages over a few days at least, sized by the thing (calibrate): small
   things (a hen, a hare, a gut pile) mostly gone in 1 to 2 days; medium (a deer, a sheep, a pig, a human body) fresh 1 day, soft
   stages to about day 4 to 6, dry by about 6 to 8, bones lingering about a season; large (a cow, a horse) soft stages to about day
   8 to 10, bones one to two seasons; warmth speeds it (summer about 1.5 times), cold slows it, frost stalls it; burial slows it and
   draws diggers; scavengers remove soft mass by how many come (a deer can be stripped in two nights). This replaces 02zu Part D's
   timings (§5).
2. **Per-pair escape-hatch numbers** on the encounter rule are allowed only as audited calibration data on a kind's row, counted by
   a guard test, so they never grow back into per-kind take tables.
3. **Targets in free words only in forays** (where the interpreter call reads them). Everywhere else a target is determinate:
   resolved like today's names, with refusals that say what is meant (§2, core C2).
4. **The daily menu is already gone** (D4-78, `view: beliefs`, in every recent world). What remains: the system text is still the
   verb manual (about 14,000 characters, listing techniques with their tool multipliers), the reply schema lists known names, and
   some refusals list technique names. The change is that **the manual lists methods as ways of doing (general), not kind-named
   techniques**. 02zu C.8 is corrected accordingly (§5).
5. **Crafting and discovering new things** is flagged for later (OPEN L-103): not designed here; a placeholder pack (K12) lists the
   content that depends on it.

**Standing:** nothing social forced (institutions emerge; forest law and seeded rights only as world options for arms; D2-194 is
already "a world may give", so it stays a world option); no bespoke one-kind actions; no attention filtering; places live in memory
(forays.md).

## 1. Findings in brief

1. **Fifteen core changes carry all the content** (§2). Three are foundations every pack needs and must be built and tested first,
   on the kinds already built, with no new content: **C1** traits on kinds and properties on methods, gear, barriers and stores with
   one encounter rule; **C2** the consolidated verbs with shared object slots and determinate targets; **C3** methods as data with
   skill and sign-reading per method family. Their test is that the built wave behaves as before while every kind-named technique
   is gone.
2. **Three more core changes make the first content packs worth building:** **C4** shared perception with wind direction, **C5**
   the animal interface additions (alarm, follow, probe, cache; typed memory; traits), and **C6** displacement and refill. Without
   C6 every defence stays private and no collective response has a physical reason to appear.
3. **Capital and keeping need their own core:** **C7** standing works with condition, upkeep, capacity and depreciation; **C8**
   kept populations in structures with trained beasts' bonds and breeding (much of it 37.4's husbandry generalisation); **C9** the
   butcher step, by-product goods and delayed processes; **C10** one decay-and-scavenging rule.
4. **Forays and the land carry knowledge and reach:** **C11** forays with land features and places in memory; **C12** works on
   parcels and edges with visibility from position; **C13** evidence and marks. **C14** world options and **C15** diagnostics
   complete the set.
5. **The content ledger has 346 rows** (§3), each mapped to a pack and a rank, from every source. Nothing is dropped silently: 31
   items go to proposed cuts (§3.9) with reasons, 38 rows are marked recast (to their physical substrate or a general method),
   and 32 duplicates point to one canonical row.
6. **Thirteen packs and a world-options set** (§4). **First** (right after the core): K0 the built kinds converted to the core; K1
   every village (fields, stores, hens); K2 the carcass, the store and decay; K3 forays, methods and knowing; K4 river and fen.
   **Later:** K5 wood and frontier; K6 keeping (waits on 37.4's husbandry); K7 land works and infrastructure; K8 crafts and wild
   goods; K9 coast and cliff; K10 illness and the hidden (waits on illness in people); K11 lodgers of buildings; K12 discovery
   (placeholder, L-103). W holds the world options for experimental arms.
7. **The biggest single change to existing code** is removing the six wild yield kinds and about twenty kind-named techniques from
   the ecology branch in favour of methods with properties (C1 to C3). It is mostly deletion and data, and it is 37.4's code.

## 2. Core mechanisms and engine changes

Owners: code under `cybertron2/` is 37.4's (CLAUDE.md); 37.2 owns the kinds' data, the numbers and the design notes. Sizes: S under
300 lines, M 300 to 1,000, L over 1,000 (code plus data, rough).

### C1. Traits on kinds; properties on methods, gear, barriers and stores; one encounter rule
- **What:** each kind row carries body and behaviour traits (size class; climbs, leaps, burrows, gnaws, flies; uses fixed runs;
  flocks and follows its kind; senses; active by day or night; lives in colonies, burrows, dens, roosts; commutes in a straight line
  to a fixed home). Each method, gear item, barrier and store carries physical properties (what the method needs of a target;
  selectivity by size; reach; strength; height; gap; raised; sealed; noise; light; scent). One rule decides what meets what, for
  takes, barriers, stores, deterrents and standing works alike. Per-pair numbers allowed only as audited calibration data on a
  kind's row, counted by a guard test (Zach, answer 2).
- **Why:** answers new kinds with old capabilities; a better net or wall answers more kinds; removes per-kind take tables (02zs
  finding 4, §8.1; 02zu C.5).
- **Content that depends on it:** every pack.
- **Changes:** `engine/wild.py` (`take`'s `takes` tables, `_targets`, `_fenced`, `_answer`), `data.py` TECHNIQUES `yield.takes`,
  RESOURCES rows (`taken`), FENCES, fittings (granary, bins, cellar); `wild/kinds.py` NEAR_PEOPLE targets; spec
  environment/wildlife.md, economy/production.md (tools by method).
- **Owner:** 37.4 (code); 37.2 (trait and property data). **Size:** M.
- **Test:** a guard test that no technique, target or barrier names a kind and that calibration rows are counted and listed;
  wave 1's outcomes (boar, deer, fox, hare, eel, fowl, rats) within tolerance of the branch's figures on the same seeds.

### C2. Consolidated verbs with shared object slots and determinate targets
- **What:** the verb grammar back to about two dozen kinds of change (verbs.md; agent_view.md point 4); `gather` and `work` take one
  object: **method** (a known way of doing), **target** (optional), **place** (here, or a named or remembered place), **gear**,
  **party**, **units**, **for**. `travel` takes a route for forays (C11).
  - **Determinate targets (Zach, answer 3), built on the existing `looking for` modifier** (on `gather`: "name it, a kind or a sort
    (boar, deer, hares, fowl, small game)", read by `wild._wanted` and `_wanted_plants`): a target is a name from a closed vocabulary: kind names and the families they are
    known by (RESOURCES `taken.family`, as `wild._wanted` already reads "deer", "small game"), goods (ITEMS), tagged or named things
    and herds (D4-68), crops and loads by name. It resolves as `KN.resolve` does today: exact name, alias, label word, a plural;
    only names the person has met (read in a sign, held, been told, or seeded) are accepted. An unknown word is refused with the
    names it knows that the method could take: "you know of red deer, roe and hares here; 'hart' is not one you know" (D4-95's
    style). No target means "whatever the method meets". Free words are read only in a foray's intent, by its interpreter.
  - **Known methods and the manual (answer 4; the coordinator's check of run 6):** the manual already lists only techniques a
    person knows (`prompt.verb_lines` filters by `KN.level`), but the wild pack seeds every wild technique into "Everyone knows"
    (about 60 crafts for every agent, including taking young herons, trapping beavers and digging out a fox earth in villages that
    may have none), each with tool multipliers ("bare hands x0.25, a copper tool x2"); the system text is about 20,000 characters
    with the pack off (verbs and reply about 12,300 of it) and about 22,300 with it on (run 6, up from 20,700 in run 1). The
    change: **methods are seeded by upbringing and by what the land holds** (D4-21), not to everyone; the manual describes each
    known method as a way of doing (what it needs, the gear, where it is done), at the depth of the person's knowledge, **without
    multipliers, yields or kind lists**; a person knows only what it knows, but enough to use it. The reply schema keeps free
    strings (agent_view.md point 8). **Refusals say what is wrong without listing the catalogue** (today `_technique` lists every
    technique of the verb from `packs.techniques`): an unknown method is refused as unknown to the person, with the methods it does
    know for that verb at most.
  - Fold the duplicates: the field watches into `guard` with gear; `shut the hens in` and the gate techniques into `set`; `fence`
    and `gate` yield kinds into `build` and `set`; `care` as a method of `work`; `searching` and `looking for` into one target slot.
- **Why:** no bespoke one-kind actions; variety by data on a few verbs (D4-24); determinate replay and checking.
- **Depends on:** C1, C3.
- **Changes:** `engine/verbs.py` (`VERB`, `_technique` and its yield-kind branches, `_as_modified`, refusals), `knowledge.py`
  (`resolve`, `options`), `prompt.py` (the verb manual, reply schema), `data.py` TECHNIQUES (methods), spec agents/actions.md,
  modifiers.md, information/prompts.md.
- **Owner:** 37.4. **Size:** M to L.
- **Test:** the coverage test verbs.md asked for (every mechanic reachable by a verb and object); replay exact; refusal audit (review
  38.50's method) shows no rise in refusals; an unknown target is refused with the known names; the system text shrinks with the
  wild pack on (no unknown or unused methods listed for anyone; no multipliers); no refusal lists the catalogue.

### C3. Methods as data; skill and sign-reading per method family
- **What:** a method row (stalk, drive, course, snare, trap, net, shoot, spear, angle, dig, gather young or eggs, follow a line
  home, decoy; guard; den and burrow work; work a crop against a load; tend, feed, harvest a kept population; butcher; smoke, salt,
  tan, render) with properties (C1), units, crew effect, danger, whether it leaves a standing work, and its **skill family**. Skill
  by practice (D2-52) and readings by skill (`perceive.practised`, `reads_as`) attach to the family and carry across targets
  (generalising `SKILL_CARRY`). Readings by skill at three levels (02zq's open item).
- **Why:** a good netter nets pigeons, fowl and partridge; transfer and improvement (02zs §1.2).
- **Depends on:** C1.
- **Changes:** `data.py` TECHNIQUES, `knowledge.py` (skill, tried), `perceive.py` (`practised`), `wild/kinds.py` (`SKILL_CARRY`,
  sign rows' `read`), spec production.md (skill), information/noticing.md.
- **Owner:** 37.4 (code), 37.2 (method data). **Size:** S to M.
- **Test:** skill earned stalking deer raises stalking roe; a netter's readings of flocks improve with netting practice only.
- **Second layer, by target (Zach, 9 Nov: "skill can still vary within a technique based on target as another layer"):** on top
  of the method family's skill, a person's familiarity with a kind (or a sort: deer, fowl, small game) grows with practice on it,
  being taught about it, and reading its signs; it raises chance and yield for that kind within the method, and carries in part to
  kinds with similar traits (C1), never to the whole family. The built per-kind expert readings ("expert:t", 02zq) become this
  layer's readings. So a snarer is good at snaring, and better at snaring the hares they know than the rabbits they do not. It also
  keeps the part of D2-192 that gives each kind its own skill, as a layer rather than as its own technique.
- **Test (second layer):** two snarers of equal method skill, one practised on hares, the other on rabbits: each does better on its
  own kind; both do better than an unpractised snarer on either.

### C4. Shared perception, and wind direction
- **What:** animals notice people by the engine's one noticing rule run from their side (senses x visibility x presence x a person's
  conspicuousness: crew, dog, noise, light, carried meat or blood, moving or still); smell uses a **wind direction** field in the
  climate (an engine gap). The "Now" section shows the wind's direction (a sense anyone has).
- **Why:** stealth, wind, crew size, dogs and fire matter consistently across kinds (02zr M1); smell of carcasses by wind (02zu D).
- **Depends on:** the noticing rule (built), the climate (built: speed only).
- **Changes:** `engine/climate.py` (direction), `perceive.py` / `things.py` (the rule called with an animal observer),
  `engine/wild.py` (`_answer`, watches), spec environment/climate, information/noticing.md.
- **Owner:** 37.4. **Size:** M.
- **Test:** an upwind approach finds deer half as often as a downwind one; a crew of four is noticed more than one person.

### C5. Animal interface additions
- **What:** primitives **emit an alarm** (a sound sign others read), **follow** (move toward one's kind), **probe** (test a door or
  gap without entering), **cache** (store food at a place); typed memory stores (places, harms, scares, people, routes) with a
  knowledge holder; a bold-shy trait per group or individual; a route graph per group (02zr M4); guard tests that modules read only
  what others emit (02zr §3.1, §3.2).
- **Why:** constitutional difference lives in modules (D2-203); sentinels, flocks, lapse probers, caching foxes and jays, culture.
- **Depends on:** D2-203's interface; C4 for alarms read by the rule.
- **Changes:** `engine/wild.py` (groups, `_groups`), `wild/kinds.py` (NEAR_PEOPLE becomes module data), spec environment/wildlife.md.
- **Owner:** 37.4 (interface), 37.2 (modules' design and data). **Size:** M.
- **Test:** blocking a route's strongest edge diverts the group within one engine night; killing the knowledge holder clears its
  stores; an alarm in a parcel lowers deer found there.

### C6. Displacement, refill and downstream loads (physical externalities)
- **What:** a raider turned or a flock lifted goes to its next known target that night; a lapse prober that fed probes the hamlet
  more; a vacated territory refills from the ring after some engine days unless the ring is also emptied; a weir takes what would
  pass downstream; retting fouls water downstream; a dam floods a meadow below.
- **Why:** makes private defence a shared problem without any rule (02zr M3; 02zs §5.3).
- **Depends on:** C5 (module responses), the area graph (built).
- **Changes:** `engine/wild.py` (raids, targets), `wild/ecology.py` (refill), spec environment/wildlife.md.
- **Owner:** 37.4 and 37.2. **Size:** S to M.
- **Test:** the unscared neighbour's field loses more when the next field is scared than when neither is; one lax household raises
  its neighbours' hen losses; a cull is offset within N engine days without neighbours' culls.

### C7. Standing works; condition, upkeep, capacity, depreciation, quality
- **What:** a thing at a place with a method (a set trap, snares, a set net, traps in a weir, a fish trap) resolved each night by C1,
  holding what it takes, robbed or emptied by whoever comes; and for all durable goods and structures (traps, nets, weirs, hives,
  pales, coops, granaries, kennels, smokehouses): condition that falls by use and weather, mending as work, a capacity, failure when
  neglected, and quality where it changes value (a hide spoiled by a bad take, a fraying net) (02zu Part B; 02zt §6).
- **Why:** capital substitutes for labour only if it works unattended, wears and holds a capacity.
- **Depends on:** C1; wear (built), fences' upkeep (built), D2-87 decay (built).
- **Changes:** `engine/night.py` (a standing-works step), `things.py` (things with methods), `wear.py`, `data.py` ITEMS, FITTINGS,
  FENCES; spec economy/production.md (tools), buildings.md (fittings).
- **Owner:** 37.4. **Size:** M.
- **Test:** a line of six traps beats foraging per unit at full game and not at a fifth (02j's figures); a trap's catch can be
  taken by a passer-by and is seen by the rule; a neglected net loses condition.

### C8. Kept populations in structures; trained beasts with bonds; breeding
- **What:** husbandry.md §4 and §7: a population is kept when its habitat is a held structure and its food a need someone meets;
  wild and kept as two rows of one lineage; wild, kept, feral as a population's state; structures with capacity for a class of kinds
  (pen, coop, sty, hutch, warren, dovecote, pond, hive, park, mews, kennel); dogs and hens as kept beasts (not a fitting and a store
  good); led beasts that multiply a method (D4-58) with a bond to the trainer that fades without handling; traits on a lineage that
  drift with which parents breed.
- **Why:** the keep family and the bridges (02zs §3.1); specialists bound to beasts.
- **Depends on:** 37.4's herds generalised into beasts (husbandry.md §7c; a board item); C7 (structures, capacity).
- **Changes:** `engine/herds.py`, `farm.py`, `data.py` (HERDS, ROLES), `wild/kinds.py` (hens), spec economy/livestock.md.
- **Owner:** 37.4. **Size:** L.
- **Test:** cattle behave exactly as now; a hound lent works at half; a warren with a broken bank leaks rabbits to feral.

### C9. The butcher step, by-product goods, delayed processes
- **What:** a general `butcher` method on any carcass (wild or kept), giving parts by the kind's body (meat, fat, hide, bone, sinew,
  horn or antler, offal); goods fat (rendered to tallow), bone, sinew, glue, feathers and down, wax, honey, a general pelt with
  quality, cord (bast first), nets, bow and arrows as weapon grades, traps (decided D2-23, not built); delayed processes (batches at
  a fitting over days: smoking, tanning, curing, rendering, training); light as a use of tallow, rushlights, horn panes and wax.
- **Why:** the carcass is the economy's hub (02zs §2.4; 02zt §4.1); light for the watch (02zq one-off 1).
- **Depends on:** C7 (fittings with capacity); recipes (built).
- **Changes:** `data.py` ITEMS, TECHNIQUES (recipes, slaughter), `farm.py` (slaughter's output), `things.py` (carcass parts),
  `engine/wild.py` (take's goods), spec economy/goods.md, production.md; water_and_preservation.md §7's smokehouse.
- **Owner:** 37.4 (code), 37.2 (goods and recipes). **Size:** M.
- **Test:** a slaughtered cow's parts sum to its body; a smokehouse batch is ready on its day and spoils if its fire is not fed.

### C10. One decay-and-scavenging rule over organic things
- **What:** every organic thing at a spot (carcass, body, remains, food left out, leavings, the midden) has a mass by part, a stage
  (fresh, ripe, putrid, dry, bones), conditions (open dry or wet, warm, cold, frozen, covered, hung inside, buried at a depth,
  salted, smoked) and a disease load; each night its stage advances on **the act clock** by its size class (Zach, answer 1: small 1 to
  2 days; medium fresh 1 day, soft to about day 4 to 6, dry by 6 to 8, bones a season; large soft to about day 8 to 10, bones one to
  two seasons; summer x1.5, cold slower, frost stalls; burial slows and draws diggers); insects and microbes take soft mass by
  warmth; scavenger kinds come by their traits (senses, diet by stage, boldness near people, range, activity, others present) and
  remove soft mass by how many come (a deer can be stripped in two nights); **burial depth is a property of the burial** (the units
  spent against the ground: frozen, stony or wet ground makes a shallow grave; proposals/graves.md, D4-99): a proper grave is very
  rarely reached, a shallow or hasty one (a beast buried, frozen ground, a body hidden in haste) is dug by foxes, badgers and dogs
  with some chance; **spillover** falls out of the general rules: a scavenger or predator that fed at a place remembers it (place
  memory, C5), comes back, and while there its raider or predator behaviour applies to what is near (hens, a fold, a calf, a person
  at a bear's cache), which can make a loop (carcasses draw wolves, wolves kill stock, more carcasses); it emits signs by stage (birds circling, smell by wind,
  flies, bones); what scavengers near people do not take, and deaths in the wild beyond them, stay in the area's carrion stock
  (wild/ecology.py).
- **Why:** things do not vanish; handling choices matter; scavengers drawn to villages; evidence; danger at a cache (02zu Part D).
- **Depends on:** C1 (traits), C4 (smell by wind), C9 (parts), D4-52, D2-87, D2-96 (built).
- **Changes:** `things.py` (`leave_carcass`, `carcass_fresh`, `body_state`, `rotting`), `data.py` THINGS, DECAY, `night.py`,
  `signs.py` (CARCASS, SLAUGHTER rows), `wild/ecology.py` (carrion), spec world/things_in_places.md (D2-95's "scavengers later",
  OPEN L-2).
- **Owner:** 37.4 (code), 37.2 (stages and kinds' data). **Size:** M.
- **Test:** a deer left in summer is stripped in about two nights where foxes and dogs are near, and lasts longer where none are;
  a frozen carcass keeps; a proper grave is almost never reached while a shallow one (frozen ground, a beast hastily buried) is dug
  with some chance; **a carcass left near the fold raises the fold's losses over the next nights against one burned or buried**;
  no kind is named in the rule.

### C11. Forays, land features, places in memory and names
- **What:** forays.md as written (an intent in the person's words; one small interpreter call a foray a day, blind to hidden state;
  a route over known places; legs walked with travel by terrain; noticing along the way; takes and finds by C1 with the gear
  carried; a short story of events; a night out if it does not return; camps and nodes later); a few **features** per area from the
  generated land (falls, pool, ford, crag, spring, an old wood's core, a clearing), which animals' modules also use; places live in
  the person's memory, which it may name (no engine table of spots).
- **Why:** local, particular knowledge; reach by units; the take, know and reach ladders (02zs §3.6, §10).
- **Depends on:** C1, C2 (`travel` with a route), C4; wild/areas.py (built on the branch); memory (D4-61, D4-64).
- **Changes:** as forays.md "Affects": spec agents/actions.md, world/places.md and parcel_graph.md, information/memory.md,
  record/execution.md, environment/wildlife.md, economy/lodging.md; `engine/verbs.py`, `roads.py`, `layout.py`, `memory.py`,
  `wild/areas.py`.
- **Owner:** 37.2 (design), 37.4 (code). **Size:** L.
- **Test:** forays.md §7.

### C12. Works on parcels and edges; visibility from position
- **What:** field-work-like works with upkeep: rides cut through a wood (raise visibility, standers' places, hauling), high seats and
  hides (raise what a watcher notices, lower animals' noticing of the watcher), lookouts (sight to the next parcels), cart tracks into
  a wood (handcarts reach it), landings and fords made good; barriers with properties on parcel edges (hedges, banks, walls, pales,
  mesh), extending fences (D2-126, D2-130; OPEN L-24 for borders).
- **Why:** infrastructure that helps many things at once (02zt §3).
- **Depends on:** C1, C4, C7; field works (D2-66, built).
- **Changes:** `farm.py` (works), `herds.py` (fences), `layout.py`, `perceive.py` (presence from a high place), spec production.md
  (field works), livestock.md (fences).
- **Owner:** 37.4. **Size:** M.
- **Test:** a watcher on a high seat notices a sounder at the next parcel; a cart track lets a handcart reach the wood.

### C13. Evidence and marks
- **What:** traces of people as well as animals (tracks in snow, a robbed snare, a cut fence, leavings of a poached kill); marks cut on
  an animal or a thing that anyone can cut, cut over or forge, read by skill; animals' memory of people (C5) shown as signs (crows
  mobbing a trapper).
- **Why:** evidence that can be faked is substrate for disputes (Zach's principle 1).
- **Depends on:** C4, C5; the trace and thing machinery (built).
- **Changes:** `things.py`, `signs.py`, `engine/wild.py` (traces), spec information/signs.md.
- **Owner:** 37.4. **Size:** S.
- **Test:** a forged mark reads as the original to the untaught and as altered to the skilled; a poacher's leavings are found by the
  rule.

### C14. World options for experimental arms
- **What:** world settings, off by default: a forest-law arm (named kinds and their cover held by a named person; dogs within it
  lawed; fences within it limited in height; a fence month closing the wood); rights in wild kinds (D2-194, "a world may give");
  seeded structures from history (old hedges, a warren, a fishpond, a weir); method-seeding arms (which households know which
  methods); invented or masked kinds and quirks for learning tests.
- **Why:** principle 1: social settings only as arms.
- **Depends on:** packs (D4-104), world files (built).
- **Owner:** 37.4 (mechanism), 37.2 (worlds). **Size:** S.
- **Test:** each option's access gates verified in a dry run (scenario_design §4).

### C15. Diagnostics (measured, never acted on)
- **What:** lines per agent-day and acted-on rates by kind (diagnostic only); method diversity per household; capital share of
  defence; kept share of meat and goods; by-product use; structures built; standing works' yield against hand work; scavenger visits
  by place; evidence found; dependence edges through wild goods; institutions that emerged (coded after runs); learning problems
  P1 to P24 as coding categories.
- **Owner:** 37.2 (analysis scripts outside the engine). **Size:** S.
- **Test:** the scripts run on the branch's existing runs.

### 2.1 Dependency graph and build order

```
C15 diagnostics ─┐     C14 world options ─┐                          (independent; build first, cheap)
                 │                        │
C1 traits+properties+encounter rule ──┬──> C3 methods, skill per family ──> C2 verbs, object slots, determinate targets
                                      │
C4 shared perception + wind ──> C5 interface additions ──> C6 displacement and refill
                                      │
C1 ──> C7 standing works, condition, capacity ──┬──> C9 butcher, by-products, delayed processes ──> C10 decay and scavenging (+C4)
                                                └──> C8 kept populations, bonds, breeding (+ 37.4's herds generalised)
C1 + C2 + C4 ──> C11 forays, features, places in memory ──> C12 works on parcels and edges (+C7)
C4 + C5 ──> C13 evidence and marks
```

**Build order:** (0) C15, C14; (1) C1, C3, C2, converting the built kinds (pack K0) with no new content; (2) C4, C5, C6 (pack K1's
mechanics); (3) C7; (4) C9, C10 (pack K2); (5) C11, C13 (pack K3); (6) C12; (7) C8 (with 37.4's husbandry; may run in parallel from
stage 3).

**Must be built and tested before any content pack:** C1, C2, C3 (with their guard tests) and C15. Each later core change gates the
packs that name it in §4.

## 3. The content ledger

Every content item from every source, one row each. **Needs** names the core changes (§2). **Pack** and **rank** are §4's (rank is
the order of building inside the pack). **Status:** *keep* (content as designed, on the core); *recast* (institution-like or bespoke,
kept as its physical substrate or as a general method); *dup* (the same item as an earlier row; it takes that row's pack and rank);
*defer* (kept, in a later pack, waiting on a dependency); *cut* (proposed, with its reason in §3.9); *option* (a world option, W).
Rows are numbered for reference; numbers run through the whole ledger.

### 3.1 Built on the ecology branch (kinds.py, plants.py, loads, diseases, sites, legends, regimes, markers, engine/wild.py)

| # | Item | Needs | Pack | Rank | Status |
|---|---|---|---|---|---|
| 1 | kind-named techniques (`stalk deer`, `boar hunt`, `snare hares`, `fowling`, `hunt`, `hunt the wild`, `set eel traps`, `trap beavers`, `fish by hand`, `take the young herons`, `take the young rooks`, `dig out the fox earth`, `break the beaver dam`) | C1, C2, C3 | K0 | 1 | recast: methods |
| 2 | field watches `watch the field (clapper, dog, fire, horn)` | C2, C4 | K0 | 2 | recast: `guard` with gear |
| 3 | `shut the hens in`; `shut the gate`, `open the gate` | C2 | K0 | 3 | recast: `set` a door or gate |
| 4 | `pick slugs at dusk`, `clear the grubs off the beans`, `top the beans` | C2, C3 | K0 | 4 | recast: work a crop against a load |
| 5 | `range: near / the wood around / far` modifiers naming seven techniques | C2, C11 | K0 | 5 | recast: range of any take; later a foray |
| 6 | `reads_as` per technique; `SKILL_CARRY` by name | C3 | K0 | 6 | recast: per method family |
| 7 | per-technique `takes` tables naming kinds | C1 | K0 | 7 | recast: traits against properties |
| 8 | kind rows: red deer, roe, wild boar, brown hare, woodpigeon, rats, wildfowl, eel, voles and mice, owls, fox, wolf, raven, brown bear (W2 food web, habitat, diet, shy) | C1 (traits added) | K0 | 8 | keep |
| 9 | NEAR_PEOPLE group machine (targets, drive, memory, return, lead nights, answers to scares, harm, wariness) | C1, C5 | K0 | 9 | recast: module data per kind |
| 10 | sign bundles (edge, raid, turned, tried) with lay and knows readings; expert readings; weather leads; work notices | C3 | K0 | 10 | keep; readings by method family, three levels |
| 11 | WHEN conditions (seasons, frost runs, snow, mast this and last autumn, hunger, pressure, hard winter, rain after dry, tomorrow) with effects | C5 | K0 | 11 | keep |
| 12 | hunting pressure (the hunted wood empties, drifts back) | C1 | K0 | 12 | keep |
| 13 | a wounded beast (blood trail, danger for two days) | C1 | K0 | 13 | keep |
| 14 | litters in a take (cubs at the earth in spring) | C3 | K0 | 14 | recast: den work method |
| 15 | followers of the harvest (rats and mice to full barns) | C1 | K0 | 15 | keep |
| 16 | migrants return by how many left (fowl) | | K0 | 16 | keep |
| 17 | ten wild plant kinds as parcel stocks; gathering; leaching acorns; poisonous mushrooms (D2-200 to D2-202) | C2 | K0 | 17 | keep |
| 18 | the mast pulse (budget, frost at flowering, fail after heavy) and its signs (one-off 7: its own function) | | K0 | 18 | keep; signs as a pulse's signs |
| 19 | loads: slugs, aphids, ladybirds, fungi (flush, flood, cold stall, misread grubs, burning stubble) | C3 | K0 | 19 | keep |
| 20 | markers: blackthorn, swallows, cuckoo, frogspawn, oak and ash, may, first frost | | K0 | 20 | keep (levers in K1 rank 12) |
| 21 | diseases: murrain, mange, swine fever, hare sickness | | K0 | 21 | keep |
| 22 | sites: heronry, rookery, beaver lodge and dam | C3, C7 | K0 | 22 | keep (holders and customs out) |
| 23 | leaders: the old sow | C5 | K0 | 23 | keep |
| 24 | legends: the great boar, the white hart, the old dog-wolf, the bear | | K0 | 24 | keep as built; recast emergent in K3 rank 20 |
| 25 | regimes: great freeze, vole plague, bare years | | K0 | 25 | keep |
| 26 | vole phase clock; owls and kestrels as presence | | K0 | 26 | keep |
| 27 | history before the run (ten years of the step) | | K0 | 27 | keep |
| 28 | hens as a store's goods, laying (one-off 3) | | K0 | 28 | keep until K6 rank 2 |
| 29 | the dog as a fitting (watch, raid alarm) | | K0 | 29 | keep until K6 rank 1 |
| 30 | `make clappers`, `make a horn` | | K0 | 30 | keep (recipes) |
| 31 | data hygiene: numbers in code, RAIN_MEAN repeating the climate, presentation spots named as choices, the herd's `ill` record (one-offs 6, 8, 9) | | K0 | 31 | keep (fix) |
| 32 | murrain meat edible with no effect (one-off 10) | illness | K10 | 4 | defer |

### 3.2 02zq's "not built" list

| # | Item | Needs | Pack | Rank | Status |
|---|---|---|---|---|---|
| 33 | pannage | C8 | K6 | 3 | defer |
| 34 | the fold | C8, C12 | K6 | 13 | defer |
| 35 | lambs (fox and wolf at lambing) | C8 | K6 | 13 | dup 34 |
| 36 | swine fever in kept pigs | C8 | K6 | 16 | defer |
| 37 | geese as watchers | C8, C5 | K6 | 2 | defer |
| 38 | hives, and the bear at them | C8 | K6 | 7 | defer |
| 39 | wasps (a wasp year; robbing hives; at the fruit) | C1 | K5 | 18 | keep |
| 40 | rabies | illness | K10 | 1 | defer |
| 41 | ergot | illness | K10 | 5 | defer |
| 42 | murrain meat and milk | illness | K10 | 4 | dup 32 |
| 43 | lore as tested belief (tallies of cases) | 37.4's belief store | K3 | 29 | defer |
| 44 | misreads held as beliefs | 37.4's belief store | K3 | 29 | dup 43 |
| 45 | mowing driving voles to the ricks | C1 | K1 | 14 | keep |
| 46 | the mast cascade (rodents, then predators' hungry year) | | K1 | 18 | keep (through the web) |
| 47 | the dangerous yearling | C5 | K5 | 5 | keep |
| 48 | readings by skill at three levels | C3 | K0 | 10 | dup 10 |
| 49 | traces that age and that rain erases | C13 | K3 | 30 | keep |

### 3.3 wild_behaviour.md (v2) §3 to §5

| # | Item | Needs | Pack | Rank | Status |
|---|---|---|---|---|---|
| 50 | facets F1 to F13 as modules | C5 | core | | recast: constitution modules; facets as views |
| 51 | F1 the search game (lie, search, clues, approach, spooked, knowledge, help, traps) | C11, C1, C4 | K3 | 1 | recast: forays |
| 52 | F2 ranging by value; defences physical; memory of people's pattern | C5, C6 | K1 | 8 | recast: route graph, spatial adversary |
| 53 | F3 prey-following; switching; surplus killing | C5 | K5 | 5 | keep |
| 54 | F4 the run or pulse; gear at points; the window | C7 | K4 | 1 | keep |
| 55 | F5 the site you steward (stock, claims, leaving) | C7 | K0 | 22 | recast: no holders or customs in the engine |
| 56 | F6 the engineer | C1 | K4 | 12 | keep (as a primitive) |
| 57 | F7 the outbreak | | K0 | 19 | dup 19 |
| 58 | F8 the lodger | C1 | K1 | 4 | keep |
| 59 | F9 danger | C1 | K0 | 13 | keep |
| 60 | F10 the informant | C5 | K3 | 9 | recast: sentinels |
| 61 | F11 taking and taming | C8 | K6 | 11 | keep |
| 62 | F12 the legend | C15 records | K3 | 20 | recast: emergent |
| 63 | F13 the calendar-giver | | K1 | 12 | keep (with sowing rules) |
| 64 | transitions wild, kept, feral, legend; mixing | C8 | K6 | 12 | keep |
| 65 | boar 1: the learning sounder | C5, C6 | K1 | 8 | recast: per-night contest, spatial adversary (P12 cut) |
| 66 | boar 2: the matriarch's memory | C5 | K5 | 1 | keep (with splitting) |
| 67 | boar 3: the mast's two years | | K5 | 2 | keep |
| 68 | boar 4: the boar hunt with a crew and hound | C3, C8 | K5 | 3 | keep |
| 69 | boar 5: rooting the turf | C1 | K5 | 1 | keep |
| 70 | boar 6: striped piglets taken and raised | C8 | K6 | 11 | defer |
| 71 | red deer 1: stalking | C11, C4 | K3 | 18 | keep (in forays) |
| 72 | red deer 2: the herd as a stock with a make-up; under a right | C14 | K5 | 4 | keep; the right is option W.2 |
| 73 | red deer 3: the hunted wood | | K0 | 12 | dup 12 |
| 74 | red deer 4: the wood that does not regrow | C1 | K5 | 4 | keep |
| 75 | red deer 5: winter at the ricks and bark | C1 | K5 | 4 | keep |
| 76 | red deer 6: a calf to a park | C8 | K6 | 11 | defer |
| 77 | roe 1: one to a patch | C6 | K3 | 17 | keep |
| 78 | roe 2: calling the buck in the summer rut | C3 | K3 | 17 | keep (a lure) |
| 79 | roe 3: the kid in the long grass | | K3 | 17 | keep (a sign at mowing) |
| 80 | wolf 1: a pack on its circuit | C5 | K5 | 5 | keep |
| 81 | wolf 2: deer first, herds when deer fail | C5 | K5 | 5 | keep |
| 82 | wolf 3: dispersers | C5 | K5 | 5 | keep |
| 83 | wolf 4: the drive and the bounty | C3 | K3 | 27 | recast: the drive kept; the bounty cut (§3.9 no. 3) |
| 84 | wolf 5: ravens follow the pack | C10 | K2 | 16 | keep |
| 85 | fox 1: one territory; tries the doors | C5, C6 | K1 | 5 | keep |
| 86 | fox 2: vole years and hen years | | K1 | 18 | keep |
| 87 | fox 3: the earth in spring | C3 | K1 | 5 | keep (den work) |
| 88 | fox 4: the winter pelt | C9 | K8 | 5 | defer (furs) |
| 89 | bear 1: the bear's year | | K5 | 6 | keep |
| 90 | bear 2: the hungry spring | | K5 | 6 | keep |
| 91 | bear 3: meeting a bear | C1 | K5 | 6 | keep |
| 92 | bear 4: the great hunt | C3 | K5 | 3 | keep |
| 93 | bear 5: rarity | | K5 | 6 | keep |
| 94 | hare 1: forms and runs | C1, C7 | K3 | 16 | keep |
| 95 | hare 2: snares are property (robbed, catch dogs) | C7, C13 | K1 | 3 | keep |
| 96 | hare 3: snared out and refilled | C6 | K3 | 16 | keep |
| 97 | hare 4: coursing | C8 | K6 | 1 | defer (sighthounds) |
| 98 | woodpigeon 1: flocks follow the food | C5, C6 | K1 | 1 | keep |
| 99 | woodpigeon 2: decoyed | C3 | K3 | 23 | keep |
| 100 | rook 1: the trade-off | C1 | K1 | 10 | keep |
| 101 | rook 2: the rookery; young taken | C3 | K3 | 26 | keep |
| 102 | raven 1: to carrion and to the wolves | C10 | K2 | 16 | keep |
| 103 | voles 1: the vole years | | K0 | 26 | dup 26 |
| 104 | voles 2: kestrels and owls follow them | | K0 | 26 | dup 26 |
| 105 | voles 3: the barn owl in the barn | C7 | K1 | 13 | keep |
| 106 | voles 4: the crash reaches the hens | | K1 | 18 | dup 86 |
| 107 | rats 1: held by how stores are built | C1 | K1 | 4 | keep |
| 108 | wildfowl 1: pushed in by the cold | | K4 | 6 | keep |
| 109 | wildfowl 2: flight lines | C3, C11 | K4 | 6 | keep |
| 110 | wildfowl 3: weak in a long freeze, fewer next winter | | K4 | 6 | keep |
| 111 | eel 1: the silver run | C7 | K4 | 1 | keep |
| 112 | eel 2: the weir and the river below | C6, C7 | K4 | 3 | keep |
| 113 | eel 3: spearing in winter | C3 | K4 | 15 | keep |
| 114 | salmon 1: up on the spate | | K4 | 4 | keep |
| 115 | salmon 2: the weir and the spawning upstream | C6, C7 | K4 | 4 | keep |
| 116 | trout: resident; tickling; refill | | K4 | 16 | recast: the water pack's stock (separate kind cut, §3.9 no. 25) |
| 117 | otter (deferred) | C7 | K4 | 10 | defer |
| 118 | heron 1: the heronry | | K0 | 22 | dup 22 |
| 119 | heron 2: the young taken | C3 | K3 | 26 | keep |
| 120 | heron 3: its size shows the fish | | K4 | 9 | keep (an expert reading) |
| 121 | beaver 1: the dam's trade-off | C6 | K4 | 12 | keep |
| 122 | beaver 2: slow to breed; trapped out | | K4 | 12 | keep |
| 123 | bees 1: lining the bees home | C3 | K5 | 7 | keep |
| 124 | bees 2: the bee tree as property | C13 | K5 | 7 | recast: a mark (substrate) |
| 125 | bees 3: the swarm into a skep | C8 | K6 | 7 | defer |
| 126 | bees 4: raided by a bear and by wasps | | K5 | 7 | keep |
| 127 | pine marten (deferred) | C9 | K5 | 15 | defer |
| 128 | falcon 1: the eyass and its training | C8 | K6 | 8 | defer |
| 129 | swan 1: marking | C13, C8 | K6 | 14 | recast: marks as tags |
| 130 | the built loads, diseases, plants, markers (§4.24) | | K0 | 19 | dup 19 to 21 |
| 131 | web chains (§5): deer hunted out to wolves at herds; heavy mast to more boar; failed mast to pigeons, boar, mice; vole crash to foxes and owls; bare autumn to a thin bear; wolf kill to ravens to fox and bear; beaver dam; weir upstream; rooks and grubs; deer browse and coppice; felling moves deer and boar; long freeze and fowl; first rain after dry; barn owl and mice | C5, C6 | K1, K4, K5 | as each kind | keep (they emerge from the kinds' rows) |

### 3.4 02zr: §4's added behaviours, M1 to M18, and other content

| # | Item | Needs | Pack | Rank | Status |
|---|---|---|---|---|---|
| 132 | boar: the per-night contest at the field (02zr's stretch contest, recast to one night's watch against distinct deterrents) | C2, C4 | K1 | 8 | recast |
| 133 | boar: the spatial adversary (next gap when one is watched) | C5 | K1 | 8 | keep |
| 134 | boar: splitting when the knowledge holder is killed | C5 | K5 | 1 | keep |
| 135 | boar: the mast race with pannage pigs | C8 | K5 | 2 | keep |
| 136 | boar: the wallow as the lie | C11 | K5 | 1 | keep |
| 137 | boar: later in the night under hunting pressure | C5 | K5 | 1 | keep |
| 138 | boar: calibration to 3 to 10% of need unwatched | | K0 | 8 | keep |
| 139 | red deer: the lord's deer at the corn with laws on the levers | C14 | W | 1 | option |
| 140 | red deer: a modest raid at the corn by default | C1, C6 | K1 | 8 | keep |
| 141 | red deer: the harbourer and the assembly | C11 | K3 | 28 | recast: knowledge told or sold; the assembly cut (§3.9 no. 11) |
| 142 | red deer: the stalk inside one act | C11 | K3 | 1 | recast: forays |
| 143 | red deer: venison as a gift raising standing | | K3 | 28 | recast: giving is built; standing cut (§3.9 no. 8) |
| 144 | red deer: the herd's count by a forester's act | C2 | K3 | 24 | recast: a count is a person's look, written if they choose |
| 145 | roe as the commoner's deer by a ruling | C14 | W | 2 | option (§3.9 no. 12) |
| 146 | roe: the bark as a sentinel | C5 | K3 | 9 | keep |
| 147 | roe: browse on new coppice | C1 | K5 | 16 | keep |
| 148 | wolf: the circuit across villages | C5 | K5 | 5 | keep |
| 149 | wolf: the bounty as an institution | | | | cut (§3.9 no. 3) |
| 150 | wolf: bounty fraud (a dog's head for a wolf's) | C13 | K3 | 30 | recast: heads as evidence read by skill |
| 151 | wolf: folding and the guard dog | C8 | K6 | 13 | defer |
| 152 | wolf: the persecuted pack grows shy | C5 | K5 | 5 | keep |
| 153 | fox: the lapse prober and the hamlet externality | C5, C6 | K1 | 5 | keep |
| 154 | fox: the treadmill (refill from the ring) | C6 | K1 | 5 | keep |
| 155 | fox: geese as the watch | C8 | K6 | 2 | defer |
| 156 | bear: the cached carcass | C10 | K2 | 13 | keep |
| 157 | hare: the form facing the wind | C1 | K3 | 16 | keep |
| 158 | hare: folklore (witches as hares) | | K3 | 19 | keep as seeded lore lines only |
| 159 | woodpigeon: local enhancement | C5 | K1 | 1 | keep |
| 160 | woodpigeon: displacement to the next field | C6 | K1 | 1 | keep |
| 161 | woodpigeon: decoyed with shot birds | C3 | K3 | 23 | dup 99 |
| 162 | rook: central-place foraging from the rookery | C5 | K1 | 10 | keep |
| 163 | rook: the trade-off shown both ways (grubs, the Four Pests misread) | C1 | K1 | 10 | keep |
| 164 | rook: the rookery and the house's fortune (folklore) | | K3 | 19 | keep as seeded lore lines only |
| 165 | raven: carcass informant; memory with corvids | C10, C5 | K2 | 16 | keep |
| 166 | voles: the owl hole | C7 | K1 | 13 | recast: a habitat fitting |
| 167 | voles: mowing to the ricks; pellets read | C1 | K1 | 14 | keep |
| 168 | rats: the cat | C5 | K1 | 7 | keep |
| 169 | rats: the rat-catcher with terriers | C3, C8 | K1 | 17 | recast: a skill and gear, hired if people hire |
| 170 | rats: poison | | K10 | | deferred to K10 (37.2 review; was §3.9 no. 27) |
| 171 | rats: black rats in thatch | C1 | K11 | 3 | defer |
| 172 | rats: plague | | K10 | | deferred to K10 (37.2 review; was §3.9 no. 26) |
| 173 | wildfowl: the decoy pond and its quiet zone | C7, C4 | K4 | 8 | keep |
| 174 | wildfowl: feathers and down to bedding | C9 | K8 | 6 | defer |
| 175 | eel: the river's lag by catchment | C11 | K4 | 1 | keep |
| 176 | eel: rents in sticks | | | | cut (§3.9 no. 6) |
| 177 | eel: traps as property, robbed | C7, C13 | K4 | 2 | keep |
| 178 | salmon: the gap in the weir | C7 | K4 | 3 | recast: a physical state of the structure |
| 179 | salmon: close time, water bailiff | | | | cut (§3.9 no. 4) |
| 180 | salmon: pearl mussels upstream | C6 | K4 | 14 | keep |
| 181 | heron: heron-hawking keeps the heronry valuable | C8 | K6 | 8 | keep (as a use, not a rule) |
| 182 | heron: the holder may forbid taking young | | | | cut (§3.9 no. 20) |
| 183 | beaver: the flooded meadow below | C6 | K4 | 12 | keep |
| 184 | bees: bee-lining as two-point triangulation | C3, C11 | K5 | 7 | keep |
| 185 | bees: marking a bee tree | C13 | K5 | 7 | recast: a mark |
| 186 | bees: brimstoning against driving | C3 | K6 | 7 | keep |
| 187 | bees: telling the bees | | | | cut as engine content (§3.9 no. 23) |
| 188 | falcon: goshawk and sparrowhawk for the lowland; peregrine on cliffs | C8 | K5 | 8 | keep |
| 189 | falcon: the bond | C8 | K6 | 8 | keep |
| 190 | falcon: hawk theft a grave crime; serjeanty; hawk ranks | | | | cut (§3.9 nos. 10, 22) |
| 191 | swan: marks; the upping; unmarked to the lord | C13 | K6 | 14 | recast: marks as tags; upping cut (§3.9 no. 21) |
| 192 | loads: keep those with a sowing or picking lever | C3 | K1 | 9 | keep |
| 193 | markers: keep only those with a lever this stretch | | K1 | 12 | recast: none withheld (attention filtering cut); markers tied to sowing rules |
| 194 | murrain and swine fever: quarantine and burning as choices | C10 | K2 | 15 | keep |
| 195 | M1 shared perception | C4 | core | | core |
| 196 | M2 the stretch contest | C2, C4 | K1 | 8 | recast: one night's act (dup 132) |
| 197 | M3 displacement and refill | C6 | core | | core |
| 198 | M4 the route graph | C5 | core | | core |
| 199 | M5 personality and selective harvest | C5 | K3 | 21 | keep |
| 200 | M6 culture in animals | C5 | K3 | 22 | keep |
| 201 | M7 sentinels and alarm networks | C5 | K3 | 9 | keep |
| 202 | M8 animals that remember people | C5, C13 | K3 | 10 | keep |
| 203 | M9 commensal niches by waste and buildings | C10 | K2 | 17 | keep |
| 204 | M10 provisioning and cultivated allies | C7 | K1 | 13 | recast: habitat fittings (owl hole, dovecote) |
| 205 | M11 deception and signalling | C3 | K3 | 23 | keep |
| 206 | M12 long projects and wild capital | C7 | core | | core |
| 207 | M13 obligations denominated in wild things | | | | cut (§3.9 nos. 6, 7, 10) |
| 208 | M14 laws that constrain levers | C14 | W | 1 | option |
| 209 | M15 places that remember; quirks | C11, C14 | K3 | 19 | keep |
| 210 | M16 contested attribution | C3 | K1 | 2 | keep |
| 211 | M17 races for a ripening pulse | C6 | K3 | 12 | keep |
| 212 | M18 the carcass as an object with stakeholders | C10 | K2 | 11 | keep |
| 213 | the attention budget; suppressing signs with no lever | | | | cut (§3.9 no. 1) |
| 214 | learning problems P1 to P24 | C15 | X | | keep as coding categories |
| 215 | society-level tests against a null arm | C15 | X | | keep |
| 216 | invented or masked kinds; quirks arms | C14 | W | 7 | option |

### 3.5 02zr §6: the 39 new kinds

| # | Item | Needs | Pack | Rank | Status |
|---|---|---|---|---|---|
| 217 | 1 the cat | C5 | K1 | 7 | dup 168 |
| 218 | 2 red kite and the midden | C10 | K2 | 5 | keep |
| 219 | 3 carrion crow and magpie | C5, C13 | K3 | 10 | keep |
| 220 | 4 house sparrow and the threshing floor | C5, C6 | K1 | 1 | keep (with birds at the corn) |
| 221 | 5 jackdaw in the chimney | C1 | K11 | 1 | defer (chimneys) |
| 222 | 6 deathwatch beetle, woodworm, dry rot | C7 | K11 | 2 | defer |
| 223 | 7 store insects (weevil, moth, mites) | C1, C7 | K2 | 10 | keep |
| 224 | 8 rabbit and the warren | C8 | K6 | 4 | defer (husbandry); rent and free warren cut or option (§3.9 no. 14) |
| 225 | 9 mole and the mole-catcher | C3, C7 | K1 | 11 | keep; pooled payment cut (§3.9 no. 15) |
| 226 | 10 grey partridge and quail | C3, C8 | K3 | 15 | keep (setting dog in K6) |
| 227 | 11 corncrake | | K7 | | deferred to K7 (37.2 review; was §3.9 no. 24) |
| 228 | 12 lapwing and the egg harvest | C3 | K3 | 13 | keep; the custom recast to relaying physics |
| 229 | 13 adder | illness | K10 | 3 | defer |
| 230 | 14 warble and horse-flies (gadding) | C1 | K1 | 15 | keep |
| 231 | 15 grub years (cockchafer, crane fly, wireworm) | C1 | K1 | 10 | keep |
| 232 | 16 poisonous lookalikes (hemlock, water dropwort, ragwort, yew) | C3 | K3 | 11 | keep; ragwort "duty" recast to work |
| 233 | 17 bracken, gorse, blackthorn | C1 | K5 | 13 | keep; rights of cutting cut (§3.9 no. 16) |
| 234 | 18 jay (sentinel and planter) | C5 | K3 | 9 | keep (planting in K5 rank 12) |
| 235 | 19 red squirrel and the nutting race | C6 | K3 | 12 | keep; nutting day cut (§3.9 no. 5) |
| 236 | 20 badger | C5 | K5 | 9 | keep |
| 237 | 21 woodcock and the cockshoot | C3, C11 | K3 | 14 | keep; the claim cut (§3.9 no. 17) |
| 238 | 22 stoat, weasel, polecat, marten | C1 | K1 | 6 | keep |
| 239 | 23 oak caterpillar years | | K5 | 11 | keep |
| 240 | 24 the veteran tree | C7 | K5 | 10 | keep |
| 241 | 25 deer park, fallow deer, the leap | C7, C8 | K5 | 14 | keep; the licence to empark to option W.3 |
| 242 | 26 the fishpond | C8 | K6 | 6 | defer |
| 243 | 27 freshwater pearl mussel | C6 | K4 | 14 | dup 180 |
| 244 | 28 medicinal leech | healing | K10 | 8 | defer |
| 245 | 29 lamprey | C7 | K4 | 5 | keep; the render cut (§3.9 no. 7) |
| 246 | 30 crayfish and the retting | C6, flax | K4 | 11 | keep; the by-law cut |
| 247 | 31 crane and bittern | | K4 | 13 | keep; the statute cut (§3.9 no. 18) |
| 248 | 32 duck decoy | C7, C8 | K4 | 8 | dup 173 |
| 249 | 33 seabird cliffs (cragsman and rope) | C3 | K9 | 1 | keep; ledges as rights cut (§3.9 no. 19) |
| 250 | 34 seals and the stranded whale | C10 | K9 | 2 | keep; the Crown's claim to option W.4 |
| 251 | 35 rabies | illness | K10 | 1 | dup 40 |
| 252 | 36 the black bane field | C10, C11 | K2 | 12 | keep |
| 253 | 37 fen ague | illness | K10 | 2 | defer |
| 254 | 38 starling roost | C6 | K5 | 19 | keep |
| 255 | 39 markers with sowing rules | | K1 | 12 | keep |

### 3.6 02zs: goods, chains, ladders, tools, scale

| # | Item | Needs | Pack | Rank | Status |
|---|---|---|---|---|---|
| 256 | fat, lard; tallow by rendering | C9 | K2 | 6 | keep |
| 257 | hide to leather (tanning with bark and lime, months) | C9 | K8 | 1 | defer |
| 258 | hide to parchment; wax to seals; quills (documents) | C9, documents built | K8 | 2 | defer |
| 259 | fur and pelt with quality | C7, C9 | K8 | 5 | defer (clothing parked, D2-10) |
| 260 | feathers and down | C9 | K8 | 6 | defer |
| 261 | eggs (seabirds, lapwings, fowl) | C3 | K3 | 13 | dup 228 |
| 262 | honey and wax | C8, C9 | K8 | 9 | defer |
| 263 | horn (panes, handles) and antler | C9 | K8 | 4 | defer (horn lantern in K2 rank 6) |
| 264 | bone (tools, glue, bone meal) | C9 | K8 | 4 | defer |
| 265 | sinew and gut (cord, bowstrings) | C9 | K8 | 3 | defer |
| 266 | glue from hides and bone | C9 | K8 | 3 | dup 265 |
| 267 | oil (seals, fish, the whale) | C9 | K8 | 8 | defer |
| 268 | castoreum | | K8 | 7 | keep (built item; use waits on illness) |
| 269 | dung for fields; pigeon dung | C8 | K8 | 12 | defer |
| 270 | wool | C8 | K6 | 13 | defer (sheep, clothing) |
| 271 | labour and service of beasts (guarding, hunting, ratting, herding, carrying) | C8 | K6 | 1 | defer |
| 272 | information from sentinels and ravens | C5, C10 | K3 | 9 | dup 201 |
| 273 | light as a real need (the watch) | C9 | K2 | 6 | dup 256 |
| 274 | status goods (never forced) | | | | cut as engine content (§3.9 no. 9) |
| 275 | the chains: leather, parchment and seals, light, cord and nets, the bow, bone and horn crafts, fertility, preserved meat and fish, pannage, kept fish | C9 | K2, K3, K6, K8 | as each | keep |
| 276 | the animal ladder (take, tend, keep, breed, intensify) and bridges | C8 | K6 | as each | keep (framework) |
| 277 | the land ladder (forage, manage, enclose, convert) | C12 | K7 | 9 | keep |
| 278 | the defence ladder (presence, barriers, structures, removal, landscape) | C7, C12 | K1, K7 | as each | keep |
| 279 | the processing ladder | C9 | K2, K8 | as each | keep |
| 280 | the knowledge ladder; the reach ladder | C11 | K3 | as each | keep |
| 281 | tools: cord (bast, sinew, hemp) | C9 | K3 | 5 | keep |
| 282 | tools: snares | C7 | K1 | 3 | keep |
| 283 | tools: traps (deadfall, box, basket, mole trap; iron jaws later) | C7 | K1 | 3 | keep (iron jaws defer) |
| 284 | tools: nets (purse, clap, flight, casting, seine) | C7, C9 | K3 | 6 | keep |
| 285 | tools: club, sling, boar spear, bow and arrows | C1, C9 | K3 | 7 | keep |
| 286 | tools: crossbow | smith, iron | K8 | 10 | defer |
| 287 | tools: firearms | | | | cut from these packs (§3.9 no. 28) |
| 288 | tools: dogs by type (mastiff, herding, scent hound, sighthound, spaniel and setter, terrier, decoy dog) | C8 | K6 | 1 | defer |
| 289 | tools: ferrets | C8 | K6 | 4 | defer |
| 290 | tools: hawks | C8 | K6 | 8 | defer |
| 291 | tools: lures, decoys, calls, bait, bird lime | C3 | K3 | 23 | dup 205 |
| 292 | tools: water structures (weir, traps, garth, pond, punts) | C7 | K4 | 2 to 7 | keep |
| 293 | tools: barriers with properties | C1, C12 | K7 | 1 | keep |
| 294 | tools: stores with properties | C1 | K1 | 4 | keep |
| 295 | tools: fire and light | C9 | K2 | 6 | dup 256 |
| 296 | tools: preservation (dry, salt, smoke, pot in fat) | C9 | K2 | 7 | keep |
| 297 | tools: poisons | | K10 | | deferred to K10 (37.2 review; was §3.9 no. 27) |
| 298 | scale responses (§5.1: household, materials, village, landscape for each problem) | C7, C12 | K1, K7 | as each | keep |
| 299 | what scale unlocks (§5.2): buildings, trades, chains; institutions only as possibilities | C7 | K7 | as each | recast: institutions removed as content |
| 300 | development trade-offs (§5.4) | C6 | K7 | 9 | keep (as consequences, measured) |
| 301 | forays and the ladders (§10) | C11 | K3 | 1 | dup 51 |
| 302 | the butcher step | C9 | K2 | 1 | keep |
| 303 | salt with no source (D2-56) | economy | K2 | 8 | keep (a dependency: needs a salt source built) |

### 3.7 02zt: improvements, prediction aids, infrastructure

| # | Item | Needs | Pack | Rank | Status |
|---|---|---|---|---|---|
| 304 | knives and the butcher's kit | C9 | K2 | 1 | keep |
| 305 | noise makers (clappers, horn, bell) as held gear | C2 | K1 | 16 | keep |
| 306 | climbing rope and harness | C9 | K9 | 1 | keep |
| 307 | punt and coracle | C7 | K4 | 7 | keep |
| 308 | gap-tight coops and pens | C1, C7 | K1 | 6 | keep |
| 309 | raised granary on staddles; stone floors; sealed bins | C1, C7 | K7 | 2 | keep (the property in K1 rank 4; the stone build here) |
| 310 | the smokehouse | C7, C9 | K2 | 7 | keep |
| 311 | salt pans and boiling at a spring | economy | K9 | 4 | keep (with 303) |
| 312 | barrels (the cooper) | C9 | K2 | 9 | keep |
| 313 | the tannery | C9 | K8 | 1 | dup 257 |
| 314 | the rendering pot and chandlery | C9 | K2 | 6 | dup 256 |
| 315 | the kennel | C8 | K6 | 1 | defer |
| 316 | the mews | C8 | K6 | 8 | defer |
| 317 | hutches for ferrets | C8 | K6 | 4 | defer |
| 318 | the warren | C8 | K6 | 4 | dup 224 |
| 319 | the dovecote | C8 | K6 | 5 | defer |
| 320 | the apiary (skeps, bee boles) | C8 | K6 | 7 | defer |
| 321 | the deer park (pale and leap) | C7 | K5 | 14 | dup 241 |
| 322 | the weir with traps and a gap | C7 | K4 | 3 | dup 178 |
| 323 | breeds: scent hounds, sighthounds, mastiffs, terriers, herding dogs, setting dogs, decoy dog | C8 | K6 | 1 | dup 288 |
| 324 | oxen and ponies to carry bulk takes | built | K6 | 15 | keep |
| 325 | techniques: stalking into the wind; the drive; working a line; netting a flight line; bee-lining; driving bees; curing; tanning; taming; coppice rotation and hedge-laying | C3 | K3, K5, K6, K7 | as each | keep (as methods) |
| 326 | a tally at the weir; a year-book; counts; a calendar of markers | documents | K3 | 24 | keep as documents people may write |
| 327 | a map or list of spots; marked trees and stones | C13, documents | K3 | 24 | keep as documents and marks; never an engine table |
| 328 | teaching and written methods | built | K3 | 24 | keep |
| 329 | a lookout; a high seat or hide; rides; a cart track into the wood; a boat landing or a ford made good | C12 | K7 | 3 to 7 | keep |
| 330 | a crew's organisation of work | | | | not content: the agents' own (agreements are built) |
| 331 | interlocks with transport (bulk takes carried; far grounds; light dear goods) | built transport, L-53 | K4, K8 | as each | keep (consequences) |
| 332 | hubs and loops (the coppice, smith, rope-maker, salter, cooper, tanner, butcher, kennel, smokehouse, boatwright) | C7, C9 | K2, K3, K8 | as each | keep (emerge from chains) |
| 333 | development trade-offs table (§5) | C6 | K7 | 9 | dup 300 |

### 3.8 02zu: chains, converters, actions, decay

| # | Item | Needs | Pack | Rank | Status |
|---|---|---|---|---|---|
| 334 | the whole-economy map and shared hubs (Part A) | | X | | keep as the design map |
| 335 | converters: works unattended, multipliers, removing a recurring need (Part B) | C7 | core | | core |
| 336 | the action survey, one-offs and consolidated design (Part C) | C1, C2, C3 | core | | core |
| 337 | decay stages by size class (recalibrated to Zach's frame) | C10 | K2 | 2 | keep |
| 338 | scavenger succession: flies, wasps, beetles; corvids, kites, buzzards, ravens; foxes, badgers, boar, dogs, rats, martens; wolves; the bear's cache; bone-chewers | C10, C1 | K2 | 3 | keep |
| 339 | handling: hang, bury at a depth (diggers), burn (fuel), feed to dogs or pigs, the midden, salt and smoke, carry or leave | C10, C9 | K2 | 4 | keep |
| 340 | disease moved with a carcass | C10 | K2 | 15 | keep |
| 341 | bones; deer and sheep chewing bones and shed antler | C10 | K2 | 14 | keep (check the natural history) |
| 342 | evidence: a poached deer's leavings; a body found by the crows | C10, C13 | K2 | 11 | dup 212 |
| 343 | windfalls: a wolf's kill found | C10 | K2 | 11 | dup 212 |
| 344 | the "unit is about two real days" reading | | | | cut (§3.9 no. 29) |
| 345 | burial depth as a property of the burial (units against the ground); shallow or hasty graves dug by foxes, badgers, dogs (Zach, 10 Nov) | C10 | K2 | 4 | keep |
| 346 | spillover: a scavenger or predator fed at a carcass returns and raids what is near (hens, the fold, a calf; a person at a cache); the carcass, wolf, kill loop (Zach, 10 Nov) | C10, C5 | K2 | 4 | keep (falls out of the rules) |

### 3.9 Proposed cuts (for Zach to review)

| No. | Item (ledger row) | Reason | Substrate kept, if any |
|---|---|---|---|
| 1 | attention budget, caps, suppressing signs without a lever (213) | Zach: never filter perception; fix the world's rates | lines per agent-day as a diagnostic (C15) |
| 2 | P12, the watch-schedule learner (65) | not learnable at a few samples a year; replaced by the spatial adversary | the spatial adversary |
| 3 | the bounty as an office (83, 149) | an institution | heads as evidence (150) |
| 4 | close times; a water bailiff (179) | an institution | the weir's gap as a physical state (178) |
| 5 | the nutting day (235) | a custom | the race for the pulse (211) |
| 6 | eel rents in sticks (176, 207) | an obligation seeded by the engine | agreements people make in goods (built) |
| 7 | the lamprey render (245, 207) | as 6 | as 6 |
| 8 | venison raising standing (143) | a social effect | giving (built) |
| 9 | status goods as engine content; seeded customs (274) | social | scarce, durable, visible goods |
| 10 | serjeanty (190, 207) | an institution | |
| 11 | the hunt's assembly (141) | an institution | the harbourer's knowledge told or sold |
| 12 | roe as the commoner's deer by a ruling (145) | law | world option W.2 |
| 13 | a parish bounty on sparrows (220) | an institution | |
| 14 | the warrener's rent; free warren (224) | an institution | the warren as a held structure; W.2 for rights |
| 15 | a pooled payment for the mole-catcher (225) | an institution | the catcher's skill and gear |
| 16 | rights of cutting bracken (233) | an institution | the cutting as work |
| 17 | claiming the cockshoot (237) | an institution | possession of a place by use (D4-23) |
| 18 | the statute protecting cranes' eggs (247) | law | |
| 19 | ledges as rights on cliffs (249) | an institution | |
| 20 | the heronry's holder forbidding takes; site customs (182, 55) | an institution | possession only |
| 21 | swan upping and the swan master (191) | an institution | marks as tags (C13) |
| 22 | hawk theft "a grave crime"; hawk ranks (190) | social | theft is taking (built) |
| 23 | "telling the bees" as engine content (187) | a custom | may be a seeded lore line in a world |
| ~~24~~ | ~~the corncrake as a kind (227)~~ | **not cut (37.2 review):** deferred to K7, low rank, for when hay work has a mowing pattern | |
| 25 | trout as a separate kind (116) | adds nothing to the water pack's fish stock | the fish stock and tickling as a method |
| ~~26~~ | ~~plague (172)~~ | **not cut (37.2 review):** deferred to K10 as a rare regime once illness in people exists; whether to build it at all is Zach's call then | |
| ~~27~~ | ~~poisons (170, 297)~~ | **not cut (37.2 review):** deferred to K10, as the reason itself says | |
| 28 | firearms (287) | an era change | economy_later.md's era list |
| 29 | the "unit is about two real days" reading (344) | Zach: units are parts of a day | |
| 30 | the search game as steps of a stalk across acts; "spots as engine knowledge items" (51, 142) | replaced by forays and memory | forays (C11) |
| 31 | the stretch semantics "share of the stretch watched" (132, 196) | the watch is one night's act | the per-night contest |

**Counts:** 346 ledger rows; 28 proposed cuts (31 less three moved to deferred by 37.2's review: corncrake, plague, poisons); 38 rows marked recast; 32 duplicates of earlier rows; 54 deferred; the rest keep.

## 4. The packs

Ordered by value for cost, as 02zr §6.8 ranked kinds: presence across generated worlds, the brief's purposes served (dependence,
problems no one solves alone, information, commons), a fast arm inside a run, novelty of the lesson, build cost, and what it waits
on. Ranks inside each pack are the ledger's. Every pack is tested against a **null arm** (the same worlds and seeds with the pack
off, D4-104), with several seeds and a strong cast (scenario_design §2), and read with a qualitative end state. Sizes are rough
(S, M, L as §2).

**First** (built and tested right after the core): K0, K1, K2, K3, K4. **Later:** K5 to K11. **Placeholder:** K12. **Options:** W.

### K0. The built kinds on the core (first; conversion, no new content)
- **Contents:** ledger rows 1 to 31 and their duplicates: kind-named techniques to methods; watches to `guard` with gear; shutting to
  `set`; crop work against loads; range as a take's reach; readings and skill by method family (three levels); traits replacing take
  tables; NEAR_PEOPLE as module data; the built signs, conditions, pressure, wounds, litters, followers, migrants, plants, mast,
  loads, markers, diseases, sites, leaders, legends, regimes, vole clock, history; hens and the dog kept as they are until K6; data
  hygiene; boar calibrated to 3 to 10% of need.
- **Core:** C1, C2, C3, C15. **Other dependencies:** none.
- **Tests:** dry: guard tests (no kind named in verbs, techniques, targets or barriers; calibration rows counted); the branch's wave-1
  outcomes reproduced within tolerance on the same seeds; refusal audit; system text size with the wild pack on below run 6's.
  Live: one short run against run 6's world to show agents use the methods (method diversity, refusals).
- **Size:** M (mostly deletion and data). **Why first:** every pack builds on it; it removes the bespoke parts.

### K1. Every village: fields, stores and hens (first)
- **Contents (by rank):** 1 birds at the corn as social followers with displacement (woodpigeon, rook, sparrow; 98, 159, 160, 220);
  2 attribution signs naming kind and deterrent (210); 3 traps and snares as goods and standing works, robbable (95, 282, 283);
  4 stores with properties against rats, mice and damp (58, 107, 294); 5 the fox as a lapse prober with the hamlet externality,
  the treadmill and den work (85, 87, 153, 154); 6 stoats, weasels and polecats by gap size, gap-tight coops (238, 308); 7 the cat
  (168); 8 boar and deer at the field: the per-night contest, the spatial adversary, displacement (wooded villages; 52, 65, 132,
  133, 140); 9 loads worked against (192); 10 rooks' trade-off both ways and the grub years (100, 162, 163, 231); 11 the mole and
  trapping (225); 12 markers with sowing rules (63, 193, 255); 13 the owl hole and barn owl (105, 166, 204); 14 mowing drives voles
  to the ricks (45, 167); 15 the gadding herd (230); 16 noise makers and light as held deterrents (305); 17 the rat-catcher as skill
  and gear (169); 18 the mast and vole cascades reaching fields and hens (46, 86, 131).
- **Core:** C1 to C7, C13. **Other dependencies:** hens stay store goods until K6; terriers wait on K6.
- **Tests:** dry: displacement (the unscared neighbour loses more); one lax household raises its neighbours' hen losses; a cull
  refills from the ring; raised stores cut rat losses and a door does not; traps beat foraging only as a line. Live: against the null
  arm, read watch and scaring arrangements, shared hedging, traps set and robbed, disputes over damage, method diversity; losses as a
  share of need.
- **Size:** M. **Why first:** present in every generated village; the strongest externalities; fast arms every run.

### K2. The carcass, the store and decay (first)
- **Contents (by rank):** 1 the butcher step and kit (302, 304); 2 decay stages by size class on the act clock (337); 3 scavengers
  by traits (338); 4 handling: hang, bury at a depth, burn, feed to dogs or pigs, carry or leave; grave depth; spillover predation
  (339, 345, 346); 5 the midden and kites (218); 6 fat to tallow; rushlights, candles, a horn lantern; light for the watch (256, 273,
  295, 314); 7 the smokehouse, salting, drying at scale (296, 310); 8 a salt source (303; D2-56); 9 barrels (312); 10 store insects
  (223); 11 the carcass as evidence and windfall (212, 342, 343); 12 the black bane field (252); 13 the bear's cache (156); 14 bones
  (341); 15 disease moved with a carcass; quarantine and burning as choices (194, 340); 16 ravens over carrion and following wolves
  (84, 102, 165); 17 commensal niches by waste (203).
- **Core:** C1, C4, C5, C7, C9, C10, C13. **Other dependencies:** a salt source (D2-56, not built); illness in people only for
  human effects of rot (not needed for the rest).
- **Tests:** dry: a deer stripped in about two nights with scavengers near; a frozen carcass keeps; graves by depth; a carcass near
  the fold raises the fold's losses against one burned or buried; the midden's place moves rats and kites. Live: butchering, burying
  and burning choices; light made and used; preserved stores; scavengers near houses; evidence found and used.
- **Size:** M. **Why first:** every village slaughters and every death leaves a body; it adds light (a real need) and preservation
  (bulk takes worth having).

### K3. Forays, methods and knowing (first)
- **Contents (by rank):** 1 forays (51, 142, 301); 2 places in memory and names; 3 land features; 4 the methods catalogue (take
  family); 5 cord and the coppice's products (withies, poles, bark, bast) (281); 6 nets (284); 7 bow, arrows, boar spear (285);
  8 stalking into the wind; 9 jays, roe bark and other sentinels (60, 146, 201, 234, 272); 10 crows and magpies that remember
  people (202, 219); 11 poisonous lookalikes (232); 12 the nutting race and the squirrel (211, 235); 13 lapwing eggs and the
  display (228, 261); 14 woodcock flight lines (237); 15 partridge and quail with nets (226); 16 hares' forms, runs, refill (94, 96,
  157); 17 roe patches, the call, the kid at mowing (77 to 79); 18 red deer stalk, slots and lies by wind (71); 19 quirks and places
  that remember; seeded folklore lines (158, 164, 209); 20 legends emergent (24, 62); 21 personality and selective harvest (199);
  22 culture in animals (200); 23 decoys, calls, lures (99, 205, 291); 24 records people write: tallies, counts, year-books, maps,
  marked trees; teaching (144, 326 to 328); 25 gathering wild plants on forays; 26 gathering young and eggs at colonies (101, 119);
  27 drives with crews (83); 28 the harbourer's knowledge; gifts (141, 143); 29 lore as tested belief (43, 44; waits on 37.4's
  belief store); 30 traces that age; heads and evidence read by skill (49, 150).
- **Core:** C1 to C5, C11, C13. **Other dependencies:** the foray interpreter's model call (forays.md); 37.4's belief store for
  rank 29; dogs for setting and coursing wait on K6.
- **Tests:** dry: forays.md §7; skill carries across a method's targets; an upwind approach is noticed; a jay's alarm lowers deer
  found. Live: places named and revisited; spots told or kept; method diversity; cord, nets and bows made and traded; teaching of
  methods; against the null arm, specialists by method and trade in wild goods.
- **Size:** L. **Why first:** it carries the take and know ladders and makes local, particular knowledge (the learning a model
  cannot recall) the person's own.

### K4. River and fen (first, in worlds with water)
- **Contents (by rank):** 1 the eel run with the catchment's lag (54, 111, 175); 2 traps in water as standing works, robbable (177);
  3 the weir as a structure with a gap and a downstream take (112, 178, 322); 4 salmon on the same module (114, 115); 5 the lamprey
  (245); 6 wildfowl pushed by cold, flight lines, nets, weakness, return by survivors (108 to 110); 7 punts and coracles (307);
  8 the decoy pond and its quiet zone (173, 248); 9 the heronry and the reading of its size (120); 10 the otter at weir and pond
  (117); 11 crayfish and retting downstream (246); 12 the beaver's dam and the meadow below (56, 121, 122, 183); 13 crane, bittern
  and drainage (247); 14 the pearl mussel (180, 243); 15 eel spearing in winter (113); 16 the water pack's fish and tickling (116).
- **Core:** C1, C3, C6, C7, C9, C11. **Other dependencies:** smoking and salt from K2; flax for retting; a trained dog (K6) for the
  decoy; boats stage A (water_and_preservation.md).
- **Tests:** dry: the run reaches each weir on its lag day; an upstream weir's shut gap lowers the downstream catch; a local who has
  seen two runs beats a newcomer who knows only the rule. Live: crews on run nights, weirs built and kept, preserved catches,
  upstream and downstream disputes against the null arm.
- **Size:** M. **Why first:** eels mattered in 13 of 20 villages (02zp §27); the strongest commons between villages.

### K5. Wood and frontier (later)
- **Contents (by rank):** 1 the sounder: route graph, the matriarch and splitting, the wallow, later at night under pressure, rooting
  (66, 69, 134, 136, 137); 2 the mast's two years and the race with pannage pigs (67, 135); 3 the boar hunt and the bear hunt with
  crews (68, 92); 4 red deer: the herd's make-up, browse on coppice, winter at the ricks (72, 74, 75); 5 the wolf: circuit,
  switching, dispersers, the persecuted pack, the dangerous yearling (47, 53, 80 to 82, 148, 152); 6 the bear's year and hungry
  spring (89 to 91, 93); 7 wild bees, bee trees marked, bee-lining, raids (123, 124, 126, 184, 185); 8 hawks' eyries and eyasses
  (188); 9 the badger (236); 10 the veteran tree (240); 11 oak caterpillar years (239); 12 the jay planting oaks (234); 13 bracken,
  gorse, blackthorn (233); 14 the deer park and the leap (241, 321); 15 the pine marten (127); 16 roe browse on coppice (147);
  17 clearing's trade-offs; 18 wasps (39); 19 the starling roost (254).
- **Core:** C1 to C7, C11, C12. **Other dependencies:** pigs and pannage (K6) for rank 2; bees kept (K6) for skeps.
- **Tests:** dry: the matriarch's death splits the sounder; deer hunted out raise wolves' kills of stock within a season; a bare
  autumn makes a hungry spring. Live: crews, drives across villages, hedging and parks, against the null arm.
- **Size:** L. **Why later:** boar and deer are present in few generated villages (3 of 20); high value where present.

### K6. Keeping: bridges and husbandry (later; waits on 37.4)
- **Contents (by rank):** 1 dogs as kept beasts with types, training bonds and the kennel; hounds, sighthounds, terriers, mastiffs,
  setters, the decoy dog (29, 97, 271, 288, 315, 323); 2 hens, ducks and geese as kept beasts; coops; geese as watchers (28, 37,
  155); 3 pigs on pannage (33); 4 the warren, ferrets and purse nets; feral rabbits (224, 289, 317, 318); 5 the dovecote and its
  dung (319); 6 the fishpond (242); 7 the apiary, skeps, bee boles, driving bees (38, 125, 186, 320); 8 hawks in the mews, falconry,
  the bond; heron-hawking (128, 181, 189, 290, 316); 9 tame decoy ducks; 10 breeding traits; 11 tamed young (61, 70, 76); 12 feral
  transitions and mixing (64); 13 sheep, folds and lambs (34, 35, 151, 270); 14 swans pinioned and marked (129, 191); 15 oxen and
  ponies carrying bulk takes (324); 16 swine fever in kept pigs (36).
- **Core:** C7, C8, C9. **Other dependencies:** 37.4's herds generalised into beasts (husbandry.md §7c, a board item); L-36
  (sheep, pigs, poultry, horses).
- **Tests:** dry: cattle unchanged; a lent hound works at half; a broken warren bank leaks rabbits. Live: kept populations started,
  specialists bound to beasts (the falconer, the warrener, the kennel-keeper), trade in pups and kits, against the null arm.
- **Size:** L.

### K7. Land works and infrastructure (later)
- **Contents (by rank):** 1 barriers with properties on parcel edges: hedges, banks, walls, pales, mesh; fences on borders (L-24)
  (293); 2 raised stone granaries and stone floors (309); 3 rides; 4 high seats and hides; 5 lookouts; 6 cart tracks into woods;
  7 landings and fords made good (329); 8 coppice rotation and hedge-laying as management (325); 9 draining and clearing at scale, and
  development's trade-offs (277, 300, 333); 10 visibility from position; what scale unlocks (298, 299); 11 the corncrake and the
  mowing pattern (227; low rank, when hay work has a pattern).
- **Core:** C7, C12. **Other dependencies:** L-24 (fences on borders).
- **Tests:** dry: a high seat's watcher notices a sounder next door; a handcart reaches the wood by its track. Live: works built,
  their upkeep, who builds and who uses them, against the null arm.
- **Size:** M.

### K8. Crafts and wild goods (later)
- **Contents (by rank):** 1 tanning and leather (257, 313); 2 parchment, wax seals, quills (258); 3 sinew, gut, glue, bowstrings;
  bowyer and fletcher (265, 266); 4 horn and bone crafts; antler (263, 264); 5 furs and pelts with quality; the winter pelt (88,
  259); 6 feathers and down (174, 260); 7 castoreum (268); 8 oil (267); 9 honey and wax as goods (262); 10 the crossbow (286);
  11 (firearms: cut); 12 dung and bone meal for fields (269).
- **Core:** C7, C9. **Other dependencies:** documents built (D2-24, decided); clothing parked (D2-10) for furs and wool; bees (K6).
- **Tests:** dry: chains complete and their intermediate goods trade; tanning takes its days. Live: specialists (tanner, chandler,
  fletcher) and trade between villages that differ by land, against the null arm.
- **Size:** M.

### K9. Coast and cliff (later, coastal worlds)
- **Contents:** 1 seabird cliffs, the climber and the rope-holder, climbing rope (249, 306); 2 seals and the stranded whale
  (250); 3 (the Crown's claim to W.4); 4 shore salt pans (311); 5 shellfish on the foreshore (water_and_preservation.md).
- **Core:** C3, C7, C10. **Other dependencies:** coastal worlds; the tide (water_and_preservation.md §6).
- **Tests:** dry: the climb's danger by the holder's skill. Live: pairs formed, the whale divided, against the null arm.
- **Size:** S.

### K10. Illness and the hidden (later; waits on illness in people)
- **Contents:** 1 rabies (40, 251); 2 the fen ague (253); 3 the adder (229); 4 murrain meat and milk (32, 42); 5 ergot (41);
  6 liver fluke; 7 flies carrying disease; 8 leeches and remedies (244, 268); 9 disease travelling between villages (wave 4); 10 poisons for rats, with their risk to dogs,
  cats and people (170, 297); 11 plague as a rare regime (172; whether to build it is Zach's call).
- **Core:** C10. **Other dependencies:** illness in people (OPEN Q-16, L-9).
- **Size:** M.

### K11. Lodgers of buildings (later)
- **Contents:** 1 jackdaws in chimneys (221); 2 deathwatch beetle, woodworm, dry rot (222); 3 black rats in thatch (171).
- **Core:** C1, C7. **Other dependencies:** chimneys in the building catalogue; building wear (built).
- **Size:** S.

### K12. Discovery and crafting new things (placeholder; OPEN L-103)
- **Not designed here.** Content that would depend on it: inventing a new method (a new trap or net design, a decoy pipe), new
  recipes from wild goods, new breeds named by people beyond traits drifting (C8), new crops from beyond the frontier, improving a
  structure's design. Until then, methods and recipes come from the world's catalogue (knowledge.md §6: no blind crafting).

### W. World options (experimental arms, off by default)
- **Contents:** W.1 the forest-law arm (the lord's deer and boar; lawed dogs; fence height; the fence month) (139, 208); W.2 rights in
  wild kinds (D2-194), including roe as a lesser beast and free warren (72, 145, 224); W.3 a licence to empark (241); W.4 claims on
  whales and swans; W.5 seeded structures from history; W.6 method-seeding arms (which households know which methods); W.7 invented
  or masked kinds and quirks for learning tests (216).
- **Core:** C14. **Tests:** every access gate verified in a dry run (scenario_design §4).

### X. Design and analysis items (not packs)
The whole-economy map (334), the learning problems as coding categories (214), society-level tests (215), and the diagnostics (C15).

## 5. What changes in the existing files (for Zach and 37.2 to act on)

1. **`proposals/wild_behaviour.md` (v2):** facets become views over constitution modules (02zr §1.3); F1's search game is replaced by
   forays; F2's P12 learner is cut (spatial adversary instead); F5's claims, customs and holders move to world options; F12 becomes
   emergent; per-kind take lists give way to traits and properties (C1); red deer keep a modest raid by default, with forest law only
   in W.1; the wolf's bounty is cut; swan marking is recast to tags; §7's build list follows §2.1's order here; a History entry.
2. **`proposals/forays.md`:** add that takes along a route resolve by C1's encounter rule with the gear carried; that forays are the
   only place free-word targets are read; that land features are shared with animals' modules (as it says); and that scavenging and
   carcasses left on a foray follow C10 (the carcass "hanging in the brake").
3. **02zq:** its "not built" list is mapped in §3.2 here; its one-off pieces 6 to 10 go into K0.
4. **The ecology branch's code (37.4's, by agreement on the board):** remove the wild yield kinds (`wild_take`'s per-technique
   `takes`, `wild_site`, `wild_shut`, `wild_guard`, `wild_watch`) and the kind-named techniques in favour of methods (C1 to C3);
   seed wild methods by upbringing and land, not to everyone; drop tool multipliers from the manual; stop refusals listing every
   technique of a verb; generalise `reads_as` and `SKILL_CARRY`; the field watch becomes `guard`; `shut` becomes `set`.
5. **02zr, 02zs, 02zt, 02zu:** each gets one line at its top pointing here (the CLAUDE.md rule for superseded session notes); 02zu Part
   D's timings are replaced by Zach's frame (§0 answer 1); 02zu C.8 is corrected (the menu is already gone, D4-78; the change is the
   manual's content); "a unit is about two real days" is withdrawn in all four.
6. **`spec/world/things_in_places.md` and `proposals/carcasses.md`, `graves.md`:** when K2 is decided, D2-95's "scavengers later"
   becomes C10, and burial depth becomes a property of the burial.
7. **`docs/cybertron2/OPEN.md`:** wind direction in the climate (C4) as an engine gap under 37.4; the D2-194 reading (decision 3
   below) under 37.2.

## 6. Decisions needed from Zach

1. The core list and its build order (§2.1), with C1, C2, C3 and C15 built and tested on the built kinds (K0) before any content.
2. The first packs (K0 to K4) and their order; K5 to K11 later.
3. D2-194 and the forest-law material as world options only (W.1, W.2); confirm D2-194 reads "a world may give".
4. The proposed cuts (§3.9), item by item.
5. Determinate targets on `looking for`, with free words only in forays (§2, C2).
6. Methods seeded by upbringing and land, and the manual without multipliers or kind lists (C2).
7. The decay frame as given, with burial depth and spillover as stated (C10).
8. Which husbandry pieces (dogs first) 37.4 takes on for K6, and when.
9. Whether K4 counts as first in worlds without water (proposed: first only where rivers or fen exist).

## Sources

The four session notes this consolidates and their sources: `docs/review/37_growth/02zr_wild_behaviour_critique.md`,
`02zs_wild_development.md`, `02zt_wild_dependences.md`, `02zu_wild_chains_capital_actions.md`; `02zr_wild_purpose_brief.md`;
`02zq_wild_audit.md`; `02zp_ecosystems_deep_dive.md` §23 to §31; `docs/cybertron2/proposals/wild_behaviour.md` (v2),
`forays.md`, `husbandry.md`, `graves.md`, `carcasses.md`, `verbs.md`, `agent_view.md`, `knowledge.md`, `water_and_preservation.md`;
`docs/scenario_design.md`; the ecology branch's `cybertron2/engine/verbs.py` (`VERB`, `_technique`), `knowledge.py` (`resolve`),
`packs.py` (`techniques`), `prompt.py` (`verb_lines`), `engine/wild.py` (`_wanted`, `take`, `watch`, `shut`, `guard`), `data.py`
(TECHNIQUES, ITEMS, THINGS, DECAY), `wild/kinds.py`, `wild/plants.py`, `wild/loads.py`, `wild/diseases.py`; the coordinator's check of
run 6's recorded system text (scratchpad `wild_run6/run.json`, not re-read here).

## History
- 10 Nov: written at Zach's request (9 Nov) to consolidate 02zr to 02zu into core engine changes and content, with every content item
  triaged into packs; with Zach's answers of 10 Nov on decay, calibration rows, determinate targets, the menu and the manual, and
  discovery (L-103), and his corrections on graves, spillover predation and known methods.
- 9 Nov: 37.2's review of the proposed cuts (Zach asked that content be lost only by an explicit decision): the corncrake, plague and
  poisons moved from cuts to deferred (K7, K10), since none was cut on principle; the other 28 cuts stand as proposed, each
  keeping its physical substrate, for Zach to confirm.
- 9 Nov: Zach added a second layer of skill within a method, by target (C3); recorded there.
