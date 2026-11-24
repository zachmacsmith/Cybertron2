# The migration and its estimate (W-112 step 4, first pass)

Session arch, 24 Nov 2026. Step 4 of [architecture_overhaul.md](../../cybertron2/proposals/architecture_overhaul.md): the order of
work to reach [target.md](target.md), in small merges to `main` after W-111's tag, with estimates. It takes the counts from
[map.md](map.md) and the surveys' own cost sections (A §6, B §8, C §8, D §10). Design only, for Zach. Nothing is built, and
nothing here changes until he answers the target's questions (Q-102 to Q-105).

## Summary

- **About 44 to 67 builder-days in all**, against feature_packages.md's 26 to 39. That figure was made on an engine of 20,400 lines;
  `engine/` is now 36,293, plus 7,917 in `wild/` and `landgen/`. The first three phases (**about 9 to 15 days**) stop the growth:
  - golden journals and the diagnostics stream;
  - the registry form, the load check and the guard;
  - the hubs as registries.

  The promotions (**about 35 to 52**) are then paced by the content that needs them, not done in one push.
- **Two ways of counting agree roughly.** Summing the surveys' own estimates gives 48 to 71 days, minus about 11 shared with
  feature_packages' phases and with each other. Counting lines rewritten (about 12,500 to 15,000) at the refactor pace
  feature_packages assumed (300 to 400 lines a builder-day) gives 31 to 50, before new code and tests.
- **A prerequisite is missing.** There are no golden journals and no prompt snapshots in `tests/`. There are 71 test files; the one
  determinism test (`test_cybertron2_engine.py`) checks that a run repeats under the same code, not that a change preserves
  behaviour. Every phase below depends on them, so they come first.

## 1. The phases

| Phase | Work | Behaviour | Builder-days | From |
|---|---|---|---|---|
| **0. Guards for the migration** (with W-111, before its tag) | golden journals for 4 to 6 scripted worlds (old and new, Eelmouth, a generated one); prompt snapshots of their system and turn prompts; the diagnostics table (target §7) with the broad `except` sites writing to it | unchanged, except diagnostics recorded | **1 to 2** | feature_packages §8, §9 phase 0 |
| **1. The registry form** | a registry with schema, links, behaviours, `requires`/`unless`, load check over the existing tables (ITEMS, TECHNIQUES, FITTINGS, COVERS, RESOURCES, PROCESSES, wild kinds, VERB, sign tables); about 350 side-table entries moved onto their rows (map.md §3); the named-branch guard's baseline list (about 1,600 sites, about 300 marked legitimate); the list of local mechanisms | unchanged (the load check fails worlds with broken rows, which is the point) | **3 to 5** | B §8 load check and properties; A §5 |
| **2. The joins as registries** | yield kinds (`verbs._technique`'s 22 branches, `farm.act`); registrations instead of import-time edits (`data.py:129-134`, `:1303-1313`, `process.register_fittings`, `PRIMITIVES.update`); seed steps (`World.__init__`'s inline installs); the night and settle as named phases (feature_packages §6); structured act results `{kind, text, data}`, read by the work loop instead of `startswith` | unchanged (byte-identical journals) | **5 to 8** | feature_packages phase 1 (4 to 6, partly); B §8 yield-kind registry |
| **3. Promotions**, each when its content comes due (below) | | some change behaviour, each named | **35 to 52** | the surveys |
| **4. Folders on touch** | a feature's code moves into its folder when it is next substantially edited (feature_packages §9's strangler path) | unchanged | spread over content work | feature_packages §9.1 |

**Phase 3, in order of the content that waits on each:**

| Promotion | Builder-days | Waits for it | Changes behaviour? |
|---|---|---|---|
| Works (9 records to one) | 3 to 4 | stage 5 (W-106: u7, works in sections, site material) | no, if in-flight works migrate exactly |
| Parts and capacity | 2 to 3 | stage 5's buildings, smoke huts, weir sections | no |
| Lives and wear (9 to one, with mending) | 3 to 5 | mending as one act; stage 5 | risk: weir wear (D2-210) and shelter levels are calibrated |
| Set gear on parts, lives and takes: **the acceptance test** (a new water gear as one row) | 1.5 to 2.5 | the waters made general (W-108) | no |
| Conditions (one grammar; the book's B7 and B8 extended; pulses, landmarks, founders, signs' `if` onto it) | 2 to 4 | the book's "seen" rules; 5b's runs on conditions | the book's false firings stop (a fix) |
| Resolver (one, over referent kinds and aliases) | 2 to 3 | W-109's parse; L-189 | yes: parses differently; live replies replayed as a fixture |
| Sign names, subjects, walkers, the observer gate, act bundles; keyed notice draws | 7 to 10 | W-103's signs design; the book reading signs by name | **yes**: keyed draws change what everyone notices (feature_packages Q4); a stimulus change, on a named day |
| Keeping by risk and remedy; draws from ordered sources | 3 to 4 | 5b part 1 (taking, making and stores) | risk: calibrated loss rates must come out the same |
| Stocks: habitat, couplings, the renewal rule's context and result | 4 to 6 | W-108 (resident fish from the generator) | risk: calibrated takes |
| People: records with terms, matching, familiarity, the mind record | 7 to 10 | the people's systems; less urgent for experiments | the old learning path stays for replay until Q-104 |
| **Total** | **35 to 52** | | |

## 2. How the numbers were made, and how far to trust them

| Survey | Its own estimate | Of which already in feature_packages or another survey |
|---|---|---|
| A, physics | 8 to 14 | load check (also B); conditions vocabulary (also C) |
| B, making | 17 to 25 (cheap tier 6 to 8) | resolver (also C, D); phase 4's technique hub and night |
| C, people | 8 to 12 | about 3 in feature_packages phase 1 |
| D, senses | 15 to 20 | about 8 in feature_packages phases 1b and 4 |
| **Sum** | **48 to 71** | **about 11 counted twice** |

- The surveys were each written in one session and have not been checked against each other. Their line counts are AST walks
  with stated under- and over-counts.
- The pace figures come from new code. No refactor of this size has been done on this engine (feature_packages.md says the same).
  The wave added about 11,350 lines in 8 days. That is building speed, not refactoring speed.
- The behaviour-changing promotions (the resolver, signs, keeping, stocks) take most of their time in checking and calibration,
  not in code. That is where the ranges are widest.

## 3. What to decide, and what it costs not to

- **The cheap first tier (phases 0 to 2, about 9 to 15 days) is worth it on any horizon.**
  - It changes no behaviour and stops the growth: the load check, the guard, registries at the joins.
  - It makes every later feature cheaper to add.
  - It is also the part whose cost grows with every week of content built without it (feature_packages §11: about 1 to 1.5
    builder-days a week of building).
- **The promotions are worth it only as the content that needs them is built.** Works before stage 5; parts, lives and set gear for
  the waters; signs with W-103. Done that way, each costs a little more than building its feature the old way (about half again,
  B §8), and saves touching the same files twice.
- **Not doing it:** every planned stage-5 and 5b item is a new record kind and a new branch in the hubs (B §8: "each a new record
  kind and a new branch in verbs.py"), and the named-branch density keeps rising, as it has at every snapshot (A §8, D §6.2).

*Current as of 24 Nov 2026 (82f8b92c).*
