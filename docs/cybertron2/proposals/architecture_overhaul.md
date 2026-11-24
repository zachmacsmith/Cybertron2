# The engine's architecture overhauled: general mechanisms over typed rows, with systems owning only their own specifics

**Status:** discussion (24 Nov 2026), opened at Zach's ask. Builds on `feature_packages.md` (16 Nov, ready for a decision, not
built). Nothing decided beyond the decisions it cites.
**Owner:** to be assigned (a new session takes it; 37.2 hands over). **Thread:** W-112 (priority thread b), with the patterns
survey W-110 under it.

## Start here (for the agent taking this thread)

1. Read CLAUDE.md, `docs/cybertron2/spec/process/how_we_work.md` (D2-353 to D2-357), `engine_overhaul.md` (37.4's process model,
   D4-103, accepted 7 Nov: the earlier overhaul this one must fit), `feature_packages.md` in full (the earlier
   plan: six categories, the kind registry, packages with manifests, `requires` and `unless`, phases 0 to 5, 26 to 39 builder-days)
   and its inventory (`docs/review/40_feature_packages/inventory_A.md` to `inventory_E.md`).
2. The patterns survey (W-110), `docs/review/37_growth/02zzzm_patterns/`: `brief.md` (the hypothesis and the questions),
   `C_people.md` and `D_senses.md` (complete), `A_physics.md` and `B_making.md` (stopped part way: their summaries are written,
   the rest is to finish), and the branch counters beside them.
3. The evidence of how things broke: `docs/review/37_growth/02zzzh_hunt_fish/wave_regressions.md`, `prompt_compare.md`,
   `build_gaps.md`; `docs/review/37_growth/02zzzl_waters_calib/generality.md`.
4. `python3 tools/records.py surface W-112` and `surface W-110`.
5. Coordinate with W-111 (the stable engine for runs, `stable_engine_for_runs.md`): experiments run on a pinned tag; this thread
   changes `main` in small merges after the tag and never under a running experiment.

## Summary

Zach (24 Nov): "I seem to keep aiming for supposedly general architectures and then they break and you build around them.
Building upon the previous proposed architectural reshuffle, I need to dig into everything and figure out how I should shuffle to
support the new processes." The engine has general parts that work (the primitives and chokepoint, the renewal registry, the food
web over kinds' rows, techniques as rows, the sign row and the noticing rule), but each content wave has added mechanisms beside
them rather than through them, faster than the clean-up passes remove them. This thread designs the target architecture and the
way to reach it, so that most of the world is data on shared, extendable mechanisms, systems own their specifics inside
themselves (D2-354), and the process keeps it so without Zach having to ask (D2-353).

## What has been going wrong (the evidence so far)

- **Branches on named things are rising:** in area A from about 0.7 to 1.2 per 100 lines (23 Oct to 14 Nov) to 3.4 to 3.9 in the wave
  (A_physics §8); in area D from 24.7 to 33.4 per 1,000 lines at every snapshot (D_senses §6). Counted by the surveys: A 393 sites
  (about 250 should be properties), B 345 (about 265), C 375 (282 added in the wave), D 508 (about 150 in functions should be
  properties).
- **Properties transposed into side tables keyed by names:** about 45 in A, about 30 in B, 192 entries in C's modules (e.g.
  `learning.CLASS_OF`, the book's `KIND_GOODS` and `SEEN`, three disagreeing lists of verb names), so "the row" is assembled nowhere
  and checked nowhere.
- **Parallel systems instead of extensions:** five sign-row formats; about 20 subject walkers; nine name resolvers in area C alone
  that disagree; seven separate matchers of intentions; three familiarity curves; condition logic in four modules; nine copies of
  "a work built up in units over days".
- **Interface and text by hand:** the act table replaced by eleven hand-written sentences (W-100), 95 hand-written event lines in
  the act handlers, word-list parsing of replies and of the book's "seen" conditions (false firings: "few fish rising" fires a rule
  on "the river rising").
- **World content patched outside the pipeline:** resident fish stocked by makers, runs on set nights, households pinned, the
  river's size lost at the land-to-world write.
- **Half-built decisions and silent failures:** D2-306 and D2-304 built in half; the founders' skipped ids, an unknown cue key,
  raising sign conditions, an attend's fallback, all silent; no registry checked at load.
- **Process:** briefs named feature units (D2-244) but not the rule against names; reviews checked behaviour and tests, not shape;
  replay kept old paths alive with no rule for when they may go; infrastructure passes came one to two weeks after the spread they
  repair (D_senses §7, C_people §6).

## The hypothesis and what the surveys found missing

The survey's hypothesis (brief.md): typed rows checked at load; behaviour on properties, never names; general mechanisms (stocks,
pulses, processes, set gear, lives and wear, acts, signs, the book); one name resolver; generated worlds entire. The surveys find
its centre right and the set **too few and partly wrongly cut**. Patterns they say are needed:

| From | Missing pattern |
|---|---|
| A | habitat (where a stock lives and its K); couplings (one population acting on another); coupled populations (the food web); movement along a network (runs, ranging, storms); driven layers and conditions derived from their memory (frost, snow, spate, ice); type transitions (forest to scrub, a dam, ice, a site); places that group places (a water body over parcels, areas, stretches); analyses that re-derive the physics (capacity, gate checks) |
| B | works (a change built up in units over days, then an effect); bodies with parts (rooms, storeys, fittings, weir sections, strips); keeping by risk and remedy; drawing a need from ordered sources (eating, fodder, fuel, inputs); (two more in B's unfinished part) |
| C | records with terms and a settling step (agreements, offers, claims, offices, the book); matched intentions (partner, try, teach and learn, join and admit, care, parties, offers); familiarity with a curve (crafts, places, kinds, landmarks); one condition grammar shared by rules, pulses, signs and the founders' lines; the day's order as a phase list; seeded lines as template rows; one resolver |
| D | the observer (what a person's knowledge, stage, office and holding let them see); the mind's dated records; a subject registry with walkers and contexts; signs split into state rows, act and craft bundles, and the noticing rule; lines known without a roll; the reply schema built from the act registry |

Several of these are feature_packages.md's object model (records, layers, populations, minds) not yet built; others are new.

## The proposal (the work of this thread)

1. **Finish the survey:** areas A and B to the brief's end (mechanisms, branches, misfits, taxonomy, history, process).
2. **The target architecture** (draft 1, 24 Nov, for Zach: [41_architecture/target.md](../../review/41_architecture/target.md): one registry
   form checked at load, three layers (core, shared mechanisms, features), and a lifecycle in which a feature's own mechanism is
   promoted to the shared layer at its second user), reconciling the surveys with feature_packages.md: the categories of thing (its six, revised), the
   general mechanisms and what each reads, the shared core every mechanism uses (one registry schema with required fields checked
   at load, one condition grammar, one name resolver, the phase list, stable sign names), the extension points each mechanism offers
   so a feature extends it instead of bypassing it, and what a system may own as its specifics and where they live (D2-354).
3. **The map:** every mechanism the surveys list (about 390) to its home in the target, and every named branch and side table to the
   property it becomes; what stays legitimately by name.
4. **The migration:** phases on `main` in small merges (feature_packages §9.1), each against golden journals and prompt
   snapshots; the replay policy (when an old path may go, and which old runs it ends); the order (the shared core first: registry
   checks, conditions, resolver, phase list; then the mechanisms; then the content moved onto them), with estimates.
5. **Guards and process,** written into `how_we_work.md` on Zach's word: the brief template's architecture section; the review
   checklist (named branches, hand text, word lists, silent skips, maker patches, coverage); load checks; the named-branch guard (a
   list that only shrinks); the interface coverage test; a sign-row check; tests by module (D2-355); an architecture audit at each
   wave's end with its findings recorded.
6. **How it meets W-111:** experiments on the tag; the overhaul after it; fixes to the tag merged forward.

## Why

Every week of content on the current shape adds parallel systems that the next pass must remove, and each break hides acts or
knowledge from the agents whose behaviour the experiments measure. A shape that new features extend, with checks that fail loudly,
is cheaper than the repeated repair.

## Alternatives considered

- **Feature packages as written** (feature_packages.md): the folder and manifest structure, without the mechanisms the surveys find
  missing; it moves code without making content data ("It does not make content into data by itself", its own weakness).
- **Phase 1 only** (registries and cycles broken): cheap, keeps most coupling.
- **A full entity-component system:** rejected in feature_packages.md for cost.
- **Guards without restructuring:** stops the growth, leaves the parallel systems.

## Open questions for Zach

1. How strict (D2-354): which systems keep their own specifics (the founders' prose, the bots, memory and the journal, others)?
2. Package granularity, the grid, weather driven or coupled, keyed notice draws (feature_packages.md's open questions 1 to 7).
3. The replay policy: may old runs stop replaying when a mechanism is replaced, and with what record?
4. The order against content: does all new content wait for the shared core, or only content in the areas being moved?

## Affects

The whole engine; `feature_packages.md` (to be revised or replaced by this); `spec/core/`; `how_we_work.md`.

## History

- **24 Nov 2026:** opened by 37.2 at Zach's ask, from the patterns survey (W-110: C and D complete, A and B part way), the wave's
  regression audit, the gaps audit and the waters' generality read, as one of two priority threads (with W-111).

- **24 Nov 2026 (later): taken over by session arch.** Surveys A and B, checked against the brief, carry every section it asks
  for (mechanisms, branches, misfits, taxonomy, history, process, verdict, cost); "stopped part way" above was written before their
  last commits. B's two further misfits are capacity and room, and populations with classes (B §3.5, §3.6).
  Zach framed the thread (24 Nov, not a decision): "Your main purpose is not to build, but to design a new target architecture,
  seeing how the engine ACTUALLY works, how this would be better served / ported into a data-central way that is more extensible but
  simultaneously fluid ... Extensibility is key with new things being able to be built and isolated in their new features etc. that
  ideally work through existing shared primitives, or introduce some new basic mechanism or specifics if necessary, that may later be
  generalised into core primitives." arch's reading, to be worked into the target: a mechanism has a **lifecycle** (specific inside
  one package, then promoted into the core when a second feature needs it), so the target is a small core, fixed seams, a
  containment rule for specifics and a promotion rule, not a full set of general mechanisms fixed in advance (the surveys' 25 or so
  missing patterns are candidates to promote, not a list to build); mechanisms stay code with declared extension points and rows
  carry properties, not logic (no rule interpreter: D2-354's rigid end); and the architecture fixes only the half of the ad hoc code
  that went ad hoc because the primitives could not be extended (A §7.3): the other half needs the guards and the review rules.

- **24 Nov 2026 (later): target architecture, draft 1** (session arch, `docs/review/41_architecture/target.md`), from the code
  (the chokepoint, the act hub, the sign walker, the night, process rows, packs, renewal) and the four surveys. Its questions for
  Zach: the shape; conditions in one grammar where another system reads them; the replay policy; content waiting only for the
  promotion it needs. Not yet done: the map (step 3), the migration and its estimates (step 4) against today's 36,293 engine lines.

## Sources

`engine_overhaul.md` (D4-103); `feature_packages.md`; `docs/review/40_feature_packages/`; `docs/review/37_growth/02zzzm_patterns/`; `wave_regressions.md`;
`prompt_compare.md`; `build_gaps.md`; `generality.md`; decisions D2-244, D2-350 to D2-357, D5-2.
