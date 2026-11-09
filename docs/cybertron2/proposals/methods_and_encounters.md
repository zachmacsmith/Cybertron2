# Methods and encounters: people answer the wild by general methods, not one action per animal

**Status:** accepted: D2-204, D2-207 (9 Nov); to be built. **Build brief 1 of 3** for the wild layer's core:
stage 0 and stage 1 and pack K0 (docs/review/37_growth/02zv_wild_consolidation.md §2.1, §4, as corrected against the engine by
02zw_wild_engine_comparison.md). Brief 2 is [wild_raiders_and_works.md](wild_raiders_and_works.md) (stages 2 and 3, pack K1);
brief 3 is [carcass_and_decay.md](carcass_and_decay.md) (stage 4, pack K2). Each is built and its gate passed before the next.
**Owner:** 37.2 (author; the wild pack's data and `engine/wild.py`, D2-199). Two small edits fall in 37.4's files (§7): they need
37.4's agreement on the board, which waits on Zach.
**Affects:** spec/environment/wildlife.md (D2-192's "each taken by its own technique and skill"); code on branch `ecology`:
`engine/data.py` (wild technique rows; RESOURCES `taken.traits`), `engine/wild.py` (`take`, `site_work`, `guard`, `watch`, `shut`,
seeding), `engine/knowledge.py` (familiarity), `engine/perceive.py` (`practised`), `engine/prompt.py` (`_craft_note`),
`engine/verbs.py` (`_technique`'s refusal), `wild/kinds.py` (`SKILL_CARRY`).

## Summary

The wild pack today gives people a technique per kind (`stalk deer`, `boar hunt`, `snare hares`, `take the young herons`, `trap
beavers`, `dig out the fox earth`, four `watch the field` variants, `pick slugs at dusk`, `top the beans`), each with a hand-written
table of what it takes, and seeds all of them to everyone. This brief replaces them **inside the engine's existing technique
system**: general method rows (hunt, stalk, drive, snare, net, trap in water, den work, gather young, pest work, guard, shut) of the
same shape as today's rows; each kind gains a few **traits**; each method's take table is **generated at load** from the method's
needs and favours against the kinds' traits, so `wild.take` is unchanged. **Skill has two layers:** the method's (the existing
per-technique skill) and a new **familiarity by kind**. Methods are **known by upbringing and by what the land holds**. The system
text describes known methods without multipliers; refusals stop listing the catalogue. Agents see the same verbs, the same grammar
and the same results; only the technique names, which ones they know, and a line on the kinds they know change.

## 1. For the builder

**This file holds for this stage** wherever another document differs (read 02zw for why).

Read first: `CLAUDE.md` (both); `docs/scenario_design.md`; `docs/review/37_growth/02zr_wild_purpose_brief.md`; 02zw (the
comparison: how each piece already works); `docs/cybertron2/guides/senses.md` (any sign you touch); on branch `ecology`:
`engine/data.py` (TECHNIQUES, RESOURCES), `engine/wild.py` (`take`, `forage`, `site_work`, `guard`, `watch`, `shut`, `_reach`,
`_wanted`), `engine/verbs.py` (`_technique`), `engine/knowledge.py`, `engine/prompt.py` (`verb_lines`, `_craft_note`),
`engine/perceive.py` (`practised`), `wild/kinds.py`, `tests/test_cybertron2_wild.py`.

Ignore for this stage: `wild_behaviour.md` v2's facets and per-kind designs; 02zr to 02zu's build orders and their redesigns of
the verbs (02zw §1 explains why they are not needed); forays, set traps, decay, shared perception (later briefs).

**Do not:** add a new verb or change the reply grammar; change `take`'s structure; build anything social (offices, customs, closed
seasons, bounties, rights, standing effects); cap or filter signs; convert acts into real days; put kind names in method rows; run
live LLM runs (dry runs only unless Zach allows); write run logs into the repository.

**Branch:** work on a branch from `ecology` (`ecology-methods`); small commits with the session trailers; `git pull --rebase`
before pushing; the existing tests stay green.

## 2. Traits on kinds

RESOURCES rows of the wild pack gain `taken.traits` (values `calibrate`); the existing `taken.detect`, `flee`, `danger`, `goods`
and `family` stay and keep their meaning.

| Trait | Values |
|---|---|
| `size` | tiny, small, medium, large |
| `runs` | true or false: uses fixed runs or paths |
| `social` | solitary, group, flock |
| `home` | none, den, burrow, lodge, colony, form |
| `water` | true or false |
| `mover` | false or cue (moves on a cue in a run) |

| Kind | size | runs | social | home | water |
|---|---|---|---|---|---|
| red deer | large | true | group | none | false |
| roe deer | medium | true | solitary | none | false |
| wild boar | large | true | group | none | false |
| brown hare | small | true | solitary | form | false |
| woodpigeon | small | false | flock | none | false |
| fox | medium | true | solitary | den | false |
| wolf | large | true | group | den | false |
| brown bear | large | false | solitary | den | false |
| wildfowl | small | false | flock | none | true |
| eel | small | false | solitary | none | true (`mover: cue`) |

Sites (kinds.SITES: heronry, rookery, beaver lodge) carry `home: colony` or `home: lodge` on the site row. Crop loads (slugs,
aphids, ladybirds' larvae) carry `on_crop: true`. Further traits (scent, senses, when active) wait for the stage that reads them.

## 3. Method rows

Each method is a TECHNIQUES row of today's shape (verb, label, aliases, `at`, units, `crew`, `uses`, `weapon`, `untaught`,
`reads_as`, `yield`), with two new fields read only at load: `needs` (traits a target must have) and `favours` (traits that raise
the match, with a factor). The loader builds `yield.takes` from them (§4); a guard test forbids hand-written `takes` on these rows.

| Method (row) | Verb | Needs | Favours | Gear (`uses` / `weapon`) | Units | Replaces |
|---|---|---|---|---|---|---|
| `hunt` | gather | size small to large | | weapon helps | 2 | hunt the wild |
| `stalk` | gather | size medium to large; `runs` | solitary x1.5 | weapon helps much | 3 | stalk deer |
| `drive` | gather (crew) | size medium to large; `social: group` | | weapon helps; crew | 4 | boar hunt |
| `snare` | gather | `runs`; size small to medium | `home: form` x1.5 | (cord or snares when they exist, brief 2) | 1 | snare hares |
| `net` | gather | size small; `social: flock` | `water` x1.5 at water | (a net when it exists) | 2 | fowling |
| `trap in water` | gather | `water`; size small | `mover: cue` on its nights (the existing `when` rows) | | 1 | set eel traps |
| `den work` | gather | `home` in den, burrow, lodge | | weapon helps; spades help | 3 | dig out the fox earth, trap beavers |
| `gather young` | gather | a site with `home: colony` | | | 1 to 2 | take the young herons, take the young rooks |
| `pest work` | work | a load with `on_crop` | | | 1 to 2 | pick slugs at dusk, top the beans, clear the grubs off the beans |
| `break a dam` | work | a dam at the site | | | 2 | break the beaver dam |
| `guard` | work | (a place; the scare is what is held) | | firewood, clappers, a horn, the dog fitting | 2 | watch the field (fire, clapper, horn, dog) |
| `shut` | work | (a building) | | | 1 | shut the hens in |

Unchanged (they name goods or a field work, not a kind): `gather wild food`, `burn the stubble`, `make clappers`, `make a horn`,
`leach acorns`, and the modifiers `range` and `looking for`.

**How the merged rows keep today's behaviour:**
- `den work` at a lodge runs today's `site_work` trap branch; at a fox earth, today's `take` with the fox's litter rule (the litter
  row moves onto the fox's RESOURCES row, keyed to `home: den`).
- `gather young` runs today's `site_work` take branch for whichever colony site is at the parcel.
- `pest work` runs today's `guard` with the load named by the field's worst load present, or by `looking for` (the load's row says
  its cut and days, as now: `yield.load`, `cut`, `days`, `thin` move from the technique rows onto the load rows).
- `guard` runs today's `watch`; the scare is read from what the person holds (firewood, clappers, a horn) or the house's dog, in
  that order unless `looking for` names one (the four rows' `scare` and `uses` become a table on the method).
- Old names stay as `aliases` of the new rows for one release, so recorded runs replay exactly and older worlds resolve.

## 4. The generated take table

At load, for each method with `needs`, and each wild kind `k` with `taken.traits`:

```
takes[k] = 0                                  if any need fails
takes[k] = base(method) x product(favour factors met) x size_fit(method, k) x calibrate(k, method)
```

`size_fit` is 1.0 inside the method's size range and 0 outside. `calibrate(k, method)` is 1.0 unless the kind's row carries
`taken.calibrate: {method: x}` with a comment saying why; a guard test counts these (at most one per kind at this stage). `take`
then runs exactly as today with this table.

**Calibration target (fixed seeds, scripted bots, the share of each kind among takes per old technique):** within about a third of

| Old technique | Old weights |
|---|---|
| hunt the wild | red deer 1.0, roe deer 1.0, boar 0.6, hare 0.8, woodpigeon 0.3, fox 0.3, wolf 0.2, bear 0.1 |
| stalk deer | red deer 2.5, roe deer 2.5, boar 0.3, wolf 0.1 |
| boar hunt | boar 3.0, red deer 0.3, bear 0.2 |
| snare hares | hare 3.0, fox 0.2 |
| fowling | wildfowl 3.0, woodpigeon 0.2 |
| set eel traps | eel 3.0 (x2 on eel nights) |
| dig out the fox earth | fox 4.0, with cubs in spring |

## 5. Skill in two layers (Zach, 9 Nov)

- **The method's skill** is the existing per-technique record (`knowledge.skill`, levels aware, rough, capable, known; D2-52,
  D4-24): since a method is one technique, a good stalker stalks red deer and roe alike. `SKILL_CARRY` is removed.
- **Familiarity by kind** (new): `Mind.know` gains `familiar: {kind: x}` (0 to 1). It rises when the person takes the kind (+0.15),
  notices one of its signs while working (+0.03), or is taught about it (to at least 0.4); it carries at half to kinds sharing the
  method's needed traits (red deer to roe), never to the whole method; it fades slowly when unused (calibrate). In `take`, the
  candidate weight and the take chance for `k` are multiplied by `1 + 0.5 x familiar[k]` (calibrate). It also gates the existing
  per-kind expert readings: a reading marked `expert` for kind `k` is shown to a person whose `familiar[k]` is at least 0.6 (today
  it is the technique's level, `perceive.practised`).
- Both are told in words: the method's level as now; familiarity in the know-how lines ("you know the hares and roe of these
  parts"), never as numbers.

## 6. Who knows what

- **Basic** (known to all, D4-103): `hunt`, `gather wild food`, `guard`, `shut`, `pest work`, `burn the stubble`.
- **By the land** (D4-21), at world build: a household knows a method if its node's land within the ring (wild/areas.py) holds a
  kind or site the method can take (from §4's table): water with eels or fowl gives `trap in water` and `net`; a wood with deer
  gives `stalk`; a wood with a group kind gives `drive` to the household heads; a colony site gives `gather young`; a den or lodge
  gives `den work`. Its members start familiar with those kinds (0.3 to 0.6 by age, calibrate). The generator's experts keep their
  levels.
- **Otherwise unknown**, learnt as any craft (watching, being told, being taught, trying where tryable). `drive` and `den work`
  are not tryable untaught.
- A world setting `wild.methods_known` (a household to methods map) overrides this for experimental arms (stage 0).

## 7. What agents see

- **Method notes** in the system text (`prompt._craft_note`, 37.4's file): a sentence of what the method is, its gear and place, no
  multipliers and no kinds: "stalk: go quietly after a beast that keeps to its paths, and take it with a weapon".
- **Familiarity** in "What you know how to do": one line of the kinds the person knows.
- **Targets:** the existing `looking for` (a kind or a sort, resolved against `taken.family`); a name that resolves is accepted
  whether or not the kind is here; an unknown word is refused with "you know of no beast called that".
- **Refusals** (`verbs._technique`, 37.4's file): an unknown method is refused without listing the verb's techniques.
- **Results** keep today's lines (`take`, `site_work`, `guard`, `watch`).

## 8. Stage 0 alongside

- **Diagnostics** (in a run-analysis script kept outside the engine, never read by it): takes by method and kind; distinct methods per
  household; familiarity gained; refusals by reason; wild sign lines per agent-day.
- **The world setting** `wild.methods_known` (§6).

## 9. Tests (the gate)

- Guard: no wild method row names a kind or carries hand-written `takes`; calibration rows counted (at most one per kind); the
  system text has no tool multipliers for these methods and no list of kinds; a refusal never lists the catalogue.
- Unit: a need that fails gives zero (a snare where nothing uses runs; a net on deer); one method answers several kinds (the snare,
  hares and now and then a fox; den work, a fox earth and a lodge); method skill earned on red deer raises roe; familiarity with
  hares raises the snare's hares and not its foxes; seeding (no `trap in water` without water in the ring; `gather young` by a
  heronry); old names resolve as aliases; replay of a recorded run is exact.
- Regression (dry, scripted bots on fixed seeds, the wild-pack worlds `cybertron2/specs/wild_probe5.json` and `wild_probe6.json` on branch `ecology` (runs 5 and 6's generated villages), run with scripted bots (`run.run(spec, out, days=8, bots=True)`)): §4's shares within about a
  third; food from wild takes per household-season within about a third of before; all 467 existing tests pass, amended only for
  renames.
- **Gate to brief 2:** all of the above, and a short dry-run report to Zach.

## Why

- Zach (9 Nov): "bespoke single actions should in general usually instead be using general methods in a specific way"; "skill can
  still vary within a technique based on target as another layer"; "someone should only ever know the things they know"; "they
  should know enough to at least know how to use the different techniques"; targets "need to be determinate"; and that the reviews
  lacked the engine's context, so everything is built from how the engine already works.
- Run 6's recorded system text: every agent was seeded about 60 crafts, including taking young herons and trapping beavers where
  there were none; the know-how list grew from about 1,700 to 2,750 characters with the pack.

## Alternatives considered

- **New verbs with shared slots and a new encounter function** (02zu C.5): not needed; the engine's verbs and `take` already have
  that shape (02zw §1).
- **Keep per-kind rows, fix only the seeding:** cheaper, but each new kind needs a new technique and skill never carries.
- **Skill per method only:** loses the hunter who knows these hares, and D2-192's own skill.

## Open questions (for Zach)

1. Adopt this as stage 1, replacing D2-192's "each taken by its own technique and skill" with "general methods, with skill by
   method and familiarity by kind"?
2. May 37.2 raise the two edits in 37.4's files (`prompt._craft_note`, `verbs._technique`'s refusal) and the familiarity record in
   `knowledge.py` with 37.4 on the board?
3. A target name resolves whether or not the kind is here: agreed?
4. The basic list (§6): right?

## History

- 9 Nov 2026: first written as the build brief for stages 0 and 1 and pack K0 of 02zv.
- 9 Nov 2026: rewritten after Zach asked why stage 1 read as an overhaul and pointed out that the reviews lacked the engine's
  context: checked against the code (02zw), the brief now works inside the existing technique system (rows of today's shape, a take
  table generated at load, `take` unchanged), with familiarity as the only new mechanism; split into three briefs.

## Sources

docs/review/37_growth/02zw_wild_engine_comparison.md, 02zv_wild_consolidation.md (C1 to C3, C14, C15, K0); proposals/knowledge.md,
agent_view.md; spec/environment/wildlife.md; branch `ecology`: `engine/data.py`, `wild.py`, `verbs.py`, `knowledge.py`, `prompt.py`,
`perceive.py`, `wild/kinds.py`; the scratchpad's `wild_run6/run.json`; D2-52, D2-93, D2-192, D2-198, D2-199, D2-203, D4-21, D4-24,
D4-78, D4-103.
- 9 Nov 2026: Zach decided D2-204, D2-207 (bodies scavenged: yes; the cat by itself or found; one small live run after brief 2's gate) and asked for the briefs to be built; open points take the briefs' defaults.
